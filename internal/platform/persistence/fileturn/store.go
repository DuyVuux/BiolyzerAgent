package fileturn

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sync"

	"biomarker/internal/analysis"
	"biomarker/internal/persistence/artifactstore"
	"biomarker/internal/persistence/turnstore"
)

const recordSchemaVersion = "1.0"

type envelope struct {
	SchemaVersion string           `json:"schema_version"`
	RecordDigest  string           `json:"record_digest"`
	Record        turnstore.Record `json:"record"`
}

// Store is a single-process, single-writer durable Turn store.
//
// It is intentionally a minimum-sufficient Stage-10 adapter:
// - one canonical file per Turn;
// - atomic create using hard-link;
// - atomic replace using same-directory rename;
// - fsync file + parent directory;
// - integrity digest for accidental corruption/tamper detection.
//
// It is NOT a multi-process database and does not provide leases/fencing.
type Store struct {
	root string
	mu   sync.Mutex
}

// Open creates/opens a file-backed store rooted at dir.
func Open(dir string) (*Store, error) {
	if dir == "" {
		return nil, errors.New("fileturn: empty root")
	}
	if err := os.MkdirAll(dir, 0o700); err != nil {
		return nil, fmt.Errorf("fileturn: create root: %w", err)
	}
	if err := os.Chmod(dir, 0o700); err != nil {
		return nil, fmt.Errorf("fileturn: chmod root: %w", err)
	}
	return &Store{root: dir}, nil
}

