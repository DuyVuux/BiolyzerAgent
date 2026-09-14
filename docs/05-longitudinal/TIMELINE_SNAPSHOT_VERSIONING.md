# Timeline Snapshot & Versioning Model

> **Status:** PROPOSED v0.2  
> **Stage:** 05 — Longitudinal Biomarker Model

---

## 1. Why snapshot?

Longitudinal output changes when:

```text
new report arrives
corrected result arrives
mapping becomes validated
normalization policy changes
```

If timeline is mutable without provenance, an old AI report cannot be reproduced.

---

# 2. Snapshot inputs

Identity is derived from:

```text
subject
selected logical measurement representations
lineage decisions
excluded-observation reasons
series projection
policy_version
source dataset snapshot IDs
```

---

# 3. Content addressing & Production Canonicalization Profile

### Stage 05 Experimental Deterministic Identity
Stage 05 experiment uses:

```text
json.dumps(sort_keys=True, separators=(",", ":"))
→ SHA-256
→ timeline_snapshot_id
```

Điều này chứng minh:
- Cùng một cấu trúc input logic trong Python → sinh ra cùng một hash xác định độc lập với thứ tự xuất hiện của mảng đầu vào.

### Production Canonicalization Requirement (RFC 8785)
Tuy nhiên, cách tiếp cận trên **chưa đủ để tuyên bố cross-language canonical identity** trong môi trường production phân tán.
Bài học từ *ai-studio* cho thấy tính toàn vẹn đa ngôn ngữ (Go/Python) đòi hỏi:
1. **RFC 8785 (JSON Canonicalization Scheme - JCS)** chuẩn hóa thứ tự key và escape ký tự.
2. **Pre-scan JSON & cấm duplicate keys**: Bác bỏ các payload chứa key trùng lặp thay vì ghi đè thầm lặng.
3. **Kiểm soát miền số RFC 7493 (I-JSON)**: Khống chế precision số học (IEEE 754 float64 / big integers).
4. **Chuẩn hóa thời gian**: Chuẩn hóa ISO 8601 UTC đồng nhất.

**Phân kỳ lộ trình:**
- **Stage 05**: Khóa yêu cầu chuẩn hóa và chứng minh tính xác định thực nghiệm ở tầng domain.
- **Stage 13**: Đóng băng chính thức *Canonical Clinical Payload Profile* cho toàn bộ hệ thống trước khi tích hợp lưu trữ production.

---

# 4. Immutability rule

Old snapshot:

```text
never update in place
```

New source data:

```text
new snapshot
```

New policy:

```text
new snapshot
```

*Lưu ý triển khai:* Tính bất biến ngữ nghĩa (Semantic Immutability) được thực thi trong Stage 05. Cơ chế PostgreSQL trigger bất biến được hoãn sang **Stage 10**.

---

# 5. Cache rule

Future caches/materialized views may store snapshot data.

But:

```text
cache hit
≠
clinical authority
```

Canonical observations + policy provenance remain reconstruction basis.

---

# 6. Relation to future report generation

A future generated physician summary should be able to record:

```text
timeline_snapshot_id
policy_version
source dataset IDs
```

so the input state can be reconstructed.

---

# 7. Version types

Do not confuse:

```text
clinical source version
normalization policy version
longitudinal policy version
analysis/report version
runtime/config version
```

Each answers a different provenance question.
