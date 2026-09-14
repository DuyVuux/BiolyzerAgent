# Result, Reference Range & Flag Model

> **Status:** PROPOSED v0.1  
> **Stage:** 02

## 1. Vì sao `value: float` là sai?

Urinalysis có thể report:

```text
25 mg/dL
Negative
Trace
1+
2+
3+
0–2 /HPF
Few
Many
```

LOINC hiện mô tả cả quantitative, ordinal, per-field/per-volume và categorical representations. Vì vậy canonical result là tagged union.

## 2. Result kinds

### Quantity

```json
{
  "kind": "quantity",
  "value": 5,
  "comparator": "<",
  "unit_source": "/HPF",
  "unit_ucum": "/[HPF]"
}
```

`<5` không được parse thành `5` và làm mất comparator.

### Interval

```json
{
  "kind": "interval",
  "low": 0,
  "high": 2,
  "unit_source": "/HPF",
  "unit_ucum": "/[HPF]"
}
```

Không collapse thành midpoint.

### Ordinal

```json
{
  "kind": "ordinal",
  "source_text": "1+",
  "normalized_code": "1_plus",
  "rank": 2
}
```

`normalized_code/rank` optional. Nếu mapping chưa validated, giữ source text là đủ.

### Categorical

```json
{
  "kind": "categorical",
  "source_text": "Negative",
  "normalized_code": "negative"
}
```

Không tự assume order.

### Text

Fallback có provenance khi source cung cấp narrative result chưa normalize an toàn.

## 3. Absence semantics

Phân biệt:

```text
Observation absent from report
Observation present with "Not detected"
Observation present but value unavailable
```

`Negative/Not detected` thường là result semantic, không phải missing.

## 4. Reference range

Reference range bắt buộc giữ:

```text
raw_text
origin
```

Optional parsed forms:

```text
numeric_interval
categorical_expected
textual
```

Stage 02 chỉ canonicalize source report range; generic range không được tự thay source range.

## 5. Source flag vs derived assessment

**SourceInterpretation**: source report in `H/L/ABN/Critical/Positive...`.

**DerivedRangeAssessment**: system deterministic comparison với verified source range.

Không dùng chung một `is_abnormal: true/false`.

## 6. Clinical risk flag là lớp thứ ba

Critical/panic/escalation semantics thuộc Stage 07 dưới clinical policy được approve. Nó không dùng chung field với source/derived range flag.

## 7. Correct mental model

```text
SOURCE VALUE
    ↓
SOURCE REFERENCE RANGE
    ↓
SOURCE INTERPRETATION
    ↓
[future] DETERMINISTIC RANGE ASSESSMENT
    ↓
[future] CLINICAL REASONING
```
