# Stage 03 — Feedback to Canonical Schema

> **Status:** NO BREAKING CHANGE REQUIRED v0.1

---

## 1. Result

Synthetic characterization did **not** require a breaking change to Stage 02 canonical schemas.

The existing model successfully represented:

```text
quantity
ordinal
categorical
interval
comparator quantity
source range
source flag
source provenance
verification state
data-quality issues
```

---

## 2. Confirmed design choices

Stage 03 evidence strengthens:

```text
raw source must survive normalization
comparator must be first-class
interval must be first-class
negative must not mean missing
source locator is mandatory
mapping/verification uncertainty must remain explicit
```

---

## 3. Non-breaking future candidates

The following may become useful after broader corpus testing:

### Candidate A — Page-level text digest

Purpose:

```text
detect source-text drift
```

Not required yet.

### Candidate B — Explicit value-absent reason

Stage 02 intentionally deferred this.

Stage 03 synthetic corpus did not produce enough evidence to lock the shape.

### Candidate C — Structured bounding box coordinate convention

Current schema allows a 4-number bounding box but does not lock:

```text
pixel
normalized
PDF points
```

Actual OCR/parser integration must choose a convention before production.

---

## 4. Decision

Do not modify Stage 02 contracts from this Stage package.

Reason:

> No measured synthetic failure requires a breaking contract change yet.
