package safety

import (
	"sort"

	"biomarker/internal/analysis"
)

// Evaluator implements the Stage-09 deterministic safety boundary.
type Evaluator struct{}

// NewEvaluator creates the deterministic evaluator.
func NewEvaluator() *Evaluator { return &Evaluator{} }

var prohibited = map[analysis.StatementClass]bool{
	analysis.StatementDiagnosis:        true,
	analysis.StatementTreatment:        true,
	analysis.StatementMedicationChange: true,
	analysis.StatementDosageChange:     true,
	analysis.StatementEmergencyTriage:  true,
}

var prohibitedInference = map[string]bool{
	"diagnostic":              true,
	"therapeutic":             true,
	"triage":                  true,
	"patient_specific_causal": true,
}

func violation(gate, code, sid, ref string) analysis.Violation {
	return analysis.Violation{Gate: gate, Code: code, StatementID: sid, RefID: ref}
}

// Evaluate applies deterministic policy to an untrusted candidate.
func (e *Evaluator) Evaluate(input analysis.ReasoningInput, candidate analysis.ReasoningCandidate) (analysis.SafetyDecision, *analysis.SafeReasoningOutput) {
	var violations []analysis.Violation
	limited := false

	if input.EvidenceBundle.ProcessingProfileDigest == "" ||
		input.Policies.ReasoningPolicyDigest == "" ||
		input.Policies.SafetyPolicyDigest == "" {
		violations = append(violations, violation("G0", "MISSING_POLICY_DIGEST", "", ""))
	}
	if input.EvidenceBundle.Status == "incomplete" {
		violations = append(violations, violation("G2", "EVIDENCE_BUNDLE_INCOMPLETE", "", input.EvidenceBundle.BundleID))
	}

	clinical := map[string]analysis.ClinicalRef{}
	for _, r := range input.ClinicalRefs {
		clinical[r.ID] = r
	}
	evidence := map[string]analysis.EvidenceClaimRef{}
	for _, r := range input.EvidenceBundle.Claims {
		evidence[r.ID] = r
	}

	if len(candidate.RequestedActions) > 0 {
		for _, a := range candidate.RequestedActions {
			violations = append(violations, violation("G3", "AMBIENT_ACTION_REQUESTED", "", a))
		}
	}

	usedClinical := map[string]bool{}
	usedEvidence := map[string]bool{}

	for _, s := range candidate.Statements {
		if prohibited[s.Class] || prohibitedInference[s.InferenceMode] {
			violations = append(violations, violation("G4", "PROHIBITED_CLINICAL_BEHAVIOR", s.ID, ""))
		}
		if s.AssertionStrength == "definitive" && s.Class == analysis.StatementBoundedInterpretation {
			violations = append(violations, violation("G4", "DEFINITIVE_PATIENT_ASSERTION", s.ID, ""))
		}

		switch s.Class {
		case analysis.StatementMeasuredFact:
			if len(s.ClinicalRefs) == 0 {
				violations = append(violations, violation("G5", "MEASURED_FACT_UNGROUNDED", s.ID, ""))
			}
		case analysis.StatementDerivedFact:
			if len(s.ClinicalRefs) == 0 || s.DerivationRef == "" {
				violations = append(violations, violation("G5", "DERIVED_FACT_UNGROUNDED", s.ID, ""))
			}
		case analysis.StatementEvidenceContext:
			if len(s.EvidenceClaimRefs) == 0 {
				violations = append(violations, violation("G5", "EVIDENCE_CONTEXT_UNGROUNDED", s.ID, ""))
			}
		case analysis.StatementBoundedInterpretation:
			if len(s.ClinicalRefs) == 0 || len(s.EvidenceClaimRefs) == 0 {
				violations = append(violations, violation("G5", "INTERPRETATION_UNGROUNDED", s.ID, ""))
			}
		}

		for _, refID := range s.ClinicalRefs {
			ref, ok := clinical[refID]
			if !ok {
				violations = append(violations, violation("G1", "UNKNOWN_CLINICAL_REF", s.ID, refID))
				continue
			}
			usedClinical[refID] = true
			if ref.VerificationState != "verified" {
				violations = append(violations, violation("G1", "CLINICAL_REF_UNVERIFIED", s.ID, refID))
			}
			if ref.ReconciliationState == "reconciliation_required" {
				violations = append(violations, violation("G1", "CLINICAL_REF_RECONCILIATION_REQUIRED", s.ID, refID))
			}
			if s.Class == analysis.StatementBoundedInterpretation &&
				(ref.TerminologyState == "candidate" || ref.TerminologyState == "unmapped") {
				violations = append(violations, violation("G1", "TERMINOLOGY_NOT_VALIDATED", s.ID, refID))
			}
			if ref.SourceSignal == "critical" &&
				input.CriticalValuePolicyState == "disabled_pending_approved_clinical_policy" {
				limited = true
				violations = append(violations, violation("G6", "CRITICAL_SIGNAL_PRESENT_POLICY_DISABLED", s.ID, refID))
			}
		}

		for _, claimID := range s.EvidenceClaimRefs {
			ref, ok := evidence[claimID]
			if !ok {
				violations = append(violations, violation("G2", "UNKNOWN_EVIDENCE_CLAIM", s.ID, claimID))
				continue
			}
			usedEvidence[claimID] = true
			switch ref.Status {
			case "unsupported":
				violations = append(violations, violation("G2", "EVIDENCE_CLAIM_UNSUPPORTED", s.ID, claimID))
			case "claim_identity_conflict":
				violations = append(violations, violation("G2", "EVIDENCE_CLAIM_IDENTITY_CONFLICT", s.ID, claimID))
			case "conflicted":
				if !s.ConflictDisclosed {
					violations = append(violations, violation("G6", "EVIDENCE_CONFLICT_NOT_DISCLOSED", s.ID, claimID))
				} else {
					limited = true
				}
			}
		}

		if input.KnownMissingContext && s.Class == analysis.StatementBoundedInterpretation {
			if !s.MissingContextAcknowledged {
				violations = append(violations, violation("G6", "MISSING_CONTEXT_NOT_DISCLOSED", s.ID, ""))
			} else {
				limited = true
			}
		}
	}

	verdict := classify(violations, limited)
	decision := analysis.SafetyDecision{Verdict: verdict, Violations: violations}
	if verdict == "reject" || verdict == "defer" {
		return decision, nil
	}

	clinicalIDs := keys(usedClinical)
	evidenceIDs := keys(usedEvidence)
	policyDigests := []string{
		input.EvidenceBundle.ProcessingProfileDigest,
		input.Policies.ReasoningPolicyDigest,
		input.Policies.SafetyPolicyDigest,
	}
	sort.Strings(policyDigests)

	output := &analysis.SafeReasoningOutput{
		PhysicianReviewRequired: true,
		ApprovedStatements:      candidate.Statements,
		ReviewBasis: analysis.ReviewBasis{
			ClinicalSnapshotID: input.ClinicalSnapshotID,
			TimelineSnapshotID: input.TimelineSnapshotID,
			EvidenceBundleID:   input.EvidenceBundle.BundleID,
			ClinicalRefs:       clinicalIDs,
			EvidenceClaimRefs:  evidenceIDs,
			PolicyDigests:      unique(policyDigests),
		},
	}
	if verdict == "approve_with_limitations" {
		output.Limitations = []string{"Structured output contains an explicit review limitation."}
	}
	return decision, output
}

