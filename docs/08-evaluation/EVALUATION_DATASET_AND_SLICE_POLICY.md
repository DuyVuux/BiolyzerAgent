# Evaluation Dataset & Slice Policy

> **Status:** PROPOSED v0.1

---

# 1. Dataset classes

```text
DEV_PUBLIC_SYNTHETIC
INTERNAL_SYNTHETIC_HARD
APPROVED_DEIDENTIFIED_REPRESENTATIVE
CLINICIAN_ADJUDICATED_RELEASE
LIVE_CLINICAL_OBSERVATIONAL
```

Current Stage 08 package contains only:

```text
DEV_PUBLIC_SYNTHETIC
```

---

# 2. Dataset split

Recommended future split:

```text
development
validation
private release test
post-deployment monitoring
```

Do not tune prompts/policies on the private release suite.

---

# 3. Slice tags

Every case may carry:

```text
risk_class
statement_class
evidence_conflict
missing_context
verification_state
terminology_state
source_critical_flag
value_kind
document_quality
```

---

# 4. Fairness/subgroup policy

FUTURE-AI includes fairness as a trustworthy AI principle.

However Stage 08 does not create demographic attributes merely to satisfy a checklist.

Subgroup analysis requires:

```text
lawful/approved data use
sufficient sample size
clinically meaningful subgroup definition
privacy controls
```

---

# 5. Distribution shift

Future representative datasets should record:

```text
site
lab/system source
document layout/version
time period
clinical department
```

where governance permits.

This allows evaluation of generalization rather than one aggregate score.

---

# 6. Data leakage

Evaluation examples, labels and private release fixtures should not be embedded into:

```text
system prompts
few-shot examples
training data
retrieval corpus
```

when they are intended to remain held-out.
