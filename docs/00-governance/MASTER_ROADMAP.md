# 12 — Master Roadmap: 16 Stages

Roadmap này phục vụ **build + learning**, không thay thế product delivery roadmap.

---

# Chặng A — Problem & Domain Foundation

## Stage 0 — Architecture Discovery Foundation

**Question:** Chúng ta reasoning, dùng Sources và đối chiếu ai-studio như thế nào?

**Output:** package hiện tại.

**ai-studio exposure:** source discipline + high-level skeleton only.

---

## Stage 1 — Product & Clinical Domain Discovery

**Question:** BioMarker giải bài toán gì, cho ai, được phép làm gì?

**Key outputs:**

- product context;
- intended use;
- users/actors;
- use cases;
- non-goals;
- safety envelope;
- clinical/regulatory open questions.

**ai-studio exposure:** minimal. Không để generic platform định nghĩa clinical product.

---

## Stage 2 — Canonical Biomarker Domain Model

**Question:** Dữ liệu lõi là gì trước khi có LLM/runtime?

**Key outputs:**

- Diagnostic/Lab Report concepts;
- Observation/Biomarker;
- Reference Range;
- Dataset & provenance;
- Claim/Evidence/Report relationship.

**ai-studio exposure:** compare only generic artifact/state modeling after first-principles model.

---

# Chặng B — Domain Capability Characterization

## Stage 3 — Lab Ingestion Characterization

**Question:** Làm sao từ PDF/image/structured input ra observations đúng?

**Experiment:** extraction corpus + metrics.

**ai-studio exposure:** object store/artifact patterns only after ingestion needs appear.

---

## Stage 4 — Normalization & Clinical Terminology

**Question:** test name, unit, specimen, range được chuẩn hóa thế nào?

**Outputs:** mapping/validation policy and benchmark.

**ai-studio exposure:** schema/registry concepts only as reference.

---

## Stage 5 — Longitudinal Biomarker Model

**Question:** nhiều kết quả theo thời gian tạo dataset/timeline thế nào?

**Outputs:** dataset version, timeline, duplicate/change semantics.

**ai-studio exposure:** canonical state/version concepts.

---

## Stage 6 — Scientific Evidence Engine

**Question:** claim có evidence traceable thế nào?

**Outputs:** query/retrieval/ranking/evidence bundle/claim linkage.

**ai-studio exposure:** Knowledge/tool boundary only after domain pipeline derived.

---

## Stage 7 — Reasoning & Clinical Safety

**Question:** LLM được làm gì? deterministic gates ở đâu?

**Outputs:** bounded reasoning workflow, safety checks, unsupported claim policy.

**ai-studio exposure:** durable tool/model boundary, policies, structured pipeline concept.

---

## Stage 8 — Evaluation & Quality Architecture

**Question:** chứng minh đúng bằng metrics/golden cases nào?

**Outputs:** eval harness design, gold datasets, error taxonomy, safety/red-team cases.

**ai-studio exposure:** exit gates/golden eval principles.

---

# Chặng C — Runtime & Platform Discovery

## Stage 9 — Single-Process Runtime

**Question:** runtime đơn giản nhất chạy domain pipeline là gì?

**Rule:** chưa queue/distributed nếu không có evidence.

**ai-studio exposure:** Eino adapter + patterns after local candidate exists.

---

## Stage 10 — State & Persistence Architecture

**Question:** state gì cần persist, owner là ai, transaction boundary là gì?

**Outputs:** state inventory, ownership, storage criteria.

**ai-studio exposure:** PostgreSQL store/objectstore as alternatives/reference.

---

## Stage 11 — Failure, Retry & Recovery Characterization

**Question:** crash/timeout/retry/unknown outcome phá hệ thống thế nào?

**Experiments:** kill process, duplicate request, partial external call, lost response.

**ai-studio exposure:** durable invokers/tool effects/recovery tests after failures are observed.

---

## Stage 12 — Durable / Distributed Runtime Decision

**Question:** có cần worker/queue/lease/fencing không?

**Outputs:** measured decision matrix + ADR.

**ai-studio exposure:** deep dive DBOS, worker, Harness, lease, fencing.

---

## Stage 13 — Configuration, Versioning & Reproducibility

**Question:** exact behavior/config/evidence nào tạo report?

**Outputs:** config lifecycle, pinning, immutable artifact decision, attestation decision.

**ai-studio exposure:** compiler, canonical JSON, manifest, SHA-256, Ed25519, registry snapshots.

---

# Chặng D — Productization & Integration

## Stage 14 — Security, Privacy, API & Product Surfaces

**Question:** protected clinical product được expose thế nào?

**Outputs:**

- identity/authorization/tenant or patient-resource rules;
- privacy/retention handling;
- API;
- upload/report/chat UX;
- security negative tests.

**ai-studio exposure:** Gateway/Auth/RBAC/API/SSE/UI patterns.

---

## Stage 15 — ai-studio Integration & Production Architecture Closure

**Question:** final relationship giữa BioMarker và ai-studio là gì?

Evaluate:

- standalone;
- ai-studio capability;
- domain service + ai-studio orchestration;
- hybrid.

**Outputs:**

- final architecture;
- compatibility matrix;
- accepted/deferred ADRs;
- production gaps;
- NFR plan;
- integration sequence.

**ai-studio exposure:** full-system comparison.

---

# Dependency Graph

```text
0
↓
1
↓
2
↓
3 → 4 → 5
      ↓
      6
      ↓
      7
      ↓
      8
      ↓
      9
      ↓
     10
      ↓
     11
      ↓
     12
      ↓
     13
      ↓
     14
      ↓
     15
```

Một số research có thể overlap, nhưng **decision freeze phải tôn trọng dependency**.

---

# Complexity unlock principle

Feature chỉ được unlock khi Stage chứng minh pressure.

```text
queue
← Stage 11/12 evidence

fencing
← multi-worker reclaim/split-brain evidence

signed manifest
← Stage 13 integrity/approval requirement

Redis SSE
← Stage 14 realtime product requirement

generic registry
← actual multiplicity/governance requirement

multi-agent
← confirmed use case
```
