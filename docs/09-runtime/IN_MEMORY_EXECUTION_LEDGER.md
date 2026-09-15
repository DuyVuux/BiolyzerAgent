# Stage 09 — In-Memory Execution Ledger

## Problem

A caller can repeat:

```text
Execute Turn T
```

because of:

```text
client retry
local transport retry
concurrent duplicate
```

Without a ledger, model generation can run twice.

## Stage-09 solution

Process-local map:

```text
turn_id
→ request digest
→ in-flight/completed result
```

Rules:

```text
new Turn
→ owner executes

same Turn + same digest while running
→ wait for owner

same Turn + same digest after completion
→ return same result

same Turn + different digest
→ conflict
```

## What it does not solve

```text
process restart
two processes
worker crash
distributed split brain
durable external effect
```

Those are intentionally left for Stages 10–12.

## Hash boundary

The request digest uses Go `encoding/json` over the typed Stage-09 request.

This is sufficient for process-local duplicate detection.

It is NOT the Stage-13 cross-language canonical serialization contract.
