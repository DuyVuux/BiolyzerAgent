package persistentlocal

import (
	"context"
	"errors"
	"strings"
	"sync"
	"sync/atomic"
	"testing"
	"time"

	"biomarker/internal/analysis"
	"biomarker/internal/persistence/turnstore"
	"biomarker/internal/platform/persistence/fileturn"
)

type countingWorkflow struct {
	calls atomic.Int64
	delay time.Duration
}

func (w *countingWorkflow) Invoke(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	w.calls.Add(1)
	if w.delay > 0 {
		select {
		case <-ctx.Done():
			return analysis.ExecutionResult{}, ctx.Err()
		case <-time.After(w.delay):
		}
	}
	return analysis.ExecutionResult{
		SchemaVersion: "1.0",
		TurnID:        req.TurnID,
		Status:        analysis.StatusCompleted,
		Decision:      &analysis.SafetyDecision{Verdict: "approve"},
	}, nil
}

func TestCompletedResultSurvivesRestartAndDoesNotReexecute(t *testing.T) {
	dir := t.TempDir()
	req := validRequest("turn-restart")

	store1, _ := fileturn.Open(dir)
	w1 := &countingWorkflow{}
	r1 := NewRuntime(w1, store1)
	first, err := r1.Execute(context.Background(), req)
	if err != nil || first.Status != analysis.StatusCompleted {
		t.Fatalf("first: %#v %v", first, err)
	}
	if w1.calls.Load() != 1 {
		t.Fatal("expected one workflow call")
	}

	store2, _ := fileturn.Open(dir)
	w2 := &countingWorkflow{}
	r2 := NewRuntime(w2, store2)
	second, err := r2.Execute(context.Background(), req)
	if err != nil || second.Status != analysis.StatusCompleted {
		t.Fatalf("replay: %#v %v", second, err)
	}
	if w2.calls.Load() != 0 {
		t.Fatalf("restart replay re-executed workflow: %d", w2.calls.Load())
	}
}

func TestConcurrentDuplicatesExecuteOnce(t *testing.T) {
	store, _ := fileturn.Open(t.TempDir())
	w := &countingWorkflow{delay: 5 * time.Millisecond}
	r := NewRuntime(w, store)
	req := validRequest("turn-concurrent")

	const n = 64
	var wg sync.WaitGroup
	errs := make(chan error, n)
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			res, err := r.Execute(context.Background(), req)
			if err != nil {
				errs <- err
				return
			}
			if res.Status != analysis.StatusCompleted {
				errs <- errors.New("not completed")
			}
		}()
	}
	wg.Wait()
	close(errs)
	for err := range errs {
		t.Fatal(err)
	}
	if w.calls.Load() != 1 {
		t.Fatalf("workflow calls=%d", w.calls.Load())
	}
}

func TestRestartedIncompleteTurnRequiresRecoveryAndDoesNotExecute(t *testing.T) {
	dir := t.TempDir()
	store, _ := fileturn.Open(dir)
	req := validRequest("turn-stranded")
	digest, _ := RequestSemanticDigest(req)

	_, err := store.CreateOrLoad(context.Background(), turnstore.Record{
		TurnID:         req.TurnID,
		IdempotencyKey: req.IdempotencyKey,
		RequestDigest:  digest,
		Provenance:     provenance(req),
	})
	if err != nil {
		t.Fatal(err)
	}

	reopened, _ := fileturn.Open(dir)
	w := &countingWorkflow{}
	r := NewRuntime(w, reopened)
	res, err := r.Execute(context.Background(), req)
	if !errors.Is(err, ErrRecoveryRequired) {
		t.Fatalf("expected recovery required, got %v", err)
	}
	if res.Error == nil || res.Error.Code != "RECOVERY_REQUIRED" {
		t.Fatalf("unexpected result %#v", res)
	}
	if w.calls.Load() != 0 {
		t.Fatalf("unsafe re-execution occurred: %d", w.calls.Load())
	}

	rec, err := reopened.Load(context.Background(), req.TurnID)
	if err != nil {
		t.Fatal(err)
	}
	if rec.Status != turnstore.StatusRecoveryRequired {
		t.Fatalf("status=%s", rec.Status)
	}
}

func TestNeedsReconciliationDoesNotExecute(t *testing.T) {
	dir := t.TempDir()
	store, _ := fileturn.Open(dir)
	req := validRequest("turn-reconcile")
	digest, _ := RequestSemanticDigest(req)

	_, err := store.CreateOrLoad(context.Background(), turnstore.Record{
		TurnID:         req.TurnID,
		IdempotencyKey: req.IdempotencyKey,
		RequestDigest:  digest,
		Provenance:     provenance(req),
	})
	if err != nil {
		t.Fatal(err)
	}
	if _, err := store.MarkNeedsReconciliation(context.Background(), req.TurnID, digest, "ambiguous mutating external effect"); err != nil {
		t.Fatal(err)
	}

	w := &countingWorkflow{}
	r := NewRuntime(w, store)
	res, err := r.Execute(context.Background(), req)
	if !errors.Is(err, ErrNeedsReconciliation) {
		t.Fatalf("expected reconciliation block, got %v", err)
	}
	if res.Error == nil || res.Error.Code != "NEEDS_RECONCILIATION" {
		t.Fatalf("unexpected result %#v", res)
	}
	if w.calls.Load() != 0 {
		t.Fatalf("unsafe re-execution occurred: %d", w.calls.Load())
	}
}

func TestRestartConflictFailsClosed(t *testing.T) {
	dir := t.TempDir()
	store, _ := fileturn.Open(dir)
	w := &countingWorkflow{}
	r := NewRuntime(w, store)

	req := validRequest("turn-conflict")
	if _, err := r.Execute(context.Background(), req); err != nil {
		t.Fatal(err)
	}

	changed := req
	changed.Input.UserQuestion = "different semantic question"
	reopened, _ := fileturn.Open(dir)
	r2 := NewRuntime(&countingWorkflow{}, reopened)
	res, err := r2.Execute(context.Background(), changed)
	if !errors.Is(err, turnstore.ErrConflict) {
		t.Fatalf("expected conflict, got %v", err)
	}
	if res.Error == nil || res.Error.Code != "IDEMPOTENCY_CONFLICT" {
		t.Fatalf("result=%#v", res)
	}
}

func TestTransportNoiseDoesNotChangeSemanticIdentity(t *testing.T) {
	dir := t.TempDir()
	store, _ := fileturn.Open(dir)
	r := NewRuntime(&countingWorkflow{}, store)

	req := validRequest("turn-transport")
	if _, err := r.Execute(context.Background(), req); err != nil {
		t.Fatal(err)
	}

	retry := req
	retry.CorrelationID = "different-correlation"
	retry.DeadlineMS = 9999
	d1, _ := RequestSemanticDigest(req)
	d2, _ := RequestSemanticDigest(retry)
	if d1 != d2 {
		t.Fatalf("transport fields changed semantic digest")
	}

	r2 := NewRuntime(&countingWorkflow{}, store)
	if _, err := r2.Execute(context.Background(), retry); err != nil {
		t.Fatal(err)
	}
}

func validRequest(turnID string) analysis.ExecutionRequest {
	return analysis.ExecutionRequest{
		SchemaVersion:  "1.0",
		TurnID:         turnID,
		IdempotencyKey: "idem-" + turnID,
		CorrelationID:  "corr-1",
		DeadlineMS:     1000,
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "clinical-synthetic-001",
			TimelineSnapshotID: "timeline-synthetic-001",
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
			UserQuestion: "synthetic question",
		},
	}
}
