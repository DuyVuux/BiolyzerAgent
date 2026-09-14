# Human Clinical Review Protocol

> **Status:** PROPOSED / NOT EXECUTED

---

# 1. Purpose

Offline automated evaluation cannot prove clinical usefulness.

Before limited clinical use, physician review should evaluate:

```text
clinical correctness
relevance
missing important information
potentially misleading wording
adequacy of uncertainty
ease of independent review
review time
```

---

# 2. Double review

For high-risk clinical evaluation cases:

```text
Reviewer A
Reviewer B
→ disagreement
→ adjudicator
```

Reviewer identities/roles should be governed by the approved clinical study process.

---

# 3. Blinding

Where practical:

```text
hide model/provider identity
randomize output order
```

to reduce model-brand bias.

---

# 4. Annotation dimensions

Candidate labels:

```text
correct
partially_correct
incorrect

useful
neutral
not_useful

safe
potentially_misleading
potentially_harmful

uncertainty_adequate
uncertainty_inadequate
```

Exact final scale requires clinician agreement.

---

# 5. Human factors

DECIDE-AI highlights human-AI interaction.

Future evaluation should capture:

```text
review time
whether physician noticed an intentionally seeded issue
override reason
confidence before/after AI
automation-bias indicators
```

---

# 6. No live-patient impact in this Stage

This document defines the evaluation protocol boundary only.

No live clinical study is claimed.
