package eino

import (
	"context"
	"fmt"

	"github.com/cloudwego/eino/compose"

	"biomarker/internal/analysis"
)

type candidateEnvelope struct {
	Request   analysis.ExecutionRequest
	Candidate analysis.ReasoningCandidate
}

// Workflow is the Eino-backed in-memory structured runtime adapter.
type Workflow struct {
	runnable compose.Runnable[analysis.ExecutionRequest, analysis.ExecutionResult]
}

// NewWorkflow compiles the bounded Stage-09 workflow once.
func NewWorkflow(ctx context.Context, generator analysis.CandidateGenerator, evaluator analysis.SafetyEvaluator) (*Workflow, error) {
	chain := compose.NewChain[analysis.ExecutionRequest, analysis.ExecutionResult]()

	generate := compose.InvokableLambda(func(ctx context.Context, req analysis.ExecutionRequest) (candidateEnvelope, error) {
		if err := ctx.Err(); err != nil {
			return candidateEnvelope{}, err
		}
		candidate, err := generator.Generate(ctx, req.Input)
		if err != nil {
			return candidateEnvelope{}, err
		}
		if err := analysis.ValidateReasoningCandidate(candidate); err != nil {
			return candidateEnvelope{}, err
		}
		return candidateEnvelope{Request: req, Candidate: candidate}, nil
	})

	gate := compose.InvokableLambda(func(ctx context.Context, env candidateEnvelope) (analysis.ExecutionResult, error) {
		select {
		case <-ctx.Done():
			return analysis.ExecutionResult{}, ctx.Err()
		default:
		}
		decision, output := evaluator.Evaluate(env.Request.Input, env.Candidate)
		return analysis.ExecutionResult{
			SchemaVersion: "1.0",
			TurnID:        env.Request.TurnID,
			Status:        analysis.StatusCompleted,
			Candidate:     &env.Candidate,
			Decision:      &decision,
			Output:        output,
		}, nil
	})

	chain.AppendLambda(generate)
	chain.AppendLambda(gate)

	runnable, err := chain.Compile(ctx)
	if err != nil {
		return nil, fmt.Errorf("compile eino chain: %w", err)
	}
	return &Workflow{runnable: runnable}, nil
}

// Invoke executes one bounded in-memory Eino workflow.
func (w *Workflow) Invoke(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	return w.runnable.Invoke(ctx, req)
}
