# 13 — Stage 1 Handoff

## Next Stage

**Stage 1 — Product & Clinical Domain Discovery**

Stage 1 chưa viết architecture runtime.

Nó phải trả lời:

```text
What is BioMarker?
Who uses it?
What problem is solved?
What input is allowed?
What output is allowed?
What must it NOT do?
What clinical risk exists?
What data is sensitive?
What is evidence?
What is intended use?
What requires clinician/human oversight?
```

---

# Required inputs

- product idea/reference: Biolyzer;
- organization context;
- expected Vinmec/Mia relationship nếu đã biết;
- target users;
- target geography/jurisdiction nếu có;
- sample report types nếu có;
- known clinical stakeholders.

Nếu chưa có, Stage 1 được phép tạo:

```text
OPEN QUESTION
TEAM DECISION REQUIRED
```

không được tự bịa.

---

# Stage 1 source strategy

## Read first

1. authoritative user/team requirement;
2. BioMarker product references;
3. applicable clinical/regulatory standards/guidance;
4. only then Mia high-level product/platform boundaries.

## Do not open deeply yet

- DBOS;
- lease/fencing;
- manifest compiler;
- worker internals;
- Redis SSE;
- PostgreSQL schema.

Những thứ này không được product problem định nghĩa ngược.

---

# Stage 1 expected artifacts

Candidate list:

```text
BIOMARKER_PRODUCT_CONTEXT.md
INTENDED_USE_AND_SAFETY_ENVELOPE.md
USERS_USE_CASES_AND_NON_GOALS.md
CLINICAL_RISK_QUESTION_REGISTER.md
DATA_AND_PRIVACY_QUESTION_REGISTER.md
SOURCE_REVIEW.md
DECISIONS.md
```

Exact ZIP structure phải tuân `AI ZIP GENERATION RULES.md`.

---

# Entry Gate

Trước khi bắt đầu Stage 1:

- Artifact Gate Stage 0: PASS
- Human learning gate Stage 0: recommended PASS
- no assumption that BioMarker is already a Mia internal capability
- no selected runtime/db/queue

---

# Key Feynman question before Stage 1

> Nếu không được nói "AI Agent", bạn mô tả sản phẩm BioMarker bằng dữ liệu đầu vào, transformation và outcome như thế nào?

Nếu chưa trả lời được, Stage 1 chính là nơi tìm câu trả lời.
