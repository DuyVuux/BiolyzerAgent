# Urinalysis Vertical Slice — Domain Stress Test

> **Status:** DOMAIN VALIDATION BASELINE v0.1  
> **Stage:** 02

## 1. Vì sao chọn Urinalysis?

Urinalysis là MVP clinical slice đã được khóa và là bài test domain model tốt vì chứa physical properties, chemical/dipstick results và microscopy results với mixed value types.

## 2. Evidence từ LOINC hiện tại

LOINC 2.83 được phát hành ngày 19/08/2026. LOINC knowledge base cho urinalysis test strips mô tả hai đường report phổ biến:

```text
quantitative concentration
OR
ordinal Negative / 1+ / 2+ / 3+
```

Urinalysis panels còn có microscopy results theo `#/volume`, `/HPF`, `/LPF` hoặc categorical như `none/few/many`.

Điều này trực tiếp validate tagged-union value model.

## 3. Structural examples

> Các ví dụ dưới đây chỉ kiểm thử **hình dạng dữ liệu**, không phải clinical reference guidance.

### Quantitative

```text
Result: 6.0
Value kind: quantity
```

### Ordinal

```text
Result: 1+
Value kind: ordinal
```

### Categorical

```text
Result: Negative
Value kind: categorical
```

### Interval microscopy

```text
Result: 0–2 /HPF
Value kind: interval
```

### Comparator quantity

```text
Result: <5 /LPF
Value kind: quantity
Comparator: <
```

## 4. Domain pressure revealed

- Local name alone không đủ để xác định observation identity.
- Ordinal không phải generic string.
- Microscopy cần unit/context.
- `Negative` không phải missing.
- Lab abnormal flag không phải diagnosis.

## 5. Minimum synthetic coverage

Stage 02 fixtures phải cover quantity, comparator, interval, ordinal, categorical, source range, source interpretation, optional LOINC mapping, UCUM, provenance và verification state.

## 6. Stage 03 phải đo riêng

```text
test-name extraction
value extraction
value-kind classification
comparator extraction
unit extraction
reference-range extraction
source-flag extraction
date extraction
source locator
```

Không dùng một metric “OCR accuracy” chung để thay thế.

## 7. Stage 04 pressure

Stage 04 phải trả lời khi nào hai local test names equivalent, khi nào LOINC mapping candidate vs validated, khi nào units convert được và khi nào observations comparable. Stage 02 không hardcode các câu trả lời này.
