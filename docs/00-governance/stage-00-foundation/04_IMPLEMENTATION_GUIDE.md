# 04 — Implementation Guide

## Stage 0 "implement" cái gì?

Không phải application code.

Implementation của Stage 0 là **operating method — phương pháp vận hành engineering**.

Khi một architecture question xuất hiện ở Stage sau, làm đúng thứ tự dưới đây.

---

## Flow chuẩn

### Step 1 — Open the question

Ghi câu hỏi dưới dạng problem, không dưới dạng technology.

Sai:

> Có dùng Redis không?

Đúng:

> Progress của analysis cần semantics gì khi client disconnect/reconnect, và state nào phải authoritative?

### Step 2 — Source review

Dùng `templates/SOURCE_REVIEW_TEMPLATE.md`.

Ghi:

- nguồn;
- status;
- authority lane;
- statement;
- conflict;
- gap.

### Step 3 — Form hypothesis

Dùng `11_ARCHITECTURE_HYPOTHESIS_REGISTER.md`.

Hypothesis phải có:

- proposition;
- evidence supporting;
- evidence against;
- falsification condition;
- consequence if false.

### Step 4 — Design minimum candidate

Không mở Mia implementation để copy.

Candidate phải là minimum solution giải requirement hiện biết.

### Step 5 — Experiment

Nếu câu hỏi đo được, dùng `templates/EXPERIMENT_TEMPLATE.md`.

Ví dụ:

```text
Question:
Có cần background durable execution không?

Experiment:
Kill process tại các điểm khác nhau của analysis.

Observe:
- user-visible outcome;
- state loss;
- duplicate calls;
- recovery cost.
```

### Step 6 — Preliminary conclusion

Ghi kết luận trước khi đọc Mia subsystem.

Điều này giúp phát hiện anchoring.

### Step 7 — Mia comparison

Dùng `templates/MIA_COMPARISON_TEMPLATE.md`.

Bắt buộc tách:

```text
Mia problem
Mia mechanism
Mia assumption
BioMarker problem
BioMarker assumption
fit
```

### Step 8 — Decision

Chỉ có bốn disposition mặc định:

```text
KEEP
ADAPT
REJECT
DEFER
```

Nếu decision material, tạo ADR từ `templates/ADR_TEMPLATE.md`.

### Step 9 — Implementation

Chỉ sau decision mới được tạo code/contract tương ứng.

### Step 10 — Verification

Test phải chứng minh requirement/failure mode, không chỉ coverage.

---

# Trường hợp conflict

Không dùng:

```text
latest file wins
```

Thực hiện protocol trong `09_SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md`.

---

# Trường hợp cần tiếp tục nhưng decision chưa có authority

Chỉ được:

1. chọn minimum safe local assumption nếu không block safety;
2. gắn `IMPLEMENTATION CHOICE` hoặc `ASSUMPTION`;
3. làm reversible;
4. không gọi nó là architecture chính thức;
5. ghi trigger phải revisit.

---

# Trường hợp phải dừng

Dừng decision-dependent implementation khi:

- clinical/safety authority chưa rõ;
- regulatory constraint có thể thay shape của product;
- trusted identity/tenant authority cần thiết nhưng chưa defined;
- public contract không thể honest nếu chưa có upstream decision;
- choice tạo migration cost lớn hoặc irreversible coupling.

Không dừng các phần độc lập với conflict.
