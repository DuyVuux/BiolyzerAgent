# Stage 10 Persistence Verification Results

> **Status:** MEASURED v0.2

## Targeted Go verification

```text
go test ./internal/platform/persistence/fileturn              PASS
go test ./internal/platform/persistence/fileartifact          PASS
go test ./internal/platform/runtime/persistentlocal           PASS
go test ./tests/integration/stage10                           PASS
go test ./tests/architecture/stage10                          PASS

go test -race ./internal/platform/persistence/fileturn        PASS
go test -race ./internal/platform/persistence/fileartifact    PASS
go test -race ./internal/platform/runtime/persistentlocal     PASS
go test -race ./tests/integration/stage10                     PASS

pnpm lint                                                     PASS
pnpm typecheck                                                PASS
pnpm test                                                     PASS
pnpm check                                                    PASS
```

## Smoke experiment

```json
{
  "completed_survives_restart": true,
  "restart_replay_workflow_calls": 0,
  "incomplete_requires_recovery": true,
  "incomplete_reexecution_calls": 0,
  "semantic_digest_ignores_transport_noise": true,
  "canonical_record_file_count": 2,
  "elapsed_ms": 0
}
```

## Interpretation

The measured run proves under the current single-process/single-writer topology:

```text
completed Turn survives reopen/restart simulation
restart replay performs zero semantic workflow calls
stranded accepted Turn is classified recovery_required
stranded Turn performs zero blind re-execution calls
transport-only correlation/deadline changes preserve semantic identity
terminal result overwrite is rejected
needs_reconciliation performs zero blind re-execution calls
immutable artifact corruption is detected by checksum verification
```

This does not prove all power-loss/crash windows. Stage 11 owns those failure-injection claims.
