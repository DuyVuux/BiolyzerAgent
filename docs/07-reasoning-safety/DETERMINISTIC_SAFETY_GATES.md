# Deterministic Safety Gates

> **Status:** PROPOSED v0.1

---

# Gate G0 — Input Closure

Checks:

```text
reasoning policy pinned
safety policy pinned
clinical snapshot identified
evidence bundle identified
evidence processing profile digest present
```

Failure:

```text
DEFER
```

---

# Gate G1 — Clinical Eligibility

Checks all clinical refs used by candidate.

Reject/defer if:

```text
unknown clinical ref
reconciliation_required
unverified fact used for interpretation
candidate terminology treated as validated
```

Measured facts may only use explicitly eligible refs.

---

# Gate G2 — Evidence Eligibility

Reject if candidate uses:

```text
unknown claim
unsupported claim
claim_identity_conflict
```

Conflicted claims require disclosure.

Incomplete bundle cannot support bounded interpretation.

---

# Gate G3 — Capability Scope

No candidate may request:

```text
web_search
new retrieval
arbitrary tool call
dynamic schema/model/tool resolution
```

Outcome:

```text
REJECT
```

---

# Gate G4 — Prohibited Clinical Behavior

Statement classes:

```text
diagnosis
treatment_recommendation
medication_change
dosage_change
emergency_triage
```

are rejected.

Structured `inference_mode`:

```text
diagnostic
therapeutic
triage
patient_specific_causal
```

is rejected.

---

# Gate G5 — Statement Grounding

### measured_fact

Requires:

```text
>= 1 clinical ref
```

### derived_fact

Requires:

```text
>= 1 clinical ref
derivation_ref
```

### evidence_context

Requires:

```text
>= 1 EvidenceClaim ref
```

### bounded_interpretation

Requires:

```text
>= 1 clinical ref
>= 1 EvidenceClaim ref
assertion_strength != definitive
```

### limitation / physician_question

Can exist without evidence support.

---

# Gate G6 — Conflict & Uncertainty

If used evidence is conflicted:

```text
conflict_disclosed = true
```

Otherwise reject.

If input says context missing and patient-specific interpretation is made:

```text
missing_context_acknowledged = true
```

Otherwise reject.

If a source-provided `critical` signal is referenced while no approved critical-value escalation policy is active:

```text
the source flag itself may be surfaced as a measured fact
+
APPROVE_WITH_LIMITATIONS
+
physician review remains required
```

The system must not convert that source flag into autonomous emergency triage.

---

# Gate G7 — Reviewability

Each approved output must expose:

```text
clinical snapshot ID
timeline snapshot ID when used
evidence bundle ID
clinical refs
evidence refs
policy digests
derivation refs where applicable
limitations
```

This enables physician review of the basis.

---

# Gate G8 — Final Payload Schema

Only a structurally valid:

```text
SafeReasoningOutput
```

can leave Stage 07.

---

# Verdict aggregation

Priority:

```text
REJECT
>
DEFER
>
APPROVE_WITH_LIMITATIONS
>
APPROVE
```

Any prohibited behavior:

```text
REJECT entire candidate
```

rather than silently deleting an unsafe sentence and presenting the remainder as if the model had been fully safe.

Reason:

```text
unsafe candidate generation is itself evaluation evidence
```

Stage 08 needs to measure it.