func classify(vs []analysis.Violation, limited bool) string {
	rejectCodes := map[string]bool{
		"AMBIENT_ACTION_REQUESTED":         true,
		"PROHIBITED_CLINICAL_BEHAVIOR":     true,
		"DEFINITIVE_PATIENT_ASSERTION":     true,
		"MEASURED_FACT_UNGROUNDED":         true,
		"DERIVED_FACT_UNGROUNDED":          true,
		"EVIDENCE_CONTEXT_UNGROUNDED":      true,
		"INTERPRETATION_UNGROUNDED":        true,
		"UNKNOWN_CLINICAL_REF":             true,
		"UNKNOWN_EVIDENCE_CLAIM":           true,
		"EVIDENCE_CLAIM_UNSUPPORTED":       true,
		"EVIDENCE_CLAIM_IDENTITY_CONFLICT": true,
		"EVIDENCE_CONFLICT_NOT_DISCLOSED":  true,
		"MISSING_CONTEXT_NOT_DISCLOSED":    true,
	}
	deferCodes := map[string]bool{
		"MISSING_POLICY_DIGEST":                true,
		"EVIDENCE_BUNDLE_INCOMPLETE":           true,
		"CLINICAL_REF_UNVERIFIED":              true,
		"CLINICAL_REF_RECONCILIATION_REQUIRED": true,
		"TERMINOLOGY_NOT_VALIDATED":            true,
	}
	for _, v := range vs {
		if rejectCodes[v.Code] {
			return "reject"
		}
	}
	for _, v := range vs {
		if deferCodes[v.Code] {
			return "defer"
		}
	}
	if limited || len(vs) > 0 {
		return "approve_with_limitations"
	}
	return "approve"
}

func keys(m map[string]bool) []string {
	out := make([]string, 0, len(m))
	for k := range m {
		out = append(out, k)
	}
	sort.Strings(out)
	return out
}

func unique(in []string) []string {
	if len(in) == 0 {
		return nil
	}
	out := []string{in[0]}
	for _, v := range in[1:] {
		if v != out[len(out)-1] {
			out = append(out, v)
		}
	}
	return out
}
