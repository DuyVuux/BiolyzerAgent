# BioMarker Agent — Users, Use Cases & Non-Goals

> **Status:** APPROVED BASELINE v1.0  
> **Approved on:** 2026-09-14  
> **Stage:** 01  
> **Purpose:** Tách “người dùng muốn đạt outcome gì” khỏi “hệ thống sẽ dùng công nghệ gì”.

---

## 1. User model chính thức

**[APPROVED DECISION — TD-01 & TD-01B]**

- **Primary User:** **Individual User / Patient** (Bệnh nhân / Người dùng cá nhân theo dõi kết quả xét nghiệm của mình trong giai đoạn **Internal Pilot** tại Vinmec).
- **Secondary Actor:** **Healthcare Professional / Clinician** (Bác sĩ điều trị - đối tượng mà người bệnh được khuyến khích trao đổi cùng với bản tóm tắt và câu hỏi do hệ thống gợi ý).
- **Clinical Reviewer:** Bác sĩ/Chuyên gia xét nghiệm phụ trách thẩm định an toàn nội dung.
- **External Clinical System:** Hệ thống LIS/EMR Vinmec trong các giai đoạn tích hợp sau.

---

## 2. Scenario xuyên suốt

Giả sử một user có hai báo cáo xét nghiệm ở hai thời điểm.

Họ muốn biết:

```text
Báo cáo có gì?
Giá trị nào khác khoảng được lab report?
Thay đổi theo thời gian ra sao?
Có evidence nào liên quan?
Điều gì hệ thống chưa biết?
Tôi nên hỏi healthcare professional câu gì?
```

Đó là scenario xuyên suốt cho Stage 01–08.

---

## 3. Use case register

### UC-01 — Submit a lab report

**Goal:** đưa report vào hệ thống để bắt đầu analysis.

**Input candidate:**

- PDF/image/structured data;
- metadata tối thiểu nếu cần.

**Outcome:**

- report được tiếp nhận;
- processing status rõ;
- không mất source provenance.

**Stage implementation:** Stage 03 trở đi.

---

### UC-02 — Verify extracted observations

**Goal:** user/reviewer có thể kiểm tra dữ liệu được hệ thống đọc ra.

**Why:** một lỗi số học hoặc unit có thể làm toàn bộ analysis sai.

**Outcome candidate:**

- observation hiển thị kèm source location;
- low-confidence/ambiguous item không bị silent accept;
- correction có provenance.

**Status:** PROPOSAL.

---

### UC-03 — Review values against source range

**Goal:** user thấy relation giữa measured value và reference interval được report.

**Must preserve:**

- value;
- unit;
- source range;
- date;
- source report.

**Must not imply:**

```text
outside range = diagnosis
inside range = guaranteed health
```

---

### UC-04 — Review change over time

**Goal:** so sánh biomarker across validated dates.

**Conditions:**

- same subject;
- comparable measurement;
- date known;
- unit normalization safe;
- duplicate handling explicit.

Stage 05 sẽ formalize.

---

### UC-05 — Read evidence-linked explanation

**Goal:** user hiểu evidence có liên quan đến observation/pattern.

**Outcome candidate:**

```text
claim
→ supporting source(s)
→ evidence type
→ limitations
→ known/unknown context
```

Stage 06 formalize evidence bundle.

---

### UC-06 — Ask follow-up questions

**Goal:** hỏi tiếp mà không làm mất provenance.

Follow-up phải scope vào:

- verified dataset version;
- analysis result;
- evidence identity/snapshot khi có;
- current safety policy.

Không được dựa duy nhất vào conversational memory.

---

### UC-07 — Identify missing context

**Goal:** hệ thống nêu rõ thông tin còn thiếu làm interpretation yếu đi.

Ví dụ generic:

- test date missing;
- unit missing;
- reference interval missing;
- specimen unknown;
- relevant contextual input absent.

Outcome:

```text
unknown remains unknown
```

---

### UC-08 — Prepare questions for professional discussion

**Goal:** giúp user chuẩn bị câu hỏi có cấu trúc.

Ví dụ form:

```text
"Chỉ số X thay đổi qua hai lần đo. Có context hoặc follow-up nào cần xem thêm không?"
```

Không biến thành automated treatment direction.

---

## 4. Candidate HCP use cases

Chỉ active nếu TD-01 xác nhận healthcare professional là intended user.

### HCP-01 — Review extracted dataset

Healthcare professional kiểm tra structured observations + provenance.

### HCP-02 — Review evidence basis

Healthcare professional có thể thấy:

- inputs;
- source;
- logic/basis ở mức phù hợp;
- limitations;
- missing data.

### HCP-03 — Compare longitudinal data

Sử dụng timeline như một support view, không thay thế judgment.

---

## 5. Non-goals — MVP baseline

### 5.1 Diagnosis

Không xây một output:

```text
patient has disease X
```

như autonomous final decision.

### 5.2 Treatment direction

Không:

- prescribe;
- stop/start/change medication;
- select treatment;
- replace healthcare professional judgment.

### 5.3 Emergency / real-time triage

Không positioning như urgent monitoring hoặc real-time care decision engine.

### 5.4 Full EHR

Không xây:

- complete patient record;
- scheduling;
- billing;
- order entry;
- hospital workflow platform.

### 5.5 Full laboratory information system

Không thay thế LIS.

### 5.6 Generic symptom checker

BioMarker scope bắt đầu từ biomarker/lab data, không mở rộng thành symptom diagnosis product ở Stage 01.

### 5.7 Generic agent authoring platform

Không rebuild ai-studio Studio/Canvas/registry trong BioMarker MVP.

### 5.8 Autonomous external actions

Không tự:

- order test;
- message clinician;
- purchase product;
- change appointment;
- trigger treatment workflow.

Nếu tương lai cần, phải có stage/ADR riêng.

---

## 6. Deferred capabilities

| Capability | Status | Revisit |
|---|---|---|
| Structured lab-system integration | DEFERRED | Stage 14–15 |
| HCP-only view | OPEN | After TD-01 |
| Patient-facing view | OPEN | After TD-01 |
| Report export/share | DEFERRED | Product decision |
| Persistent personal health timeline | OPEN | Stage 05/10 |
| Recommendation engine | RESTRICTED | Clinical/regulatory review |
| Generic Studio authoring | DEFERRED | Stage 15 |
| Multi-agent orchestration | DEFERRED | Need proven use case |

---

## 7. Acceptance questions

Một use case chỉ được chuyển thành requirement khi trả lời được:

1. Ai là actor?
2. Actor đang cố đạt outcome gì?
3. Input nào được phép?
4. Output nào được phép?
5. Safety risk là gì?
6. Data nào nhạy cảm?
7. Human review ở đâu?
8. Failure được hiển thị thế nào?
9. Capability này có thật sự cần AI không?
10. Nó thuộc Stage nào?

---

## 8. Feynman check cho product team

Không nhìn tài liệu, hãy giải thích:

> Nếu bỏ toàn bộ chữ “AI” khỏi pitch, BioMarker còn giá trị gì?

Một câu trả lời tốt phải nói được về:

```text
structured data
provenance
longitudinal context
evidence
limitations
```

chứ không chỉ:

```text
chatbot phân tích xét nghiệm
```
