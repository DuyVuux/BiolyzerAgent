# 05 — Decisions

## A. Implemented from existing source

### D-0001 — Preserve decision status

- **Status:** IMPLEMENTED FROM SOURCE
- **Context:** Mia historical documents phân biệt `PROPOSAL` với approved/canonical fact.
- **Decision:** BioMarker giữ nguyên distinction; implementation detail không tự nâng authority.
- **Impact:** mọi Stage phải label decision.
- **Source:** Mia AI context, architecture docs, AI ZIP rules.

### D-0002 — Source-first before implementation

- **Status:** IMPLEMENTED FROM SOURCE
- **Decision:** mọi Stage dùng chain:

```text
Source
→ Requirement
→ Learning
→ Design
→ Implementation
→ Verification
```

- **Source:** AI ZIP GENERATION RULES.

---

## B. Implementation choices

### D-0003 — Blind-first, reference-second workflow

- **Status:** IMPLEMENTATION CHOICE / STAGE-0 PROCESS
- **Context:** user muốn tự build từ đầu và học từ Mia skeleton.
- **Options:**
  1. copy-first;
  2. Mia-first design review;
  3. blind-first, reference-second.
- **Chosen:** 3.
- **Why:** giảm anchoring nhưng vẫn khai thác reference mạnh.
- **Trade-off:** chậm hơn copy-first; reasoning trace tốt hơn.
- **Impact:** mọi Stage có checkpoint trước khi Mia comparison.

### D-0004 — Authority lanes thay vì một precedence list tuyệt đối

- **Status:** IMPLEMENTATION CHOICE / PROCESS
- **Context:** business, safety, integration và empirical evidence không cùng loại authority.
- **Chosen:** resolve conflict theo lane trước, sau đó precedence trong lane.
- **Why:** benchmark không được ghi đè safety requirement; Mia code không ghi đè BioMarker business scope.
- **Trade-off:** process phức tạp hơn nhưng ít category error hơn.

### D-0005 — Mia skeleton is reference evidence by default

- **Status:** IMPLEMENTATION CHOICE / PROCESS
- **Decision:** current Mia implementation không tự động là BioMarker architecture authority.
- **Exception:** nếu một Mia contract được xác nhận là mandatory upstream integration contract cho BioMarker, contract đó trở thành constraint trong integration lane.
- **Why:** user muốn build độc lập trước rồi đối chiếu.

### D-0006 — Stage 0 creates no production skeleton

- **Status:** IMPLEMENTATION CHOICE
- **Chosen:** docs + templates only.
- **Why:** chưa đủ evidence cho language, DB, queue, runtime topology.
- **Trade-off:** chưa có runnable app; đây là intentional.

---

## C. Assumptions

### A-0001 — BioMarker repository can be explored independently

- **Status:** ASSUMPTION
- **Meaning:** giai đoạn học/build đầu được phép tồn tại như repo/package riêng trước khi integration decision.
- **Trigger to revisit:** authoritative requirement bắt buộc BioMarker nằm trực tiếp trong Mia repo.

### A-0002 — Mia current skeleton is later/more mature than historical Mia source package

- **Status:** ASSUMPTION SUPPORTED BY EVIDENCE
- **Evidence:** skeleton chứa concrete runtime/store/worker/durable/manifest features mà historical specs từng defer.
- **Caution:** "later/more mature" không có nghĩa mọi choice đã formally approved cho BioMarker.

---

## D. Open questions

### Q-0001

BioMarker cuối cùng là:

- standalone service;
- Mia product package;
- domain service + Mia orchestration;
- hybrid?

**Status:** OPEN QUESTION  
**Target:** Stage 15, có thể constrain sớm hơn nếu team requirement xuất hiện.

### Q-0002

BioMarker có multi-tenancy từ MVP hay reuse tenant context của Mia?

**Status:** OPEN QUESTION  
**Target:** Stage 14 / earlier if product requirement requires.

### Q-0003

Clinical data persistence/retention requirements nào áp dụng?

**Status:** OPEN QUESTION  
**Target:** Stage 1 safety framing, Stage 10 persistence.

### Q-0004

Production deployment jurisdiction/compliance path là gì?

**Status:** OPEN QUESTION  
**Target:** Stage 1 product/safety framing.

---

## E. Team decisions required

### TD-0001 — Mandatory Mia integration constraint

Team cần xác nhận khi phù hợp:

> BioMarker có bắt buộc tuân thủ một canonical Mia runtime/API/config contract cụ thể ngay từ đầu hay được phát triển như domain system rồi tích hợp sau?

Stage 0 không tự trả lời.

---

## F. Deferred decisions

- programming language;
- database;
- queue;
- DBOS;
- Redis;
- worker topology;
- manifest/attestation;
- Eino usage;
- FHIR implementation;
- LOINC terminology service;
- UCUM library;
- model/provider;
- AuthN;
- cloud/deployment.

`DEFERRED` không phải bug.
