package model

import (
	"context"
	"fmt"
	"sync/atomic"

	"biomarker/internal/analysis"
)

// DeterministicGenerator is a local no-network model substitute for Stage 09.
type DeterministicGenerator struct {
	calls atomic.Int64
}

// NewDeterministicGenerator creates a deterministic generator.
func NewDeterministicGenerator() *DeterministicGenerator {
	return &DeterministicGenerator{}
}

// Calls returns the number of actual generation executions.
func (g *DeterministicGenerator) Calls() int64 { return g.calls.Load() }

// Generate creates a stable candidate from the closed input universe.
func (g *DeterministicGenerator) Generate(ctx context.Context, input analysis.ReasoningInput) (analysis.ReasoningCandidate, error) {
	select {
	case <-ctx.Done():
		return analysis.ReasoningCandidate{}, ctx.Err()
	default:
	}
	g.calls.Add(1)

	if len(input.ClinicalRefs) == 0 {
		return analysis.ReasoningCandidate{}, fmt.Errorf("no clinical references available")
	}

	firstClinical := input.ClinicalRefs[0].ID
	if len(input.EvidenceBundle.Claims) == 0 {
		return analysis.ReasoningCandidate{
			SchemaVersion: "1.0",
			CandidateID:   "deterministic-measured-fact",
			Statements: []analysis.Statement{{
				ID: "s1", Class: analysis.StatementMeasuredFact,
				Text:          "Synthetic measured fact from the provided clinical reference.",
				InferenceMode: "none", AssertionStrength: "direct_source",
				ClinicalRefs: []string{firstClinical},
			}},
		}, nil
	}

	return analysis.ReasoningCandidate{
		SchemaVersion: "1.0",
		CandidateID:   "deterministic-bounded-interpretation",
		Statements: []analysis.Statement{{
			ID: "s1", Class: analysis.StatementBoundedInterpretation,
			Text:          "Synthetic bounded interpretation grounded in the provided clinical and evidence references.",
			InferenceMode: "association", AssertionStrength: "bounded",
			ClinicalRefs:               []string{firstClinical},
			EvidenceClaimRefs:          []string{input.EvidenceBundle.Claims[0].ID},
			ConflictDisclosed:          input.EvidenceBundle.Claims[0].Status == "conflicted",
			MissingContextAcknowledged: input.KnownMissingContext,
		}},
	}, nil
}
