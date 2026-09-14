# BioMarker Agent — Intended Use & Safety Envelope

> **Status:** APPROVED BASELINE v1.0  
> **Approved on:** 2026-09-14  
> **Stage:** 01 — Product & Clinical Domain Discovery  
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

## 2. Approved Intended Use

**[APPROVED INTENDED USE]**

> BioMarker Agent được định hướng như một hệ thống **physician-facing clinical information support tool** hỗ trợ bác sĩ trong quy trình chuyên môn: tóm tắt kết quả xét nghiệm, làm nổi bật/gắn cờ các kết quả bất thường dựa trên dữ liệu nguồn, cung cấp giải thích ngắn gọn và bằng chứng/ngữ cảnh y khoa (evidence/provenance) để bác sĩ kiểm tra. Hệ thống không tự trở thành clinical authority, không tự động đưa ra chẩn đoán, không chỉ định điều trị hay thay đổi thuốc, và không thay thế phán đoán chuyên môn của bác sĩ.

---

## 3. Primary User & Rollout Strategy

**[APPROVED DECISION — TD-01 & TD-01B]**

- **TD-01 (Primary User):** **Option B — Healthcare Professional / Physician**
  - Trước mắt là bác sĩ sử dụng kết quả xét nghiệm trong quy trình chuyên môn tại bệnh viện.
  - BioMarker Agent ở giai đoạn MVP **không được thiết kế như một sản phẩm self-service dành trực tiếp cho bệnh nhân/người dùng phổ thông**.
  - *Quy định phạm vi:* **Patient / Individual User = OUT OF CURRENT MVP SCOPE**.
- **TD-01B (Rollout Strategy):** **Internal Clinical Pilot → Physician UAT → Limited Go-live**
  - *01/10/2026:* Bắt đầu triển khai;
  - *30/10/2026:* Demo tính năng AI tóm tắt kết quả, gắn cờ bất thường và giải thích ngắn gọn cho bác sĩ;
  - *30/11/2026:* UAT với bác sĩ cho use case AI đọc kết quả xét nghiệm nước tiểu;
  - *31/12/2026:* Go-live cho Khoa Nội tổng hợp tại một bệnh viện (Vinmec);
  - *Hướng nâng cấp tiếp theo:* Phân tích xu hướng dọc qua nhiều lần xét nghiệm để hỗ trợ tầm soát và cảnh báo sớm.

Nguồn:

- FDA Clinical Decision Support Software, issued 2026-01-29  
  https://www.fda.gov/media/109618/download
- FDA Town Hall summary  
  https://www.fda.gov/medical-devices/medical-devices-news-and-events/town-hall-clinical-decision-support-software-final-guidance-03112026

---

## 4. Capability classes & Safety envelope

Để tránh scope trượt dần và loại trừ triệt để hiện tượng trôi dạt ngữ nghĩa (semantic drift), các năng lực của BioMarker Agent được phân loại thành các Capability Classes rõ ràng:

### LEVEL A — DATA PRESENTATION (ALLOWED)

Năng lực trích xuất, chuẩn hóa và bảo toàn dữ liệu quan sát gốc.

Ví dụ:
- Chỉ ra giá trị biomarker được ghi nhận trong báo cáo;
- Hiển thị khoảng tham chiếu gốc (source reference range) và đơn vị gốc;
- Bảo toàn tính toàn vẹn và nguồn gốc dữ liệu (data provenance);
- Nêu rõ các giới hạn dữ liệu (data limitations).

**Status:** ALLOWED / IN SCOPE FOR MVP.

### LEVEL B — EVIDENCE-LINKED EXPLANATION (ALLOWED)

Năng lực giải thích ngữ cảnh khoa học gắn liền với bằng chứng y văn.

Ví dụ:
- Giải thích định nghĩa thuật ngữ xét nghiệm và ý nghĩa sinh học;
- Liên kết biomarker với y văn/hướng dẫn chuyên môn (evidence/guidelines) đã được công nhận;
- Phân biệt rõ mối tương quan (correlation) và quan hệ nhân quả (causation);
- Trình bày ngữ cảnh đã biết và chưa biết (known/unknown context).

**Status:** ALLOWED / IN SCOPE FOR MVP (Bắt buộc có evidence provenance và claim grounding).

### CONTROLLED — CLINICIAN INTERPRETATION (APPROVED FOR MVP)

Năng lực hỗ trợ bác sĩ nhận diện nhanh bất thường và tóm tắt tổng quan trong quy trình chuyên môn.

Ví dụ:
- Gắn cờ bất thường (abnormal flags) dựa trên so sánh trực tiếp với khoảng tham chiếu của phòng xét nghiệm;
- Tóm tắt súc tích báo cáo xét nghiệm phục vụ bác sĩ tiết kiệm thời gian đọc kết quả;
- Cung cấp gợi ý giải thích kỹ thuật để bác sĩ tham khảo trong quá trình đánh giá chuyên môn.

**Điều kiện kiểm soát bắt buộc (Strict Governance):**
1. **Deterministic / Rules-based only:** Các cờ bất thường và phát hiện lệch ngưỡng bắt buộc phải dựa trên quy tắc logic xác định (deterministic rules), tuyệt đối không suy diễn tự do;
2. **Human-in-the-loop:** Đầu ra chỉ hiển thị trong giao diện chuyên môn của bác sĩ (Physician View). Bác sĩ giữ quyền quyết định chuyên môn tối cao và kiểm chứng độc lập;
3. Không đưa ra chẩn đoán xác định hay chỉ định điều trị.