// CreateOrLoad atomically creates the canonical accepted record or returns
// the existing same-request record. A different semantic request conflicts.
func (s *Store) CreateOrLoad(ctx context.Context, initial turnstore.Record) (turnstore.Reservation, error) {
	if err := ctx.Err(); err != nil {
		return turnstore.Reservation{}, err
	}
	if err := validateInitial(initial); err != nil {
		return turnstore.Reservation{}, err
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	path := s.recordPath(initial.TurnID)
	existing, err := s.loadPath(path)
	switch {
	case err == nil:
		if existing.RequestDigest != initial.RequestDigest || existing.IdempotencyKey != initial.IdempotencyKey {
			return turnstore.Reservation{}, turnstore.ErrConflict
		}
		return turnstore.Reservation{Record: existing, Created: false}, nil
	case !errors.Is(err, turnstore.ErrNotFound):
		return turnstore.Reservation{}, err
	}

	initial.SchemaVersion = recordSchemaVersion
	initial.Status = turnstore.StatusAccepted
	initial.Revision = 1
	initial.Result = nil
	initial.ResultRef = nil
	initial.RecoveryReason = ""
	initial.ReconciliationReason = ""

	if err := s.atomicCreate(path, initial); err != nil {
		if errors.Is(err, os.ErrExist) {
			existing, loadErr := s.loadPath(path)
			if loadErr != nil {
				return turnstore.Reservation{}, loadErr
			}
			if existing.RequestDigest != initial.RequestDigest || existing.IdempotencyKey != initial.IdempotencyKey {
				return turnstore.Reservation{}, turnstore.ErrConflict
			}
			return turnstore.Reservation{Record: existing, Created: false}, nil
		}
		return turnstore.Reservation{}, err
	}
	return turnstore.Reservation{Record: initial, Created: true}, nil
}

// Load returns one verified canonical Turn record.
func (s *Store) Load(ctx context.Context, turnID string) (turnstore.Record, error) {
	if err := ctx.Err(); err != nil {
		return turnstore.Record{}, err
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.loadPath(s.recordPath(turnID))
}

// CommitTerminal atomically replaces ACCEPTED with a terminal result.
// It is single-writer by Stage-10 topology.
func (s *Store) CommitTerminal(ctx context.Context, turnID, requestDigest string, result analysis.ExecutionResult, resultRef *artifactstore.Ref) (turnstore.Record, error) {
	if err := ctx.Err(); err != nil {
		return turnstore.Record{}, err
	}
	s.mu.Lock()
	defer s.mu.Unlock()

	path := s.recordPath(turnID)
	rec, err := s.loadPath(path)
	if err != nil {
		return turnstore.Record{}, err
	}
	if rec.RequestDigest != requestDigest {
		return turnstore.Record{}, turnstore.ErrConflict
	}
	if rec.Status != turnstore.StatusAccepted {
		if isTerminal(rec.Status) && rec.Result != nil && equalResult(*rec.Result, result) && equalRef(rec.ResultRef, resultRef) {
			return rec, nil
		}
		return turnstore.Record{}, turnstore.ErrInvalidTransition
	}

	switch result.Status {
	case analysis.StatusCompleted:
		rec.Status = turnstore.StatusCompleted
	case analysis.StatusFailed:
		rec.Status = turnstore.StatusFailed
	case analysis.StatusCancelled:
		rec.Status = turnstore.StatusCancelled
	default:
		return turnstore.Record{}, fmt.Errorf("%w: unsupported result status %q", turnstore.ErrInvalidTransition, result.Status)
	}
	rec.Result = &result
	rec.ResultRef = cloneRef(resultRef)
	rec.Revision++
	rec.RecoveryReason = ""
	rec.ReconciliationReason = ""

	if err := s.atomicReplace(path, rec); err != nil {
		return turnstore.Record{}, err
	}
	return rec, nil
}

// MarkRecoveryRequired converts a stranded ACCEPTED record to a durable,
// fail-closed recovery-required state. It never re-executes the Turn.
func (s *Store) MarkRecoveryRequired(ctx context.Context, turnID, requestDigest, reason string) (turnstore.Record, error) {
	if err := ctx.Err(); err != nil {
		return turnstore.Record{}, err
	}
	s.mu.Lock()
	defer s.mu.Unlock()

	path := s.recordPath(turnID)
	rec, err := s.loadPath(path)
	if err != nil {
		return turnstore.Record{}, err
	}
	if rec.RequestDigest != requestDigest {
		return turnstore.Record{}, turnstore.ErrConflict
	}

	if rec.Status == turnstore.StatusRecoveryRequired {
		return rec, nil
	}
	if rec.Status != turnstore.StatusAccepted {
		return turnstore.Record{}, turnstore.ErrInvalidTransition
	}

	rec.Status = turnstore.StatusRecoveryRequired
	rec.Revision++
	rec.RecoveryReason = reason
	rec.ReconciliationReason = ""
	if err := s.atomicReplace(path, rec); err != nil {
		return turnstore.Record{}, err
	}
	return rec, nil
}

// MarkNeedsReconciliation freezes a Turn whose external effect may have
// happened but cannot be proven safe to replay.
func (s *Store) MarkNeedsReconciliation(ctx context.Context, turnID, requestDigest, reason string) (turnstore.Record, error) {
	if err := ctx.Err(); err != nil {
		return turnstore.Record{}, err
	}
	s.mu.Lock()
	defer s.mu.Unlock()

	path := s.recordPath(turnID)
	rec, err := s.loadPath(path)
	if err != nil {
		return turnstore.Record{}, err
	}
	if rec.RequestDigest != requestDigest {
		return turnstore.Record{}, turnstore.ErrConflict
	}

	if rec.Status == turnstore.StatusNeedsReconciliation {
		return rec, nil
	}
	if rec.Status != turnstore.StatusAccepted && rec.Status != turnstore.StatusRecoveryRequired {
		return turnstore.Record{}, turnstore.ErrInvalidTransition
	}

	rec.Status = turnstore.StatusNeedsReconciliation
	rec.Revision++
	rec.RecoveryReason = ""
	rec.ReconciliationReason = reason
	if err := s.atomicReplace(path, rec); err != nil {
		return turnstore.Record{}, err
	}
	return rec, nil
}

func validateInitial(rec turnstore.Record) error {
	if rec.TurnID == "" || rec.IdempotencyKey == "" || rec.RequestDigest == "" {
		return errors.New("fileturn: turn_id, idempotency_key and request_digest are required")
	}
	if rec.Provenance.ClinicalSnapshotID == "" || rec.Provenance.EvidenceBundleID == "" ||
		rec.Provenance.ReasoningPolicyDigest == "" || rec.Provenance.SafetyPolicyDigest == "" {
		return errors.New("fileturn: closed input provenance is incomplete")
	}
	return nil
}

func (s *Store) recordPath(turnID string) string {
	sum := sha256.Sum256([]byte(turnID))
	name := hex.EncodeToString(sum[:]) + ".json"
	return filepath.Join(s.root, name)
}

func (s *Store) atomicCreate(path string, rec turnstore.Record) error {
	data, err := encodeEnvelope(rec)
	if err != nil {
		return err
	}

	tmp, err := os.CreateTemp(s.root, ".turn-create-*")
	if err != nil {
		return fmt.Errorf("fileturn: temp create: %w", err)
	}
	tmpName := tmp.Name()
	defer os.Remove(tmpName)

	if err := tmp.Chmod(0o600); err != nil {
		tmp.Close()
		return fmt.Errorf("fileturn: chmod temp: %w", err)
	}
	if _, err := tmp.Write(data); err != nil {
		tmp.Close()
		return fmt.Errorf("fileturn: write temp: %w", err)
	}
	if err := tmp.Sync(); err != nil {
		tmp.Close()
		return fmt.Errorf("fileturn: fsync temp: %w", err)
	}
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("fileturn: close temp: %w", err)
	}

	if err := os.Link(tmpName, path); err != nil {
		return err
	}
	if err := syncDir(s.root); err != nil {
		return err
	}
	return nil
}

func (s *Store) atomicReplace(path string, rec turnstore.Record) error {
	data, err := encodeEnvelope(rec)
	if err != nil {
		return err
	}

	tmp, err := os.CreateTemp(s.root, ".turn-replace-*")
	if err != nil {
		return fmt.Errorf("fileturn: temp replace: %w", err)
	}
	tmpName := tmp.Name()
	defer os.Remove(tmpName)

	if err := tmp.Chmod(0o600); err != nil {
		tmp.Close()
		return fmt.Errorf("fileturn: chmod temp: %w", err)
	}
	if _, err := tmp.Write(data); err != nil {
		tmp.Close()
		return fmt.Errorf("fileturn: write temp: %w", err)
	}
	if err := tmp.Sync(); err != nil {
		tmp.Close()
		return fmt.Errorf("fileturn: fsync temp: %w", err)
	}
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("fileturn: close temp: %w", err)
	}
	if err := os.Rename(tmpName, path); err != nil {
		return fmt.Errorf("fileturn: atomic rename: %w", err)
	}
	if err := syncDir(s.root); err != nil {
		return err
	}
	return nil
}

