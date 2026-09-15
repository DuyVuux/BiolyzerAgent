# Persistence Technology Decision

> **Status:** STAGE-10 DECISION — SEMANTIC PORT FROZEN, PRODUCTION DATABASE NOT FROZEN

---

## 1. Options considered

### A — Hand-built durable file record

Strengths:

```text
zero new dependency
works inside single-process topology
transparent failure surface
good for proving exact semantics
```

Weaknesses:

```text
no multi-record transaction
no rich query/index
single-writer assumption
hand-built crash semantics
no migration engine
not suitable as a final production database claim
```

Stage-10 use:

```text
IMPLEMENTED AS REFERENCE / EXPERIMENTAL ADAPTER
```

---

### B — SQLite

Official SQLite documentation states that transactions are ACID and are designed to remain atomic across program/OS crash and power failure, subject to documented filesystem/hardware assumptions.

Useful properties for this project:

```text
embedded
no database service
transactional uniqueness
single-host friendly
mature crash testing
```

WAL trade-off:

```text
all processes must be on the same host
WAL is not a network-filesystem distributed solution
```

Sources:

```text
https://www.sqlite.org/transactional.html
https://www.sqlite.org/atomiccommit.html
https://www.sqlite.org/wal.html
```

Assessment:

```text
STRONG NEXT LOCAL-DURABILITY CANDIDATE
NOT FROZEN IN STAGE 10
```

Reason not frozen yet:

Stage 11 still has to characterize actual crash windows and recovery requirements.

---

### C — PostgreSQL

Strengths:

```text
strong transactional constraints
multi-process/server topology
mature concurrency
future distributed workers fit naturally
```

Weakness:

```text
external service and operational complexity
not required merely to make one local process restart-durable
```

Assessment:

```text
DEFER
```

until topology/workload/recovery experiments justify it.

---

## 2. Decision

Freeze:

```text
TurnStore semantic port
canonical Turn state model
restart replay behavior
conflict behavior
recovery-required behavior
```

Do NOT freeze:

```text
production database vendor
SQL schema
connection pool
replication
HA
```

This keeps Stage 11 experiments capable of changing the storage adapter without rewriting domain/runtime semantics.
