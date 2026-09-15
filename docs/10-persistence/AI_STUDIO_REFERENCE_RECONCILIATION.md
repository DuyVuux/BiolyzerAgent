# Stage 10 — ai-studio Reference Reconciliation

> **Method:** derive BioMarker state model first → reference-second.

## Useful reference patterns

Available `ai-studio` architecture/spec evidence consistently separates:

```text
logical Turn / canonical state
from
runtime worker/process state
```

It also treats duplicate-safe start and unknown-outcome recovery as explicit integration concerns, and treats caches as projections rather than canonical owners.

## KEEP

```text
stable logical Turn identity
canonical owner separated from runtime worker
duplicate-safe start
persisted outcome replay
cache/checkpoint not authority
immutable artifact refs for payload bytes
physical execution evidence separate from canonical transcript
needs_reconciliation for ambiguous mutating effects
terminal status immutability
```

## ADAPT

`ai-studio` uses a mature database-backed authoritative model.

BioMarker Stage 10 adapts only the semantic boundary:

```text
TurnStore
ArtifactStore
PhysicalCall evidence model
```

while using a smaller local adapter to expose the actual persistence problem.

## REJECT for Stage 10

```text
queue as source of truth
checkpoint as exactly-once proof
runtime process as canonical owner
```

## DEFER

```text
PostgreSQL server
DBOS
durable queue
lease/fencing
worker topology
distributed artifact store
```

These may become justified by Stage 11/12 evidence.

## Stage 10 v0.2 changes from actual ai-studio inspection

The actual repository inspection added evidence for a tripartite split:

```text
canonical logical state
durable execution/checkpoint journal
immutable payload/object store
```

BioMarker keeps the first and third immediately, and documents physical
execution evidence without adopting DBOS. Stage 11 must prove whether physical
Attempt rows, checkpoint replay, leases, or a database substrate are necessary.

## Why not copy the mature store now?

Because the current question is:

```text
what state must survive restart?
```

not:

```text
how do we operate a distributed durable platform?
```

The latter requires evidence not yet produced by BioMarker.
