# 01 — Learning Guide: Cách học architecture bằng cách tự xây rồi đối chiếu Mia

## Bạn đang ở đâu?

BioMarker chưa có architecture được khóa. Ta có một reference cực mạnh là Mia skeleton, nhưng chính lợi thế đó tạo ra rủi ro lớn nhất: **anchoring — bị neo tư duy vào lời giải đã có**.

Nếu bắt đầu bằng cách nhìn:

```text
cmd/
internal/harness/
internal/durable/
internal/platform/compiler/
internal/platform/store/
```

rồi dựng y hệt, ta có thể tạo được một hệ thống trông chuyên nghiệp mà không trả lời được:

- vì sao cần worker;
- vì sao cần queue;
- vì sao lease chưa đủ và phải có fencing;
- vì sao config phải compile thành immutable manifest;
- vì sao tool phải đi qua durable invoker;
- vì sao Redis chỉ là live event transport chứ không phải source of truth.

Stage 0 không dạy các implementation này. Stage 0 dạy **cách tìm ra lý do khiến chúng xuất hiện**.

---

## 1. Bài toán thực tế

Giả sử BioMarker MVP nhận một file xét nghiệm.

Thiết kế đơn giản nhất có thể là:

```text
HTTP request
→ parse PDF
→ call model
→ generate report
→ return response
```

Rồi ta gặp câu hỏi:

- request chạy 2 phút thì sao?
- browser disconnect thì sao?
- process crash sau khi evidence search nhưng trước report thì sao?
- retry có chạy lại external tool không?
- config bị sửa giữa một analysis thì sao?
- report sau này có tái tạo được không?

Nếu nhìn Mia từ đầu, rất dễ trả lời ngay:

> DBOS, worker, lease, fencing, manifest pin.

Nhưng engineer chưa học được **problem pressure — áp lực của bài toán**.

Cách học Stage 0 yêu cầu:

```text
simple design
→ failure
→ evidence
→ candidate solution
→ Mia comparison
```

---

## 2. Mental model cực đơn giản

Hãy coi Mia như lời giải cuối sách bài tập.

Không được mở lời giải trước khi:

1. đọc đề;
2. tự làm;
3. chỉ ra chỗ mình chưa chắc;
4. thử ví dụ phản chứng.

Sau đó mới mở lời giải.

Nếu Mia khác ta, không kết luận ngay:

```text
Mia đúng, ta sai
```

mà hỏi:

```text
Mia đang giải requirement nào?
BioMarker có requirement đó không?
Mia đang ở maturity level nào?
Ta đang ở maturity level nào?
```

---

## 3. Định nghĩa chính xác: First-principles design

**First-principles design — thiết kế từ nguyên lý nền tảng** ở đây không có nghĩa bỏ qua mọi kiến thức có sẵn.

Nó nghĩa là:

> Bắt đầu từ requirement, invariant, workload, failure mode và measurable evidence; không bắt đầu từ component name hoặc technology.

Ví dụ:

Sai:

```text
Ta cần Redis vì hệ thống realtime.
```

Đúng hơn:

```text
Requirement:
User cần xem progress của một analysis đang chạy.

Questions:
- cần durable event history hay chỉ live update?
- disconnect/reconnect semantics?
- event loss có chấp nhận không?
- authoritative progress state nằm đâu?

Candidate:
SSE direct from process.

Only when evidence shows a problem:
evaluate broker / Redis Streams / alternatives.
```

---

## 4. Blind-first, reference-second

Đây là workflow chính thức của BioMarker.

### Blind-first

"Blind" chỉ có nghĩa **chưa dùng Mia implementation làm lời giải**.

Ta vẫn phải:

- đọc BioMarker requirements;
- đọc chuẩn relevant;
- research alternatives;
- đo;
- prototype;
- threat model.

### Reference-second

Sau khi có preliminary candidate:

1. tìm subsystem tương ứng trong Mia;
2. giải thích subsystem đó đang giải vấn đề gì;
3. tìm failure mode mà Mia xử lý;
4. kiểm tra BioMarker có cùng failure mode hay không;
5. chọn:
   - `KEEP`
   - `ADAPT`
   - `REJECT`
   - `DEFER`

---

## 5. Source không chỉ có một loại authority

Đây là điểm dễ sai nhất.

Một benchmark không thể ghi đè một regulatory requirement.

Một Mia implementation không thể ghi đè BioMarker business requirement.

Một clinical standard không quyết định queue topology.

Do đó Stage 0 dùng **authority lanes — các làn authority** thay vì một bảng xếp hạng duy nhất.

Các lane chính:

1. Product / Business
2. Clinical / Safety / Regulatory
3. Platform Integration
4. Semantic / Domain Specification
5. Machine Contract
6. Empirical Evidence
7. Reference Architecture
8. Engineering Inference

Chi tiết tại `09_SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md`.

---

## 6. Mia Sources và Mia skeleton không cùng một loại bằng chứng

### Mia historical Sources

Nhiều tài liệu được viết khi:

```text
GREENFIELD
SOURCE CODE ≈ 0
```

và cố ý giữ:

```text
PROPOSAL ≠ APPROVED DECISION
```

