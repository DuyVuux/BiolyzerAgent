# BioMarker Agent — Ingestion Requirements

> **Status:** PROPOSED REQUIREMENTS v0.1  
> **Derived from:** Stage 03 synthetic characterization

---

## ING-001 — Detect machine-readable text

Before selecting parsing path, ingestion must determine whether usable page text exists.

No assumption:

```text
PDF = text PDF
```

---

## ING-002 — OCR is an explicit fallback path

Image-only PDF must not silently produce empty report.

Allowed outcomes:

```text
OCR fallback
OR
explicit unsupported/unreadable error
```

---

## ING-003 — Preserve source artifact identity

Every canonical observation must trace to:

```text
source_document_id
```

---

## ING-004 — Preserve source locator

At minimum for Stage 03:

```text
page
raw line/text
```

Future extractor may add coordinates.

---

## ING-005 — Extract report metadata separately

Metadata fields are evaluated independently from observation rows.

At minimum:

```text
subject_ref candidate
specimen
effective/collection time
issued time
report status when available
```

---

## ING-006 — Extract observation fields independently

At minimum:

```text
local test name
source result
unit
source reference range
source flag
```

---

## ING-007 — Preserve raw result before typing

Pipeline:

```text
raw result text
→ value-kind classification
→ structured value
```

not:

```text
structured guess
→ discard raw
```

---

## ING-008 — Value-kind classification is measured

Required classes from Stage 02:

```text
quantity
interval
ordinal
categorical
text
```

Stage 03 corpus exercises first four.

---

## ING-009 — Comparator is first-class

```text
<5
```

must preserve `<`.

---

## ING-010 — Unit is not inferred silently

If unit is not present or ambiguous:

```text
unknown / issue
```

Do not infer from test name alone during ingestion.

---

## ING-011 — Source range is not replaced

Extraction preserves source range.

Generic knowledge cannot substitute missing source range in ingestion.

---

## ING-012 — Source flag is source assertion

`ABN`, `H`, `L`, etc. are preserved as source interpretation.

No diagnosis inference.

---

## ING-013 — Structural validation is mandatory but insufficient

Every candidate canonical dataset must pass contract validation before downstream use.

Additional semantic completeness checks are still required.

---

## ING-014 — Empty native extraction must not be success

Zero/near-zero machine text on a non-empty document must trigger fallback or explicit failure.

---

## ING-015 — No silent parser recovery

If row structure is ambiguous:

```text
record issue
→ require verification
```

Do not invent field alignment.

---

## ING-016 — Confidence is evidence, not authority

OCR/parser confidence may be stored as measurement.

It must not by itself authorize clinical use until calibrated.

---

## ING-017 — Failure must be typed

Candidate classes:

```text
NO_MACHINE_TEXT
OCR_UNAVAILABLE
OCR_LOW_QUALITY
METADATA_PARSE_FAILURE
ROW_PARSE_FAILURE
VALUE_KIND_AMBIGUOUS
UNIT_AMBIGUOUS
REFERENCE_RANGE_AMBIGUOUS
SOURCE_FLAG_AMBIGUOUS
CONTRACT_INVALID
SEMANTIC_COMPLETENESS_FAILURE
```

---

## ING-018 — Development data remains synthetic

Stage 03 package contains no real patient data.

---

## ING-019 — Parser implementation remains experimental

Current Python code is not production parser.

No downstream component may treat it as approved production implementation.

---

## ING-020 — Production threshold requires representative evaluation

No auto-accept threshold may be locked from this synthetic benchmark alone.
