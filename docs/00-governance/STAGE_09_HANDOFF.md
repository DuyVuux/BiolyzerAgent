# Stage 09 Handoff — Single-Process Runtime

> **Status:** CANDIDATE IMPLEMENTED AND LOCALLY VERIFIED  
> **Next Stage:** 10 — State & Persistence Architecture

## Delivered

```text
root Go module
thin apps/api composition root
domain/runtime ports
deterministic local model
Go safety evaluator
Eino structured workflow adapter
in-memory duplicate-safe Turn ledger
local internal HTTP adapter
runtime JSON Schemas
Go unit/integration tests
runtime smoke characterization
```

## Key guarantee

Within one process:

```text
same Turn + same request
→ exactly one semantic generation

same Turn + changed request
→ fail closed
```

## Important non-guarantee

After process restart:

```text
ledger is gone
```

Therefore:

```text
CROSS_RESTART_DEDUPE = NOT PROVIDED
DURABLE_RECOVERY = NOT PROVIDED
```

This is the problem Stage 10/11 must address.

## ai-studio survey applied

The root integration incorporates the ai-studio runtime survey as Stage-09-safe adaptations:

```text
static Eino/import boundary tests
process-local context scope bridge
candidate output preflight before safety gate
node-boundary cancellation guard
```

Durable invokers, DBOS, lease/fencing, Redis, worker topology and ReAct tool-loop controls remain deferred.

## Framework decision

```text
Go + Eino v0.9.19
structured composition
Eino isolated behind adapter
```

## Stage 10 entry

Stage 10 should answer:

```text
what state must survive restart?
which state is canonical?
what is derived/cache?
what persistence model is minimum sufficient?
how is lineage/version preserved?
```

It must not introduce distributed workers merely because persistence exists.
