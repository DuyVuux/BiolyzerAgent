# 02 — Stage 0 Task Breakdown

## Mục tiêu đo được

Sau Stage 0, người học phải có thể:

1. phân loại một source theo authority lane và status;
2. phân biệt requirement, proposal, implementation evidence và empirical evidence;
3. xử lý một conflict Mia Source ↔ Mia skeleton mà không chọn bừa;
4. viết một architecture hypothesis có falsification condition;
5. đối chiếu một Mia subsystem theo `problem → mechanism → assumption → fit`;
6. giải thích roadmap 16 Stage và lý do runtime complexity xuất hiện muộn;
7. biết decision nào Stage 0 cố ý chưa đưa ra.

---

## Task 0.1 — Inventory sources

### Input

Mia source package, Mia skeleton, ZIP rules, BioMarker project context hiện có.

### Action

Phân loại source theo:

```text
scope
status
authority lane
time/maturity
canonical vs derived
reference-only vs governing
```

### Output

`09_SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md`

---

## Task 0.2 — Define conflict protocol

Phải xử lý ít nhất các case:

- historical proposal vs later implementation;
- semantic spec vs machine-readable schema;
- BioMarker requirement vs Mia design;
- safety constraint vs performance experiment;
- accepted integration contract vs local implementation preference.

Output nằm trong `09_SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md`.

---

## Task 0.3 — Initialize Mia Reference Ledger

Không liệt kê file đơn thuần.

Mỗi entry phải trả lời:

```text
What problem does Mia appear to solve?
What mechanism is used?
What assumptions make it necessary?
What BioMarker evidence would justify adopting it?
Current BioMarker decision?
```

Output:

`10_MIA_REFERENCE_LEDGER.md`

---

## Task 0.4 — Initialize Architecture Hypothesis Register

Initial hypotheses phải là falsifiable — có thể bị evidence bác bỏ.

Ví dụ đúng:

> H-0001: Stage 9 MVP có thể chạy single-process mà chưa cần durable queue. Bị bác bỏ nếu confirmed workload yêu cầu execution sống qua request/process lifetime hoặc fault-injection cho thấy unacceptable loss.

Ví dụ sai:

> H-0001: PostgreSQL is best.

Output:

`11_ARCHITECTURE_HYPOTHESIS_REGISTER.md`

---

## Task 0.5 — Freeze process, not architecture

Stage 0 được phép freeze:

- source labels;
- conflict procedure;
- comparison workflow;
- experiment/ADR format;
- gate format.

Stage 0 không được freeze:

- runtime topology;
- DB;
- queue;
- language;
- framework;
- AuthN implementation;
- tenancy semantics;
- clinical domain schema.

---

## Task 0.6 — Define 16-stage roadmap

Roadmap phải giữ dependency:

```text
problem/domain
before
runtime/infrastructure
```

Output:

`12_MASTER_ROADMAP_16_STAGES.md`

---

## Task 0.7 — Create Stage 1 handoff

Stage 1 chỉ bắt đầu khi Stage 0 Gate PASS.

Output:

`13_STAGE_01_HANDOFF.md`

---

# Out of scope tasks

Không thực hiện trong Stage 0:

- generate app scaffold;
- `go mod init`;
- Docker Compose;
- DB migrations;
- FHIR implementation;
- parser proof-of-concept;
- LLM prompt;
- Eino graph;
- external provider call;
- tenant/security code.

---

# Observable value của Stage 0

Stage 0 tạo một behavior có thể quan sát:

> Khi gặp một architecture question mới, engineer có thể phân loại nguồn, ghi hypothesis, research/experiment, đối chiếu Mia và record decision mà không cần AI tự bịa architecture để tiếp tục.

Đây là capability quản trị engineering, không phải application capability.
