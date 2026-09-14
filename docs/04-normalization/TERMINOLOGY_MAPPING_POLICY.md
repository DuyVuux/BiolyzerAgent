# Terminology Mapping Policy

> **Status:** PROPOSED v0.1  
> **Stage:** 04

---

## 1. Mapping objective

Mục tiêu không phải:

```text
map everything
```

Mục tiêu là:

```text
map only when evidence is sufficient
```

---

## 2. Evidence hierarchy

Candidate mapping evidence được ưu tiên:

```text
1. Exact known local-code dictionary, if governed
2. Component/local alias
3. Specimen/system
4. Property/scale inferred from result semantics only when rule is explicit
5. Method
6. Unit compatibility
7. Panel membership/context
```

Không dùng model similarity làm authority ở Stage 04.

---

## 3. Validation rule

A mapping may become `validated` in the experiment only when exactly one catalog concept remains after all required semantic dimensions are checked.

Nếu:

```text
candidate_count > 1
```

status phải là:

```text
candidate
```

Nếu:

```text
candidate_count = 0
```

status:

```text
unmapped
```

---

## 4. Missing method

Missing method không được auto-filled từ common practice.

Ví dụ:

```text
Leukocyte esterase + Urine + Ordinal
```

không đủ để phân biệt:

```text
5799-2
60026-2
```

nếu source không cho biết method.

---

## 5. Mapping catalog is versioned

Experiment catalog records:

```text
terminology_system
terminology_version
code
semantic dimensions
rule source URL
```

Production catalog lifecycle sẽ được Stage 13/15 xem xét.

---

## 6. No silent terminology upgrade

Nếu LOINC version thay đổi:

```text
new catalog version
→ explicit review
→ regression eval
```

Không silently remap historical observations.

---

## 7. Clinical review boundary

Terminology mapping correctness là domain/data quality concern.

Nó không biến canonical code thành:

```text
diagnosis
clinical recommendation
```
