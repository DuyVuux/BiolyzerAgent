package analysis

import "context"

// CandidateGenerator produces untrusted structured reasoning candidates.
type CandidateGenerator interface {
	Generate(ctx context.Context, input ReasoningInput) (ReasoningCandidate, error)
}

// SafetyEvaluator is the deterministic safety authority for a candidate.
type SafetyEvaluator interface {
	Evaluate(input ReasoningInput, candidate ReasoningCandidate) (SafetyDecision, *SafeReasoningOutput)
}

// Workflow executes the bounded reasoning flow once.
type Workflow interface {
	Invoke(ctx context.Context, req ExecutionRequest) (ExecutionResult, error)
}

// Runtime is the stable Stage-09 execution port.
type Runtime interface {
	Execute(ctx context.Context, req ExecutionRequest) (ExecutionResult, error)
}
