package analysis

// ExecutionStatus is the internal single-process execution outcome.
type ExecutionStatus string

const (
	StatusCompleted ExecutionStatus = "completed"
	StatusFailed    ExecutionStatus = "failed"
	StatusCancelled ExecutionStatus = "cancelled"
)

// StatementClass is a structured clinical statement class.
type StatementClass string

const (
	StatementMeasuredFact          StatementClass = "measured_fact"
	StatementDerivedFact           StatementClass = "derived_fact"
	StatementEvidenceContext       StatementClass = "evidence_context"
	StatementBoundedInterpretation StatementClass = "bounded_interpretation"
	StatementLimitation            StatementClass = "limitation"
	StatementPhysicianQuestion     StatementClass = "physician_question"

	StatementDiagnosis        StatementClass = "diagnosis"
	StatementTreatment        StatementClass = "treatment_recommendation"
	StatementMedicationChange StatementClass = "medication_change"
	StatementDosageChange     StatementClass = "dosage_change"
	StatementEmergencyTriage  StatementClass = "emergency_triage"
)

// ClinicalRef is the minimum Stage-09 runtime view over a closed clinical reference.
type ClinicalRef struct {
	ID                  string `json:"id"`
	Type                string `json:"type"`
	VerificationState   string `json:"verification_state"`
	ReconciliationState string `json:"reconciliation_state"`
	TerminologyState    string `json:"terminology_state"`
	SourceSignal        string `json:"source_signal,omitempty"`
}

// EvidenceClaimRef is the minimum Stage-09 runtime view over a frozen evidence claim.
type EvidenceClaimRef struct {
	ID     string `json:"id"`
	Status string `json:"status"`
}

// EvidenceBundleRef pins the exact Stage-06 evidence bundle used by reasoning.
type EvidenceBundleRef struct {
	BundleID                string             `json:"bundle_id"`
	Status                  string             `json:"status"`
	ProcessingProfileDigest string             `json:"processing_profile_digest"`
	Claims                  []EvidenceClaimRef `json:"claims"`
}

// PolicyClosure pins the reasoning/safety policy identities.
type PolicyClosure struct {
	ReasoningPolicyDigest string `json:"reasoning_policy_digest"`
	SafetyPolicyDigest    string `json:"safety_policy_digest"`
}

// ReasoningInput is the closed input universe consumed by the runtime.
type ReasoningInput struct {
	ClinicalSnapshotID       string            `json:"clinical_snapshot_id"`
	TimelineSnapshotID       string            `json:"timeline_snapshot_id,omitempty"`
	EvidenceBundle           EvidenceBundleRef `json:"evidence_bundle"`
	ClinicalRefs             []ClinicalRef     `json:"clinical_refs"`
	Policies                 PolicyClosure     `json:"policies"`
	UserQuestion             string            `json:"user_question"`
	KnownMissingContext      bool              `json:"known_missing_context,omitempty"`
	CriticalValuePolicyState string            `json:"critical_value_policy_state,omitempty"`
}

// ExecutionRequest is the Stage-09 internal runtime request contract.
type ExecutionRequest struct {
	SchemaVersion  string         `json:"schema_version"`
	TurnID         string         `json:"turn_id"`
	IdempotencyKey string         `json:"idempotency_key"`
	CorrelationID  string         `json:"correlation_id,omitempty"`
	DeadlineMS     int64          `json:"deadline_ms,omitempty"`
	Input          ReasoningInput `json:"input"`
}

// Statement is a model-generated structured statement candidate.
type Statement struct {
	ID                         string         `json:"statement_id"`
	Class                      StatementClass `json:"statement_class"`
	Text                       string         `json:"text"`
	InferenceMode              string         `json:"inference_mode"`
	AssertionStrength          string         `json:"assertion_strength"`
	ClinicalRefs               []string       `json:"clinical_refs,omitempty"`
	EvidenceClaimRefs          []string       `json:"evidence_claim_refs,omitempty"`
	DerivationRef              string         `json:"derivation_ref,omitempty"`
	ConflictDisclosed          bool           `json:"conflict_disclosed,omitempty"`
	MissingContextAcknowledged bool           `json:"missing_context_acknowledged,omitempty"`
}

// ReasoningCandidate is untrusted model output.
type ReasoningCandidate struct {
	SchemaVersion    string      `json:"schema_version"`
	CandidateID      string      `json:"candidate_id"`
	RequestedActions []string    `json:"requested_actions"`
	Statements       []Statement `json:"statements"`
}

// Violation is a deterministic safety-policy finding.
type Violation struct {
	Gate        string `json:"gate"`
	Code        string `json:"code"`
	StatementID string `json:"statement_id,omitempty"`
	RefID       string `json:"ref_id,omitempty"`
}

// SafetyDecision is the deterministic gate verdict.
type SafetyDecision struct {
	Verdict    string      `json:"verdict"`
	Violations []Violation `json:"violations"`
}

// ReviewBasis lets a physician independently trace approved output.
type ReviewBasis struct {
	ClinicalSnapshotID string   `json:"clinical_snapshot_id"`
	TimelineSnapshotID string   `json:"timeline_snapshot_id,omitempty"`
	EvidenceBundleID   string   `json:"evidence_bundle_id"`
	ClinicalRefs       []string `json:"clinical_refs"`
	EvidenceClaimRefs  []string `json:"evidence_claim_refs"`
	PolicyDigests      []string `json:"policy_digests"`
}

// SafeReasoningOutput is the only Stage-09 model-derived output allowed downstream.
type SafeReasoningOutput struct {
	PhysicianReviewRequired bool        `json:"physician_review_required"`
	ApprovedStatements      []Statement `json:"approved_statements"`
	ReviewBasis             ReviewBasis `json:"review_basis"`
	Limitations             []string    `json:"limitations,omitempty"`
}

// RuntimeError is a safe internal failure classification.
type RuntimeError struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

// ExecutionResult is the Stage-09 internal runtime result.
type ExecutionResult struct {
	SchemaVersion string               `json:"schema_version"`
	TurnID        string               `json:"turn_id"`
	Status        ExecutionStatus      `json:"status"`
	Candidate     *ReasoningCandidate  `json:"candidate,omitempty"`
	Decision      *SafetyDecision      `json:"decision,omitempty"`
	Output        *SafeReasoningOutput `json:"output,omitempty"`
	Error         *RuntimeError        `json:"error,omitempty"`
}
