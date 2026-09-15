package integration

import (
	"context"
	"errors"
	"testing"

	"biomarker/internal/analysis"
	"biomarker/internal/platform/model"
	einoruntime "biomarker/internal/platform/runtime/eino"
	"biomarker/internal/platform/runtime/local"
	"biomarker/internal/safety"
)

func fixture() analysis.ExecutionRequest {
	return analysis.ExecutionRequest{
		SchemaVersion: "1.0", TurnID: "turn-integration", IdempotencyKey: "idem-integration",
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "clinical-synth-1",
			TimelineSnapshotID: "timeline-synth-1",
			EvidenceBundle: analysis.EvidenceBundleRef{
				BundleID: "evidence-synth-1", Status: "verified", ProcessingProfileDigest: "profile",
				Claims: []analysis.EvidenceClaimRef{{ID: "claim-synth-1", Status: "supported"}},
			},
			ClinicalRefs: []analysis.ClinicalRef{{
				ID: "obs-synth-1", Type: "observation", VerificationState: "verified",
				ReconciliationState: "resolved", TerminologyState: "validated",
			}},
			Policies:     analysis.PolicyClosure{ReasoningPolicyDigest: "reasoning", SafetyPolicyDigest: "safety"},
			UserQuestion: "Provide a bounded synthetic summary.",
		},
	}
}

func TestEndToEndSingleProcessRuntime(t *testing.T) {
	g := model.NewDeterministicGenerator()
	w, err := einoruntime.NewWorkflow(context.Background(), g, safety.NewEvaluator())
	if err != nil {
		t.Fatal(err)
	}
	rt := local.NewRuntime(w, local.NewLedger())
	got, err := rt.Execute(context.Background(), fixture())
	if err != nil {
		t.Fatal(err)
	}
	if got.Status != analysis.StatusCompleted || got.Decision == nil || got.Decision.Verdict != "approve" || got.Output == nil {
		t.Fatalf("unexpected result %#v", got)
	}
	if !got.Output.PhysicianReviewRequired {
		t.Fatal("review flag missing")
	}
	if g.Calls() != 1 {
		t.Fatalf("generator calls=%d", g.Calls())
	}
}

func TestDuplicateSameTurnDoesNotRegenerate(t *testing.T) {
	g := model.NewDeterministicGenerator()
	w, err := einoruntime.NewWorkflow(context.Background(), g, safety.NewEvaluator())
	if err != nil {
		t.Fatal(err)
	}
	rt := local.NewRuntime(w, local.NewLedger())
	req := fixture()
	_, err = rt.Execute(context.Background(), req)
	if err != nil {
		t.Fatal(err)
	}
	_, err = rt.Execute(context.Background(), req)
	if err != nil {
		t.Fatal(err)
	}
	if g.Calls() != 1 {
		t.Fatalf("duplicate regenerated calls=%d", g.Calls())
	}
}

func TestConflictingSameTurnFailsClosed(t *testing.T) {
	g := model.NewDeterministicGenerator()
	w, err := einoruntime.NewWorkflow(context.Background(), g, safety.NewEvaluator())
	if err != nil {
		t.Fatal(err)
	}
	rt := local.NewRuntime(w, local.NewLedger())
	req := fixture()
	_, _ = rt.Execute(context.Background(), req)
	req.Input.UserQuestion = "Different semantic input"
	_, err = rt.Execute(context.Background(), req)
	if !errors.Is(err, local.ErrIdempotencyConflict) {
		t.Fatalf("expected conflict, got %v", err)
	}
	if g.Calls() != 1 {
		t.Fatalf("conflict caused second generation calls=%d", g.Calls())
	}
}
