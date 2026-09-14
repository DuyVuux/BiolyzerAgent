# Clinical Statement & Grounding Model

> **Status:** PROPOSED v0.1

---

## 1. Why statement-level objects?

A free-form paragraph hides:

```text
what is source fact
what is deterministic derivation
what is literature context
what is model interpretation
```

Therefore candidate reasoning is decomposed into statements.

---

## 2. Candidate statement fields

```text
statement_id
statement_class
text
inference_mode
assertion_strength
clinical_refs[]
evidence_claim_refs[]
derivation_ref?
conflict_disclosed
missing_context_acknowledged
```

---

## 3. Statement classes

Allowed:

```text
measured_fact
derived_fact
evidence_context
bounded_interpretation
limitation
physician_question
```

Candidate-only prohibited types:

```text
diagnosis
treatment_recommendation
medication_change
dosage_change
emergency_triage
```

The candidate contract can represent prohibited types so the safety harness can detect and measure them.

The final output contract cannot contain them.

---

## 4. Inference mode

```text
none
association
uncertainty
diagnostic
therapeutic
triage
patient_specific_causal
```

Final output permits only:

```text
none
association
uncertainty
```

---

## 5. Assertion strength

```text
direct_source
deterministic
evidence_supported
uncertain
definitive
```

`definitive` is not allowed for bounded patient-specific interpretation.

---

## 6. Grounding registry

Final output can be mechanically inspected:

```text
statement
→ clinical ref(s)
→ observation/timeline source

statement
→ evidence claim ref(s)
→ claim
→ source/passage
```

This trace is required before Stage 08 evaluation.

---

## 7. No chain-of-thought storage requirement

Stage 07 does not require private model chain-of-thought.

Safety/audit relies on:

```text
structured claims
references
policy decisions
gate violations
```

not hidden reasoning text.
