# BioMarker Agent — State & Persistence Architecture

> **Status:** CANDIDATE v0.2  
> **Stage:** 10 — State & Persistence Architecture  
> **Topology:** Single application process / single writer  
> **Goal:** Make logical Turn identity and canonical outcome survive process restart without prematurely introducing distributed runtime infrastructure.

---

## 1. The failure exposed by Stage 09

Stage 09 proved:

```text
same process
+ same Turn
→ one semantic execution
```

but its ledger lived in RAM.

Therefore:

```text
process restart
→ ledger disappears
→ same Turn can look new
```

That is a correctness problem, not merely an optimization problem.

---

## 2. State taxonomy

### Canonical durable state

Must survive restart:

```text
Turn identity
idempotency key
semantic request digest
closed-input provenance
canonical Turn status
canonical terminal result
revision
recovery-required classification
needs-reconciliation classification
artifact references for externalized payloads/results
```

### Durable immutable upstream references

Referenced, not re-owned here:

```text
Clinical Dataset Snapshot ID
Longitudinal Timeline Snapshot ID
Evidence Bundle ID
reasoning policy digest
safety policy digest
```

### Ephemeral runtime state

Must NOT become canonical:

```text
context.Context
deadline timer
goroutine
Eino node state
model token buffer
temporary candidate buffer
current-process waiter/channel
HTTP connection
physical provider socket/request handle
```

### Derived/cache state

May be rebuilt:

```text
compiled Eino graph
parsed schema
provider client
read cache
```

---

## 3. Canonical owner

Stage 10 introduces:

```text
turnstore.Store
artifactstore.Store
```

as the logical ownership boundaries.

The current file adapters are implementations.

Therefore:

```text
canonical state owner
≠
file format
≠
database vendor
```

Future SQLite/PostgreSQL adapters must preserve the same semantics.

Stage 10 v0.2 keeps this additional split:

```text
canonical Turn state
immutable payload bytes
physical execution evidence
canonical selected transcript/result
```

This preserves the useful ai-studio invariant without importing PostgreSQL,
DBOS, leases, queues or worker topology.

---

## 4. Durable Turn lifecycle

Current Stage-10 states:

```text
ACCEPTED
COMPLETED
FAILED
CANCELLED
RECOVERY_REQUIRED
NEEDS_RECONCILIATION
```

The state describes one logical Turn.

It does NOT describe physical attempts.

```text
Turn
≠
Attempt
```

Stage 11 may add attempt/recovery evidence without changing logical identity.

`NEEDS_RECONCILIATION` is stronger than `RECOVERY_REQUIRED`.

```text
RECOVERY_REQUIRED
→ ownership/retry policy is unresolved

NEEDS_RECONCILIATION
→ an external effect may have happened
→ no automated retry
→ operator or explicit recovery policy required
```

---

## 5. Reservation semantics

First valid request:

```text
TurnID + idempotency key + semantic digest
→ ACCEPTED
```

Retry with same logical semantics:

```text
same identity + same digest
→ existing record
```

Same Turn reused for different semantics:

```text
→ IDEMPOTENCY_CONFLICT
→ zero second execution
```

---

## 6. Semantic request digest

Stage 09 hashed the whole transport request.

Stage 10 refines this:

Included:

```text
schema version
Turn ID
idempotency key
closed ReasoningInput
```

Excluded:

```text
correlation ID
remaining deadline
```

Why?

A retry of the same logical Turn may legitimately arrive with a new trace/correlation ID or a different remaining transport deadline.

Transport noise must not redefine clinical intent.

---

## 7. Restart replay

If a terminal canonical result exists:

```text
restart
→ same Turn arrives
→ return stored canonical result
→ workflow calls = 0
```

This is the Stage-10 durable-idempotency guarantee.

---

## 8. Incomplete record after restart

If durable state is:

```text
ACCEPTED
```

but the current process has no live ownership record:

```text
DO NOT BLINDLY RE-EXECUTE
```

Stage 10 marks:

```text
RECOVERY_REQUIRED
```

and returns a safe recovery-required outcome.

Stage 11 decides which crash windows may safely retry, reconcile, fail or resume.

If Stage 11 observes an ambiguous mutating side effect, the safe classification is:

```text
NEEDS_RECONCILIATION
```

not `RECOVERY_REQUIRED`.

---

## 9. Canonical result commit

The file adapter writes terminal state via:

```text
temp file
→ fsync(temp)
→ same-directory atomic rename
→ fsync(parent directory)
```

Initial reservation uses:

```text
temp file
→ fsync
→ atomic hard-link to final name
→ fsync(parent)
```

This gives a useful single-host/single-writer durability baseline.

It is not claimed to be equivalent to a mature transactional database under every OS/filesystem/power-loss failure.

---

## 10. Integrity digest

Each record envelope contains:

```text
record_digest = SHA-256(serialized record)
```

This detects:

```text
accidental corruption
unexpected modification
```

It does NOT provide authenticity against an attacker who can rewrite both payload and digest.

Cryptographic attestation/key management remains a later security decision.

---

## 11. Data minimization

The canonical Turn record stores:

```text
semantic digest
provenance IDs/digests
canonical result
canonical result_ref when payload is externalized
```

It intentionally does not persist raw `user_question` simply for duplicate detection.

Large or sensitive payloads should be written to immutable artifact storage:

```text
same bucket/key + same bytes
→ idempotent success

same bucket/key + different bytes
→ immutable conflict

artifact read
→ SHA-256 verification
```

Production encryption, retention, storage location and access policy remain Stage 14 / applicable-governance concerns.

---

## 12. Guarantees

Stage 10 now guarantees, within its topology:

```text
completed Turn survives application restart
terminal result replay does not re-execute workflow
same identity + different semantics fails closed
concurrent duplicate in one process executes once
incomplete restarted Turn does not blindly execute again
record corruption is detected
transport-only retry changes do not cause semantic conflict
terminal state cannot be overwritten by a different result
ambiguous external outcomes can be frozen as needs_reconciliation
immutable artifact bytes are checksum-verified
```

---

## 13. Non-guarantees

Still NOT guaranteed:

```text
multi-process concurrent writers
distributed ownership
lease/fencing
exactly-once external side effects
resume from a workflow checkpoint
power-loss correctness across every filesystem/device
cross-host replication
automatic recovery of unknown execution
complete physical Attempt model
automatic operator reconciliation
```

Those belong to Stage 11/12 or later.
