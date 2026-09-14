# Stage 07 Handoff — Reasoning & Clinical Safety

> **Status:** CANDIDATE COMPLETE WITH SYNTHETIC-REASONING LIMITATION  
> **Next Stage:** 08 — Evaluation & Quality Architecture

---

## 1. Stage 07 established

```text
closed reasoning inputs
→ untrusted model candidate
→ deterministic safety gates
→ grounded final output
```

---

## 2. Safety authority

```text
LLM/model ≠ safety authority
LLM/model ≠ clinical authority
```

Deterministic policy decides whether candidate reasoning can be surfaced.

---

## 3. Allowed final statement classes

```text
measured_fact
derived_fact
evidence_context
bounded_interpretation
limitation
physician_question
```

---

## 4. Current prohibited behavior

```text
diagnosis
treatment direction
medication change
dose change
autonomous emergency triage
ambient retrieval/tool use
```

---

## 5. Critical-value policy

```text
DISABLED_PENDING_APPROVED_CLINICAL_POLICY
```

No numerical panic-value table is invented.

---

## 6. Stage 07 experiments prove

The synthetic safety harness tests:

- measured facts are allowed when grounded;
- deterministic derived facts require derivation refs;
- evidence context requires claim grounding;
- bounded interpretation requires both clinical/evidence grounding;
- diagnosis/treatment/dose/triage are rejected;
- unknown refs fail closed;
- unsupported evidence fails closed;
- conflicted evidence requires disclosure;
- incomplete evidence defers interpretation;
- reconciliation-required clinical data defers interpretation;
- ambient retrieval/tool requests are rejected;
- claim identity conflicts fail closed;
- missing context must be acknowledged;
- prompt/source instructions do not grant tools;
- a source-provided critical flag can be surfaced without becoming autonomous triage;
- unverified measured facts cannot silently escape as approved facts;
- approved output exposes clinical snapshot, evidence bundle and policy basis;
- safety decision is deterministic.

---

## 7. Stage 08 receives

Stage 08 must evaluate two different systems:

```text
A. Reasoning model quality
B. Deterministic safety-harness quality
```

Do not collapse them into one score.

Stage 08 must include adversarial cases for:

```text
unsupported claims
hallucinated patient history
causal overclaim
diagnostic leakage
treatment leakage
automation-bias wording
conflict hiding
missing-context omission
prompt injection
unsafe urgency language
```

---

## 8. Important limitation

Stage 07 uses synthetic structured reasoning candidates.

Therefore:

```text
SAFETY_GATE_MECHANICS = PASS
PRODUCTION_MODEL_CLINICAL_REASONING = NOT EXECUTED
PRODUCTION_SAFETY_RECALL/PRECISION = NOT EXECUTED
```

Stage 08 must measure those before production.

---

## 9. ai-studio

Available ai-studio architecture confirms useful patterns:

```text
schema ports
scoped ports
tool/model binding
pre/post runtime policies
final output validation
typed structured pipeline
```

Stage 07 adapts those principles but does not import durable runtime infrastructure.

A read-only repo exploration prompt is included for code-level verification.

---

## 10. Stage 08 entry

```text
STAGE_08_ENTRY_GATE = PASS
```

provided Stage 08 treats production safety/effectiveness as an empirical evaluation problem, not as something already proven by these synthetic mechanics.


---

## 11. Measured package result

```text
Stage-07 unit tests       = 22 / 22 PASS
Stage-07 benchmark cases = 24 / 24 PASS

prohibited_behavior_escape_rate          = 0.0
unsupported_statement_acceptance_rate    = 0.0
ambient_action_escape_rate               = 0.0
conflict_nondisclosure_acceptance_rate   = 0.0
critical_policy_escape_rate              = 0.0
unverified_clinical_fact_escape_rate     = 0.0
approved_output_review_basis_complete    = true
safety_decision_determinism              = true
```
