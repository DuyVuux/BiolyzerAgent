# 08 — Integration Guide

## Trước khi integrate

Package này là **candidate documentation package**, không phải project độc lập và không phải application scaffold.

Sau khi integrate:

### Repository SẼ có

- source/conflict discipline;
- hypothesis workflow;
- Mia reference ledger;
- 16-stage master roadmap;
- experiment/ADR/source review templates.

### Repository SẼ thay đổi

Chỉ documentation/process nếu bạn chọn merge.

### Repository CHƯA có

- runtime;
- DB;
- API;
- parser;
- LLM integration;
- FHIR/LOINC/UCUM implementation;
- security implementation;
- frontend;
- deployment.

---

# Suggested integration process

## 1. Tạo feature branch

Ví dụ:

```bash
git switch -c docs/biomarker-stage-00
```

Mục đích: tách thay đổi Stage 0 khỏi work khác.

## 2. Inspect package

Không copy đè ngay.

So sánh:

- naming convention hiện tại;
- repo có `docs/` chưa;
- repo có decision folder chưa;
- đã có roadmap/conflict register tương đương chưa.

## 3. Chọn target path

Stage 0 không áp đặt final repo skeleton.

Ví dụ nếu repo mới:

```text
docs/
  00-foundation/
```

có thể là target hợp lý, nhưng đây chỉ là integration choice.

## 4. Integrate từng file

Ưu tiên preserve semantic content.

Nếu đổi path/name:

- update links;
- update manifest local copy nếu package được lưu trong repo;
- không đổi decision status.

## 5. Review git diff

```bash
git status
git diff --stat
git diff
```

Mục đích:

- không có unrelated formatting;
- không có accidental deletion;
- không có generated app files.

## 6. Run project-specific docs checks nếu repo có

Stage 0 không thêm linter dependency.

## 7. Human review

Review tập trung:

- authority lanes có phù hợp organization không;
- mandatory Mia integration constraint đã biết chưa;
- naming `BioMarker` hay `Biomarker` theo product convention;
- Stage 1 owner/reviewer.

---

# Conflict có thể xảy ra ở đâu?

## Existing source hierarchy

Nếu repo đã có source precedence:

- không overwrite;
- compare;
- merge only if semantics compatible;
- record difference as explicit decision.

## Existing ADR template

Reuse project template nếu authority cao hơn. Stage 0 template chỉ là candidate.

## Existing roadmap

Không merge blindly. Giữ 16-stage roadmap như learning/build roadmap nếu product roadmap là tài liệu khác.

---

# Dependencies added

None.

# Environment variables added

None.

# Migration required

None.

# Tests required

No application tests.

# Integration recommendation

**SAFE TO INTEGRATE AS DOCUMENTATION CANDIDATE AFTER REVIEW.**

Không dùng `cp -r package/* repo/` mù quáng.
