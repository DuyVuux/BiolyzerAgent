# Stage 04 Handoff — Normalization & Clinical Terminology

> **Status:** CANDIDATE COMPLETE WITH SYNTHETIC-CATALOG LIMITATION  
> **Next Stage:** 05 — Longitudinal Biomarker Model

---

## 1. Stage 04 established

```text
local identity ≠ canonical identity
alias match ≠ validated mapping
source unit ≠ normalized UCUM unit
unit normalization ≠ numeric conversion
same analyte name ≠ comparable observation
```

---

## 2. Mapping state

Kept from Stage 02:

```text
unmapped
candidate
validated
not_applicable
```

Ambiguous method/scale/specimen must remain candidate/unmapped.

---

## 3. Comparability classes

```text
EXACT_COMPARABLE
CONVERTIBLE_COMPARABLE
RELATED_NOT_COMPARABLE
INDETERMINATE
```

Stage 05 must use these semantics before creating longitudinal series.

---

## 4. Measured synthetic experiment

```text
mapping status accuracy       PASS
validated code exactness      PASS
false validation              PASS (0 false validations)
unit normalization            PASS
safe conversion               PASS
comparability classification  PASS
Stage-03 no-guess check       PASS
```

Detailed machine outputs live in:

```text
experiments/stage-04/results/
```

---

## 5. Production limitations

Stage 04 does not approve:

```text
full LOINC coverage
production local-code dictionary
terminology server
fuzzy/LLM auto-mapping
production unit conversion engine
cross-method trend merging
```

---

## 6. Stage 05 may now model

```text
observation series identity
chronology
same-subject grouping
duplicate semantics
comparable-series construction
trend computation boundaries
snapshot/version semantics
```

Stage 05 must not merge observations classified as `RELATED_NOT_COMPARABLE` or `INDETERMINATE` without explicit later policy.

---

## 7. Gate

```text
SYNTHETIC_MAPPING_GATE            = PASS
FALSE_VALIDATION_GATE             = PASS
UNIT_NORMALIZATION_GATE           = PASS
SAFE_CONVERSION_GATE              = PASS
COMPARABILITY_GATE                = PASS
STAGE03_NO_GUESS_GATE             = PASS
REAL_LOCAL_TERMINOLOGY_GATE       = NOT EXECUTED
PRODUCTION_TERMINOLOGY_GATE       = BLOCKED_BY_NO_APPROVED_LOCAL_MAPPING_CORPUS
ROOT_CONFIG_INTEGRITY             = PASS_BY_PACKAGE_CONTENT
PNPM_CHECK                        = NOT_EXECUTED
HUMAN_LEARNING_GATE               = NOT EXECUTED_BY_AI
```
