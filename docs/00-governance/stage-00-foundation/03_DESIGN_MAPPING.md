# 03 — Design Mapping

Stage 0 không có application code. Vì vậy mapping của Stage này là:

```text
Source / Requirement
→ Working Protocol
→ Artifact
→ Verification
```

## Mapping Matrix

| Source / Requirement | Design | Artifact | Verification |
|---|---|---|---|
| ZIP rules: source trước code | Stage 0 không tạo application code | README, manifest | file tree check |
| ZIP rules: không silent resolve open question | Explicit labels + decision register | `05_DECISIONS.md` | acceptance A-06 |
| Mia AI context: PROPOSED không thành fact | preserve status | `09_SOURCE_AUTHORITY...` | scenario V-01 |
| Mia AI context: conflict unresolved không silently choose | conflict procedure | `09_SOURCE_AUTHORITY...` | scenario V-02 |
| Historical Mia runtime topics deferred | do not import runtime complexity early | `11_ARCHITECTURE_HYPOTHESIS_REGISTER.md` | scenario V-03 |
| Current Mia skeleton is much more mature | use as reference evidence | `10_MIA_REFERENCE_LEDGER.md` | Feynman gate |
| User requirement: build from scratch but compare step-by-step | blind-first/reference-second | learning guide + template | V-04 |
| User requirement: optimize across conflicts | authority lanes, not timestamp-only | source protocol | V-05 |
| User requirement: 16 stages | master roadmap | `12_MASTER_ROADMAP_16_STAGES.md` | roadmap check |
| ZIP rules: Engineering understanding separately from code pass | dual gate | acceptance + verification | GATE-00 |

---

## Tại sao không có code mapping?

Rule yêu cầu "map lý thuyết sang code" khi Phase có implementation.

Stage 0 cố ý không có application implementation. Việc tạo fake `src/` chỉ để thỏa cấu trúc sẽ vi phạm:

```text
Minimum Sufficient Implementation
```

và:

```text
Không tạo thư mục rỗng.
```

Do đó Stage 0 mapping kết thúc ở **governance artifacts**.

Từ Stage có code, `03_DESIGN_MAPPING.md` phải chuyển thành:

```text
Requirement
→ Design
→ File / Function
→ Test
```

---

# Dependency direction được khóa ở Stage 0

Không phải code dependency mà là **reasoning dependency**:

```text
Requirement
    ↓
Domain / invariant
    ↓
Hypothesis
    ↓
Evidence
    ↓
Decision
    ↓
Contract
    ↓
Implementation
```

Không được đảo thành:

```text
Framework
→ code
→ documentation rationale
```
