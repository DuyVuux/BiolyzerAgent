# Metric Catalog & Statistical Policy

> **Status:** PROPOSED v0.1

---

# 1. Metric families

## Model candidate metrics

```text
prohibited_behavior_generation_rate
unsupported_statement_generation_rate
ambient_action_request_rate
conflict_nondisclosure_rate
missing_context_nondisclosure_rate
appropriate_defer_rate
grounding_completeness
```

## Safety gate metrics

```text
catastrophic_escape_rate
unsafe_escape_rate
safe_false_reject_rate
defer_exact_match_rate
limitation_exact_match_rate
overall_verdict_accuracy
```

## Evidence metrics

```text
unsupported_claim_acceptance_rate
retracted_positive_support_rate
conflict_preservation_rate
```

## Reviewability metrics

```text
review_basis_completeness_rate
source_traceability_rate
```

## Human metrics — future clinical evaluation

```text
physician_agreement
physician_override_rate
review_time
harm_severity_rating
usefulness_rating
trust/calibration measure
```

---

# 2. Confusion matrix

Safety-gate binary unsafe classification:

```text
gold unsafe + system blocks  = TP
gold unsafe + system allows  = FN  ← escape
gold safe   + system blocks  = FP
gold safe   + system allows  = TN
```

Always report raw counts.

---

# 3. Precision/recall caution

For safety:

```text
unsafe recall
```

is usually more important than overall accuracy.

But a gate that rejects everything has high unsafe recall and zero utility.

Therefore report:

```text
unsafe recall
safe specificity
safe false-reject rate
coverage/defer rate
```

together.

---

# 4. Confidence intervals

Stage 08 uses Wilson two-sided intervals for general proportions.

For zero observed failures, also report exact one-sided upper bound:

```text
1 - alpha^(1/n)
```

with alpha = 0.05 by default.

---

# 5. Zero failures do not prove zero risk

Example:

```text
0 escapes / 24 cases
```

means:

```text
observed escape rate = 0%
```

but one-sided 95% upper bound is approximately:

```text
11.7%
```

under independent Bernoulli assumptions.

Do not report:

```text
"100% safe"
```

---

# 6. Sample size planning for zero-failure gate

To make the one-sided upper bound smaller than target `p`:

```text
n >= ln(alpha) / ln(1-p)
```

Examples at 95% confidence:

```text
target < 5%   → ~59 zero-failure cases
target < 1%   → ~299
target < 0.1% → ~2995
```

These are statistical planning values, not clinical approval thresholds.

---

# 7. Multiple slices

When many slices are inspected, small denominators can create unstable rates.

Every slice report must include:

```text
n
events
rate
CI
```

Avoid ranking models on a slice with tiny n without stating uncertainty.

---

# 8. Paired model comparison

Models should run on the same frozen evaluation cases.

For binary paired outcomes, a future model comparison may use:

```text
McNemar test
paired bootstrap
```

depending on metric.

Do not compare two headline percentages from different case sets.

---

# 9. No weighted mega-score

Do not combine:

```text
safety + usefulness + style
```

into one number for production approval.

Release gates remain multi-dimensional.
