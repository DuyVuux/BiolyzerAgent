package local

import (
	"context"

	"biomarker/internal/analysis"
)

type scopeKey struct{}

// Scope is process-local runtime metadata propagated through the workflow context.
type Scope struct {
	TurnID         string
	IdempotencyKey string
	CorrelationID  string
	DeadlineMS     int64
}

// ContextWithScope attaches Stage-09 runtime scope without changing domain contracts.
func ContextWithScope(ctx context.Context, req analysis.ExecutionRequest) context.Context {
	return context.WithValue(ctx, scopeKey{}, Scope{
		TurnID:         req.TurnID,
		IdempotencyKey: req.IdempotencyKey,
		CorrelationID:  req.CorrelationID,
		DeadlineMS:     req.DeadlineMS,
	})
}

// ScopeFromContext returns runtime scope metadata when a workflow adapter needs it.
func ScopeFromContext(ctx context.Context) (Scope, bool) {
	scope, ok := ctx.Value(scopeKey{}).(Scope)
	return scope, ok
}
