# Claim Entailment & Conflict Policy

> **Status:** PROPOSED v0.1

---

## 1. Claim-source relation

Every claim-source passage relation is one of:

```text
supports
contradicts
context_only
not_entailed
```

Only `supports` can count as positive support.

---

## 2. Citation validity is not enough

A citation can be:

```text
real
relevant topic
high-quality publication
```

and still fail to support the exact sentence.

Therefore:

```text
citation exists
≠
claim entailed
```

---

## 3. Claim ledger

Example:

```text
Claim C1
  supported_by: S1:P2, S4:P1
  contradicted_by: S7:P3
  context_only: S8:P1
```

The claim ledger must preserve disagreement.

---

## 4. Scope matching

Entailment must respect:

```text
population
measurement/test
outcome
direction
time horizon
study context
```

A source about a different population may be relevant context but not direct support.

---

## 5. Synthetic experiment

Stage 06 uses explicit structured proposition keys in synthetic passages.

Purpose:

```text
validate ledger mechanics
```

Not:

```text
claim production-grade biomedical NLI accuracy
```

Production entailment model/rules must be evaluated in Stage 08.

---

## 6. Unsupported claim

A claim with zero supporting relations:

```text
cannot enter selected verified claim ledger
```

It may be retained as:

```text
rejected candidate claim
```

for audit.

---

## 7. Contradiction

Support + contradiction:

```text
conflicted claim
```

Do not collapse to majority vote.

---

## 8. Retraction

A retracted source cannot be counted as positive support.

Its relation may remain stored for history/audit, marked unusable for active support.

---

## 9. Claim Identity Collision Semantics (EVID-019)

Re-extracting claims within the same bundle must observe strict collision semantics:

- **Same logical claim_id + same proposition payload:**
  Idempotent replay (returns canonical claim without duplication).
- **Same logical claim_id + different proposition payload:**
  `CLAIM_IDENTITY_CONFLICT` — fail closed. The conflicting claim is marked with status `claim_identity_conflict`, isolated from active bundle selection, and recorded in the audit conflict ledger.

