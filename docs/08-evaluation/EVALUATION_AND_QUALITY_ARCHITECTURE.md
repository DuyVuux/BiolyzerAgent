# BioMarker Agent — Evaluation & Quality Architecture

> **Status:** PROPOSED EVALUATION BASELINE v0.1  
> **Stage:** 08 — Evaluation & Quality Architecture  
> **Primary user:** Healthcare Professional / Physician  
> **Critical distinction:** Stage 07 safety rules are a **policy-compliance oracle**, not universal clinical ground truth.

---

# 1. Why Stage 08 exists

A system can have perfect schema validation and still be clinically poor.

A model can pass a safety gate and still be:

```text
irrelevant
incomplete
poorly grounded
misleadingly worded
clinically unhelpful
```

A safety gate can also be too strict and reject useful output.

Therefore Stage 08 evaluates separate layers instead of hiding them in one score.

---

# 2. Five evaluation layers

```text
L1 — Upstream Data Quality
L2 — Evidence Quality
L3 — Model Reasoning Quality
L4 — Safety-Gate Quality
L5 — Human / End-to-End Clinical Usefulness
```

## L1 — Upstream Data Quality

Consumes metrics already defined in Stages 03–05:

```text
extraction correctness
normalization correctness
lineage correctness
timeline correctness
```

Stage 08 does not collapse these into model quality.

## L2 — Evidence Quality

Consumes Stage 06 outputs:

```text
retrieval/source identity
claim support
conflict preservation
bundle closure
```

Production biomedical entailment quality is a separate gate.

## L3 — Model Reasoning Quality

Measures model candidate before deterministic safety filtering:

```text
grounding completeness
unsupported statement rate
diagnostic leakage
treatment leakage
causal overclaim
conflict disclosure
missing-context awareness
useful defer behavior
```

## L4 — Safety-Gate Quality

Measures Stage 07 gate behavior against independent gold labels:

```text
unsafe escape rate
safe false-reject rate
defer classification accuracy
limited-output classification accuracy
```

## L5 — Human / End-to-End Clinical Usefulness

Requires clinician evaluation:

```text
correctness
usefulness
review burden
trust calibration
time-to-review
override/disagreement reasons
```

This layer is NOT executed by synthetic Stage 08 fixtures.

---

# 3. Oracle hierarchy

Not every evaluator is ground truth.

Candidate oracle classes:

```text
DETERMINISTIC_CONTRACT_ORACLE
SOURCE_GROUNDED_ORACLE
CLINICIAN_ADJUDICATED_GOLD
STATISTICAL_ORACLE
MODEL_JUDGE
```

Authority:

```text
model judge
<
deterministic/source-grounded labels
<
clinician adjudication for clinical judgments
```

An LLM-as-judge can assist review but must not be the sole clinical/safety authority.

---

# 4. Avoid circular evaluation

Incorrect:

```text
Stage 07 gate says REJECT
→ Stage 08 defines REJECT as correct
→ Stage 07 accuracy = 100%
```

Correct:

```text
independent case gold label
→ run Stage 07
→ compare actual verdict with independent label
```

Stage 08 synthetic gold labels are separately materialized in:

```text
testdata/synthetic/stage-08/evaluation_cases.json
```

The evaluator then consumes Stage 07 decisions as system output.

---

# 5. Evaluation unit

One `EvaluationCase` pins:

```text
case_id
case_version
risk_class
slice_tags
input reference
candidate reference
independent expected verdict
expected violation families
clinical-review requirement
```

Cases are immutable/versioned evaluation artifacts.

---

# 6. EvaluationRun

Every run pins:

```text
dataset manifest digest
model manifest
prompt/program digest
reasoning policy digest
safety policy digest
evidence policy digest
evaluator version
metric catalog version
```

Changing any one produces a new EvaluationRun identity.

---

# 7. Model manifest

Model comparison requires exact provenance:

```text
provider
model_id
model_version
model_config_digest
prompt_or_program_digest
temperature
seed if supported
tool/capability profile
```

Never compare labels such as:

```text
"Model A"
vs
"Model B"
```

without version/config provenance.

---

# 8. No single composite score

Stage 08 rejects:

```text
quality_score = 87/100
```

as primary approval logic.

Reason:

A model could compensate:

```text
1 catastrophic diagnosis escape
```

with many stylistic successes.

Metrics stay separated by risk class.

---

# 9. Safety-first release logic

Necessary conditions may include:

```text
no observed catastrophic-policy escape in release suite
all contract/schema gates pass
no evidence/clinical identity collision escape
review basis complete
```

But:

```text
zero observed failures
≠
zero true failure probability
```

Statistical uncertainty must always accompany rate metrics.

---

# 10. Confidence interval rule

Every critical rate should report:

```text
numerator
denominator
point estimate
confidence interval
```

For zero observed failures, Stage 08 also reports the exact one-sided zero-failure upper bound:

```text
upper95 = 1 - 0.05^(1/n)
```

Examples:

```text
0 / 24   → upper95 ≈ 11.7%
0 / 299  → upper95 < 1%
```

This prevents misleading claims of “100% safe”.

---

# 11. Slice evaluation

Overall accuracy can hide failure clusters.

Required slice dimensions when present and ethically/legally appropriate:

```text
risk category
statement class
value kind
evidence conflict
missing context
terminology state
verification state
critical-source signal
document quality class
clinical use-case
```

Demographic fairness slices require approved data governance and suitable datasets; Stage 08 does not invent protected-attribute data.

---

# 12. Adversarial evaluation

Adversarial cases cover:

```text
prompt injection
evidence injection
unknown refs
policy-digest mismatch
unsupported diagnosis
treatment/dose advice
causal overclaim
conflict hiding
unverified fact laundering
terminology upgrading
ambient retrieval
critical flag → triage escalation
schema-invalid candidate
```

---

# 13. Metamorphic evaluation

A metamorphic test changes an input in a way with a known expected relationship.

Examples:

```text
reordering independent statements
→ safety verdict unchanged

same logical case + reordered refs
→ verdict unchanged

hidden conflict → conflict disclosed
→ REJECT becomes APPROVE_WITH_LIMITATIONS

unverified → verified under otherwise same facts
→ DEFER may become APPROVE

add ambient web action
→ safe candidate becomes REJECT
```

This tests invariants without requiring a new clinical answer for every variation.

---

# 14. Human factors boundary

WHO warns that generative health AI can produce false/incomplete outputs and can encourage automation bias.

DECIDE-AI emphasizes human–AI interaction and early live clinical evaluation.

Therefore offline technical metrics are not equivalent to clinical usefulness.

Before go-live, physician-facing evaluation must measure:

```text
review behavior
error detection
override behavior
review time
calibrated trust
workflow integration
```

Stage 08 architecture defines the protocol boundary but does not claim live clinical evaluation has happened.

---

# 15. Production quality gate

Current Stage 08 can approve:

```text
evaluation architecture
metric definitions
synthetic evaluator mechanics
release-gate mechanics
```

It cannot approve:

```text
a production LLM
clinical usefulness
real-world safety
regulatory classification
```

Those require representative/approved datasets and clinician review.
