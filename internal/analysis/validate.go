package analysis

import (
	"errors"
	"fmt"
	"strings"
)

var (
	ErrInvalidRequest = errors.New("invalid execution request")
)

// ValidateExecutionRequest performs minimum single-process runtime validation.
func ValidateExecutionRequest(req ExecutionRequest) error {
	if req.SchemaVersion != "1.0" {
		return fmt.Errorf("%w: unsupported schema version", ErrInvalidRequest)
	}
	if strings.TrimSpace(req.TurnID) == "" {
		return fmt.Errorf("%w: turn_id required", ErrInvalidRequest)
	}
	if strings.TrimSpace(req.IdempotencyKey) == "" {
		return fmt.Errorf("%w: idempotency_key required", ErrInvalidRequest)
	}
	if strings.TrimSpace(req.Input.ClinicalSnapshotID) == "" {
		return fmt.Errorf("%w: clinical_snapshot_id required", ErrInvalidRequest)
	}
	if strings.TrimSpace(req.Input.EvidenceBundle.BundleID) == "" {
		return fmt.Errorf("%w: evidence bundle required", ErrInvalidRequest)
	}
	if strings.TrimSpace(req.Input.Policies.ReasoningPolicyDigest) == "" ||
		strings.TrimSpace(req.Input.Policies.SafetyPolicyDigest) == "" {
		return fmt.Errorf("%w: policy closure required", ErrInvalidRequest)
	}
	if req.DeadlineMS < 0 {
		return fmt.Errorf("%w: deadline_ms cannot be negative", ErrInvalidRequest)
	}
	return nil
}

// ValidateReasoningCandidate performs the Stage-09 output-shape preflight check.
func ValidateReasoningCandidate(candidate ReasoningCandidate) error {
	if candidate.SchemaVersion != "1.0" {
		return fmt.Errorf("%w: unsupported candidate schema version", ErrInvalidRequest)
	}
	if strings.TrimSpace(candidate.CandidateID) == "" {
		return fmt.Errorf("%w: candidate_id required", ErrInvalidRequest)
	}
	if len(candidate.Statements) == 0 {
		return fmt.Errorf("%w: at least one candidate statement required", ErrInvalidRequest)
	}
	for i, statement := range candidate.Statements {
		if strings.TrimSpace(statement.ID) == "" {
			return fmt.Errorf("%w: statement_id required at index %d", ErrInvalidRequest, i)
		}
		if strings.TrimSpace(string(statement.Class)) == "" {
			return fmt.Errorf("%w: statement_class required for %s", ErrInvalidRequest, statement.ID)
		}
		if strings.TrimSpace(statement.Text) == "" {
			return fmt.Errorf("%w: statement text required for %s", ErrInvalidRequest, statement.ID)
		}
	}
	return nil
}
