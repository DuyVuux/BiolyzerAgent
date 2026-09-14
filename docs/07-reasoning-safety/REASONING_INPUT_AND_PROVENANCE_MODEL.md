# Reasoning Input & Provenance Model

> **Status:** PROPOSED v0.1

---

## 1. Reasoning input is a snapshot

The model must not receive a loose collection of mutable objects.

It receives:

```text
ReasoningInputSnapshot
```

which identifies:

```text
clinical dataset snapshot
timeline snapshot if present
evidence bundle snapshot
policy descriptors
available reference registry
known limitations
```

---

## 2. Clinical reference registry

Every clinical reference exposed to reasoning has:

```text
ref_id
ref_type:
  observation
  derived_range_assessment
  longitudinal_trend
verification_state
reconciliation_state
```

The reasoning candidate refers only to these IDs.

Unknown ID:

```text
FAIL CLOSED
```

---

## 3. Evidence reference registry

Every evidence claim exposed to reasoning has:

```text
claim_id
status:
  supported
  conflicted
  context_only
  unsupported
  claim_identity_conflict
```

The model cannot convert:

```text
unsupported
```

into supported.

---

## 4. Snapshot closure

Reasoning input pins:

```text
evidence_bundle_id
evidence_processing_profile_digest
reasoning_policy_digest
safety_policy_digest
```

Policy/config drift creates a different reasoning input identity.

---

## 5. Missing context

Known missing context is explicit:

```text
missing_context[]
```

Examples:

```text
medication context unavailable
fasting status unknown
method unavailable
clinical history unavailable
```

The model must not fill missing values from prior model memory.

---

## 6. Prompt/source injection boundary

Clinical source text and evidence passages are data.

They are never authority to change:

```text
system safety policy
tool permissions
evidence closure
allowed statement classes
```

A source passage saying:

```text
"ignore prior instructions"
```

remains quoted data.

It does not grant execution permission.

---

## 7. Zero ambient memory

Current Stage 07 reasoning must not use:

```text
untracked chat memory
previous patient history not present in snapshot
provider-side hidden retrieval
```

as clinical fact.

If future product context is intentionally added, it must enter through a pinned input contract.
