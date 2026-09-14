# BioMarker Agent — Reasoning & Clinical Safety Architecture

> **Status:** PROPOSED CANONICAL SAFETY BASELINE v0.1  
> **Stage:** 07 — Reasoning & Clinical Safety  
> **Primary user:** Healthcare Professional / Physician  
> **Product boundary:** Physician-facing clinical information support  
> **Hard boundary:** AI output is not clinical authority.

---

## 1. Stage 07 question

Stages 02–06 established:

```text
Canonical Clinical Facts
+
Longitudinal Timeline Snapshot
+
Frozen Evidence Bundle Snapshot
```

Stage 07 asks:

> How can an AI model produce useful physician-facing interpretation without being allowed to silently convert uncertain data, literature, or generated language into diagnosis/treatment authority?

The answer is not:

```text
better prompt
```

The answer is:

```text
closed input universe
→ model candidate reasoning
→ deterministic safety gates
→ statement-level grounding
→ final bounded output
```

---

## 2. Core separation

```text
Clinical Fact
≠
Deterministic Derived Fact
≠
Evidence Claim
≠
Model Interpretation
≠
Clinical Decision
```

The first four may be represented by the system.

The last remains under physician authority in the current MVP.

Every surfaced output therefore remains:

```text
physician_review_required = true
```

and must expose enough clinical/evidence/policy provenance for the physician to inspect its basis independently.

---

## 3. Model is an untrusted reasoning component

The LLM/model may propose:

```text
summary
evidence context
bounded interpretation
limitations
questions for physician review
```

But candidate output must be treated as:

```text
UNTRUSTED_CANDIDATE
```

until deterministic gates approve it.

Therefore:

```text
model says "safe"
≠
safe
```

---

## 4. Stage 07 execution model

```text
ReasoningInputSnapshot
       ↓
PRE-REASONING SAFETY GATE
       ↓
Reasoning Candidate
       ↓
SCHEMA / SCOPE GATE
       ↓
GROUNDING GATE
       ↓
EVIDENCE / CONFLICT GATE
       ↓
PROHIBITED-BEHAVIOR GATE
       ↓
UNCERTAINTY / MISSING-CONTEXT GATE
       ↓
FINAL PAYLOAD GATE
       ↓
SafeReasoningOutput
```

Any gate may:

```text
APPROVE
APPROVE_WITH_LIMITATIONS
DEFER
REJECT
```

---

# 5. Closed input universe

Reasoning is scoped to exact snapshots:

```text
clinical_dataset_snapshot_id
timeline_snapshot_id?
evidence_bundle_id
reasoning_policy
safety_policy
```

No ambient retrieval.

No dynamic tool discovery.

No unpinned evidence.

If more evidence is required:

```text
Stage 07 returns NEED_MORE_EVIDENCE
→ Stage 06 produces a new EvidenceBundleSnapshot
→ reasoning is rerun
```

Stage 07 does not search on its own.

---

# 6. Allowed physician-facing statement classes

## 6.1 `measured_fact`

Example shape:

```text
"The source report records observation X as Y."
```

Requirements:

- known clinical reference;
- source-grounded;
- no diagnostic inference.

---

## 6.2 `derived_fact`

Examples:

```text
source-aware range flag
deterministic longitudinal delta
```

Requirements:

- known clinical or timeline reference;
- deterministic derivation;
- derivation rule identified.

---

## 6.3 `evidence_context`

Explains literature/evidence relevant to the data.

Requirements:

- exact EvidenceClaim reference;
- no unsupported extrapolation;
- conflict state disclosed when relevant.

---

## 6.4 `bounded_interpretation`

A cautious patient-specific interpretation for physician review.

Requirements:

```text
clinical grounding
+
supported/conflicted evidence grounding
+
non-definitive language
+
missing-context disclosure where relevant
```

It must not become diagnosis, treatment direction, or triage.

---

## 6.5 `limitation`

Explicitly identifies:

