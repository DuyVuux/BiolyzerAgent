package eino

import (
	"context"
	"errors"
	"testing"

	"biomarker/internal/analysis"
	"biomarker/internal/platform/model"
	"biomarker/internal/safety"
)

func TestWorkflowInvokesDeterministicStructuredPipeline(t *testing.T) {
	input := analysis.ReasoningInput{
		ClinicalSnapshotID: "clinical-1",
		EvidenceBundle: analysis.EvidenceBundleRef{
			BundleID: "evidence-1", Status: "verified", ProcessingProfileDigest: "p",
			Claims: []analysis.EvidenceClaimRef{{ID: "claim-1", Status: "supported"}},
		},
		ClinicalRefs: []analysis.ClinicalRef{{
			ID: "obs-1", VerificationState: "verified", ReconciliationState: "resolved", TerminologyState: "validated",
		}},
		Policies: analysis.PolicyClosure{ReasoningPolicyDigest: "r", SafetyPolicyDigest: "s"},
	}
	w, err := NewWorkflow(context.Background(), model.NewDeterministicGenerator(), safety.NewEvaluator())
	if err != nil {
		t.Fatal(err)
	}
	got, err := w.Invoke(context.Background(), analysis.ExecutionRequest{
		SchemaVersion: "1.0", TurnID: "turn-1", IdempotencyKey: "idem-1", Input: input,
	})
	if err != nil {
		t.Fatal(err)
	}
	if got.Status != analysis.StatusCompleted || got.Decision == nil || got.Decision.Verdict != "approve" || got.Output == nil {
		t.Fatalf("unexpected result: %#v", got)
	}
}

type spyGenerator struct {
	called bool
}

func (g *spyGenerator) Generate(ctx context.Context, input analysis.ReasoningInput) (analysis.ReasoningCandidate, error) {
	g.called = true
	return analysis.ReasoningCandidate{}, nil
}

func TestWorkflowChecksContextBeforeGenerationNode(t *testing.T) {
	g := &spyGenerator{}
	w, err := NewWorkflow(context.Background(), g, safety.NewEvaluator())
	if err != nil {
		t.Fatal(err)
	}

	ctx, cancel := context.WithCancel(context.Background())
	cancel()

	_, err = w.Invoke(ctx, analysis.ExecutionRequest{
		SchemaVersion:  "1.0",
		TurnID:         "turn-cancelled",
		IdempotencyKey: "idem-cancelled",
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "clinical-1",
			EvidenceBundle:     analysis.EvidenceBundleRef{BundleID: "evidence-1", Status: "verified", ProcessingProfileDigest: "p"},
			Policies:           analysis.PolicyClosure{ReasoningPolicyDigest: "r", SafetyPolicyDigest: "s"},
		},
	})
	if !errors.Is(err, context.Canceled) {
		t.Fatalf("expected context cancellation before generation, got %v", err)
	}
	if g.called {
		t.Fatal("generator was called after context had already been cancelled")
	}
}

type malformedGenerator struct{}

func (malformedGenerator) Generate(ctx context.Context, input analysis.ReasoningInput) (analysis.ReasoningCandidate, error) {
	return analysis.ReasoningCandidate{
		SchemaVersion: "1.0",
		Statements: []analysis.Statement{{
			ID:                "s1",
			Class:             analysis.StatementMeasuredFact,
			Text:              "Synthetic measured fact.",
			InferenceMode:     "none",
			AssertionStrength: "direct_source",
			ClinicalRefs:      []string{"obs-1"},
		}},
	}, nil
}

func TestWorkflowRejectsMalformedCandidateBeforeSafetyGate(t *testing.T) {
	w, err := NewWorkflow(context.Background(), malformedGenerator{}, safety.NewEvaluator())
	if err != nil {
		t.Fatal(err)
	}

	_, err = w.Invoke(context.Background(), analysis.ExecutionRequest{
		SchemaVersion:  "1.0",
		TurnID:         "turn-malformed",
		IdempotencyKey: "idem-malformed",
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "clinical-1",
			EvidenceBundle:     analysis.EvidenceBundleRef{BundleID: "evidence-1", Status: "verified", ProcessingProfileDigest: "p"},
			ClinicalRefs: []analysis.ClinicalRef{{
				ID: "obs-1", VerificationState: "verified", ReconciliationState: "resolved", TerminologyState: "validated",
			}},
			Policies: analysis.PolicyClosure{ReasoningPolicyDigest: "r", SafetyPolicyDigest: "s"},
		},
	})
	if err == nil {
		t.Fatal("expected malformed candidate to fail before safety evaluation")
	}
}
