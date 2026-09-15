package analysis

import "testing"

func TestValidateReasoningCandidateRejectsMissingCandidateIdentity(t *testing.T) {
	candidate := ReasoningCandidate{
		SchemaVersion: "1.0",
		Statements: []Statement{{
			ID:                "s1",
			Class:             StatementMeasuredFact,
			Text:              "Synthetic measured fact.",
			InferenceMode:     "none",
			AssertionStrength: "direct_source",
			ClinicalRefs:      []string{"obs-1"},
		}},
	}

	if err := ValidateReasoningCandidate(candidate); err == nil {
		t.Fatal("expected missing candidate_id to fail candidate validation")
	}
}

func TestValidateReasoningCandidateRejectsMissingStatementIdentity(t *testing.T) {
	candidate := ReasoningCandidate{
		SchemaVersion: "1.0",
		CandidateID:   "candidate-1",
		Statements: []Statement{{
			Class:             StatementMeasuredFact,
			Text:              "Synthetic measured fact.",
			InferenceMode:     "none",
			AssertionStrength: "direct_source",
			ClinicalRefs:      []string{"obs-1"},
		}},
	}

	if err := ValidateReasoningCandidate(candidate); err == nil {
		t.Fatal("expected missing statement_id to fail candidate validation")
	}
}

func TestValidateReasoningCandidateAllowsMinimumStructuredCandidate(t *testing.T) {
	candidate := ReasoningCandidate{
		SchemaVersion: "1.0",
		CandidateID:   "candidate-1",
		Statements: []Statement{{
			ID:                "s1",
			Class:             StatementMeasuredFact,
			Text:              "Synthetic measured fact.",
			InferenceMode:     "none",
			AssertionStrength: "direct_source",
			ClinicalRefs:      []string{"obs-1"},
		}},
	}

	if err := ValidateReasoningCandidate(candidate); err != nil {
		t.Fatalf("unexpected candidate validation error: %v", err)
	}
}
