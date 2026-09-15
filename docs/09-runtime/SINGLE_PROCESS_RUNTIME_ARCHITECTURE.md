# Stage 09 — Single-Process Runtime Architecture

> **Status:** IMPLEMENTED CANDIDATE v0.1  
> **Runtime:** Go + CloudWeGo Eino v0.9.19  
> **Topology:** one process, in-memory execution, no durable infrastructure

## 1. Purpose

Stage 09 is the first stage that turns BioMarker's contracts into production-shape Go code.

The goal is not production scale.

The goal is to prove:

```text
closed clinical/evidence input
→ structured candidate generation
→ deterministic safety
→ physician-reviewable output
```

inside one Go process with explicit framework boundaries.

## 2. Architecture

```text
apps/api
   ↓
local internal HTTP adapter
   ↓
analysis.Runtime port
   ↓
SingleProcess Runtime
   ├── in-memory Turn ledger
   └── Eino Workflow adapter
          ↓
     CandidateGenerator
          ↓
     SafetyEvaluator
          ↓
     typed ExecutionResult
```

## 3. Framework boundary

```text
BioMarker domain
        ↓
runtime port
        ↓
internal/platform/runtime/eino
```

Domain packages do not import Eino.

Eino graph/workflow types do not leak into:

```text
clinical domain
safety policy
evidence semantics
timeline semantics
```

## 4. Why structured composition, not ReAct

The clinical core is bounded:

```text
Generate structured candidate
→ deterministic safety gate
→ output
```

There is no requirement for open-ended autonomous tool selection in Stage 09.

Eino composition is used because it provides explicit execution sequencing while keeping the framework behind an adapter.

## 5. Process-local guarantees

Within one running process:

```text
same Turn + same semantic request
→ one workflow execution
→ duplicates wait/reuse canonical result

same Turn + different request
→ fail closed with idempotency conflict
```

These guarantees end when the process stops.

Stage 09 does not claim cross-restart durability.

## 6. State ownership

The in-memory ledger is:

```text
execution coordination state
```

not:

```text
canonical clinical state
clinical document repository
long-term conversation store
```

## 7. No side-effect tools

Current workflow contains no external tool effect.

This is intentional.

Stage 11/12 must characterize retry/recovery/durability before tool side effects are introduced into a durable topology.

## 8. Transport boundary

`/internal/runtime/execute` is a local development transport only.

It is NOT:

```text
public API contract
production authentication boundary
Stage-14 OpenAPI
```

The app binds to `127.0.0.1` by default.

## 9. Logging

Runtime code does not log:

```text
clinical values
evidence text
model candidate text
```

The composition root logs operational startup/shutdown only.

## 10. ai-studio survey adaptations

Stage 09 applies the read-only ai-studio runtime survey without importing durable infrastructure:

```text
Eino import boundary test
process-local context scope bridge
candidate output preflight before safety
explicit node-boundary cancellation checks
```

ReAct tool-loop controls, durable invokers, leases and fencing remain deferred because Stage 09 has no side-effect tools and only one process.

## 11. Deferred

```text
PostgreSQL
Redis
DBOS
worker
queue
checkpoint
durable retry
cross-process dedupe
cross-restart resume
production model provider
production authentication
public API
```
