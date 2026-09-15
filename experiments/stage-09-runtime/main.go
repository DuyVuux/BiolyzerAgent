package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"sync"
	"sync/atomic"
	"time"

	"biomarker/internal/analysis"
	"biomarker/internal/platform/runtime/local"
)

type fixtureEnvelope struct {
	Request analysis.ExecutionRequest `json:"request"`
}

type semanticWorkflow struct {
	calls atomic.Int64
}

func (w *semanticWorkflow) Invoke(ctx context.Context, req analysis.ExecutionRequest) (analysis.ExecutionResult, error) {
	w.calls.Add(1)
	select {
	case <-ctx.Done():
		return analysis.ExecutionResult{}, ctx.Err()
	case <-time.After(2 * time.Millisecond):
		return analysis.ExecutionResult{
			SchemaVersion: "1.0",
			TurnID:        req.TurnID,
			Status:        analysis.StatusCompleted,
		}, nil
	}
}

func main() {
	b, err := os.ReadFile("testdata/synthetic/stage-09/runtime_request.json")
	if err != nil {
		panic(err)
	}
	var fixture fixtureEnvelope
	if err := json.Unmarshal(b, &fixture); err != nil {
		panic(err)
	}

	w := &semanticWorkflow{}
	rt := local.NewRuntime(w, local.NewLedger())

	start := time.Now()
	const duplicates = 64
	var wg sync.WaitGroup
	errCh := make(chan error, duplicates)
	for i := 0; i < duplicates; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			got, err := rt.Execute(context.Background(), fixture.Request)
			if err != nil {
				errCh <- err
				return
			}
			if got.Status != analysis.StatusCompleted {
				errCh <- fmt.Errorf("status=%s", got.Status)
			}
		}()
	}
	wg.Wait()
	close(errCh)
	for err := range errCh {
		panic(err)
	}

	report := map[string]any{
		"concurrent_duplicate_requests": duplicates,
		"semantic_workflow_calls":       w.calls.Load(),
		"exactly_once_in_process":       w.calls.Load() == 1,
		"elapsed_ms":                    time.Since(start).Milliseconds(),
	}
	out, _ := json.MarshalIndent(report, "", "  ")
	fmt.Println(string(out))
	if w.calls.Load() != 1 {
		os.Exit(1)
	}
}
