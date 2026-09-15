package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"sync/atomic"
	"time"

	"biomarker/internal/analysis"
	"biomarker/internal/persistence/turnstore"
	"biomarker/internal/platform/persistence/fileturn"
	"biomarker/internal/platform/runtime/persistentlocal"
)

type workflow struct{ calls atomic.Int64 }

func (w *workflow) Invoke(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	w.calls.Add(1)
	return analysis.ExecutionResult{
		SchemaVersion: "1.0",
		TurnID:        req.TurnID,
		Status:        analysis.StatusCompleted,
	}, nil
}

type report struct {
	CompletedSurvivesRestart            bool  `json:"completed_survives_restart"`
	RestartReplayWorkflowCalls          int64 `json:"restart_replay_workflow_calls"`
	IncompleteRequiresRecovery          bool  `json:"incomplete_requires_recovery"`
	IncompleteReexecutionCalls          int64 `json:"incomplete_reexecution_calls"`
	SemanticDigestIgnoresTransportNoise bool  `json:"semantic_digest_ignores_transport_noise"`
	FileCount                           int   `json:"canonical_record_file_count"`
	ElapsedMS                           int64 `json:"elapsed_ms"`
}

func main() {
	start := time.Now()
	dir, err := os.MkdirTemp("", "biomarker-stage10-*")
	if err != nil {
		panic(err)
	}
	defer os.RemoveAll(dir)

	req := request("turn-completed")
	s1, _ := fileturn.Open(dir)
	w1 := &workflow{}
	r1 := persistentlocal.NewRuntime(w1, s1)
	if _, err := r1.Execute(context.Background(), req); err != nil {
		panic(err)
	}

	s2, _ := fileturn.Open(dir)
	w2 := &workflow{}
	r2 := persistentlocal.NewRuntime(w2, s2)
	res, err := r2.Execute(context.Background(), req)
	if err != nil {
		panic(err)
	}

	strandedReq := request("turn-stranded")
	digest, _ := persistentlocal.RequestSemanticDigest(strandedReq)
	_, err = s2.CreateOrLoad(context.Background(), turnstore.Record{
		TurnID:         strandedReq.TurnID,
		IdempotencyKey: strandedReq.IdempotencyKey,
		RequestDigest:  digest,
		Provenance: turnstore.Provenance{
			ClinicalSnapshotID:    strandedReq.Input.ClinicalSnapshotID,
			TimelineSnapshotID:    strandedReq.Input.TimelineSnapshotID,
			EvidenceBundleID:      strandedReq.Input.EvidenceBundle.BundleID,
			ReasoningPolicyDigest: strandedReq.Input.Policies.ReasoningPolicyDigest,
			SafetyPolicyDigest:    strandedReq.Input.Policies.SafetyPolicyDigest,
		},
	})
	if err != nil {
		panic(err)
	}

	s3, _ := fileturn.Open(dir)
	w3 := &workflow{}
	r3 := persistentlocal.NewRuntime(w3, s3)
	_, recoverErr := r3.Execute(context.Background(), strandedReq)

	retry := req
	retry.CorrelationID = "new-correlation"
	retry.DeadlineMS = 9999
	d1, _ := persistentlocal.RequestSemanticDigest(req)
	d2, _ := persistentlocal.RequestSemanticDigest(retry)

	entries, _ := os.ReadDir(dir)
	out := report{
		CompletedSurvivesRestart:            res.Status == analysis.StatusCompleted,
		RestartReplayWorkflowCalls:          w2.calls.Load(),
		IncompleteRequiresRecovery:          recoverErr == persistentlocal.ErrRecoveryRequired,
		IncompleteReexecutionCalls:          w3.calls.Load(),
		SemanticDigestIgnoresTransportNoise: d1 == d2,
		FileCount:                           len(entries),
		ElapsedMS:                           time.Since(start).Milliseconds(),
	}
	b, _ := json.MarshalIndent(out, "", "  ")
	fmt.Println(string(b))
}

func request(turnID string) analysis.ExecutionRequest {
	return analysis.ExecutionRequest{
		SchemaVersion:  "1.0",
		TurnID:         turnID,
		IdempotencyKey: "idem-" + turnID,
		CorrelationID:  "corr-1",
		DeadlineMS:     1000,
		Input: analysis.ReasoningInput{
			ClinicalSnapshotID: "clinical-synthetic-001",
			TimelineSnapshotID: "timeline-synthetic-001",
			EvidenceBundle: analysis.EvidenceBundleRef{
				BundleID:                "evidence-synthetic-001",
				Status:                  "verified",
				ProcessingProfileDigest: strings.Repeat("c", 64),
				Claims:                  []analysis.EvidenceClaimRef{{ID: "claim-1", Status: "supported"}},
			},
			ClinicalRefs: []analysis.ClinicalRef{{
				ID: "obs-1", Type: "observation",
				VerificationState:   "verified",
				ReconciliationState: "resolved",
				TerminologyState:    "validated",
			}},
			Policies: analysis.PolicyClosure{
				ReasoningPolicyDigest: strings.Repeat("a", 64),
				SafetyPolicyDigest:    strings.Repeat("b", 64),
			},
			UserQuestion: "synthetic stage10 question",
		},
	}
}
