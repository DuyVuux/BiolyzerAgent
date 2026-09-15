package persistentlocal

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"sync"
	"time"

	"biomarker/internal/analysis"
	"biomarker/internal/persistence/turnstore"
)

var (
	ErrRecoveryRequired    = errors.New("durable turn exists in nonterminal state and requires recovery")
	ErrNeedsReconciliation = errors.New("durable turn has ambiguous external outcome and requires reconciliation")
	ErrIdempotencyConflict = turnstore.ErrConflict
)

type flight struct {
	digest string
	done   chan struct{}
	result analysis.ExecutionResult
	err    error
}

// Runtime adds restart-durable Turn identity/result semantics to the
// Stage-09 single-process workflow.
//
// It still assumes one application process. The in-memory flights map only
// coordinates concurrent callers in the current process; canonical identity
// lives in the durable Store.
type Runtime struct {
	workflow analysis.Workflow
	store    turnstore.Store

	mu      sync.Mutex
	flights map[string]*flight
}

func NewRuntime(workflow analysis.Workflow, store turnstore.Store) *Runtime {
	return &Runtime{
		workflow: workflow,
		store:    store,
		flights:  make(map[string]*flight),
	}
}

func (r *Runtime) Execute(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	if err := analysis.ValidateExecutionRequest(req); err != nil {
		return failed(req.TurnID, "INVALID_REQUEST", "request failed structural runtime validation"), err
	}

	digest, err := RequestSemanticDigest(req)
	if err != nil {
		return failed(req.TurnID, "REQUEST_DIGEST_FAILED", "request could not be fingerprinted"), err
	}

	// Current-process duplicate coordination happens before durable reserve so
	// a second caller joins the live execution instead of misclassifying it as
	// a restart-stranded record.
	r.mu.Lock()
	if f, ok := r.flights[req.TurnID]; ok {
		if f.digest != digest {
			r.mu.Unlock()
			return failed(req.TurnID, "IDEMPOTENCY_CONFLICT", "turn identity conflicts with an active request"), turnstore.ErrConflict
		}
		r.mu.Unlock()
		return waitFlight(ctx, f)
	}

	initial := turnstore.Record{
		TurnID:         req.TurnID,
		IdempotencyKey: req.IdempotencyKey,
		RequestDigest:  digest,
		Provenance:     provenance(req),
	}
	reservation, err := r.store.CreateOrLoad(ctx, initial)
	if err != nil {
		r.mu.Unlock()
		if errors.Is(err, turnstore.ErrConflict) {
			return failed(req.TurnID, "IDEMPOTENCY_CONFLICT", "turn identity conflicts with persisted semantic request"), err
		}
		return failed(req.TurnID, "PERSISTENCE_RESERVE_FAILED", "durable Turn state could not be reserved"), err
	}

	if !reservation.Created {
		switch reservation.Record.Status {
		case turnstore.StatusCompleted, turnstore.StatusFailed, turnstore.StatusCancelled:
			r.mu.Unlock()
			if reservation.Record.Result == nil {
				err := turnstore.ErrIntegrity
				return failed(req.TurnID, "PERSISTED_RESULT_MISSING", "terminal Turn is missing canonical result"), err
			}
			return *reservation.Record.Result, terminalError(*reservation.Record.Result)
		case turnstore.StatusNeedsReconciliation:
			r.mu.Unlock()
			return failed(req.TurnID, "NEEDS_RECONCILIATION", "durable Turn has an ambiguous outcome and requires reconciliation"), ErrNeedsReconciliation
		case turnstore.StatusAccepted, turnstore.StatusRecoveryRequired:
			if reservation.Record.Status == turnstore.StatusAccepted {
				_, _ = r.store.MarkRecoveryRequired(
					context.Background(),
					req.TurnID,
					digest,
					"process restart or lost current-process execution ownership",
				)
			}
			r.mu.Unlock()
			return failed(req.TurnID, "RECOVERY_REQUIRED", "durable Turn requires recovery before any re-execution"), ErrRecoveryRequired
		default:
			r.mu.Unlock()
			return failed(req.TurnID, "PERSISTED_STATE_INVALID", "durable Turn has unsupported state"), turnstore.ErrIntegrity
		}
	}

	f := &flight{digest: digest, done: make(chan struct{})}
	r.flights[req.TurnID] = f
	r.mu.Unlock()

	result, runErr := r.invoke(ctx, req)

	committed, commitErr := r.store.CommitTerminal(context.Background(), req.TurnID, digest, result, nil)
	if commitErr != nil {
		result = failed(req.TurnID, "PERSISTENCE_COMMIT_FAILED", "execution finished but canonical durable outcome could not be committed")
		runErr = fmt.Errorf("commit durable outcome: %w", commitErr)
	} else if committed.Result != nil {
		result = *committed.Result
	}

	r.mu.Lock()
	f.result = result
	f.err = runErr
	close(f.done)
	delete(r.flights, req.TurnID)
	r.mu.Unlock()

	return result, runErr
}