**Status:** CONTROLLED / APPROVED FOR MVP (Physician Workflow).

### RESTRICTED — PERSON-SPECIFIC RECOMMENDATION (NOT APPROVED FOR MVP)

Năng lực đưa ra khuyến nghị can thiệp sức khỏe cá thể hóa.

Ví dụ:
- Đề xuất thay đổi lối sống, chế độ ăn uống, tập luyện cá nhân hóa;
- Đề xuất chỉ định thêm xét nghiệm chuyên sâu tiếp theo dựa trên hồ sơ cá nhân;
- Đưa ra lời khuyên can thiệp y tế cá thể hóa.

**Status:** RESTRICTED / OUT OF MVP SCOPE (Cần đánh giá lâm sàng và phê duyệt quy chế chuyên sâu trước khi xem xét ở các phiên bản tiếp theo).

### PROHIBITED — AUTONOMOUS DIAGNOSIS / TREATMENT (STRICTLY BANNED)

Năng lực can thiệp trực tiếp vào quyết định chẩn đoán hoặc điều trị y khoa.

Ví dụ:
- Tự động đưa ra kết luận chẩn đoán bệnh lý thay bác sĩ;
- Chỉ định, ngừng, thay đổi liều lượng thuốc hoặc kê đơn thuốc;
- Quyết định phác đồ điều trị;
- Tự động phân loại cấp cứu (emergency triage) hoặc điều khiển chăm sóc khẩn cấp.

**Status:** PROHIBITED / STRICTLY BANNED (TUYỆT ĐỐI CẤM ở mọi giai đoạn phát triển và triển khai).

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

### Approved decision

**[APPROVED DECISION — TD-02]**

Target geography/jurisdiction chính thức được phê duyệt: **Vinmec - Việt Nam**.
Hệ thống tuân thủ Luật Khám bệnh, chữa bệnh 2023 và các quy định chuyển đổi số y tế của Bộ Y Tế Việt Nam. Các hướng dẫn của US FDA CDS được sử dụng làm **tài liệu tham chiếu quốc tế** về phương pháp phân định rủi ro.

---

## 13. Safety envelope table

| Capability | Capability Class | Approved status | Governance condition |
|---|---|---|---|
| Extract biomarker values | LEVEL A | ALLOWED (Stage 03+) | Preserves raw values, units, ranges; Stage 03 accuracy gate |
| Preserve source range/unit/date | LEVEL A | ALLOWED (Stage 03+) | Full provenance preservation |
| Longitudinal trend display | LEVEL A | ALLOWED (Stage 05+) | Correct subject/date mapping; factual display only |
| Explain biomarker terminology | LEVEL B | ALLOWED (Stage 01+) | Educational framing; validated medical dictionaries |
| Evidence-linked contextualization | LEVEL B | ALLOWED (Stage 08+) | Provenance + claim grounding + limitation disclaimer |
| Highlight relation to source range | CONTROLLED | ALLOWED (MVP) | Deterministic rule-based comparison; doctor review |
| Abnormal flags display | CONTROLLED | ALLOWED (MVP) | Deterministic rules; physician interface only |
| Concise physician summary | CONTROLLED | ALLOWED (MVP) | Clinical summary for physician review; no autonomous inference |
| Follow-up chat on verified data | CONTROLLED | ALLOWED (Stage 07+) | Dataset-scoped; physician oversight |
| Lifestyle recommendation | RESTRICTED | NOT IN MVP | Clinical & regulatory review required post-pilot |
| Test ordering recommendation | RESTRICTED | NOT IN MVP | Suggest questions for doctor only; no autonomous order |
| Medication change / prescription | PROHIBITED | STRICTLY BANNED | TUYỆT ĐỐI CẤM ở mọi giai đoạn |
| Autonomous diagnosis | PROHIBITED | STRICTLY BANNED | TUYỆT ĐỐI CẤM ở mọi giai đoạn |
| Emergency triage | PROHIBITED | STRICTLY BANNED | TUYỆT ĐỐI CẤM ở mọi giai đoạn |
| Autonomous treatment decision | PROHIBITED | STRICTLY BANNED | TUYỆT ĐỐI CẤM ở mọi giai đoạn |

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

## 15. Exit condition & Sign-off

**[APPROVED BASELINE — ALL EXIT CONDITIONS MET ON 2026-09-14]**

- [x] Primary user được quyết định: **Option B — Healthcare Professional / Physician (Clinical Pilot & UAT tại Vinmec)**
- [x] Jurisdiction được quyết định: **Vinmec - Việt Nam**
- [x] Clinical reviewer/owner được xác định: **Vinmec Clinical Reviewer / Laboratory Specialist**
- [x] Allowed output capability classes được approve:
  - **LEVEL A (Data Presentation)** & **LEVEL B (Evidence-Linked Explanation)**
  - **CONTROLLED (Clinician Interpretation: Abnormal flags + concise physician summary - deterministic, rules-based, doctor review required)**
- [x] Restricted capabilities được xác nhận: **RESTRICTED (Person-specific recommendation - NOT approved for MVP)**
- [x] Prohibited output được approve: **PROHIBITED (Autonomous diagnosis, medication change, prescription, treatment directive, emergency triage bị cấm tuyệt đối)**
- [x] Product claims và UX copy tương thích với safety boundary.
