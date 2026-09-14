# Observation Comparability Model

> **Status:** PROPOSED v0.1  
> **Stage:** 04

---

## 1. Vì sao comparability cần model riêng?

Stage 05 sẽ phân tích longitudinal trend.

Nếu Stage 04 chỉ normalize tên mà không xác định comparability, Stage 05 dễ nối các điểm không cùng semantics.

---

## 2. Four classes

```mermaid
flowchart TD
    Pair["So sánh hai Biomarker Observations (A, B)"] --> ValidCheck{"Cả hai đều có mã LOINC Validated?"}
    
    ValidCheck -->|Không| Indet["INDETERMINATE\n(Chưa đủ điều kiện so sánh)"]
    ValidCheck -->|Có| SameConcept{"Cùng LOINC Canonical Code?"}
    
    SameConcept -->|Không| RelCheck{"Cùng họ chất phân tích (analyte / component)?"}
    RelCheck -->|Có| RelNot["RELATED_NOT_COMPARABLE\n(Khác method / scale / property -> không merge)"]
    RelCheck -->|Không| Indet
    
    SameConcept -->|Có| ValKindCheck{"Cùng tương thích ValueKind?"}
    ValKindCheck -->|Không| Indet
    ValKindCheck -->|Có| UnitCheck{"Ngữ nghĩa đơn vị (UCUM)?"}
    
    UnitCheck -->|Cùng đơn vị chuẩn hóa| Exact["EXACT_COMPARABLE\n(So sánh / vẽ biểu đồ trực tiếp)"]
    UnitCheck -->|Đơn vị khác nhưng có phép chuyển đổi chuẩn| Conv["CONVERTIBLE_COMPARABLE\n(Quy đổi tuyến tính an toàn)"]
    UnitCheck -->|Đơn vị không tương thích / không quy đổi được| Indet
```

### EXACT_COMPARABLE

```text
same validated canonical code
+
same normalized unit semantics
+
compatible value kind
```

### CONVERTIBLE_COMPARABLE

```text
same validated canonical code
+
units connected by approved exact conversion
+
compatible value kind
```

### RELATED_NOT_COMPARABLE

Có liên hệ concept nhưng khác method/property/scale/code.

Ví dụ:

```text
Leukocyte esterase by Test strip
vs
Leukocyte esterase by Automated test strip
```

Conservative Stage 04 policy: không merge trend mặc định.

### INDETERMINATE

Mapping candidate/unmapped hoặc thiếu context.

---

## 3. Same name is insufficient

```text
RBC
```

có thể là:

```text
presence
#/volume
#/area HPF
automated count
manual microscopy
```

Do đó display name không phải comparability key.

---

## 4. Same component is insufficient

```text
Glucose urine presence
```

khác:

```text
Glucose urine mass concentration
```

về property/scale.

Không đưa lên cùng numeric trend.

---

## 5. Unit conversion does not fix semantic mismatch

Ngay cả khi hai values có units convert được, nếu canonical identity khác:

```text
NOT COMPARABLE
```

Identity first, conversion second.

---

## 6. Stage 05 handoff

Stage 05 chỉ được tạo longitudinal series khi comparability evaluator trả:

```text
EXACT_COMPARABLE
or
CONVERTIBLE_COMPARABLE
```

Mọi class khác cần tách series hoặc explicit review.
