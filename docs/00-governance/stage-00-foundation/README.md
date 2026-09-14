# Stage 0 — Architecture Discovery Foundation

**Package:** `stage-00-architecture-discovery-foundation-v0.1`  
**Status:** CANDIDATE / LEARNING & DESIGN FOUNDATION  
**Project:** BioMarker Agent  
**Stage:** 0 of 15 (16 stages total)

## Stage này làm gì?

Stage 0 không xây BioMarker Agent, không chọn database, không chọn queue, không dựng worker và không tạo runtime production.

Stage này tạo **cơ chế làm việc** để các Stage sau có thể tự thiết kế BioMarker từ first principles — nguyên lý nền tảng — rồi mới đối chiếu với Mia như một reference architecture mạnh.

Mục tiêu là tránh hai sai lầm đối lập:

1. **Copy Mia** rồi đổi tên thành BioMarker.
2. **Cố tình khác Mia** dù Mia đã giải đúng một vấn đề giống hệt.

Quy trình khóa cho các Stage sau:

```text
BioMarker problem
        ↓
Source review
        ↓
First-principles reasoning
        ↓
Hypothesis
        ↓
Experiment / prototype
        ↓
Preliminary candidate
        ↓
Mia comparison
        ↓
KEEP / ADAPT / REJECT / DEFER
        ↓
Decision / ADR
        ↓
Implementation
        ↓
Verification
```

## Tại sao Stage 0 cần tồn tại?

Mia Sources lịch sử và skeleton hiện tại mô tả các mức trưởng thành khác nhau:

- các tài liệu ban đầu mô tả một project greenfield, nhiều nội dung vẫn là `PROPOSED`, nhiều runtime topic còn deferred;
- skeleton Mia hiện tại đã có PostgreSQL authoritative state, DBOS, leases/fencing, immutable signed manifests, durable invokers, Eino adapter, Redis SSE và nhiều hardening tests.

Vì vậy BioMarker không thể dùng quy tắc đơn giản:

```text
newest implementation always wins
```

và cũng không thể dùng:

```text
oldest source always wins
```

Stage 0 thiết lập cách phân loại nguồn và giải conflict theo đúng loại authority.

## Input

Các nguồn chính dùng trong Stage 0:

- `AI ZIP GENERATION RULES.md`
- `PROJECT_SKELETON.md`
- `00_PROJECT_CONTEXT.md`
- `01_SYSTEM_ARCHITECTURE.md`
- `02_AGENT_CONFIGURATION_SPEC.md`
- `03_SECURITY_TENANCY_AUTHORIZATION.md`
- `04_CHAT_SESSION_SPEC.md`
- `05_RUNTIME_INTEGRATION.md`
- `AI_CONTEXT.md`
- `THREAT_MODEL.md`
- `CROSS_TENANT_TEST_MATRIX.md`

Biolyzer và các chuẩn external chưa trở thành authority của Stage 0; chúng chỉ được đưa vào Source Classification để dùng ở các Stage domain sau.

## Output

Stage này tạo:

- Source Authority & Conflict Protocol;
- Mia Reference Ledger;
- Architecture Hypothesis Register;
- Master Roadmap 16 Stage;
- các template chuẩn cho ADR, experiment, source review và Mia comparison;
- Stage 1 handoff;
- gate để kiểm tra **Engineering Understanding PASS** riêng với **Artifact PASS**.

## IN SCOPE

- source discipline cho BioMarker;
- conflict resolution giữa BioMarker Sources, Mia Sources và Mia skeleton;
- blind-first, reference-second workflow;
- registry cho hypothesis;
- registry cho Mia references;
- decision taxonomy;
- Stage 0 gate;
- 16-stage roadmap;
- Stage 1 entry conditions.

## OUT OF SCOPE

Stage 0 **không**:

- chọn Go/Python/Rust cho BioMarker implementation;
- chọn PostgreSQL;
- chọn DBOS/Temporal/queue;
- dựng Eino graph;
- chọn FHIR/LOINC/UCUM implementation strategy;
- thiết kế lab parser;
- thiết kế clinical safety policy chi tiết;
- viết API;
- tạo authentication;
- tạo tenant model;
- tạo production repo skeleton;
- tích hợp trực tiếp BioMarker vào Mia.

## Integration dependency

- Mia artifacts là reference evidence.
- Nếu tương lai có authoritative requirement rằng BioMarker phải chạy trong Mia, accepted Mia public/integration contracts có thể trở thành upstream constraint. Quyết định đó **chưa được Stage 0 tự giả định**.

## Đường đọc

1. `docs/01_LEARNING_GUIDE.md`
2. `docs/09_SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md`
3. `docs/10_MIA_REFERENCE_LEDGER.md`
4. `docs/11_ARCHITECTURE_HYPOTHESIS_REGISTER.md`
5. `docs/12_MASTER_ROADMAP_16_STAGES.md`
6. `docs/02_TASK_BREAKDOWN.md`
7. `docs/03_DESIGN_MAPPING.md`
8. `docs/05_DECISIONS.md`
9. `docs/06_ACCEPTANCE_CRITERIA.md`
10. `docs/07_VERIFICATION_GUIDE.md`
11. `docs/13_STAGE_01_HANDOFF.md`

## Gate

**GATE-00 — ARCHITECTURE_DISCOVERY_FOUNDATION_READY**

Chỉ PASS khi:

- source authority lanes được hiểu;
- conflict protocol có thể áp dụng;
- người học giải thích được vì sao Mia skeleton không phải automatic authority;
- hypothesis register có initial hypotheses nhưng không khóa implementation;
- Mia Reference Ledger phân biệt `problem` và `solution`;
- roadmap 16 Stage không kéo runtime complexity về sớm;
- không có architecture decision production nào bị hardcode;
- Stage 1 có input rõ ràng.

Xem chi tiết tại `docs/06_ACCEPTANCE_CRITERIA.md`.

## Repository hiện SẼ có gì nếu integrate package này?

Chỉ có tài liệu/process foundation tương đương các file trong package này.

## Repository hiện CHƯA có gì?

Chưa có BioMarker application code, runtime, DB, parser, API, UI, authentication, queue, worker hay clinical logic.

Đó là chủ đích, không phải thiếu sót.
