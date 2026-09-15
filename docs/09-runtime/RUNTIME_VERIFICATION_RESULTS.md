# Stage 09 — Verification Results

> **Status:** PASS AFTER ROOT INTEGRATION
> **Verified on:** 2026-09-15

## 1. Environment

```text
go version go1.27.1 linux/amd64
github.com/cloudwego/eino v0.9.19
```

`go mod tidy` completed and generated `go.sum` in the root repository.

## 2. Executed Checks

```text
go vet ./...        PASS
go test ./...       PASS
go test -race ./... PASS
pnpm check          PASS
```

`pnpm check` now runs the root Go checks without swallowing failures. The `@biomarker/api` workspace task also executes `go test ./...`.

## 3. Runtime Smoke

```json
{
  "concurrent_duplicate_requests": 64,
  "elapsed_ms": 2,
  "exactly_once_in_process": true,
  "semantic_workflow_calls": 1
}
```

## 4. ai-studio Survey Adaptation Tests

Additional root integration checks cover:

```text
Eino import boundary
no deferred distributed infrastructure imports
candidate output-shape preflight
node-boundary cancellation before generation
process-local runtime scope propagation through context.Context
```

## 5. Remaining Non-Guarantees

Stage 09 still intentionally does not provide:

```text
cross-restart dedupe
durable recovery
lease/fencing
DBOS
Redis
worker topology
side-effect tool replay
production model provider
public API/authentication
```

These remain Stage 10+ / Stage 11+ / Stage 12+ / Stage 14 concerns according to the roadmap.
