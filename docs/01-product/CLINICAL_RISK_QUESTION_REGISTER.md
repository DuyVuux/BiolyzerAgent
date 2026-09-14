# BioMarker Agent — Clinical Risk Question Register

> **Status:** OPEN REGISTER v0.1  
> **Stage:** 01  
> **Purpose:** Ghi nhận risk questions cần được giải quyết ở các Stage sau. Đây chưa phải formal risk-management file theo một regulatory framework cụ thể.

---

## 1. Cách đọc

Mỗi item có:

```text
ID
Risk question
Potential harm
Current control hypothesis
Owner needed
Target Stage
Status
```

Không được hiểu:

```text
risk listed
= risk solved
```

---

## 2. Risk questions

### CR-001 — Wrong numeric extraction

**Question:** Điều gì xảy ra nếu một giá trị bị đọc sai một chữ số hoặc dấu thập phân?

**Potential harm:** downstream interpretation sai nhưng output có vẻ hợp lý.

**Control hypothesis:** source-linked extraction + confidence + verification gate.

**Target:** Stage 03 / 08  
**Status:** OPEN

---

### CR-002 — Wrong unit

**Question:** Nếu value đúng nhưng unit sai hoặc bị mất thì sao?

**Potential harm:** so sánh range/trend sai lớn.

**Control hypothesis:** unit is mandatory-or-unresolved; no silent conversion.

**Target:** Stage 03–04  
**Status:** OPEN

---

### CR-003 — Wrong reference interval

**Question:** Nếu hệ thống dùng generic range thay vì source lab range?

**Potential harm:** false flag hoặc false reassurance.

**Control hypothesis:** source range has priority; generic reference never silently overrides.

**Target:** Stage 02–04  
**Status:** OPEN

---

### CR-004 — Subject/report mix-up

**Question:** Hai report của hai người khác nhau có thể bị merge không?

**Potential harm:** severe privacy and clinical error.

**Control hypothesis:** explicit subject/dataset identity + authorization + merge validation.

**Target:** Stage 05 / 14  
**Status:** OPEN

---

### CR-005 — Date ordering error

**Question:** Duplicate/recent value bị ưu tiên sai do date parsing?

**Potential harm:** trend conclusion ngược thực tế.

**Control hypothesis:** typed date provenance; ambiguous date blocks trend interpretation.

**Target:** Stage 03 / 05  
**Status:** OPEN

---

### CR-006 — Missing context treated as fact

**Question:** Model có đoán fasting state, medication, specimen hoặc history không?

**Potential harm:** confident but invalid interpretation.

**Control hypothesis:** unknown remains explicit unknown.

**Target:** Stage 07  
**Status:** OPEN

---

### CR-007 — Correlation becomes causation

**Question:** Evidence về association bị viết thành causal statement?

**Potential harm:** user thay đổi behavior dựa trên causal claim không support.

**Control hypothesis:** claim typing + evidence entailment + safety checker.

**Target:** Stage 06–08  
**Status:** OPEN

---

### CR-008 — Fabricated or unsupported citation

**Question:** Citation tồn tại nhưng không support claim, hoặc source không tồn tại?

**Potential harm:** false authority.

**Control hypothesis:** citation validation + claim-source entailment evaluation.

**Target:** Stage 06 / 08  
**Status:** OPEN

---

### CR-009 — False reassurance

**Question:** Output làm user hiểu rằng “range normal” đồng nghĩa không cần medical review?

**Potential harm:** delayed care.

**Control hypothesis:** wording policy + no “normal health guaranteed” inference.

**Target:** Stage 07 / clinical review  
**Status:** OPEN

---

### CR-010 — Excessive alarm

**Question:** Một minor deviation bị diễn giải như severe problem?

**Potential harm:** anxiety, unnecessary action.

**Control hypothesis:** calibrated language + source context + limitation.

**Target:** Stage 07 / 08  
**Status:** OPEN

---

### CR-011 — Critical flag handling

**Question:** Nếu source report đã đánh dấu critical, product hiển thị/escalate thế nào?

**Potential harm:** hidden urgent signal hoặc unsafe directive.

**Control hypothesis:** no autonomous triage; explicit policy requires clinical review.

**Owner needed:** Clinical owner  
**Target:** Stage 07 / 14  
**Status:** TEAM DECISION REQUIRED

---

### CR-012 — Recommendation boundary drift

**Question:** Chat bắt đầu ở educational explanation nhưng follow-up dần thành treatment advice?

**Potential harm:** safety envelope bị vượt qua qua nhiều turns.

**Control hypothesis:** conversation-level policy enforced every turn, not only initial prompt.

**Target:** Stage 07 / 14  
**Status:** OPEN

---

### CR-013 — Evidence population mismatch

**Question:** Evidence population khác user context nhưng output không nói rõ?

**Potential harm:** overgeneralization.

**Control hypothesis:** evidence metadata + applicability limitation.

**Target:** Stage 06–08  
**Status:** OPEN

---

### CR-014 — Stale evidence

**Question:** Hệ thống dùng guideline/study version cũ mà không show date/version?

**Potential harm:** outdated context.

**Control hypothesis:** evidence date/version + retrieval policy.

**Target:** Stage 06  
**Status:** OPEN

---

### CR-015 — Automation bias

**Question:** User tin output vì wording/UI quá authoritative?

**Potential harm:** over-reliance.

**Control hypothesis:** basis-first UX, uncertainty, independent-review support.

**Target:** Stage 07 / 14  
**Status:** OPEN

---

### CR-016 — Clinical language misunderstanding

**Question:** Technical term đúng nhưng user hiểu sai?

**Potential harm:** incorrect self-action.

**Control hypothesis:** plain-language layer + term definitions + usability review.

**Target:** Stage 07 / 14  
**Status:** OPEN

---

### CR-017 — Cross-report incompatible measurements

**Question:** Hai values cùng display name nhưng khác specimen/method/unit có bị plot chung?

**Potential harm:** invalid trend.

**Control hypothesis:** canonical identity requires semantic compatibility.

**Target:** Stage 04–05  
**Status:** OPEN

---

### CR-018 — Missing biomarker inferred as normal

**Question:** Không thấy marker trong report có bị model nói là normal?

**Potential harm:** fabricated clinical fact.

**Control hypothesis:** absent ≠ measured.

**Target:** Stage 02 / 07  
**Status:** OPEN

---

## 3. Risk review gate

Trước khi Stage 07 được close:

- CR-001..018 phải có owner/status;
- critical risks phải map sang control;
- control phải map sang test/eval;
- unresolved high-risk behavior không được hidden bằng prompt wording.

---

## 4. Regulatory note

Risk register này không tự tuyên bố compliance với ISO 14971 hoặc framework khác.

Nếu intended use/jurisdiction khiến formal medical-device risk management applicable, team phải tạo workstream/quality process riêng với qualified owner.
