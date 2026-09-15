# Stage 09 — ai-studio Runtime Survey Application

> **Status:** APPLIED TO STAGE-09 ROOT INTEGRATION

This note records how the read-only ai-studio runtime survey was applied to BioMarker Stage 09.

## Source Findings

The ai-studio survey found:

- Eino is an in-memory graph adapter, not the platform/domain boundary.
- Production graph lifecycle compiles once and reuses the runnable.
- Context cancellation is checked at node boundaries.
- Mock and real model paths must satisfy the same invocation contract.
- Model output passes through validation before exposure.
- DBOS, leases, fencing, durable invokers, PostgreSQL, Redis and worker topology solve later durable/distributed failure modes.

## Applied In Stage 09

KEEP:

- Eino remains isolated in `internal/platform/runtime/eino`.
- The Stage-09 workflow is compiled once in `NewWorkflow`.
- The deterministic generator remains the no-network model substitute.
- Static architecture tests guard Eino and deferred-infra boundaries.

ADAPT:

- ai-studio's DBOS context bridge becomes a process-local runtime scope on `context.Context`.
- ai-studio's output validation funnel becomes `ValidateReasoningCandidate` before deterministic safety evaluation.
- Node-boundary cancellation is explicit before candidate generation and before safety gating.

REJECT for Stage 09:

- DBOS as a required runtime dependency.
- Eino types in domain or safety packages.
- Direct production provider calls from domain packages.

DEFER:

- Durable model/tool invokers.
- Lease/fencing.
- PostgreSQL authoritative run state.
- Redis live events.
- Worker process.
- ReAct tool loop, tool-call ID tracking and max-turn enforcement.

## Implementation Hooks

- Candidate output preflight: `internal/analysis/ValidateReasoningCandidate`.
- Context scope bridge: `internal/platform/runtime/local/ContextWithScope`.
- Eino adapter guard: `internal/platform/runtime/eino.NewWorkflow`.
- Architecture boundary tests: `tests/architecture`.

## Stage Boundary

The survey does not change Stage 09's topology:

```text
single process
in-memory Turn ledger
no durable side effects
no distributed workers
```

Tool support and ReAct loop controls become concrete only when a later stage authorizes side-effect tools or autonomous tool selection.
