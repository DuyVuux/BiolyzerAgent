# Uncertainty, Conflict & Defer Policy

> **Status:** PROPOSED v0.1

---

## 1. Uncertainty is data

The system must preserve:

```text
unknown
missing
unverified
conflicted
reconciliation_required
```

It must not turn them into fluent certainty.

---

## 2. Reconciliation-required clinical data

If a candidate interpretation depends on a clinical fact marked:

```text
reconciliation_required
```

verdict:

```text
DEFER
```

The model may provide a limitation-only message.

---

## 3. Incomplete evidence

If evidence bundle is incomplete:

```text
measured/source facts may still be summarized safely
patient-specific bounded interpretation must DEFER
```

---

## 4. Conflicted evidence

A conflict is not a bug to hide.

Allowed:

```text
"The included evidence is conflicting..."
```

with explicit refs.

Rejected:

```text
definitive interpretation based on only one side
```

---

## 5. Missing context

If a bounded interpretation is made while the input snapshot lists relevant missing context:

```text
missing_context_acknowledged = true
```

is required.

Otherwise:

```text
REJECT
```

---

## 6. Candidate mapping

A terminology mapping marked:

```text
candidate
unmapped
```

cannot be repaired by model intuition.

Return limitation/defer instead.

---

## 7. Claim identity conflict

An EvidenceClaim marked:

```text
claim_identity_conflict
```

is never eligible for current reasoning.

Verdict:

```text
DEFER
```

or `REJECT` if the candidate attempts to use it.
