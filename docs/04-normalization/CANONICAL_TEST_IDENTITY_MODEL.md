# Canonical Test Identity Model

> **Status:** PROPOSED v0.1  
> **Stage:** 04

---

## 1. Test identity là gì?

Canonical test identity trả lời:

> Observation này đang đo **chính xác concept nào**, trong specimen nào, theo scale và method nào?

Tên hiển thị không đủ.

---

## 2. Semantic fingerprint

Candidate fingerprint:

```text
component
property
system/specimen
scale
method
unit dimension when relevant
```

LOINC formalizes these dimensions strongly enough để Stage 04 dùng làm mapping evidence.

---

## 3. Local identity phải tồn tại song song

Canonical observation giữ:

```text
local_test_name
canonical_test.system
canonical_test.code
canonical_test.display
canonical_test.version
mapping_status
```

Không overwrite local name.

---

## 4. Alias discovery không phải validation

Alias table có thể nói:

```text
"LE"
"Leukocyte esterase"
```

cùng trỏ tới component candidate.

Nhưng nếu source chỉ có:

```text
LE
Urine
Ordinal
```

mà không biết `Test strip` hay `Automated test strip`, mapper phải giữ:

```text
candidate
```

với nhiều mã có thể phù hợp.

---

## 5. Method-sensitive examples

### Leukocyte esterase

```text
5799-2  → Test strip
60026-2 → Automated test strip
```

### pH

```text
5803-2  → Test strip
50560-2 → Automated test strip
```

### Glucose presence

```text
25428-4 → Test strip
50555-2 → Automated test strip
```

Tên analyte giống nhau nhưng method khác làm code khác.

---

## 6. Scale-sensitive examples

Urinalysis glucose có thể dùng:

```text
Presence / ordinal
Mass concentration / quantitative
Moles concentration / quantitative
```

Do đó:

```text
"Glucose urine"
```

không phải mapping đủ chính xác.

---

## 7. Microscopy example

RBC urine sediment by high-power-field microscopy:

```text
13945-1
```

Fingerprint bao gồm:

```text
Component = Erythrocytes
System    = Urine sediment
Scale     = Quantitative
Method    = Microscopy high power field
Unit      = /[HPF]
```

Nếu chỉ biết:

```text
RBC urine
```

không được validate mã này.

---

## 8. Mapping evidence record

Stage 04 experiment output có thể ghi:

```text
candidate_codes
matched_dimensions
missing_dimensions
terminology_version
catalog_rule_id
```

Production mapping provenance có thể mở rộng sau Stage 10/13.

---

## 9. False validation là failure hạng nhất

Một mapper tốt không được tối ưu duy nhất:

```text
mapping coverage
```

Phải đo:

```text
false_validation_rate
```

Nếu context thiếu nhưng system vẫn trả `validated`, đó là lỗi nghiêm trọng.

---

## 10. Domain rule

```text
same local label
≠
same canonical test
```

và:

```text
same component
≠
longitudinally comparable
```
