# Stage 05 Handoff — Longitudinal Biomarker Model

> **Status:** 
> - `STAGE_05_v0.1 = PASS WITH REFERENCE FOLLOW-UP`
> - `STAGE_05_v0.2 = CANDIDATE COMPLETE (SURGICAL UPDATE)`  
> **Next Stage:** 06 — Scientific Evidence Engine

---

## 1. Stage 05 established

```text
observation representation ≠ logical measurement
logical measurement ≠ timeline series
timeline series ≠ trend interpretation
```

---

## 2. Core policies & v0.2 Invariants

```text
same subject only
effective_at drives clinical chronology (out-of-order backfill handled at domain level)
issued_at drives revision chronology only
received_at is operational only
same value/time does not prove duplicate
candidate/unmapped observations do not join validated series
different canonical methods/codes remain separate
timeline snapshot is immutable derived projection
```

### v0.2 Surgical Invariant: LONG-016 — Identity Collision Fails Closed
```text
(source_system, external_observation_id) / source identity
must identify one semantic representation.

Same identity + same canonical payload
→ duplicate / idempotent replay (resolution: duplicate_collapsed)

Same identity + different canonical payload
+ no explicit revision lineage
→ ClinicalIdentityConflict (hard conflict / resolution: unresolved_conflict)

Unless:
explicit revision/correction lineage proves
that the new representation supersedes the old one.
```

### v0.2 State: Reconciliation Required
```text
incomplete/truncated LIS response OR
missing revision predecessor
→ resolution: reconciliation_required
→ excluded from active timeline series until reconciled
```

### v0.2 Canonicalization Profile Requirement
- Stage 05 uses `json.dumps(sort_keys=True, separators=(",",":")) -> SHA-256` as deterministic experimental identity.
- Production cross-language canonical identity REQUIRES a formal Canonical Clinical Payload Profile (RFC 8785 / JCS, duplicate key rejection, RFC 7493 I-JSON numeric bounds, ISO 8601 UTC).
- The profile implementation is formally frozen in Stage 13 before production persistence.

---

## 3. Trend boundaries

```text
quantity   → deterministic delta when eligible
ordinal    → direction only with validated rank
categorical→ changed/unchanged
interval   → history only
comparator → no naïve exact delta
```

---

## 4. Measured synthetic gates (v0.2 Benchmark: 15/15 PASS)

Stage 05 experiment covers:

- out-of-order arrival (chronology sorting by `effective_at`);
- exact duplicate import;
- corrected representation;
- distinct same-value/same-time events;
- convertible units;
- different-method series split;
- candidate terminology exclusion;
- cross-subject rejection;
- ordinal trend;
- categorical change;
- interval history;
- censored quantity;
- **[v0.2]** identity collision with same payload → idempotent duplicate (`duplicate_collapsed`);
- **[v0.2]** identity collision with different payload → hard conflict (`unresolved_conflict` / LONG-016);
- **[v0.2]** ambiguous representation → `reconciliation_required` exclusion;
- deterministic timeline snapshot.

Detailed benchmark results:
```text
experiments/stage-05/results/RUN_REPORT.md
experiments/stage-05/results/benchmark.json
```

---

## 5. ai-studio actual repository reconciliation

Rà soát mã nguồn thực tế của `ai-studio` đã xác nhận:
1. **Phân tách Logical Identity và Physical Attempt**: Đã áp dụng vào Stage 05 (Logical Measurement vs Observation representation) và chuyển giao cho Stage 06.
2. **Identity collision fail closed**: Đã chuẩn hóa thành Invariant LONG-016 trong Stage 05 v0.2.
3. **Reconciliation required**: Đã bổ sung trạng thái trong Stage 05 v0.2.
4. **PostgreSQL trigger & Immutable object store**: Không áp đặt vào Stage 05; bảo lưu tính bất biến ngữ nghĩa và hoãn cài đặt vật lý sang Stage 10.
5. **Lease/fencing/DBOS**: Bác bỏ khỏi domain Stage 05; thuần túy là hạ tầng runtime (Stage 11/12).

---

## 6. Stage 06 nhận bàn giao & Kế hoạch nâng cấp (Scientific Evidence Engine)

Mục tiêu cốt lõi của Stage 06 không đổi: **Scientific Evidence Engine**.
Tuy nhiên, nhờ bài học từ `ai-studio`, luồng nghiên cứu và kiến trúc Stage 06 được nâng cấp toàn diện:

```text
Clinical Question
      ↓
Evidence Query Intent
      ↓
Physical Retrieval Attempt(s)
      ↓
Retrieved Source Artifact(s)
      ↓
Source Identity + Version + Content Hash
      ↓
Evidence Claim Extraction
      ↓
Claim ↔ Source Entailment
      ↓
Canonical Evidence Selection
      ↓
Immutable Evidence Bundle Snapshot
      ↓
Future Clinical Synthesis (Stage 07)
```

### 5 nâng cấp bắt buộc cho Stage 06:
1. **Phân tách rõ ràng:** `RetrievalAttempt ≠ EvidenceSource ≠ EvidenceClaim ≠ EvidenceBundleSnapshot`.
2. **Evidence Source toàn diện:** `source_id`, `canonical_locator`, `title`, `publisher`, `publication_date`, `source_type`, `version`, `content_digest` (không dùng URL trần).
3. **Đóng băng EvidenceBundleSnapshot trước khi suy luận:** Không ambient-retrieve "latest" trong khi phân tích. Muốn chứng cứ mới phải tạo snapshot mới.
4. **Source Collision Fails Closed:** Cùng DOI/source_id nhưng nội dung khác nhau kích hoạt conflict/versioning.
5. **Evidence Claim Ledger:** Khóa quan hệ entailment có bằng chứng, bảo đảm không bị mất dấu provenance khi tổng hợp giải thích cho bác sĩ.

---

## 7. Production limitation

Current lineage/dedup experiment uses synthetic explicit source-event keys.
Actual hospital/LIS source identity semantics have not been inspected.

Therefore:

```text
SYNTHETIC_LONGITUDINAL_GATE = PASS (v0.2)
SOURCE_SYSTEM_LINEAGE_GATE  = NOT EXECUTED
PRODUCTION_DEDUP_GATE       = BLOCKED BY NO ACTUAL SOURCE IDENTITY CONTRACT
```

This does not block Stage 06.
