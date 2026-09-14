# 11 — Architecture Hypothesis Register

## Cách dùng

Một hypothesis tốt phải có thể bị bác bỏ.

Format:

```text
ID
Statement
Why we believe it
Evidence for
Evidence against
Falsification condition
If false
Target Stage
Status
```

Status:

```text
OPEN
SUPPORTED
WEAKENED
FALSIFIED
SUPERSEDED
```

Không dùng `PROVEN FOREVER`.

---

## H-0001 — Không cần distributed/durable runtime ở early MVP

**Statement**

Một BioMarker prototype đầu có thể chạy single-process trước khi requirement/failure evidence chứng minh cần background durable execution.

**Why**

Giảm platform complexity để tập trung domain pipeline.

**Evidence for**

- chưa có confirmed workload/uptime/recovery requirement trong Stage 0;
- historical Mia cũng từng defer generic async/distributed runtime khi chưa có use case.

**Evidence against**

- BioMarker analysis có thể chứa nhiều external calls và kéo dài;
- raw file + evidence pipeline có thể vượt request lifetime.

**Falsification**

Bất kỳ điều nào:

- confirmed requirement execution phải survive request/process;
- measured p95 không phù hợp synchronous UX;
- fault-injection gây unacceptable work loss;
- retry không thể safe nếu execution restart.

**If false**

Stage 12 evaluate queue/durable workflow candidates, including Mia DBOS design.

**Target Stage:** 11–12  
**Status:** OPEN

---

## H-0002 — Structured pipeline phù hợp hơn autonomous ReAct cho core clinical analysis

**Statement**

Core analysis có thể biểu diễn bằng typed/bounded stages; unconstrained action loop không cần thiết cho MVP.

**Why**

Dữ liệu clinical cần provenance và deterministic safety checkpoints.

**Falsification**

Một confirmed use case đòi dynamic planning/tool selection mà fixed/conditional graph tạo complexity lớn hơn và vẫn có safe control.

**If false**

Evaluate bounded ReAct / planner-worker pattern with explicit safety/tool policy.

**Target Stage:** 7–9  
**Status:** OPEN

---

## H-0003 — Canonical clinical domain model phải tồn tại độc lập LLM

**Statement**

Extraction output, observations, units, ranges, dates và provenance phải có typed domain representation trước reasoning.

**Falsification**

Không kỳ vọng bị falsify ở principle level; exact model shape có thể thay đổi.

**If challenged**

Require explicit design review because this impacts auditability and evaluation.

**Target:** 2–4  
**Status:** OPEN / STRONG

---

## H-0004 — Không dùng FHIR resource model trực tiếp làm internal persistence schema mặc định

**Statement**

FHIR nên là interoperability reference/boundary; internal canonical model được derive theo BioMarker needs trước.

**Why**

Interoperability representation và internal domain/persistence concern không đồng nhất.

**Falsification**

Confirmed environment requires native FHIR repository semantics end-to-end and internal model adds no value.

**Target:** 2  
**Status:** OPEN

---

## H-0005 — Human verification gate cần cho low-confidence extraction

**Statement**

Các observation extraction không chắc chắn cần user/clinician confirmation hoặc explicit unresolved state thay vì silent inference.

**Falsification**

Extraction benchmark + source format guarantees đạt threshold đủ cao và product/safety authority chấp nhận fully automated processing.

**Target:** 3 / 7  
**Status:** OPEN

---

## H-0006 — Evidence subsystem tách khỏi reasoning

**Statement**

Retrieval/ranking/provenance là subsystem/contract riêng, không để LLM tự do web-search rồi synthesize không trace.

**Falsification**

Một alternative architecture chứng minh cùng traceability/evaluation/safety mà không cần boundary logical riêng.

**Target:** 6  
**Status:** OPEN

---

## H-0007 — Exact dataset/config/evidence provenance cần cho report reproducibility

**Statement**

Report phải trace được về dataset version + relevant analysis/config/evidence identity.

**Falsification**

Product use case không cần persistence/review/reproduction và safety authority chấp nhận ephemeral explanation-only use.

**Target:** 5 / 6 / 13  
**Status:** OPEN

---

## H-0008 — PostgreSQL chưa được justify ở Stage 0

**Statement**

Chưa đủ evidence để chọn PostgreSQL cho BioMarker chỉ vì Mia dùng nó.

**Falsification**

Một authoritative platform constraint yêu cầu shared PostgreSQL model hoặc Stage 10 persistence analysis lựa chọn PostgreSQL theo criteria.

**Target:** 10  
**Status:** OPEN

---

## H-0009 — Signed Ed25519 manifest chưa được justify ở Stage 0

**Statement**

Versioned immutable config/artifact có thể đủ trước khi attestation requirement xuất hiện.

**Falsification**

Security/approval/supply-chain/offline worker requirements đòi cryptographic attestation.

**Target:** 13  
**Status:** OPEN

---

## H-0010 — BioMarker không nên rebuild generic Mia Studio ở MVP

**Statement**

MVP cần domain workflow/product surface; generic visual agent authoring Studio chưa phải validated need.

**Falsification**

Product requirement xác nhận non-engineer admins phải author configurable BioMarker workflows independent of deploy cycle.

**Target:** 14–15  
**Status:** OPEN

---

# Register rule

Mỗi Stage:

1. review hypotheses target Stage;
2. add evidence;
3. update status;
4. không xóa hypothesis bị falsified — giữ lịch sử;
5. decision material phải chuyển thành ADR.
