# BioMarker Agent — Data & Privacy Question Register

> **Status:** OPEN REGISTER v0.1  
> **Stage:** 01  
> **Purpose:** Xác định câu hỏi về dữ liệu nhạy cảm trước khi chọn storage, logging, model provider hoặc integration.

---

## 1. Zero-PHI rule cho development artifacts

**[CONSTRAINT]**

Stage 01–08 artifacts, fixtures và examples không được chứa real patient data.

Allowed:

```text
synthetic data
explicitly approved de-identified fixtures
```

Default for current project:

```text
synthetic only
```

---

## 2. Data classes candidate

| Data class | Example | Sensitivity posture |
|---|---|---|
| Raw lab document | PDF/image | HIGH |
| Extracted observation | test/value/unit/range/date | HIGH |
| User context | age, medication, history if allowed | HIGH |
| Dataset identity | subject/dataset linkage | HIGH |
| Evidence source | public paper/guideline | Usually public |
| Evidence query | may contain user-derived terms | Potentially sensitive |
| Analysis report | synthesized health context | HIGH |
| Chat follow-up | user questions + analysis context | HIGH |
| Telemetry | IDs/status/timing | Must be minimized |
| Security/audit event | actor/resource/action | Sensitive operational data |

Exact classification taxonomy cần security/privacy owner approve ở Stage 14.

---

## 3. Questions

### DP-001 — Raw document retention

Có lưu raw report sau processing không?

**[APPROVED DECISION — TD-05 Tiered Retention Policy]**
- **Giai đoạn Phát triển (Development / Stage 01–08):**
  - **Quy tắc tuyệt đối (Zero-PHI):** Không lưu file bệnh nhân thật. Chỉ dùng file synthetic ở `testdata/synthetic/lab-reports/`.
  - **Ephemeral Processing:** File upload thử nghiệm cục bộ lưu tại `var/uploads/` (gitignored) và bị xóa sau khi hoàn tất trích xuất (`DEV_PURGE_UPLOADS_ON_COMPLETION=true`).
- **Giai đoạn Sản phẩm tại Vinmec (Production / Stage 10+):**
  - **Delegated Storage:** Báo cáo gốc được lưu trữ trong hạ tầng lưu trữ bảo mật của Vinmec (EMR/PACS/ObjectStore có mã hóa AES-256).
  - BioMarker chỉ lưu trữ Document Hash (SHA-256) và URI liên kết để truy vết nguồn gốc, không tự ý nhân bản file PDF ra ngoài ranh giới bảo mật của bệnh viện.

**Status:** APPROVED (2026-09-14)

---

### DP-002 — Structured dataset retention

Có giữ canonical observations lâu hơn raw document không?

Impact:

- longitudinal analysis;
- deletion semantics;
- breach surface;
- provenance;
- reproducibility.

**Target:** Stage 05 / 10 / 14  
**Status:** OPEN

---

### DP-003 — Identity linkage

Dataset gắn với:

- platform user;
- patient/subject identifier;
- pseudonymous analysis subject;
- external clinical identifier?

**Status:** TEAM DECISION REQUIRED before real integration.

---

### DP-004 — Model provider boundary

Raw clinical content có được gửi tới external model provider không?

Cần quyết định:

- data processing terms;
- retention/training settings;
- region;
- minimum necessary content;
- redaction/pseudonymization.

**Target:** Stage 09 / 14  
**Status:** OPEN

---

### DP-005 — Evidence search leakage

Search query có thể lộ sensitive context không?

Control hypothesis:

```text
derive minimum necessary research query
≠
send full report/chat history to search provider
```

**Target:** Stage 06 / 14  
**Status:** OPEN

---

### DP-006 — Logging

Default không log:

- raw report;
- full health context;
- model prompt containing clinical data;
- raw provider response;
- credentials.

Need safe trace IDs/provenance without raw payload.

**Target:** Stage 09 / 14  
**Status:** PROPOSAL

---

### DP-007 — Cross-subject isolation

Resource locator không được xem như authority.

Need future tests:

```text
subject/user A cannot retrieve dataset/report of subject/user B without explicit authorized relationship
```

**Target:** Stage 14  
**Status:** OPEN

---

### DP-008 — De-identification vs pseudonymization

“Strip PII” có thể làm mất context cần cho:

- age-related range;
- sex-related range;
- longitudinal linkage.

Do đó product cần phân biệt:

```text
remove unnecessary direct identifiers
≠
erase clinically relevant context
```

**Target:** Stage 03 / 14  
**Status:** OPEN

---

### DP-009 — User deletion

Nếu product lưu data:

- user có delete được không?
- raw, structured, report, chat, artifact, backup xử lý thế nào?
- audit record nào phải giữ?

**Target:** Stage 10 / 14  
**Status:** OPEN

---

### DP-010 — Evidence/report provenance retention

Nếu source evidence thay đổi, report cũ cần giữ exact evidence identity không?

**Target:** Stage 06 / 13  
**Status:** OPEN

---

### DP-011 — Data residency

Target geography quyết data residency requirement nào?

**Dependency:** TD-02 jurisdiction  
**Status:** BLOCKED

---

### DP-012 — Access by clinical reviewer

Clinical review có dùng real data không?

Stage 01–08 answer:

```text
No real patient data in project artifacts.
```

Future pilot requires approved access model.

---

## 4. Privacy principle baseline

**[PROPOSAL]**

```text
minimum necessary data
+
explicit purpose
+
bounded retention
+
least privilege
+
traceable access
+
no raw sensitive logging by default
```

---

## 5. Handoff to later Stages

- Stage 03: provenance/redaction questions during ingestion.
- Stage 05: subject/timeline identity.
- Stage 06: safe evidence queries.
- Stage 09–10: runtime/state/storage.
- Stage 14: authorization/privacy/retention implementation.
