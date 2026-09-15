# Stage 10 Handoff — State & Persistence Architecture

> **Status:** CANDIDATE COMPLETE v0.2 — SINGLE-WRITER DURABILITY BASELINE  
> **Next Stage:** 11 — Failure, Retry & Recovery Characterization

## Stage 10 closes

```text
canonical-vs-ephemeral state
durable Turn identity
restart replay
persisted terminal outcome
semantic idempotency conflict
incomplete-turn recovery boundary
storage adapter boundary
immutable artifact boundary
logical-vs-physical execution evidence boundary
needs-reconciliation freeze state
```

## Canonical rule

```text
TurnStore = logical durable authority

process memory = coordination only
checkpoint/cache/queue = never canonical by implication
ArtifactStore = immutable payload authority
PhysicalCall = execution evidence, not canonical transcript by itself
```

## Implementation baseline

```text
fileturn.Store
+
fileartifact.Store
+
persistentlocal.Runtime
```

This is a minimum-sufficient single-process durability adapter, not a final production database choice.

Stage 10 now preserves ai-studio's useful invariant without copying its infrastructure:

```text
canonical Turn state
+
immutable payload refs
+
physical execution evidence model
```

The file adapter still does not implement distributed leases, DBOS checkpoints, or PostgreSQL transactions.

## Stage 11 receives explicit crash windows

```text
W0 before ACCEPTED
W1 after ACCEPTED before workflow completion
W2 result computed before terminal commit
W3 terminal commit before response
```

Stage 11 must inject failure into these windows rather than infer behavior.

## Stage 11 key questions

```text
Which window is safe to retry?
Which window requires reconciliation?
Should safe/read-only work re-execute?
What is UNKNOWN?
Do we need physical Attempt records?
Which external effects become needs_reconciliation?
Do checkpoints improve recovery without becoming authority?
Does file persistence survive the required crash model?
Does evidence force SQLite/PostgreSQL/durable runtime?
```

## Gate

```text
STAGE_11_ENTRY_GATE = PASS
```

Production persistence technology remains deliberately unfrozen.
