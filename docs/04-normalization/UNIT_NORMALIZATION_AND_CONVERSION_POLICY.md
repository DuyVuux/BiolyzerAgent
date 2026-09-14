# Unit Normalization & Conversion Policy

> **Status:** PROPOSED v0.1  
> **Stage:** 04

---

## 1. Hai lớp khác nhau

### Representation normalization

Chuẩn hóa cách viết của cùng một unit.

Ví dụ:

```text
mg/dl → mg/dL
/HPF  → /[HPF]
```

### Numeric conversion

Thay đổi giá trị số để biểu diễn cùng đại lượng ở unit khác.

Ví dụ:

```text
30 mg/dL → 0.3 g/L
```

Hai thao tác không được trộn.

---

## 2. Preserve source

Mọi normalized observation phải giữ:

```text
unit_source
unit_ucum
```

Nếu conversion diễn ra, provenance phải biết:

```text
source value/unit
normalized value/unit
conversion rule
```

Stage 04 experiment ghi rule ID; production lineage được defer.

---

## 3. Baseline UCUM lexical rules

Experiment catalog hỗ trợ:

```text
mg/dL   → mg/dL
mg/dl   → mg/dL
MG/DL   → mg/dL
g/L     → g/L
/HPF    → /[HPF]
/[HPF]  → /[HPF]
/LPF    → /[LPF]
/[LPF]  → /[LPF]
pH      → [pH]
[pH]    → [pH]
```

Không có nghĩa đây là full UCUM parser.

---

## 4. Safe conversion rule

Stage 04 chỉ cho phép conversion khi:

```text
same dimension
+
explicit approved conversion rule
+
no analyte-specific chemistry assumption
```

Experiment:

```text
mg/dL ↔ g/L
```

Factor:

```text
1 mg/dL = 0.01 g/L
```

---

## 5. Unsafe conversion baseline

Không tự convert:

```text
mg/dL ↔ mmol/L
```

vì cần molecular weight/analyte context.

Không tự convert:

```text
/[HPF] ↔ /[LPF]
```

vì field area/method semantics không đơn giản là unit factor chung.

---

## 6. Unitless does not mean unknown

Một số observations có semantic unit-like representation riêng hoặc không có conventional unit.

Ví dụ specific gravity hoặc categorical presence results.

Do đó:

```text
unit missing
```

không luôn là data-quality error.

---

## 7. Failure classes

```text
UNIT_UNKNOWN
UNIT_AMBIGUOUS
UNIT_DIMENSION_MISMATCH
CONVERSION_RULE_MISSING
ANALYTE_SPECIFIC_CONVERSION_REQUIRED
```

Fail closed:

```text
unknown conversion
→ do not change numeric value
```
