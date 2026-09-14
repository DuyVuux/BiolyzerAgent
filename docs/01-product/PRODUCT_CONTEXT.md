# BioMarker Agent — Product Context

> **Status:** PROPOSAL v0.1  
> **Stage:** 01 — Product & Clinical Domain Discovery  
> **Audience:** Product owner, technical lead, clinical reviewer, engineering team  
> **Purpose:** Xác định BioMarker Agent đang giải bài toán gì trước khi quyết định data model, runtime, database hoặc tích hợp platform.

---

## 1. Bài toán thực tế

Một kết quả xét nghiệm thường được phát hành dưới dạng báo cáo có nhiều chỉ số, đơn vị, khoảng tham chiếu, ghi chú và thời điểm lấy mẫu. Với người không làm chuyên môn, ba vấn đề xuất hiện ngay:

1. **Dữ liệu khó đọc như một hệ thống thống nhất.** Một chỉ số riêng lẻ có thể dễ nhìn, nhưng nhiều chỉ số qua nhiều lần xét nghiệm tạo ra một bức tranh khó theo dõi.
2. **Khoảng tham chiếu không tự động giải thích ý nghĩa.** Một giá trị nằm ngoài khoảng của phòng xét nghiệm không đồng nghĩa với một chẩn đoán, còn giá trị nằm trong khoảng cũng không chứng minh rằng mọi thứ đều ổn.
3. **Tìm evidence thủ công tốn thời gian và dễ mất provenance.** Người dùng có thể đọc rất nhiều bài viết nhưng khó biết claim nào dựa trên nguồn nào, mức độ chắc chắn ra sao và điều gì vẫn còn thiếu ngữ cảnh.

BioMarker Agent được đề xuất để tổ chức ba lớp thông tin này thành một flow có thể kiểm chứng:

```text
Lab report
→ structured observations
→ source-aware interpretation
→ longitudinal context
→ evidence-linked explanation
→ bounded follow-up conversation
```

Stage 01 chỉ xác định **product problem và safety envelope**. Stage này không chọn parser, model, database, queue, framework runtime hoặc topology triển khai.

---

## 2. Product statement

**[PROPOSAL]**

> BioMarker Agent là một sản phẩm hỗ trợ người dùng hiểu dữ liệu biomarker từ báo cáo xét nghiệm theo cách có cấu trúc, có provenance và có evidence; sản phẩm không được xem như một hệ thống tự động đưa ra chẩn đoán hoặc quyết định điều trị.

Một cách mô tả không dùng từ “Agent”:

> Hệ thống nhận báo cáo xét nghiệm, tổ chức các quan sát thành dữ liệu có cấu trúc, giữ lại nguồn và bối cảnh quan trọng, hỗ trợ xem thay đổi theo thời gian, tìm evidence liên quan và tạo phần giải thích có thể truy vết về dữ liệu và nguồn đã sử dụng.

---

## 3. Reference product: Biolyzer

**[SOURCE FACT — EXTERNAL REFERENCE]**

Trang `biolyzer.ai` hiện mô tả các capability:

- AI-powered biomarker analysis and chat;
- study-backed biomarker analysis;
- personalized insights;
- research-driven reports;
- relevant scientific studies;
- contextual biomarker analysis;
- actionable health insights;
- claim về xử lý riêng tư: không lưu dữ liệu, loại PII trước phân tích và xóa file sau xử lý.

Nguồn tham khảo:

- https://biolyzer.ai/
- Truy cập: 2026-09-14

**[CONSTRAINT]**

Biolyzer là **reference product**, không phải requirement authority.

Do đó:

```text
Biolyzer has capability X
≠
BioMarker must implement capability X
```

Ví dụ, việc reference product quảng bá “recommendations” không đủ để BioMarker được phép đưa recommendation mang tính chẩn đoán, điều trị hoặc thay đổi thuốc.

---

## 4. Candidate value proposition

**[PROPOSAL]**

BioMarker nên tạo giá trị quan sát được theo thứ tự:

### 4.1 Data understanding

Người dùng có thể biết:

- báo cáo chứa những biomarker nào;
- giá trị, đơn vị và khoảng tham chiếu gốc là gì;
- dữ liệu nào thiếu hoặc không chắc chắn;
- giá trị nào nằm ngoài khoảng do **chính nguồn báo cáo** cung cấp.

### 4.2 Longitudinal understanding

Khi có nhiều lần xét nghiệm:

- phân biệt các lần đo theo ngày;
- không nhầm bản ghi cũ với bản ghi mới;
- phát hiện duplicate;
- hiển thị xu hướng mà không tự biến xu hướng thành diagnosis.

### 4.3 Evidence-linked explanation

Hệ thống có thể:

- đặt câu hỏi evidence dựa trên dữ liệu đã xác minh;
- tìm nguồn phù hợp;
- tách observation khỏi hypothesis;
- liên kết claim với evidence;
- hiển thị limitations và missing context.

### 4.4 Follow-up conversation

Người dùng có thể hỏi tiếp dựa trên:

```text
verified dataset
+
analysis result
+
evidence bundle
```

thay vì model “nhớ” dữ liệu lâm sàng chỉ từ chat history.

---

## 5. Candidate users

### 5.1 Primary user

**[TEAM DECISION REQUIRED — TD-01]**

Chưa có source đủ mạnh để khóa primary user.

Các option cần product owner quyết định:

| Option | Mô tả | Ảnh hưởng |
|---|---|---|
| A | End user / patient tự xem kết quả | Tăng yêu cầu explainability, safety, consumer wording và regulatory review |
| B | Healthcare professional | Có thể hỗ trợ review chuyên môn nhưng cần workflow và evidence transparency phù hợp |
| C | Cả hai, với mode khác nhau | Scope lớn hơn; cần tách output policy và UX |
| D | Internal pilot/research only | Giảm product surface ban đầu nhưng không xóa nghĩa vụ về data safety |

**Baseline của Stage 01:** chưa khóa A/B/C/D.

---

## 6. Candidate stakeholders

| Stakeholder | Quan tâm chính |
|---|---|
| End user | Hiểu dữ liệu, hạn chế thuật ngữ khó, biết limitation |
| Healthcare professional | Nguồn evidence, provenance, missing context, không bị model che reasoning basis |
| Clinical reviewer | Safety policy, risk cases, wording, escalation |
| Product owner | Intended use, target market, value, non-goals |
| Engineering | Data quality, traceability, failure behavior |
| Security/privacy | Sensitive-data boundary, retention, access |
| Platform team | Integration contract nếu sau này dùng ai-studio |

---

## 7. Candidate input classes

Stage 01 không khóa exact format, nhưng product problem dự kiến có các lớp input:

### 7.1 Lab report

**[PROPOSAL]**

- PDF;
- image;
- structured export;
- future clinical-system adapter.

### 7.2 Context supplied by user or system

Có thể gồm:

- age range hoặc age nếu cần cho interpretation;
- sex-related reference context khi cần;
- test date;
- fasting context;
- known medications hoặc conditions nếu product owner và clinical reviewer cho phép sử dụng.

**[OPEN QUESTION]**

Context nào là required, optional hoặc prohibited chưa được quyết định.

### 7.3 Prior reports

Có thể được dùng cho longitudinal analysis nếu:

- đúng subject;
- chronology rõ;
- data quality đủ;
- permission hợp lệ.

---

## 8. Candidate outputs

**[PROPOSAL]**

Output v0 nên ưu tiên:

1. **Structured result summary** — biomarker, value, unit, source range, date, source provenance.
2. **Out-of-source-range view** — chỉ mô tả quan hệ với reference range được báo cáo.
3. **Data-quality warnings** — unit không rõ, range thiếu, date mâu thuẫn, extraction confidence thấp.
4. **Longitudinal view** — khi có dữ liệu đủ.
5. **Evidence-linked explanation** — claim có source và limitation.
6. **Questions for discussion** — câu hỏi người dùng có thể mang tới healthcare professional.
7. **Follow-up chat** — bị scope vào verified data/evidence.

---

## 9. Product invariants đề xuất

Các invariant dưới đây là **PROPOSAL** cần review:

```text
Document ≠ Diagnostic Report ≠ Observation ≠ Interpretation ≠ Clinical Claim

Reference Range ≠ Diagnosis

Outside Range ≠ Disease

Inside Range ≠ Guaranteed Normal Health

Correlation ≠ Causation

Missing Biomarker ≠ Normal Biomarker

Model Output ≠ Clinical Fact

Evidence Citation ≠ Proof of Claim

Chat History ≠ Canonical Clinical Dataset
```

Những distinction này sẽ được formalize ở Stage 02 trở đi.

---

## 10. Product boundary với ai-studio

**[REFERENCE EVIDENCE]**

ai-studio được xem là reference platform có các concern như:

- interaction surface;
- configuration;
- gateway/security boundary;
- runtime integration;
- execution provenance.

Stage 01 không cho phép platform reference quyết định ngược product semantics.

Rule:

```text
BioMarker product need
→ derive domain requirement
→ later map to platform contract
```

không phải:

```text
platform component exists
→ invent BioMarker feature to use it
```

Quan hệ triển khai chính thức giữa BioMarker và ai-studio được defer đến Stage 15.

---

## 11. Success outcome của Stage 01

Stage 01 được xem là đạt product-discovery baseline khi team có thể trả lời:

- BioMarker giải quyết pain point nào?
- Đâu là output hữu ích nhưng không vượt safety envelope?
- Đâu là capability reference, đâu là requirement?
- Ai là target user? Nếu chưa biết, decision nào đang block?
- Dữ liệu nào nhạy cảm?
- Product không được làm gì?
- Regulatory/jurisdiction question nào phải được review trước pilot thật?
- Stage 02 được phép model domain ở mức nào?

---

## 12. Open decisions quan trọng

| ID | Question | Status |
|---|---|---|
| TD-01 | Primary user là end user, HCP, cả hai hay internal pilot? | TEAM DECISION REQUIRED |
| TD-02 | Geography/jurisdiction mục tiêu là gì? | TEAM DECISION REQUIRED |
| TD-03 | Clinical owner/reviewer nào sign off safety wording? | TEAM DECISION REQUIRED |
| TD-04 | Có cho phép lifestyle/follow-up recommendation không, và ở mức nào? | TEAM DECISION REQUIRED |
| TD-05 | Có lưu report/dataset sau analysis không? | TEAM DECISION REQUIRED |
| TD-06 | Có yêu cầu tích hợp clinical system ở MVP không? | OPEN QUESTION |

---

## 13. Stage boundary

Stage 01 **không quyết định**:

- canonical data schema;
- FHIR persistence;
- LOINC mapping implementation;
- UCUM conversion implementation;
- parser/OCR;
- model provider;
- runtime framework;
- Go module;
- React app;
- database;
- worker;
- queue;
- infrastructure deployment.

Các quyết định này thuộc các Stage sau.