func (s *Store) loadPath(path string) (turnstore.Record, error) {
	f, err := os.Open(path)
	if errors.Is(err, os.ErrNotExist) {
		return turnstore.Record{}, turnstore.ErrNotFound
	}
	if err != nil {
		return turnstore.Record{}, fmt.Errorf("fileturn: open: %w", err)
	}
	defer f.Close()

	data, err := io.ReadAll(io.LimitReader(f, 8<<20))
	if err != nil {
		return turnstore.Record{}, fmt.Errorf("fileturn: read: %w", err)
	}
	var env envelope
	if err := json.Unmarshal(data, &env); err != nil {
		return turnstore.Record{}, fmt.Errorf("%w: malformed record: %v", turnstore.ErrIntegrity, err)
	}
	if env.SchemaVersion != recordSchemaVersion {
		return turnstore.Record{}, fmt.Errorf("%w: unsupported envelope version", turnstore.ErrIntegrity)
	}
	expected, err := recordDigest(env.Record)
	if err != nil {
		return turnstore.Record{}, err
	}
	if env.RecordDigest != expected {
		return turnstore.Record{}, turnstore.ErrIntegrity
	}
	return env.Record, nil
}

func encodeEnvelope(rec turnstore.Record) ([]byte, error) {
	digest, err := recordDigest(rec)
	if err != nil {
		return nil, err
	}
	env := envelope{
		SchemaVersion: recordSchemaVersion,
		RecordDigest:  digest,
		Record:        rec,
	}
	b, err := json.Marshal(env)
	if err != nil {
		return nil, fmt.Errorf("fileturn: marshal envelope: %w", err)
	}
	return append(b, '\n'), nil
}

func recordDigest(rec turnstore.Record) (string, error) {
	b, err := json.Marshal(rec)
	if err != nil {
		return "", fmt.Errorf("fileturn: marshal record: %w", err)
	}
	sum := sha256.Sum256(b)
	return hex.EncodeToString(sum[:]), nil
}

func equalResult(a, b analysis.ExecutionResult) bool {
	aj, errA := json.Marshal(a)
	bj, errB := json.Marshal(b)
	return errA == nil && errB == nil && string(aj) == string(bj)
}

func cloneRef(ref *artifactstore.Ref) *artifactstore.Ref {
	if ref == nil {
		return nil
	}
	cloned := *ref
	return &cloned
}

func equalRef(a, b *artifactstore.Ref) bool {
	if a == nil || b == nil {
		return a == nil && b == nil
	}
	return *a == *b
}

func isTerminal(status turnstore.Status) bool {
	switch status {
	case turnstore.StatusCompleted, turnstore.StatusFailed, turnstore.StatusCancelled:
		return true
	default:
		return false
	}
}

func syncDir(dir string) error {
	f, err := os.Open(dir)
	if err != nil {
		return fmt.Errorf("fileturn: open parent dir: %w", err)
	}
	defer f.Close()
	if err := f.Sync(); err != nil {
		return fmt.Errorf("fileturn: fsync parent dir: %w", err)
	}
	return nil
}
