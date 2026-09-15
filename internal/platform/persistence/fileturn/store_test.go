package fileturn

import (
	"context"
	"errors"
	"os"
	"strings"
	"testing"

	"biomarker/internal/analysis"
	"biomarker/internal/persistence/artifactstore"
	"biomarker/internal/persistence/turnstore"
)

func TestRecordSurvivesReopen(t *testing.T) {
	dir := t.TempDir()
	s1, err := Open(dir)
	if err != nil {
		t.Fatal(err)
	}

	initial := testRecord("turn-1", "digest-1")
	res, err := s1.CreateOrLoad(context.Background(), initial)
	if err != nil || !res.Created {
		t.Fatalf("reserve: %#v %v", res, err)
	}

	result := completedResult("turn-1")
	if _, err := s1.CommitTerminal(context.Background(), "turn-1", "digest-1", result, nil); err != nil {
		t.Fatal(err)
	}

	s2, err := Open(dir)
	if err != nil {
		t.Fatal(err)
	}
	got, err := s2.Load(context.Background(), "turn-1")
	if err != nil {
		t.Fatal(err)
	}
	if got.Status != turnstore.StatusCompleted || got.Result == nil || got.Result.TurnID != "turn-1" {
		t.Fatalf("unexpected persisted record: %#v", got)
	}
}

func TestSameIdentityDifferentDigestConflicts(t *testing.T) {
	s, _ := Open(t.TempDir())
	if _, err := s.CreateOrLoad(context.Background(), testRecord("turn-1", "a")); err != nil {
		t.Fatal(err)
	}
	_, err := s.CreateOrLoad(context.Background(), testRecord("turn-1", "b"))
	if !errors.Is(err, turnstore.ErrConflict) {
		t.Fatalf("expected conflict, got %v", err)
	}
}

func TestTamperedRecordFailsIntegrity(t *testing.T) {
	dir := t.TempDir()
	s, _ := Open(dir)
	if _, err := s.CreateOrLoad(context.Background(), testRecord("turn-1", "a")); err != nil {
		t.Fatal(err)
	}

	path := s.recordPath("turn-1")
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	data = []byte(strings.Replace(string(data), `"accepted"`, `"completed"`, 1))
	if err := os.WriteFile(path, data, 0o600); err != nil {
		t.Fatal(err)
	}

	_, err = s.Load(context.Background(), "turn-1")
	if !errors.Is(err, turnstore.ErrIntegrity) {
		t.Fatalf("expected integrity failure, got %v", err)
	}
}

func TestOrphanTempFileDoesNotBecomeCanonical(t *testing.T) {
	dir := t.TempDir()
	s, _ := Open(dir)
	if err := os.WriteFile(dir+"/.turn-replace-orphan", []byte(`garbage`), 0o600); err != nil {
		t.Fatal(err)
	}

	_, err := s.Load(context.Background(), "turn-missing")
	if !errors.Is(err, turnstore.ErrNotFound) {
		t.Fatalf("orphan temp affected canonical state: %v", err)
	}
}

func TestRequestPayloadIsNotPersistedByTurnRecord(t *testing.T) {
	dir := t.TempDir()
	s, _ := Open(dir)
	if _, err := s.CreateOrLoad(context.Background(), testRecord("turn-privacy", "digest")); err != nil {
		t.Fatal(err)
	}

	data, err := os.ReadFile(s.recordPath("turn-privacy"))
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(string(data), "user_question") || strings.Contains(string(data), "synthetic raw question") {
		t.Fatal("raw request payload leaked into durable Turn record")
	}
}

func TestTerminalResultReferenceIsPersisted(t *testing.T) {
	s, _ := Open(t.TempDir())
	if _, err := s.CreateOrLoad(context.Background(), testRecord("turn-ref", "digest")); err != nil {
		t.Fatal(err)
	}

	ref := artifactstore.Ref{
		Bucket:      "runtime",
		ObjectKey:   "turn-ref/result.json",
		SHA256:      strings.Repeat("c", 64),
		SizeBytes:   17,
		ContentType: "application/json",
	}
	committed, err := s.CommitTerminal(context.Background(), "turn-ref", "digest", completedResult("turn-ref"), &ref)
	if err != nil {
		t.Fatal(err)
	}
	if committed.ResultRef == nil || *committed.ResultRef != ref {
		t.Fatalf("result ref not persisted: %#v", committed.ResultRef)
	}

	reopened, err := s.Load(context.Background(), "turn-ref")
	if err != nil {
		t.Fatal(err)
	}
	if reopened.ResultRef == nil || *reopened.ResultRef != ref {
		t.Fatalf("result ref not reopened: %#v", reopened.ResultRef)
	}
}

