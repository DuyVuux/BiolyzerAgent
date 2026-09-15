package local

import (
	"context"
	"errors"
	"sync"
	"sync/atomic"
	"testing"
	"time"

	"biomarker/internal/analysis"
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
	return analysis.ExecutionResult{SchemaVersion: "1.0", TurnID: req.TurnID, Status: analysis.StatusCompleted}, nil
}

func req(turn, idem, question string) analysis.ExecutionRequest {
	return analysis.ExecutionRequest{
		SchemaVersion: "1.0", TurnID: turn, IdempotencyKey: idem,
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "clinical-1",
			EvidenceBundle:     analysis.EvidenceBundleRef{BundleID: "evidence-1", Status: "verified", ProcessingProfileDigest: "p"},
			Policies:           analysis.PolicyClosure{ReasoningPolicyDigest: "r", SafetyPolicyDigest: "s"},
			UserQuestion:       question,
		},
	}
}

func TestSameTurnSamePayloadExecutesOnce(t *testing.T) {
	w := &countingWorkflow{}
	rt := NewRuntime(w, NewLedger())
	first, err := rt.Execute(context.Background(), req("t1", "i1", "q"))
	if err != nil {
		t.Fatal(err)
	}
	second, err := rt.Execute(context.Background(), req("t1", "i1", "q"))
	if err != nil {
		t.Fatal(err)
	}
	if first.Status != second.Status || w.calls.Load() != 1 {
		t.Fatalf("dedupe failed calls=%d first=%#v second=%#v", w.calls.Load(), first, second)
	}
}

func TestSameTurnDifferentPayloadConflicts(t *testing.T) {
	w := &countingWorkflow{}
	rt := NewRuntime(w, NewLedger())
	_, _ = rt.Execute(context.Background(), req("t1", "i1", "q1"))
	_, err := rt.Execute(context.Background(), req("t1", "i1", "q2"))
	if !errors.Is(err, ErrIdempotencyConflict) {
		t.Fatalf("expected idempotency conflict, got %v", err)
	}
	if w.calls.Load() != 1 {
		t.Fatalf("unexpected second execution calls=%d", w.calls.Load())
	}
}

func TestConcurrentDuplicateExecutesOnce(t *testing.T) {
	w := &countingWorkflow{delay: 20 * time.Millisecond}
	rt := NewRuntime(w, NewLedger())
	const n = 32
	var wg sync.WaitGroup
	errs := make(chan error, n)
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			got, err := rt.Execute(context.Background(), req("t-shared", "i-shared", "q"))
			if err != nil {
				errs <- err
				return
			}
			if got.Status != analysis.StatusCompleted {
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
		t.Fatalf("expected one workflow call, got %d", w.calls.Load())
	}
}

func TestDeadlineCancellationIsCanonicalForTurn(t *testing.T) {
	w := &countingWorkflow{delay: 50 * time.Millisecond}
	rt := NewRuntime(w, NewLedger())
	r := req("t-deadline", "i-deadline", "q")
	r.DeadlineMS = 5
	got, err := rt.Execute(context.Background(), r)
	if !errors.Is(err, context.DeadlineExceeded) {
		t.Fatalf("expected deadline error, got %v", err)
	}
	if got.Status != analysis.StatusCancelled {
		t.Fatalf("unexpected status %#v", got)
	}
	again, err := rt.Execute(context.Background(), r)
	if !errors.Is(err, context.DeadlineExceeded) || again.Status != analysis.StatusCancelled || w.calls.Load() != 1 {
		t.Fatalf("cancel result not deduped %#v err=%v calls=%d", again, err, w.calls.Load())
	}
}

type scopeWorkflow struct {
	scope Scope
	ok    bool
}

func (w *scopeWorkflow) Invoke(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	scope, ok := ScopeFromContext(ctx)
	w.scope = scope
	w.ok = ok
	return analysis.ExecutionResult{SchemaVersion: "1.0", TurnID: req.TurnID, Status: analysis.StatusCompleted}, nil
}

func TestRuntimeBindsScopeBeforeWorkflow(t *testing.T) {
	w := &scopeWorkflow{}
	rt := NewRuntime(w, NewLedger())
	r := req("t-scope", "i-scope", "q")
	r.CorrelationID = "corr-scope"

	_, err := rt.Execute(context.Background(), r)
	if err != nil {
		t.Fatal(err)
	}
	if !w.ok {
		t.Fatal("workflow context did not contain runtime scope")
	}
	if w.scope.TurnID != "t-scope" || w.scope.IdempotencyKey != "i-scope" || w.scope.CorrelationID != "corr-scope" {
		t.Fatalf("unexpected scope: %#v", w.scope)
	}
}
