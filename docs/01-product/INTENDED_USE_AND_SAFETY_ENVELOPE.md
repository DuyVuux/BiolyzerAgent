# BioMarker Agent — Intended Use & Safety Envelope

> **Status:** PROPOSAL v0.1 — REQUIRES PRODUCT + CLINICAL REVIEW  
> **Stage:** 01  
> **Purpose:** Xác định ranh giới sản phẩm được phép làm gì trước khi thiết kế model, workflow hoặc UI.

---

## 1. Tại sao intended use phải viết trước code?

Cùng một thuật toán có thể có mức risk khác nhau tùy người dùng và cách output được dùng.

Ví dụ conceptual:

```text
"Đây là giá trị và khoảng tham chiếu trong báo cáo"
```

khác với:

```text
"Bạn có bệnh X"
```

và tiếp tục khác với:

```text
"Hãy dùng/ngừng một phương án điều trị"
```

Do đó, intended use không phải câu marketing. Nó điều khiển:

- safety controls;
- evidence requirements;
- evaluation;
- human oversight;
- regulatory assessment;
- wording;
- escalation;
- acceptable error.

---

## 2. Candidate intended use v0

**[PROPOSAL]**

> BioMarker Agent được đề xuất cho **non-time-critical informational review** của dữ liệu biomarker từ báo cáo xét nghiệm. Hệ thống tổ chức và giải thích dữ liệu đã được xác minh, cho phép so sánh theo thời gian khi có đủ dữ liệu, và cung cấp evidence-linked educational context. Hệ thống không được thiết kế để tự động thiết lập chẩn đoán, chỉ định điều trị, thay đổi thuốc, hoặc thay thế phán đoán của healthcare professional.

Đây là candidate intended use để Stage 02–08 có safety boundary làm việc.

Nó **chưa phải approved product claim**.

---

## 3. Intended user chưa được khóa

**[TEAM DECISION REQUIRED — TD-01]**

FDA 2026 phân biệt rất mạnh giữa một số CDS dành cho healthcare professional và software đưa recommendation tới patient/caregiver. Hướng dẫn này chỉ có authority trực tiếp trong phạm vi Hoa Kỳ và không tự động quyết định classification cho sản phẩm ở jurisdiction khác.

Do đó Stage 01 không được phép tự chọn:

```text
consumer product
```

hoặc:

```text
clinician CDS
```

chỉ để tiếp tục implementation.

Nguồn:

- FDA Clinical Decision Support Software, issued 2026-01-29  
  https://www.fda.gov/media/109618/download
- FDA Town Hall summary  
  https://www.fda.gov/medical-devices/medical-devices-news-and-events/town-hall-clinical-decision-support-software-final-guidance-03112026

---

## 4. Safety levels

Để tránh scope trượt dần, capability được phân thành bốn level.

### Level A — Data explanation

Ví dụ:

- chỉ ra giá trị được report;
- hiển thị source reference range;
- giải thích thuật ngữ;
- nêu data limitation.

**Baseline:** IN SCOPE candidate.

### Level B — Evidence-linked contextualization

Ví dụ:

- liên kết biomarker với evidence có liên quan;
- nêu hypothesis có điều kiện;
- phân biệt correlation và causation;
- trình bày known/unknown context.

**Baseline:** IN SCOPE candidate, nhưng phải có provenance và grounding.

### Level C — Person-specific recommendation

Ví dụ:

- đề xuất một hành động sức khỏe cụ thể;
- đề xuất xét nghiệm follow-up;
- ưu tiên option dựa trên dữ liệu cá nhân.

**Baseline:** RESTRICTED / TEAM + CLINICAL + REGULATORY REVIEW REQUIRED.

Reference product có capability tương tự không tạo authority cho BioMarker.

### Level D — Diagnosis / treatment direction

Ví dụ:

- xác định disease như output cuối;
- chỉ định/ngừng/thay đổi thuốc;
- quyết định treatment;
- điều khiển urgent care theo automation.

**Baseline:** OUT OF SCOPE cho candidate MVP.

---

## 5. Time-critical use

**[PROPOSAL SAFETY CONSTRAINT]**

BioMarker MVP không được thiết kế làm hệ thống time-critical.

Không được positioning như:

- emergency triage;
- real-time critical monitoring;
- automatic urgent-care directive;
- bedside decision engine.

FDA 2026 nhấn mạnh time-critical use làm giảm khả năng user độc lập review cơ sở của recommendation; WHO cũng yêu cầu well-defined use case, safety, accountability và human oversight.

---

## 6. Human autonomy

**[SOURCE-GROUNDED DESIGN PRINCIPLE]**

WHO guidance về AI for health nêu các nguyên tắc gồm:

- protect human autonomy;
- promote well-being and safety;
- transparency/explainability;
- responsibility/accountability;
- inclusiveness/equity;
- responsive/sustainable AI.

Nguồn:

- https://www.who.int/publications/i/item/9789240029200
- https://www.who.int/publications/i/item/9789240084759

**BioMarker implication — PROPOSAL:**

Hệ thống phải giúp người dùng thấy:

```text
input used
known data
missing data
source of evidence
confidence/limitation
```

thay vì chỉ trả một câu trả lời có vẻ chắc chắn.

---

## 7. Clinical claim policy baseline

