# BioMarker Agent — Product Context

> **Status:** APPROVED BASELINE v1.0  
> **Approved on:** 2026-09-14  
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

**[APPROVED PRODUCT CLAIM]**

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
 
### 5.1 Primary User — TD-01

**Status:** APPROVED PRODUCT DIRECTION

#### Quyết định

Primary User của BioMarker Agent trong phạm vi MVP là:

> **Healthcare Professional — trước mắt là bác sĩ sử dụng kết quả xét nghiệm trong quy trình chuyên môn.**

BioMarker Agent ở giai đoạn MVP **không được thiết kế như một sản phẩm self-service dành trực tiếp cho bệnh nhân/người dùng phổ thông**.

#### Cơ sở quyết định

Roadmap sản phẩm hiện tại xác định rõ chuỗi triển khai:

* **01/10/2026:** bắt đầu triển khai;
* **30/10/2026:** demo tính năng AI tóm tắt kết quả, gắn cờ bất thường và giải thích ngắn gọn **cho bác sĩ**;
* **30/11/2026:** UAT với **bác sĩ** cho use case AI đọc kết quả xét nghiệm nước tiểu;
* **31/12/2026:** go-live cho **Khoa Nội tổng hợp tại một bệnh viện**;
* hướng nâng cấp tiếp theo là phân tích xu hướng qua nhiều lần xét nghiệm để hỗ trợ tầm soát và cảnh báo sớm nguy cơ bệnh.

Từ roadmap trên, actor sử dụng trực tiếp hệ thống trong MVP là bác sĩ.

#### Phân biệt Primary User và Rollout Strategy

`Internal Pilot` không được xem là một loại Primary User.

Hai khái niệm phải được tách:

```text
Primary User
= Healthcare Professional / Physician

Initial Rollout Strategy
= Internal Clinical Pilot
  → Physician UAT
  → Limited Go-live tại một khoa / một bệnh viện
```

Nói cách khác, **bác sĩ là người sử dụng sản phẩm**, còn **internal pilot là cách sản phẩm được triển khai và kiểm chứng trước khi mở rộng**.

#### Product positioning cho MVP

BioMarker Agent được định hướng như một hệ thống **physician-facing clinical information support tool** hỗ trợ bác sĩ:

```text
Lab result
→ structured understanding
→ abnormal-result highlighting
→ concise explanation
→ evidence/context support
→ longitudinal analysis trong các phiên bản sau
```

Hệ thống hỗ trợ việc đọc và tổng hợp thông tin; output của AI **không tự trở thành clinical authority và không thay thế phán đoán chuyên môn của bác sĩ**.

Việc có được phân loại chính thức là Clinical Decision Support software hoặc thuộc một regulatory category cụ thể hay không **không được quyết định chỉ từ TD-01**. Việc đó còn phụ thuộc intended use, chức năng thực tế, mức độ recommendation/automation và jurisdiction mục tiêu.

#### Scope consequence

Với quyết định này:

**IN SCOPE cho MVP:**

* tóm tắt kết quả xét nghiệm;
* làm nổi bật/gắn cờ các kết quả bất thường dựa trên dữ liệu nguồn và rule được xác định;
* giải thích ngắn gọn cho bác sĩ;
* cung cấp provenance và context cần thiết để bác sĩ kiểm tra;
* hỗ trợ UAT trên use case xét nghiệm nước tiểu;
* chuẩn bị architecture để sau này phân tích xu hướng nhiều lần xét nghiệm.

**KHÔNG suy ra từ TD-01:**

* AI được quyền tự chẩn đoán;
* AI được quyền quyết định điều trị;
* AI được quyền tự đưa ra cảnh báo lâm sàng có tính authority;
* bác sĩ bắt buộc phải làm theo recommendation của AI;
* sản phẩm đã được regulatory-classified.

#### Future users

Patient-facing experience có thể được xem xét trong một phase sản phẩm khác, nhưng hiện tại:

> **Patient / Individual User = OUT OF CURRENT MVP SCOPE**

Nếu sau này mở sản phẩm trực tiếp cho bệnh nhân, intended use, safety envelope, UX, evidence presentation và regulatory assessment phải được review lại; không được mặc định tái sử dụng nguyên policy dành cho bác sĩ.

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

## 12. Approved product decisions

