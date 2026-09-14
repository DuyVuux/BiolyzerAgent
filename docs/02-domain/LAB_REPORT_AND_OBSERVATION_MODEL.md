# Lab Report & Observation Model

> **Status:** PROPOSED v0.1  
> **Stage:** 02

## 1. Vấn đề

Trong lab systems, các từ `test`, `result`, `panel`, `observation`, `report` thường bị dùng lẫn nhau. Nếu code cũng làm vậy, ta dễ tạo object trộn artifact, clinical result và AI interpretation.

Stage 02 cấm cách đó.

## 2. Bốn lớp

### 2.1 SourceDocument

Artifact vật lý/logical: PDF, image hoặc structured export.

### 2.2 LabReport

Diagnostic report có context: subject, specimen, time, diagnostic service, status, atomic results và source conclusion.

FHIR R5 cũng tách DiagnosticReport khỏi atomic Observation. BioMarker học semantic distinction đó nhưng không clone resource.

### 2.3 BiomarkerObservation

Atomic result gồm test identity, value, unit, range, method, specimen, time, source interpretation và provenance.

### 2.4 Analysis / Clinical Claim

Không thuộc Stage 02. Một câu kiểu “pattern này gợi ý...” là downstream interpretation/claim, không được nhét vào Observation.

## 3. Vì sao boundary này là safety control?

Nếu Observation và interpretation cùng field, downstream không còn biết cái gì source report nói, cái gì model suy luận và cái gì bác sĩ xác nhận.

Correct separation:

```text
Observation = source-grounded data
Derived Assessment = deterministic comparison
Clinical Claim = later reasoning artifact
Physician Judgment = external professional authority
```

## 4. Report status baseline

```text
registered
partial
preliminary
modified
final
amended
corrected
appended
cancelled
entered_in_error
unknown
```

Nếu source không có status, dùng `unknown`, không default `final`.

## 5. Observation status baseline

```text
registered
preliminary
final
amended
corrected
cancelled
entered_in_error
unknown
```

## 6. Time semantics

Tách `effective_at`, `issued_at`, và document `received_at`. Observation có thể có effective time riêng nếu source support. Exact inheritance policy defer Stage 03–05.

## 7. Group/panel semantics

Urinalysis có thể là panel. Stage 02 không hardcode panel members; report giữ `observation_ids[]`.

## 8. Source conclusion

Nếu original report có narrative conclusion, preserve thành `source_conclusion_text`. Không rename thành `ai_summary` hoặc diagnosis.

## 9. FHIR cross-check

FHIR R5 mô tả DiagnosticReport như report-level context chứa Observation references cho atomic results và nêu Observation không nên dùng như nơi ghi clinical diagnosis trong boundary thông thường.

BioMarker invariant tương ứng:

```text
report context stays report context
atomic result stays observation
diagnosis does not enter canonical observation
```
