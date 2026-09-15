package artifactstore

import (
	"context"
	"errors"
)

var (
	ErrNotFound          = errors.New("artifact not found")
	ErrIntegrity         = errors.New("artifact integrity verification failed")
	ErrImmutableConflict = errors.New("artifact key exists with different immutable content")
)

// Ref is a durable reference to immutable payload bytes.
//
// Stage 10 uses refs to keep large or sensitive payloads out of canonical
// Turn records while preserving replay and integrity evidence.
type Ref struct {
	Bucket      string `json:"bucket"`
	ObjectKey   string `json:"object_key"`
	SHA256      string `json:"sha256"`
	SizeBytes   int64  `json:"size_bytes"`
	ContentType string `json:"content_type,omitempty"`
}

type Store interface {
	PutImmutable(ctx context.Context, bucket, objectKey string, data []byte, contentType string) (Ref, error)
	Get(ctx context.Context, ref Ref) ([]byte, error)
	Verify(ctx context.Context, ref Ref) error
}
