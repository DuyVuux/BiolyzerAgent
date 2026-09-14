# Terminology & Interoperability Boundary

> **Status:** PROPOSED v0.1  
> **Stage:** 02

## 1. Ba bài toán khác nhau

```text
FHIR → interoperability/resource semantics
LOINC → observation/test identity terminology
UCUM → machine-readable unit semantics
```

Không dùng một standard để giải quyết vấn đề của standard khác.

## 2. FHIR

FHIR R5 hiện là current published version. Stage 02 dùng FHIR như semantic cross-check:

```text
DiagnosticReport → report context
Observation → atomic measurement/assertion
referenceRange → interpretation guidance
value[x] → multiple result types
```

Stage 02 không chọn FHIR persistence, không tạo FHIR server, không khóa Vinmec integration version.

## 3. LOINC

Current reference tại thời điểm review:

```text
LOINC 2.83
released 2026-08-19
```

Canonical mapping object:

```text
system = "http://loinc.org"
code
display
version
```

Mapping status bắt buộc tách `candidate` và `validated`.

LOINC identity phụ thuộc nhiều dimensions như Component, Property, Time, System, Scale, Method; vì vậy same display name không đủ để kết luận same observation.

## 4. UCUM

Official specification review:

```text
Version 2.2
Date 2024-06-17
```

Canonical value giữ cả:

```text
unit_source
unit_ucum
```

Normalization không overwrite source unit.

## 5. Adapter architecture

```text
PDF / LIS / HIS / FHIR / other
          ↓
      adapters
          ↓
BioMarker Canonical Domain
          ↓
  downstream analysis
          ↓
FHIR/API/ai-studio adapters later
```

## 6. Version policy

Terminology version phải được giữ khi mapping materialize. Không assume terminology mapping bất biến vĩnh viễn.

## 7. Non-goal

Stage 02 không xây terminology server, LOINC auto-mapper, UCUM conversion engine hoặc FHIR endpoint.