func TestTerminalResultCannotBeOverwrittenWithDifferentOutcome(t *testing.T) {
	s, _ := Open(t.TempDir())
	if _, err := s.CreateOrLoad(context.Background(), testRecord("turn-terminal", "digest")); err != nil {
		t.Fatal(err)
	}
	if _, err := s.CommitTerminal(context.Background(), "turn-terminal", "digest", completedResult("turn-terminal"), nil); err != nil {
		t.Fatal(err)
	}

	changed := analysis.ExecutionResult{
		SchemaVersion: "1.0",
		TurnID:        "turn-terminal",
		Status:        analysis.StatusFailed,
		Error:         &analysis.RuntimeError{Code: "DIFFERENT", Message: "different terminal result"},
	}
	_, err := s.CommitTerminal(context.Background(), "turn-terminal", "digest", changed, nil)
	if !errors.Is(err, turnstore.ErrInvalidTransition) {
		t.Fatalf("expected invalid transition, got %v", err)
	}
	loaded, err := s.Load(context.Background(), "turn-terminal")
	if err != nil {
		t.Fatal(err)
	}
	if loaded.Status != turnstore.StatusCompleted {
		t.Fatalf("terminal status was overwritten: %#v", loaded)
	}
}

func TestRecoveryRequiredCannotBecomeTerminalWithoutReconciliation(t *testing.T) {
	s, _ := Open(t.TempDir())
	if _, err := s.CreateOrLoad(context.Background(), testRecord("turn-recovery", "digest")); err != nil {
		t.Fatal(err)
	}
	if _, err := s.MarkRecoveryRequired(context.Background(), "turn-recovery", "digest", "lost owner"); err != nil {
		t.Fatal(err)
	}

	_, err := s.CommitTerminal(context.Background(), "turn-recovery", "digest", completedResult("turn-recovery"), nil)
	if !errors.Is(err, turnstore.ErrInvalidTransition) {
		t.Fatalf("expected invalid transition, got %v", err)
	}
}

func TestNeedsReconciliationFreezesTurnUntilManualResolution(t *testing.T) {
	s, _ := Open(t.TempDir())
	if _, err := s.CreateOrLoad(context.Background(), testRecord("turn-unknown", "digest")); err != nil {
		t.Fatal(err)
	}

	rec, err := s.MarkNeedsReconciliation(context.Background(), "turn-unknown", "digest", "mutating external effect outcome unknown")
	if err != nil {
		t.Fatal(err)
	}
	if rec.Status != turnstore.StatusNeedsReconciliation || rec.ReconciliationReason == "" {
		t.Fatalf("unexpected reconciliation record: %#v", rec)
	}

	_, err = s.CommitTerminal(context.Background(), "turn-unknown", "digest", completedResult("turn-unknown"), nil)
	if !errors.Is(err, turnstore.ErrInvalidTransition) {
		t.Fatalf("expected invalid transition, got %v", err)
	}
	_, err = s.MarkRecoveryRequired(context.Background(), "turn-unknown", "digest", "lost owner")
	if !errors.Is(err, turnstore.ErrInvalidTransition) {
		t.Fatalf("expected invalid transition, got %v", err)
	}
}

func testRecord(turnID, digest string) turnstore.Record {
	return turnstore.Record{
		TurnID:         turnID,
		IdempotencyKey: "idem-1",
		RequestDigest:  digest,
		Provenance: turnstore.Provenance{
			ClinicalSnapshotID:    "clinical-synthetic-001",
			TimelineSnapshotID:    "timeline-synthetic-001",
			EvidenceBundleID:      "evidence-synthetic-001",
			ReasoningPolicyDigest: strings.Repeat("a", 64),
			SafetyPolicyDigest:    strings.Repeat("b", 64),
		},
	}
}

func completedResult(turnID string) analysis.ExecutionResult {
	return analysis.ExecutionResult{
		SchemaVersion: "1.0",
		TurnID:        turnID,
		Status:        analysis.StatusCompleted,
	}
}
