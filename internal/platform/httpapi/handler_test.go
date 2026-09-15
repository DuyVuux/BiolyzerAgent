package httpapi

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"biomarker/internal/analysis"
)

type fakeRuntime struct{}

func (fakeRuntime) Execute(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	return analysis.ExecutionResult{SchemaVersion: "1.0", TurnID: req.TurnID, Status: analysis.StatusCompleted}, nil
}

func TestHealthz(t *testing.T) {
	r := httptest.NewRequest(http.MethodGet, "/healthz", nil)
	w := httptest.NewRecorder()
	NewHandler(fakeRuntime{}).Routes().ServeHTTP(w, r)
	if w.Code != http.StatusOK {
		t.Fatalf("status=%d", w.Code)
	}
}

func TestExecuteRejectsUnknownJSONField(t *testing.T) {
	body := []byte(`{"schema_version":"1.0","turn_id":"t","idempotency_key":"i","input":{},"unexpected":true}`)
	r := httptest.NewRequest(http.MethodPost, "/internal/runtime/execute", bytes.NewReader(body))
	w := httptest.NewRecorder()
	NewHandler(fakeRuntime{}).Routes().ServeHTTP(w, r)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("status=%d body=%s", w.Code, w.Body.String())
	}
}

func TestExecuteReturnsTypedResult(t *testing.T) {
	req := analysis.ExecutionRequest{
		SchemaVersion: "1.0", TurnID: "t1", IdempotencyKey: "i1",
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "c1",
			EvidenceBundle:     analysis.EvidenceBundleRef{BundleID: "e1"},
			Policies:           analysis.PolicyClosure{ReasoningPolicyDigest: "r", SafetyPolicyDigest: "s"},
		},
	}
	b, _ := json.Marshal(req)
	r := httptest.NewRequest(http.MethodPost, "/internal/runtime/execute", bytes.NewReader(b))
	w := httptest.NewRecorder()
	NewHandler(fakeRuntime{}).Routes().ServeHTTP(w, r)
	if w.Code != http.StatusOK {
		t.Fatalf("status=%d body=%s", w.Code, w.Body.String())
	}
}
