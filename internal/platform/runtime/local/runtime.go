package local

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"biomarker/internal/analysis"
)

// Runtime is the Stage-09 single-process execution coordinator.
type Runtime struct {
	workflow analysis.Workflow
	ledger   *Ledger
}

// NewRuntime creates the single-process runtime.
func NewRuntime(workflow analysis.Workflow, ledger *Ledger) *Runtime {
	return &Runtime{workflow: workflow, ledger: ledger}
}

// Execute performs duplicate-safe in-process execution for one logical Turn.
func (r *Runtime) Execute(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	if err := analysis.ValidateExecutionRequest(req); err != nil {
		return failed(req.TurnID, "INVALID_REQUEST", "request failed structural runtime validation"), err
	}

	digest, err := requestDigest(req)
	if err != nil {
		return failed(req.TurnID, "REQUEST_DIGEST_FAILED", "request could not be fingerprinted"), err
	}

	ticket, err := r.ledger.Start(req.TurnID, digest)
	if err != nil {
		return failed(req.TurnID, "IDEMPOTENCY_CONFLICT", "turn identity conflicts with an existing request"), err
	}
	if !ticket.Owner() {
		return ticket.Wait(ctx)
	}

	execCtx := ctx
	cancel := func() {}
	if req.DeadlineMS > 0 {
		execCtx, cancel = context.WithTimeout(ctx, time.Duration(req.DeadlineMS)*time.Millisecond)
	}
	defer cancel()
	execCtx = ContextWithScope(execCtx, req)

	result, runErr := r.workflow.Invoke(execCtx, req)
	if runErr != nil {
		status := analysis.StatusFailed
		code := "RUNTIME_EXECUTION_FAILED"
		message := "runtime execution failed"
		if errors.Is(runErr, context.Canceled) || errors.Is(runErr, context.DeadlineExceeded) {
			status = analysis.StatusCancelled
			code = "RUNTIME_CANCELLED"
			message = "runtime execution was cancelled or exceeded its deadline"
		}
		result = analysis.ExecutionResult{
			SchemaVersion: "1.0", TurnID: req.TurnID, Status: status,
			Error: &analysis.RuntimeError{Code: code, Message: message},
		}
	}
	ticket.Complete(result, runErr)
	return result, runErr
}

func requestDigest(req analysis.ExecutionRequest) (string, error) {
	b, err := json.Marshal(req)
	if err != nil {
		return "", fmt.Errorf("marshal request: %w", err)
	}
	sum := sha256.Sum256(b)
	return hex.EncodeToString(sum[:]), nil
}

func failed(turnID, code, message string) analysis.ExecutionResult {
	return analysis.ExecutionResult{
		SchemaVersion: "1.0", TurnID: turnID, Status: analysis.StatusFailed,
		Error: &analysis.RuntimeError{Code: code, Message: message},
	}
}
