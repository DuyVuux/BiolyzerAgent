package local

import (
	"context"
	"errors"
	"sync"

	"biomarker/internal/analysis"
)

var ErrIdempotencyConflict = errors.New("turn identity reused with different semantic request")

type entry struct {
	digest string
	done   chan struct{}
	result analysis.ExecutionResult
	err    error
	once   sync.Once
}

// Ticket represents ownership or observation of one logical Turn execution.
type Ticket struct {
	entry *entry
	owner bool
}

// Ledger deduplicates logical Turn execution for the lifetime of one process.
type Ledger struct {
	mu      sync.Mutex
	entries map[string]*entry
}

// NewLedger creates an empty in-memory ledger.
func NewLedger() *Ledger {
	return &Ledger{entries: make(map[string]*entry)}
}

// Start claims a Turn or joins an existing same-payload execution.
func (l *Ledger) Start(turnID, digest string) (*Ticket, error) {
	l.mu.Lock()
	defer l.mu.Unlock()

	if existing, ok := l.entries[turnID]; ok {
		if existing.digest != digest {
			return nil, ErrIdempotencyConflict
		}
		return &Ticket{entry: existing, owner: false}, nil
	}

	e := &entry{digest: digest, done: make(chan struct{})}
	l.entries[turnID] = e
	return &Ticket{entry: e, owner: true}, nil
}

// Owner reports whether the caller owns execution.
func (t *Ticket) Owner() bool { return t.owner }

// Complete publishes the owner result exactly once.
func (t *Ticket) Complete(result analysis.ExecutionResult, err error) {
	if !t.owner {
		return
	}
	t.entry.once.Do(func() {
		t.entry.result = result
		t.entry.err = err
		close(t.entry.done)
	})
}

// Wait waits for the canonical in-process execution result.
func (t *Ticket) Wait(ctx context.Context) (analysis.ExecutionResult, error) {
	select {
	case <-ctx.Done():
		return analysis.ExecutionResult{}, ctx.Err()
	case <-t.entry.done:
		return t.entry.result, t.entry.err
	}
}
