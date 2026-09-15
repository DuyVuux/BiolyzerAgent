package stage10

import (
	"context"
	"strings"
	"sync/atomic"
	"testing"

	"biomarker/internal/analysis"
	"biomarker/internal/platform/persistence/fileturn"
	"biomarker/internal/platform/runtime/persistentlocal"
)

type workflow struct{ calls atomic.Int64 }

func (w *workflow) Invoke(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	w.calls.Add(1)
	return analysis.ExecutionResult{
		SchemaVersion: "1.0",
		TurnID:        req.TurnID,
		Status:        analysis.StatusCompleted,
	}, nil
}

func TestCrossRestartCanonicalReplay(t *testing.T) {
	dir := t.TempDir()
	req := request()

	s1, _ := fileturn.Open(dir)
	w1 := &workflow{}
	r1 := persistentlocal.NewRuntime(w1, s1)
	if _, err := r1.Execute(context.Background(), req); err != nil {
		t.Fatal(err)
	}

	s2, _ := fileturn.Open(dir)
	w2 := &workflow{}
	r2 := persistentlocal.NewRuntime(w2, s2)
	if _, err := r2.Execute(context.Background(), req); err != nil {
		t.Fatal(err)
	}

	if w1.calls.Load() != 1 || w2.calls.Load() != 0 {
		t.Fatalf("unexpected calls first=%d restart=%d", w1.calls.Load(), w2.calls.Load())
	}
}

func request() analysis.ExecutionRequest {
	return analysis.ExecutionRequest{
		SchemaVersion:  "1.0",
		TurnID:         "turn-stage10-integration",
		IdempotencyKey: "idem-stage10",
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "clinical-synthetic-001",
			EvidenceBundle: analysis.EvidenceBundleRef{
				BundleID:                "evidence-synthetic-001",
				Status:                  "verified",
				ProcessingProfileDigest: strings.Repeat("c", 64),
				Claims:                  []analysis.EvidenceClaimRef{{ID: "claim-1", Status: "supported"}},
			},
			ClinicalRefs: []analysis.ClinicalRef{{
				ID: "obs-1", Type: "observation",
				VerificationState:   "verified",
				ReconciliationState: "resolved",
				TerminologyState:    "validated",
			}},
			Policies: analysis.PolicyClosure{
				ReasoningPolicyDigest: strings.Repeat("a", 64),
				SafetyPolicyDigest:    strings.Repeat("b", 64),
			},
			UserQuestion: "synthetic stage10 question",
		},
	}
}
