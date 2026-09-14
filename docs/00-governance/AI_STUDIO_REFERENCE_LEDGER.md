# 10 — ai-studio Reference Ledger

## Purpose

Ledger này không phải backlog để copy ai-studio.

Mỗi entry ghi:

```text
ai-studio mechanism
→ problem it appears to solve
→ assumptions
→ BioMarker evidence needed
→ disposition
```

Disposition:

- `KEEP` — same problem/constraints; retain concept/mechanism after review.
- `ADAPT` — same core problem but different domain/constraints.
- `REJECT` — not appropriate under confirmed BioMarker requirements.
- `DEFER` — cannot justify yet.

---

## AS-001 — PostgreSQL authoritative source of truth

### ai-studio

Skeleton mô tả PostgreSQL quản lý:

- Run FSM;
- leases/fencing;
- budgets;
- tool effects;
- manifest pins;
- artifacts metadata.

### Problem solved

Durable canonical state + transactional coordination.

### Assumptions

- state phải survive process;
- multiple workers;
- atomic transitions matter;
- relational transactions valuable.

### BioMarker evidence needed

Stage 10:

- state inventory;
- consistency requirements;
- transaction boundaries;
- workload;
- clinical retention requirements.

### Current disposition

**DEFER**

Không chọn DB ở Stage 0.

---

## AS-002 — DBOS queue / execution journal

### ai-studio mechanism

Atomic acceptance + queue/journal + replay/recovery.

### Problem solved

Execution lifetime tách khỏi request/process lifetime; crash recovery.

### BioMarker evidence needed

Stage 11 fault injection:

- long-running analysis;
- crash loss;
- retry semantics;
- user expectation;
- side effects.

### Current disposition

**DEFER**

---

## AS-003 — Lease + fencing token

### ai-studio mechanism

Worker acquires lease; fencing prevents stale worker commits.

### Problem solved

Split brain khi ownership chuyển worker.

### Required condition

Multiple execution owners + reclaim + stale process risk.

### BioMarker disposition

**DEFER**

Stage 12 only if distributed worker model emerges.

---

## AS-004 — Immutable signed manifest

### ai-studio mechanism

```text
ExecutionDefinition
→ canonical JSON
→ SHA-256
→ Ed25519 attestation
→ immutable manifest
→ runtime pin
```

### Problem solved

Reproducibility, integrity, approved artifact identity, runtime drift prevention.

### BioMarker evidence needed

Stage 13:

- exact reproducibility requirement;
- authoring/publish trust model;
- config mutation risk;
- audit/approval requirements.

### Current disposition

**DEFER**

---

## AS-005 — Eino as adapter, not authority

### ai-studio mechanism

Platform Harness controls lifecycle; Eino runs in-memory graph.

### Problem solved

Avoid coupling platform durability/security semantics to graph framework.

### BioMarker relevance

High potential because BioMarker may use a structured pipeline.

### Current disposition

**REFERENCE / DEFER DECISION**

Stage 9 evaluates simplest runtime first.

---

## AS-006 — DurableModelInvoker / DurableToolInvoker

### Problem solved

Centralized accounting, timeout, replay/side-effect tracking, policy.

### BioMarker nuance

Evidence search may be read-only; future clinical/external tools may differ in side-effect profile.

### Current disposition

**ADAPT CANDIDATE, NOT YET ADOPTED**

Evaluate Stage 7/11.

---

## AS-007 — Scoped Ports

### Problem solved

Execution/tenant capability isolation.

### BioMarker relevance

Potentially important for patient/tenant clinical data.

### Current disposition

**KEEP CONCEPT AS REFERENCE; IMPLEMENTATION DEFERRED**

Security design Stage 14.

---

## AS-008 — Redis Streams for realtime SSE only

### Problem solved

Live progress distribution without making Redis authoritative.

### BioMarker evidence needed

Product UX:

- need live progress?
- reconnect?
- durable event history?
- expected concurrency?

### Current disposition

**DEFER**

---

## AS-009 — React pattern

### ai-studio

`react@1` bounded reasoning/action loop.

### BioMarker concern

Clinical pipeline may be safer as explicit structured pipeline rather than unconstrained ReAct loop.

### Current disposition

**REJECT AS DEFAULT / RESEARCH IF A CONCRETE USE CASE REQUIRES**

Not a permanent rejection.

---

## AS-010 — Structured Pipeline pattern

### Problem solved

Typed sequential stages.

### BioMarker fit

Potentially strong fit for:

```text
ingest
→ extract
→ validate
→ normalize
→ retrieve
→ reason
→ safety
→ report
```

### Current disposition

**ADAPT CANDIDATE**

Must derive workflow independently in Stages 3–9 before comparing implementation.

---

## AS-011 — Object Store abstraction

### ai-studio

LocalFS + S3/MinIO adapters.

### BioMarker problem

Raw lab files and derived artifacts may require blob/object storage.

### Evidence needed

Stage 10:

- retention;
- access;
- size;
- deletion;
- audit;
- encryption;
- locality.

### Current disposition

**LIKELY DOMAIN NEED, TECHNOLOGY DEFERRED**

---

## AS-012 — Registry (models/tools/schemas/skills/policies/MCP)

### Problem solved

Controlled catalog and immutable resolution.

### BioMarker MVP

May not need a generic registry initially.

### Current disposition

**DEFER**

Avoid platform-building before actual multiplicity requires it.

---

## AS-013 — Compiler

### Problem solved

Translate authoring representation to runtime artifact and validate boundaries.

### BioMarker disposition

**DEFER TO STAGE 13**

First establish whether authoring/runtime representations differ.

---

## AS-014 — 15 exit gates / hardening tests

### Problem solved

Architecture invariants become executable acceptance.

### BioMarker fit

Very high conceptually.

### Current disposition

**KEEP PRINCIPLE**

BioMarker should develop gates gradually, domain-specific:

- extraction;
- normalization;
- evidence;
- safety;
- recovery;
- security.

---

## AS-015 — Frontend Visual Canvas / YAML Studio

### Problem solved

General Agent authoring.

### BioMarker MVP

Likely not a first-order domain problem.

### Current disposition

**REJECT FOR EARLY STAGES / DEFER PRODUCT NEED**

If BioMarker later becomes configurable product inside ai-studio, reuse ai-studio Studio is more likely than rebuilding Studio.

---

# Review rule

Không đổi `DEFER` thành `KEEP` chỉ vì implementation trông mạnh.

Mỗi Stage phải update ledger bằng evidence.
