package safety

import (
	"testing"

	"biomarker/internal/analysis"
)

func baseInput() analysis.ReasoningInput {
	return analysis.ReasoningInput{
		ClinicalSnapshotID: "clinical-1",
		TimelineSnapshotID: "timeline-1",
		EvidenceBundle: analysis.EvidenceBundleRef{
			BundleID:                "evidence-1",
			Status:                  "verified",
			ProcessingProfileDigest: "profile-digest",
			Claims:                  []analysis.EvidenceClaimRef{{ID: "claim-1", Status: "supported"}},
		},
		ClinicalRefs: []analysis.ClinicalRef{{
			ID: "obs-1", Type: "observation", VerificationState: "verified",
			ReconciliationState: "resolved", TerminologyState: "validated",
		}},
		Policies: analysis.PolicyClosure{
			ReasoningPolicyDigest: "reasoning-digest",
			SafetyPolicyDigest:    "safety-digest",
		},
	}
}

func TestEvaluatorAllowsGroundedBoundedInterpretation(t *testing.T) {
	c := analysis.ReasoningCandidate{
		SchemaVersion: "1.0", CandidateID: "c1",
		Statements: []analysis.Statement{{
			ID: "s1", Class: analysis.StatementBoundedInterpretation,
			Text: "Synthetic bounded interpretation.", InferenceMode: "association",
			AssertionStrength: "bounded", ClinicalRefs: []string{"obs-1"},
			EvidenceClaimRefs: []string{"claim-1"},
		}},
	}
	d, out := NewEvaluator().Evaluate(baseInput(), c)
	if d.Verdict != "approve" || out == nil || !out.PhysicianReviewRequired {
		t.Fatalf("unexpected verdict/output: %#v %#v", d, out)
	}
}

func TestEvaluatorRejectsDiagnosis(t *testing.T) {
	c := analysis.ReasoningCandidate{
		SchemaVersion: "1.0", CandidateID: "c2",
		Statements: []analysis.Statement{{
			ID: "s1", Class: analysis.StatementDiagnosis,
			Text: "Synthetic diagnosis.", InferenceMode: "diagnostic",
			AssertionStrength: "definitive", ClinicalRefs: []string{"obs-1"},
		}},
	}
	d, out := NewEvaluator().Evaluate(baseInput(), c)
	if d.Verdict != "reject" || out != nil {
		t.Fatalf("diagnosis escaped: %#v %#v", d, out)
	}
}

func TestEvaluatorRejectsAmbientAction(t *testing.T) {
	c := analysis.ReasoningCandidate{
		SchemaVersion: "1.0", CandidateID: "c3",
		RequestedActions: []string{"web_search"},
		Statements:       []analysis.Statement{{ID: "s1", Class: analysis.StatementLimitation, Text: "Synthetic limitation."}},
	}
	d, _ := NewEvaluator().Evaluate(baseInput(), c)
	if d.Verdict != "reject" {
		t.Fatalf("ambient action escaped: %#v", d)
	}
}