### Allowed candidate forms

```text
"The source report shows..."
"The reported reference interval is..."
"Across the available dates..."
"Published evidence has reported an association..."
"Available data are insufficient to determine..."
"This may be worth discussing with a qualified healthcare professional..."
```

### Disallowed baseline forms

```text
"You definitely have..."
"This proves..."
"You do not need medical review..."
"Stop/start/change medication..."
"This result guarantees..."
```

Exact language policy sẽ được formalize ở Stage 07.

---

## 8. Reference range policy baseline

**[PROPOSAL]**

Priority:

```text
source lab range
>
validated context-specific range
>
generic educational reference
```

Generic knowledge không được silent override source report.

Một range có thể phụ thuộc vào:

- lab method;
- specimen;
- age;
- sex-related context;
- timing;
- fasting state;
- local laboratory practice.

Stage 01 chỉ đặt safety rule; exact model nằm Stage 02–04.

---

## 9. Missing-context policy

**[PROPOSAL]**

Nếu interpretation phụ thuộc context không có sẵn:

```text
missing context
→ explicit unknown
```

không phải:

```text
missing context
→ model guesses
```

Ví dụ context cần cân nhắc ở các Stage sau:

- test date;
- specimen;
- fasting status;
- medication;
- condition history;
- assay/method;
- demographic context khi reference phụ thuộc.

---

## 10. Evidence safety baseline

Một claim không được xem là grounded chỉ vì có URL.

Candidate safety rules:

1. claim phải liên kết với source cụ thể;
2. source phải được classify;
3. hệ thống phải tách source content khỏi model inference;
4. evidence conflict phải được thể hiện khi material;
5. date/version của guideline cần được giữ khi phù hợp;
6. unsupported citation phải bị xem là quality failure;
7. evidence không được tự động biến association thành causal claim.

Stage 06 sẽ formalize retrieval/ranking. Stage 08 sẽ formalize evaluation.

---

## 11. Automation bias

**[SOURCE FACT — FDA/WHO RISK CONTEXT]**

FDA 2026 thảo luận automation bias trong CDS và nhấn mạnh independent review basis cho một số HCP CDS. WHO cũng nhấn mạnh human autonomy và accountability.

**BioMarker proposal:**

UI/report không nên dùng wording hoặc visual hierarchy khiến người dùng hiểu:

```text
AI output = authoritative diagnosis
```

Future UX nên ưu tiên:

```text
data
→ basis
→ limitation
→ interpretation
```

---

## 12. Regulatory posture

**[CONSTRAINT]**

Stage 01 không tự tuyên bố:

```text
"not a medical device"
```

và cũng không tự tuyên bố:

```text
"medical device"
```

Classification phụ thuộc tối thiểu vào:

- intended use;
- intended user;
- output;
- jurisdiction;
- labeling/marketing claims;
- workflow;
- level of automation.

### Required decision

**[TEAM DECISION REQUIRED — TD-02]**

Target geography/jurisdiction phải được xác định trước khi product claim được freeze.

### U.S. reference only

FDA 2026 hiện nêu rằng software function cung cấp/support recommendation cho patient/caregiver có thể vẫn thuộc device definition, trong khi một số HCP CDS có thể thuộc exclusion khi thỏa các criteria cụ thể.

Đây là **regulatory reference**, không phải legal advice và không quyết định product status ở Việt Nam hoặc jurisdiction khác.

---

## 13. Safety envelope table

| Capability | Candidate status | Condition |
|---|---|---|
| Extract biomarker values | IN SCOPE LATER | Stage 03 accuracy gate |
| Preserve source range/unit/date | IN SCOPE LATER | Must keep provenance |
| Highlight relation to source range | IN SCOPE LATER | No diagnosis inference |
| Longitudinal trend display | IN SCOPE LATER | Correct subject/date mapping |
| Explain biomarker terminology | IN SCOPE | Educational framing |
| Evidence-linked contextualization | IN SCOPE LATER | Grounding + limitation |
| Follow-up chat on verified data | IN SCOPE LATER | Dataset-scoped |
| Lifestyle recommendation | RESTRICTED | Clinical/product/regulatory decision |
| Test ordering recommendation | RESTRICTED | Clinical/product/regulatory decision |
| Medication change | OUT OF SCOPE | MVP |
| Autonomous diagnosis | OUT OF SCOPE | MVP |
| Emergency triage | OUT OF SCOPE | MVP |
| Autonomous treatment decision | OUT OF SCOPE | MVP |

---

## 14. Safety escalation questions

Stage 07 cần quyết định:

- Critical-value display policy là gì?
- Hệ thống có chỉ dẫn user liên hệ healthcare professional hay không?
- Wording nào được clinical reviewer approve?
- Khi source report có explicit critical flag, product phải làm gì?
- Khi evidence và source report mâu thuẫn, output policy là gì?
- Khi extraction confidence thấp, bắt buộc human verification ở mức nào?

---

## 15. Exit condition

Tài liệu này chỉ được nâng từ `PROPOSAL` khi tối thiểu:

- primary user được quyết định;
- jurisdiction được quyết định;
- clinical reviewer/owner được xác định;
- allowed output level được approve;
- prohibited output được approve;
- product claims và UX copy tương thích với safety boundary.