| ID | Vấn đề / Quyết định | Lựa chọn chính thức | Trạng thái |
|---|---|---|---|
| **TD-01** | Primary User | **Option B — Healthcare Professional / Physician** (Bác sĩ sử dụng trong quy trình chuyên môn) | **APPROVED (2026-09-14)** |
| **TD-01B** | Initial Rollout Strategy | **Internal Clinical Pilot → Physician UAT (30/11: Nước tiểu) → Limited Go-live Khoa Nội tổng hợp (31/12)** | **APPROVED (2026-09-14)** |
| **TD-02** | Geography & Jurisdiction | **Vinmec - Việt Nam** (Tuân thủ Luật Khám bệnh, chữa bệnh 2023 & quy chuẩn BYT) | **APPROVED (2026-09-14)** |
| **TD-03** | Clinical Owner / Sign-off | **Vinmec Clinical Reviewer / Laboratory Specialist** phụ trách duyệt safety wording | **APPROVED (2026-09-14)** |
| **TD-04** | Follow-up & Recommendation | **Capability Classes:** ALLOWED (Level A Data, Level B Evidence); CONTROLLED (Abnormal flags + physician summary - rules-based); RESTRICTED (Recommendations - out of MVP); PROHIBITED (Diagnosis/Treatment) | **APPROVED (2026-09-14)** |
| **TD-05** | Raw PDF Retention Policy | **Semantic Policy (RFC-2119):** Not an authoritative record store; source files remain in hospital system; BioMarker stores only derived observations + provenance; Dev uses synthetic/ephemeral; Physical DB/Crypto deferred to Stage 10/14/15 | **APPROVED (2026-09-14)** |
| **TD-06** | Clinical System Integration | Defer đến Stage 10/15 khi pipeline cốt lõi hoàn tất | **DEFERRED (Stage 15)** |

### 12.1 Chi tiết quyết định TD-04 — Capability Classes & Clinical Boundary

- **ALLOWED (Level A & Level B):** Trích xuất, chuẩn hóa, bảo toàn giá trị/đơn vị/ngưỡng tham chiếu gốc; giải thích định nghĩa y khoa và trích dẫn bằng chứng y văn có căn cứ (claim grounding).
- **CONTROLLED (Clinician Interpretation):** Năng lực gắn cờ bất thường (abnormal flags) và tóm tắt súc tích báo cáo cho bác sĩ. **Ranh giới:** Bắt buộc tuân theo quy tắc xác định (deterministic rules), phục vụ workflow của bác sĩ (Physician View), bác sĩ toàn quyền thẩm định độc lập.
- **RESTRICTED (Person-Specific Recommendation):** Khuyến nghị can thiệp lối sống, chỉ định thêm xét nghiệm chuyên sâu $\rightarrow$ **OUT OF MVP SCOPE**.
- **PROHIBITED (Autonomous Diagnosis & Treatment):** Chẩn đoán bệnh, kê đơn thuốc, thay đổi liều, quyết định điều trị, phân loại cấp cứu $\rightarrow$ **TUYỆT ĐỐI CẤM ở mọi giai đoạn**.

### 12.2 Chi tiết quyết định TD-05 — Semantic Data Retention Policy (RFC-2119)

1. **Authoritative Record Boundary:** BioMarker Agent **SHALL NOT** đóng vai trò là kho lưu trữ hồ sơ bệnh án pháp lý (authoritative clinical document repository).
2. **Document Custody:** BioMarker Agent **SHALL NOT** sở hữu hay nhân bản tài liệu gốc (raw reports). Toàn bộ tệp báo cáo gốc **SHALL** thuộc quyền quản lý của hệ thống quản lý tài liệu lâm sàng được Vinmec phê duyệt.
3. **Retained Data Scope:** BioMarker Agent **SHALL** chỉ lưu trữ dữ liệu quan sát phái sinh có cấu trúc tối thiểu (derived structured observations) và thông tin nguồn gốc tối thiểu (provenance metadata) phục vụ đối chiếu xu hướng và y văn.
4. **Development Lifecycle:** Trong Stage 01–08, hệ thống **SHALL** tuân thủ nguyên tắc Zero-PHI (chỉ dùng synthetic fixtures). Tệp upload thử nghiệm cục bộ **SHALL** chỉ tồn tại tạm thời (ephemeral) trong `var/uploads/` và **SHALL** bị xóa ngay sau khi xử lý.
5. **Deferred Technical Scope:** Các quyết định kỹ thuật về cơ sở dữ liệu vật lý, định dạng lưu trữ (relational/JSONB), thuật toán mã hóa tại chỗ và giao thức tích hợp hệ thống bệnh viện **SHALL BE DEFERRED** đến Stage 10, Stage 14 và Stage 15.

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