Các topic như distributed worker scheduler, queue topology, long-running job platform, advanced retry orchestration từng được deferred.

### Mia skeleton

Skeleton hiện tại mô tả implementation trưởng thành hơn:

- PostgreSQL source of truth;
- DBOS;
- worker;
- lease/fencing;
- signed manifest;
- durable invokers;
- Redis Streams;
- registry;
- Eino adapter;
- hardening tests.

Do đó:

```text
historical spec
= semantic/history evidence

current skeleton
= implementation/reference evidence
```

Không cái nào tự động là BioMarker requirement.

---

## 7. Ví dụ xuyên suốt: một BioMarker analysis

Ta dùng scenario này xuyên các Stage:

```text
User A
→ upload Lab Report R1
→ system extracts Observations
→ normalize
→ retrieve evidence
→ synthesize Analysis A1
→ produce Report P1
→ user asks follow-up
```

Ở Stage sau ta sẽ làm nó khó dần:

```text
process crash
provider timeout
duplicate retry
same file uploaded twice
new lab result later
wrong unit
ambiguous analyte
cross-user access
cross-tenant access
config change during analysis
```

Mỗi complexity phải xuất hiện vì scenario hoặc requirement, không phải vì framework có feature đó.

---

## 8. Những nhầm lẫn thường gặp

### "Mia có rồi, reuse luôn cho nhanh"

Reuse code và reuse decision là hai việc khác nhau.

Có thể reuse một adapter sau khi đã chấp nhận contract, nhưng vẫn phải hiểu vì sao contract tồn tại.

### "Build lại từ đầu nghĩa là không dùng Mia"

Sai.

Mục tiêu là **independent reasoning**, không phải anti-reuse.

### "Experiment thắng thì requirement đổi"

Sai.

Experiment thay đổi hiểu biết empirical, không tự thay business/safety authority.

### "Skeleton là code nên authority hơn Markdown"

Sai.

Implementation chứng minh "đang làm thế nào", không tự chứng minh "nên làm thế nào" cho project khác.

### "PROPOSED rất chi tiết nên coi như approved"

Sai.

Độ dài tài liệu không thay đổi trạng thái authority.

---

## 9. Nếu bỏ Stage 0 thì sao?

Ta có ba failure mode lớn:

### Failure A — Architecture cargo cult

Copy:

```text
DBOS + Redis + manifest + fencing
```

mà chưa có requirement.

### Failure B — Historical document trap

Bám một proposal cũ dù implementation đã khám phá được vấn đề mới.

### Failure C — AI silent decision

AI gặp gap và tự chọn technology để tiếp tục code, sau đó viết tài liệu hợp thức hóa.

File `AI ZIP GENERATION RULES.md` cấm chính hành vi C.

---

## 10. Mapping sang artifact

| Concept | Artifact |
|---|---|
| Authority lanes | `09_SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md` |
| Mia as reference | `10_MIA_REFERENCE_LEDGER.md` |
| Unknowns to test | `11_ARCHITECTURE_HYPOTHESIS_REGISTER.md` |
| Stage sequencing | `12_MASTER_ROADMAP_16_STAGES.md` |
| Decision recording | `05_DECISIONS.md`, `ADR_TEMPLATE.md` |
| Experiment discipline | `EXPERIMENT_TEMPLATE.md` |
| Verification | `06_ACCEPTANCE_CRITERIA.md`, `07_VERIFICATION_GUIDE.md` |

---

# Feynman Gate

## Level 1 — Giải thích cực đơn giản

Không nhìn phần trên:

> Tại sao chúng ta không copy Mia skeleton cho BioMarker dù Mia được làm rất mạnh?

## Level 2 — Tự giải thích

Giải thích bằng ngôn ngữ của bạn:

> `Mia implementation` khác `BioMarker requirement` ở đâu?

## Level 3 — Tìm lỗ hổng

Một experiment cho thấy synchronous processing đạt latency tốt.

> Điều đó có chứng minh BioMarker không bao giờ cần durable execution không? Vì sao?

## Level 4 — Áp dụng

Trong package này:

> File nào lưu một giả thuyết như "MVP chưa cần queue"?

## Level 5 — Phá mô hình

Nếu từ Stage 1 AI thấy Mia có PostgreSQL + DBOS và tự thêm chúng vào BioMarker repository mà không có requirement:

- rule nào bị vi phạm?
- ta mất cơ hội học gì?
- decision đó phải được sửa thế nào?

---

## Gợi ý

Tự trả lời trước khi xem phần dưới.

## Đáp án tham khảo ngắn

1. Mia là reference solution cho một tập requirement/maturity cụ thể; BioMarker phải chứng minh cùng pressure trước khi kế thừa complexity.
2. Implementation là evidence của một cách giải; requirement là điều hệ thống phải đạt.
3. Không. Nó chỉ hỗ trợ hypothesis trong workload đã đo; requirement tương lai hoặc failure mode khác có thể thay đổi kết luận.
4. `11_ARCHITECTURE_HYPOTHESIS_REGISTER.md`.
5. Vi phạm source discipline, minimum sufficient implementation và no-silent-architecture-decision; phải rollback thành hypothesis/option và đánh giá bằng evidence.
