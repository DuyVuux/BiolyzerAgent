package fileartifact

import (
	"bytes"
	"context"
	"errors"
	"os"
	"testing"
)

func TestPutImmutableIsIdempotentForSameContent(t *testing.T) {
	store, err := Open(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}

	first, err := store.PutImmutable(context.Background(), "runtime", "turn-1/result.json", []byte(`{"ok":true}`), "application/json")
	if err != nil {
		t.Fatal(err)
	}
	second, err := store.PutImmutable(context.Background(), "runtime", "turn-1/result.json", []byte(`{"ok":true}`), "application/json")
	if err != nil {
		t.Fatal(err)
	}

	if first != second {
		t.Fatalf("same immutable content returned different refs: %#v %#v", first, second)
	}
}

func TestPutImmutableConflictsForSameKeyDifferentContent(t *testing.T) {
	store, err := Open(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}

	if _, err := store.PutImmutable(context.Background(), "runtime", "turn-1/result.json", []byte(`{"ok":true}`), "application/json"); err != nil {
		t.Fatal(err)
	}
	_, err = store.PutImmutable(context.Background(), "runtime", "turn-1/result.json", []byte(`{"ok":false}`), "application/json")
	if !errors.Is(err, ErrImmutableConflict) {
		t.Fatalf("expected immutable conflict, got %v", err)
	}
}

func TestGetVerifiesChecksumAndDetectsCorruption(t *testing.T) {
	dir := t.TempDir()
	store, err := Open(dir)
	if err != nil {
		t.Fatal(err)
	}

	ref, err := store.PutImmutable(context.Background(), "runtime", "turn-1/result.json", []byte(`{"ok":true}`), "application/json")
	if err != nil {
		t.Fatal(err)
	}
	path := store.objectPath(ref.Bucket, ref.ObjectKey)
	if err := os.WriteFile(path, []byte(`{"ok":"tampered"}`), 0o600); err != nil {
		t.Fatal(err)
	}

	_, err = store.Get(context.Background(), ref)
	if !errors.Is(err, ErrIntegrity) {
		t.Fatalf("expected integrity error, got %v", err)
	}
}

func TestObjectPathIgnoresUnsafeKeyTraversal(t *testing.T) {
	store, err := Open(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}

	ref, err := store.PutImmutable(context.Background(), "runtime", "../turn-1/result.json", []byte(`{"ok":true}`), "application/json")
	if err != nil {
		t.Fatal(err)
	}
	data, err := store.Get(context.Background(), ref)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(data, []byte(`{"ok":true}`)) {
		t.Fatalf("unexpected content: %s", data)
	}
}
