# 07 — Verification Guide

Stage 0 không có application tests. Verification tập trung vào:

1. package integrity;
2. source/decision consistency;
3. scenario reasoning;
4. human learning gate.

---

# 1. File-tree verification

Expected:

```text
stage-00-architecture-discovery-foundation-v0.1/
├── README.md
├── PACKAGE_MANIFEST.yaml
├── docs/
│   ├── 01_LEARNING_GUIDE.md
│   ├── 02_TASK_BREAKDOWN.md
│   ├── 03_DESIGN_MAPPING.md
│   ├── 04_IMPLEMENTATION_GUIDE.md
│   ├── 05_DECISIONS.md
│   ├── 06_ACCEPTANCE_CRITERIA.md
│   ├── 07_VERIFICATION_GUIDE.md
│   ├── 08_INTEGRATION_GUIDE.md
│   ├── 09_SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md
│   ├── 10_MIA_REFERENCE_LEDGER.md
│   ├── 11_ARCHITECTURE_HYPOTHESIS_REGISTER.md
│   ├── 12_MASTER_ROADMAP_16_STAGES.md
│   └── 13_STAGE_01_HANDOFF.md
└── templates/
    ├── ADR_TEMPLATE.md
    ├── EXPERIMENT_TEMPLATE.md
    ├── MIA_COMPARISON_TEMPLATE.md
    └── SOURCE_REVIEW_TEMPLATE.md
```

Không được có:

```text
src/
tests/
cmd/
internal/
docker-compose.yml
go.mod
package.json
```

---

# 2. Scenario verification

## V-01 — Detailed proposal

Một 80-page spec ghi `PROPOSED`, còn một implementation nhỏ đã chạy.

Question:

> Có được gọi proposal là approved vì code đã tồn tại không?

Expected:

```text
NO
```

Implementation là evidence; decision status phải được xác nhận độc lập.

---

## V-02 — Historical spec vs current Mia skeleton

Historical spec defer distributed queue.

Current skeleton có DBOS.

Expected reasoning:

1. đây có thể là evidence-state/maturity change;
2. không kết luận historical doc "sai";
3. không import DBOS vào BioMarker;
4. ghi Mia mechanism vào Reference Ledger;
5. tạo BioMarker hypothesis/experiment khi runtime stage đến.

---

## V-03 — Benchmark vs safety

Benchmark cho thấy bỏ validation step giảm latency 40%.

Expected:

> Benchmark không có authority ghi đè safety requirement. Optimization phải tìm option khác hoặc safety authority phải formally revise requirement.

---

## V-04 — Mia integration constraint

Team xác nhận BioMarker phải gọi một canonical Mia Runtime API.

Expected:

> Public/integration contract trở thành upstream constraint. Internal implementation của Mia phía sau contract vẫn không tự trở thành BioMarker implementation requirement.

---

## V-05 — Unknown database

Stage 2 cần lưu sample data cho experiment nhưng DB production chưa quyết định.

Expected:

> dùng fixture/file/in-memory nếu đủ; gắn development-only choice; không tự chọn PostgreSQL chỉ vì Mia dùng PostgreSQL.

---

# 3. Decision verification

Đọc `05_DECISIONS.md` và kiểm tra:

- mỗi implementation choice có status;
- assumption có trigger revisit;
- open question chưa có answer giả;
- deferred technology không xuất hiện như chosen stack.

---

# 4. Human Feynman verification

Thực hiện câu hỏi trong:

`06_ACCEPTANCE_CRITERIA.md`

Kết quả dùng:

```text
PASS
FAIL
NOT EXECUTED
```

Không dùng:

```text
probably understood
```

---

# 5. Expected final status

Artifact verification:

**PASS**

Human learning verification:

**NOT EXECUTED** cho đến khi engineer tự trả lời.

Do đó package status:

**PASS WITH HUMAN LEARNING GATE PENDING**
