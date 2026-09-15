package fileartifact

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"biomarker/internal/persistence/artifactstore"
)

var (
	ErrNotFound          = artifactstore.ErrNotFound
	ErrIntegrity         = artifactstore.ErrIntegrity
	ErrImmutableConflict = artifactstore.ErrImmutableConflict
)

// Store is a local immutable content store for Stage-10 payload refs.
//
// It uses caller-visible bucket/key identity plus SHA-256 verification. The
// object key is never trusted as a filesystem path.
type Store struct {
	root string
}

func Open(dir string) (*Store, error) {
	if dir == "" {
		return nil, errors.New("fileartifact: empty root")
	}
	if err := os.MkdirAll(dir, 0o700); err != nil {
		return nil, fmt.Errorf("fileartifact: create root: %w", err)
	}
	if err := os.Chmod(dir, 0o700); err != nil {
		return nil, fmt.Errorf("fileartifact: chmod root: %w", err)
	}
	return &Store{root: dir}, nil
}

func (s *Store) PutImmutable(ctx context.Context, bucket, objectKey string, data []byte, contentType string) (artifactstore.Ref, error) {
	if err := ctx.Err(); err != nil {
		return artifactstore.Ref{}, err
	}
	if bucket == "" || objectKey == "" {
		return artifactstore.Ref{}, errors.New("fileartifact: bucket and object_key are required")
	}

	sum := sha256.Sum256(data)
	ref := artifactstore.Ref{
		Bucket:      bucket,
		ObjectKey:   objectKey,
		SHA256:      hex.EncodeToString(sum[:]),
		SizeBytes:   int64(len(data)),
		ContentType: contentType,
	}
	indexPath := s.indexPath(bucket, objectKey)

	existingRef, err := s.readIndex(indexPath)
	if err == nil {
		if existingRef.SHA256 == ref.SHA256 && existingRef.SizeBytes == ref.SizeBytes && existingRef.ContentType == ref.ContentType {
			return existingRef, nil
		}
		return artifactstore.Ref{}, artifactstore.ErrImmutableConflict
	}
	if !errors.Is(err, artifactstore.ErrNotFound) {
		return artifactstore.Ref{}, err
	}

	contentPath := s.contentPath(ref.SHA256)
	if err := s.writeContent(contentPath, data); err != nil {
		return artifactstore.Ref{}, err
	}
	if err := s.writeIndex(indexPath, ref); err != nil {
		return artifactstore.Ref{}, err
	}
	return ref, nil
}

func (s *Store) Get(ctx context.Context, ref artifactstore.Ref) ([]byte, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	data, err := os.ReadFile(s.contentPath(ref.SHA256))
	if errors.Is(err, os.ErrNotExist) {
		return nil, artifactstore.ErrNotFound
	}
	if err != nil {
		return nil, fmt.Errorf("fileartifact: read: %w", err)
	}
	if err := verifyBytes(ref, data); err != nil {
		return nil, err
	}
	return data, nil
}

func (s *Store) Verify(ctx context.Context, ref artifactstore.Ref) error {
	_, err := s.Get(ctx, ref)
	return err
}

func (s *Store) objectPath(bucket, objectKey string) string {
	indexRef, err := s.readIndex(s.indexPath(bucket, objectKey))
	if err != nil {
		return s.contentPath(strings.Repeat("0", 64))
	}
	return s.contentPath(indexRef.SHA256)
}

func (s *Store) writeContent(path string, data []byte) error {
	existing, err := os.ReadFile(path)
	if err == nil {
		if bytes.Equal(existing, data) {
			return nil
		}
		return artifactstore.ErrIntegrity
	}
	if !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("fileartifact: read content: %w", err)
	}
	return atomicWrite(path, data)
}

func (s *Store) readIndex(path string) (artifactstore.Ref, error) {
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return artifactstore.Ref{}, artifactstore.ErrNotFound
	}
	if err != nil {
		return artifactstore.Ref{}, fmt.Errorf("fileartifact: read index: %w", err)
	}
	var ref artifactstore.Ref
	if err := json.Unmarshal(data, &ref); err != nil {
		return artifactstore.Ref{}, fmt.Errorf("%w: malformed index", artifactstore.ErrIntegrity)
	}
	return ref, nil
}

func (s *Store) writeIndex(path string, ref artifactstore.Ref) error {
	data, err := json.Marshal(ref)
	if err != nil {
		return fmt.Errorf("fileartifact: marshal index: %w", err)
	}
	return atomicWrite(path, append(data, '\n'))
}

func atomicWrite(path string, data []byte) error {
	if err := os.MkdirAll(filepath.Dir(path), 0o700); err != nil {
		return fmt.Errorf("fileartifact: create dir: %w", err)
	}
	tmp, err := os.CreateTemp(filepath.Dir(path), ".artifact-*")
	if err != nil {
		return fmt.Errorf("fileartifact: temp create: %w", err)
	}
	tmpName := tmp.Name()
	defer os.Remove(tmpName)

	if err := tmp.Chmod(0o600); err != nil {
		tmp.Close()
		return fmt.Errorf("fileartifact: chmod temp: %w", err)
	}
	if _, err := tmp.Write(data); err != nil {
		tmp.Close()
		return fmt.Errorf("fileartifact: write temp: %w", err)
	}
	if err := tmp.Sync(); err != nil {
		tmp.Close()
		return fmt.Errorf("fileartifact: fsync temp: %w", err)
	}
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("fileartifact: close temp: %w", err)
	}
	if err := os.Rename(tmpName, path); err != nil {
		return fmt.Errorf("fileartifact: atomic rename: %w", err)
	}
	if err := syncDir(filepath.Dir(path)); err != nil {
		return err
	}
	return nil
}

func (s *Store) indexPath(bucket, objectKey string) string {
	sum := sha256.Sum256([]byte(bucket + "\x00" + objectKey))
	digest := hex.EncodeToString(sum[:])
	return filepath.Join(s.root, safeSegment(bucket), "keys", digest[:2], digest+".json")
}

func (s *Store) contentPath(digest string) string {
	return filepath.Join(s.root, "objects", digest[:2], digest)
}

func verifyBytes(ref artifactstore.Ref, data []byte) error {
	if int64(len(data)) != ref.SizeBytes {
		return artifactstore.ErrIntegrity
	}
	sum := sha256.Sum256(data)
	if hex.EncodeToString(sum[:]) != ref.SHA256 {
		return artifactstore.ErrIntegrity
	}
	return nil
}

func safeSegment(value string) string {
	value = strings.ToLower(value)
	var b strings.Builder
	for _, r := range value {
		switch {
		case r >= 'a' && r <= 'z':
			b.WriteRune(r)
		case r >= '0' && r <= '9':
			b.WriteRune(r)
		case r == '-' || r == '_':
			b.WriteRune(r)
		default:
			b.WriteByte('_')
		}
	}
	if b.Len() == 0 {
		return "_"
	}
	return b.String()
}

func syncDir(dir string) error {
	f, err := os.Open(dir)
	if err != nil {
		return fmt.Errorf("fileartifact: open parent dir: %w", err)
	}
	defer f.Close()
	if err := f.Sync(); err != nil {
		return fmt.Errorf("fileartifact: fsync parent dir: %w", err)
	}
	return nil
}