func (r *Runtime) invoke(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	execCtx := ctx
	cancel := func() {}
	if req.DeadlineMS > 0 {
		execCtx, cancel = context.WithTimeout(ctx, time.Duration(req.DeadlineMS)*time.Millisecond)
	}
	defer cancel()

	result, runErr := r.workflow.Invoke(execCtx, req)
	if runErr == nil {
		return result, nil
	}

	status := analysis.StatusFailed
	code := "RUNTIME_EXECUTION_FAILED"
	message := "runtime execution failed"
	if errors.Is(runErr, context.Canceled) || errors.Is(runErr, context.DeadlineExceeded) {
		status = analysis.StatusCancelled
		code = "RUNTIME_CANCELLED"
		message = "runtime execution was cancelled or exceeded its deadline"
	}
	return analysis.ExecutionResult{
		SchemaVersion: "1.0",
		TurnID:        req.TurnID,
		Status:        status,
		Error:         &analysis.RuntimeError{Code: code, Message: message},
	}, runErr
}

func waitFlight(ctx context.Context, f *flight) (analysis.ExecutionResult, error) {
	select {
	case <-ctx.Done():
		return analysis.ExecutionResult{}, ctx.Err()
	case <-f.done:
		return f.result, f.err
	}
}

// RequestSemanticDigest excludes transport-only correlation/deadline values.
// A retry of the same logical Turn may have a different correlation ID or
// remaining deadline without becoming a different clinical request.
func RequestSemanticDigest(req analysis.ExecutionRequest) (string, error) {
	semantic := struct {
		SchemaVersion  string                  `json:"schema_version"`
		TurnID         string                  `json:"turn_id"`
		IdempotencyKey string                  `json:"idempotency_key"`
		Input          analysis.ReasoningInput `json:"input"`
	}{
		SchemaVersion:  req.SchemaVersion,
		TurnID:         req.TurnID,
		IdempotencyKey: req.IdempotencyKey,
		Input:          req.Input,
	}
	b, err := json.Marshal(semantic)
	if err != nil {
		return "", fmt.Errorf("marshal semantic request: %w", err)
	}
	sum := sha256.Sum256(b)
	return hex.EncodeToString(sum[:]), nil
}

func provenance(req analysis.ExecutionRequest) turnstore.Provenance {
	return turnstore.Provenance{
		ClinicalSnapshotID:    req.Input.ClinicalSnapshotID,
		TimelineSnapshotID:    req.Input.TimelineSnapshotID,
		EvidenceBundleID:      req.Input.EvidenceBundle.BundleID,
		ReasoningPolicyDigest: req.Input.Policies.ReasoningPolicyDigest,
		SafetyPolicyDigest:    req.Input.Policies.SafetyPolicyDigest,
	}
}

func terminalError(result analysis.ExecutionResult) error {
	if result.Status == analysis.StatusCompleted {
		return nil
	}
	if result.Error != nil {
		return errors.New(result.Error.Message)
	}
	return errors.New("persisted execution did not complete successfully")
}

func failed(turnID, code, message string) analysis.ExecutionResult {
	return analysis.ExecutionResult{
		SchemaVersion: "1.0",
		TurnID:        turnID,
		Status:        analysis.StatusFailed,
		Error:         &analysis.RuntimeError{Code: code, Message: message},
	}
}
