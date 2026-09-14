# 06 — Acceptance Criteria

# GATE-00 — ARCHITECTURE_DISCOVERY_FOUNDATION_READY

Stage 0 chỉ PASS khi cả hai gate dưới đây PASS.

---

## A. Artifact Gate

### Scope

- [x] Stage 0 IN SCOPE được ghi rõ.
- [x] OUT OF SCOPE được ghi rõ.
- [x] Không có application source code.
- [x] Không có fake production component.
- [x] Không có dependency mới.

### Source discipline

- [x] Có authority lanes.
- [x] Có status taxonomy.
- [x] `PROPOSAL ≠ APPROVED DECISION`.
- [x] Mia skeleton mặc định là reference evidence.
- [x] Có rule cho mandatory Mia integration contract nếu tương lai được xác nhận.

### Conflict

- [x] Có conflict protocol.
- [x] Không dùng "latest wins".
- [x] Có cách xử lý historical proposal vs implementation.
- [x] Có cách xử lý empirical evidence vs safety requirement.

### Learning

- [x] Learning Guide đi từ problem → mental model → formal method → examples → failure → Feynman.
- [x] Có đường đọc.
- [x] Có câu hỏi tự kiểm tra.
- [x] Có "nếu bỏ Stage 0 thì sao?".

### Architecture discovery

- [x] Có initial Mia Reference Ledger.
- [x] Có initial Architecture Hypothesis Register.
- [x] Hypothesis có falsification condition.
- [x] Có template experiment.
- [x] Có template ADR.
- [x] Có template Mia comparison.

### Roadmap

- [x] Có đủ Stage 0–15.
- [x] Domain precedes runtime complexity.
- [x] Durable/distributed runtime không bị pre-decided.

### Package integrity

- [x] `PACKAGE_MANIFEST.yaml` phản ánh đúng files.
- [x] `modifies: []`.
- [x] `deletes: []`.
- [x] Không có empty directory.
- [x] Không chứa secret.
- [x] Không chứa production data.

---

## B. Engineering Understanding Gate

Người học phải trả lời **không nhìn tài liệu**:

1. Tại sao BioMarker không copy Mia skeleton ngay?
2. Mia historical Sources và current skeleton khác loại evidence thế nào?
3. Tại sao không dùng một precedence list duy nhất cho business + safety + benchmark?
4. Blind-first có nghĩa là không research external alternatives không?
5. Khi nào một Mia contract có thể trở thành constraint thật của BioMarker?
6. Một architecture hypothesis tốt cần gì để falsifiable?
7. `KEEP / ADAPT / REJECT / DEFER` dùng ở bước nào?
8. Tại sao Stage 0 không tạo `src/`?
9. Nếu experiment chứng minh sync runtime đủ nhanh, điều đó có loại bỏ durable execution vĩnh viễn không?
10. Khi conflict chưa resolve, phần công việc nào vẫn được phép tiếp tục?

### PASS rule

- 8/10 câu trả lời đúng và có reasoning;
- bắt buộc đúng câu 1, 3, 5, 6;
- không được trả lời theo kiểu nhớ keyword mà không giải thích tại sao.

---

## Gate Result

### Artifact Gate

**PASS**

### Engineering Understanding Gate

**NOT EXECUTED BY AI**

Reason:

> Gate này thuộc về engineer. AI không được tự tuyên bố người học đã hiểu.

### Overall

**PASS WITH HUMAN LEARNING GATE PENDING**

Stage 1 có thể được **chuẩn bị**, nhưng trước khi coi Stage 0 hoàn tất về learning, user nên tự trả lời Feynman Gate.
