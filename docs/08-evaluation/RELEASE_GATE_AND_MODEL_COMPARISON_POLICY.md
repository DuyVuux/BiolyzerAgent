# Release Gate & Model Comparison Policy

> **Status:** PROPOSED v0.1

---

# 1. Model comparison unit

A `ModelEvaluationManifest` pins:

```text
provider
model_id
model_version
configuration
prompt/program digest
policy digests
evaluation dataset digest
```

---

# 2. Hard gates

Candidate hard blockers include:

```text
contract/schema failure
clinical/evidence identity collision escape
prohibited clinical behavior reaching safe output
ambient capability escape
review basis incomplete
```

Observed zero failures is necessary for a release suite but is not enough to infer zero population risk.

---

# 3. Soft / comparative dimensions

Examples:

```text
grounding completeness
appropriate defer
safe-answer coverage
conflict disclosure
usefulness
brevity/readability
review burden
```

A model can be better on one and worse on another.

---

# 4. No “best model” without purpose

Selection requires the intended task:

```text
physician-facing urinalysis summary
```

not generic benchmark prestige.

---

# 5. Production model selection status

Stage 08 architecture supports comparison.

This package does not approve a production model because:

```text
no approved representative clinical corpus
no clinician-adjudicated gold set
no actual provider/model benchmark run in this environment
```

---

# 6. Stage 09 relationship

Stage 09 may begin with:

```text
deterministic/mock model adapter
```

because runtime architecture does not require production model approval.

But:

```text
production go-live
```

remains blocked until real-model and clinical-evaluation gates pass.

---

# 7. Version changes require re-evaluation

Any material change in:

```text
model version
system prompt/program
reasoning policy
safety policy
evidence policy
normalization policy
```

should produce a new EvaluationRun.

A previous pass does not automatically transfer.
