# Evaluation Oracle & Labeling Model

> **Status:** PROPOSED v0.1

---

# 1. Evaluator ≠ Oracle

An evaluator executes a comparison.

An oracle supplies the expected truth/policy label.

---

# 2. Oracle classes

## Deterministic contract oracle

Suitable for:

```text
schema validity
known prohibited statement class
unknown reference
policy digest mismatch
ambient capability request
```

## Source-grounded oracle

Suitable for:

```text
value equals source
citation exists
claim points to selected evidence
```

## Clinician-adjudicated oracle

Required for judgments such as:

```text
clinical correctness
appropriateness of bounded interpretation
usefulness
potential for harm
acceptable uncertainty wording
```

## Statistical oracle

Used for:

```text
confidence intervals
rate comparison
sample-size planning
```

## Model judge

May help with:

```text
style
semantic similarity
triage of evaluation workload
```

but cannot be the only oracle for:

```text
clinical correctness
diagnosis leakage
treatment safety
critical escalation
```

---

# 3. Gold label structure

A gold label records:

```text
gold_verdict
risk_severity
expected_violation_families
label_source
reviewer_count
adjudication_status
```

---

# 4. Severity classes

Candidate baseline:

```text
S0_INFORMATIONAL
S1_QUALITY
S2_CLINICAL_MISLEADING
S3_PROHIBITED_CLINICAL_ACTION
S4_CRITICAL_SAFETY
```

Severity is used for reporting and release blocking.

It is not a diagnosis-risk score.

---

# 5. Label lifecycle

```text
draft
double_reviewed
adjudicated
frozen
```

Cases used for production model approval should not rely on one unreviewed annotator for clinical judgments.

---

# 6. Inter-rater agreement

For two reviewers on categorical labels:

```text
Cohen's kappa
```

can be reported.

Kappa is diagnostic evidence about labeling consistency.

It does not replace disagreement adjudication.

---

# 7. Blind review

Where feasible:

```text
reviewer does not know model/vendor identity
```

to reduce brand/model bias.

---

# 8. Gold-set leakage

Production evaluation cases should be protected from prompt/model-development leakage.

Public/synthetic developer tests and private release tests should be separate.

---

# 9. Versioning

Changing a gold label after adjudication:

```text
new case version
```

Do not silently rewrite historical evaluation results.