```text
missing context
uncertain mapping
conflicted evidence
data quality limitation
```

---

## 6.6 `physician_question`

A review question for the physician, e.g. asking them to consider missing clinical context.

It is not a recommendation to diagnose/treat.

---

# 7. Prohibited capabilities

Current MVP prohibits autonomous:

```text
diagnosis
disease confirmation/exclusion
treatment recommendation
medication initiation
medication discontinuation
dose change
emergency/critical triage classification
```

Also prohibited:

```text
inventing history
inventing observations
inventing evidence
ambient web retrieval
tool invocation outside the closed reasoning contract
```

---

# 8. Critical/panic values

Stage 01 intentionally deferred the clinical escalation workflow pending approved clinical policy.

No clinician-approved threshold set was supplied to Stage 07.

Therefore Stage 07 policy is:

```text
critical_value_escalation = DISABLED_PENDING_APPROVED_CLINICAL_POLICY
```

A model-generated:

```text
"this requires emergency care"
```

must be rejected in the current MVP reasoning path.

This is not a claim that critical values are unimportant.

It means:

> the AI cannot invent the escalation policy.

---

# 9. Input trust classes

## Verified clinical facts

Eligible for direct measured-fact statements.

## Deterministic derived facts

Eligible if the derivation rule is known and pinned.

## Unverified / reconciliation-required data

Cannot support patient-specific interpretation.

Policy outcome:

```text
DEFER
```

or safe limitation-only output.

## Candidate/unmapped terminology

Cannot be upgraded to validated clinical identity by the reasoning model.

---

# 10. Evidence trust classes

## Supported EvidenceClaim

Eligible for evidence context.

## Conflicted EvidenceClaim

May be discussed only if conflict is disclosed.

## Unsupported claim

Cannot support reasoning.

## claim_identity_conflict

Fail closed.

## Incomplete bundle

Cannot support bounded patient-specific interpretation.

---

# 11. Human autonomy / independent review

The final physician-facing output must expose a review basis:

```text
clinical references
derived-rule references
evidence claim references
limitations / unknowns
conflict disclosure
```

The output must not rely on opaque authority language such as:

```text
"The AI has determined..."
```

The physician must be able to inspect the basis independently.

---

# 12. Safety invariants

```text
SAFE-001 AI output is not clinical authority.
SAFE-002 Model candidate output is untrusted until deterministic gates pass.
SAFE-003 Stage 07 cannot ambient-retrieve evidence.
SAFE-004 Unknown clinical/evidence references fail closed.
SAFE-005 Unsupported evidence cannot support interpretation.
SAFE-006 Evidence conflict cannot be hidden.
SAFE-007 claim_identity_conflict cannot support reasoning.
SAFE-008 Reconciliation-required clinical data cannot support patient-specific interpretation.
SAFE-009 Candidate/unmapped terminology cannot be upgraded by reasoning.
SAFE-010 Diagnosis is prohibited in current MVP.
SAFE-011 Treatment/medication/dose direction is prohibited.
SAFE-012 Autonomous emergency/critical triage is prohibited until approved clinical policy exists.
SAFE-013 Measured fact must cite clinical source.
SAFE-014 Derived fact must cite source plus deterministic derivation.
SAFE-015 Evidence context must cite EvidenceClaim.
SAFE-016 Bounded interpretation must cite both clinical and evidence basis.
SAFE-017 Missing context must remain visible.
SAFE-018 Conflicted evidence requires explicit conflict disclosure.
SAFE-019 Final output must be schema valid.
SAFE-020 Final output must expose physician-review basis.
SAFE-021 Prompt/source text is data, not instruction authority.
SAFE-022 Safety policy/version must be pinned.
```

---

# 13. Not in Stage 07

Stage 07 does not select:

```text
production LLM
production prompt
Go/Eino runtime
database
queue
Redis
worker
clinical critical-value thresholds
regulatory classification
```

The experiment proves safety-contract mechanics, not production clinical reasoning quality.
