package turnstore

import (
	"context"
	"errors"

	"biomarker/internal/analysis"
	"biomarker/internal/persistence/artifactstore"
)

var (
	ErrNotFound          = errors.New("turn record not found")
	ErrConflict          = errors.New("turn identity conflicts with existing semantic request")
	ErrIntegrity         = errors.New("turn record integrity verification failed")
	ErrInvalidTransition = errors.New("invalid durable turn state transition")
)

// Status is the durable canonical lifecycle of one logical Turn.
// It intentionally does not model physical execution attempts.
type Status string

const (
	StatusAccepted            Status = "accepted"
	StatusCompleted           Status = "completed"
	StatusFailed              Status = "failed"
	StatusCancelled           Status = "cancelled"
	StatusRecoveryRequired    Status = "recovery_required"
	StatusNeedsReconciliation Status = "needs_reconciliation"
)

// Provenance is the minimum immutable execution-input provenance needed
// to reconstruct which closed clinical/evidence universe a Turn used.
// It deliberately excludes raw user question text.
type Provenance struct {
	ClinicalSnapshotID    string `json:"clinical_snapshot_id"`
	TimelineSnapshotID    string `json:"timeline_snapshot_id,omitempty"`
	EvidenceBundleID      string `json:"evidence_bundle_id"`
	ReasoningPolicyDigest string `json:"reasoning_policy_digest"`
	SafetyPolicyDigest    string `json:"safety_policy_digest"`
}

// Record is the canonical durable state for one logical Turn.
type Record struct {
	SchemaVersion        string                    `json:"schema_version"`
	TurnID               string                    `json:"turn_id"`
	IdempotencyKey       string                    `json:"idempotency_key"`
	RequestDigest        string                    `json:"request_digest"`
	Provenance           Provenance                `json:"provenance"`
	Status               Status                    `json:"status"`
	Result               *analysis.ExecutionResult `json:"result,omitempty"`
	ResultRef            *artifactstore.Ref        `json:"result_ref,omitempty"`
	Revision             uint64                    `json:"revision"`
	RecoveryReason       string                    `json:"recovery_reason,omitempty"`
	ReconciliationReason string                    `json:"reconciliation_reason,omitempty"`
}

// Reservation describes CreateOrLoad.
type Reservation struct {
	Record  Record
	Created bool
}

// Store owns canonical durable Turn state.
//
// Stage 10 assumes one application process / one writer topology.
// Cross-process ownership, leases and fencing are explicitly Stage 11/12 concerns.
type Store interface {
	CreateOrLoad(ctx context.Context, initial Record) (Reservation, error)
	Load(ctx context.Context, turnID string) (Record, error)
	CommitTerminal(ctx context.Context, turnID, requestDigest string, result analysis.ExecutionResult, resultRef *artifactstore.Ref) (Record, error)
	MarkRecoveryRequired(ctx context.Context, turnID, requestDigest, reason string) (Record, error)
	MarkNeedsReconciliation(ctx context.Context, turnID, requestDigest, reason string) (Record, error)
}
