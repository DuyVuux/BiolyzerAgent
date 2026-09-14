# Provenance, Verification & Data Quality Model

> **Status:** PROPOSED v0.1  
> **Stage:** 02

## 1. Vấn đề

Clinical AI có thể tạo output nghe hợp lý ngay cả khi input extraction sai. Vì vậy canonical observation phải biết nó đến từ đâu, được đọc thế nào, đã verify chưa và uncertainty nào còn tồn tại.

## 2. Provenance layers

### Document provenance

```text
document_id
content_sha256
source_system_label
received_at
```

Hash là integrity identity, không phải clinical identity hay authorization.

### Observation source locator

Candidate locator:

```text
page
section
row_label
field_label
raw_text
bounding_box?
```

Stage 03 xác định locator thực tế parser/OCR tạo được ổn định tới đâu.

### Extraction provenance

Candidate metadata:

```text
extraction_method
extractor_name
extractor_version
confidence?
```

Confidence không được coi là calibrated probability nếu experiment chưa chứng minh calibration.

## 3. Verification state

```text
unverified
verified
corrected
rejected
```

Optional metadata:

```text
verified_at
verified_by_role
correction_note
```

## 4. Mapping state

```text
unmapped
candidate
validated
not_applicable
```

Candidate LOINC mapping không được downstream xem là authority.

## 5. Data-quality issue classes

```text
missing_unit
ambiguous_unit
missing_reference_range
ambiguous_reference_range
missing_effective_time
ambiguous_test_identity
low_extraction_confidence
source_conflict
unsupported_value_format
```

Issue generation phải context-aware; categorical test không nhất thiết cần unit.

## 6. Human-in-the-loop

Stage 01 cố ý chưa khóa threshold như `0.95`. Stage 02 chỉ model đủ `confidence + issues + verification status` để Stage 03/08 quyết threshold dựa trên evidence.

## 7. Correction lineage

Nếu bác sĩ sửa extraction, raw source text vẫn phải preserve. Exact correction event model defer Stage 03/10.

## 8. Downstream consumption rule

Reasoning Stage 07 không được tự dùng unverified/candidate-mapped/conflicted data như verified fact nếu policy không cho phép.

## 9. Minimum trace requirement

Một observation dùng downstream phải trace được:

```text
canonical observation ID
→ source report ID
→ source document ID
→ source locator/raw text
```
