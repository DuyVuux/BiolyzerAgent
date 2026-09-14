# BioMarker Agent — Ingestion Failure Taxonomy

> **Status:** PROPOSED v0.1

---

## F-301 — NO_MACHINE_TEXT

**Example:** image-only PDF returns zero native text.

**Risk:** empty report silently accepted.

**Required behavior:** OCR fallback or explicit failure.

---

## F-302 — OCR_CHARACTER_SUBSTITUTION

Example structural pattern:

```text
timezone letter → digit
```

**Risk:** timestamp or identifier becomes wrong but syntactically plausible.

**Detection:** exact-field benchmark, source comparison, validation where possible.

---

## F-303 — OCR_IDENTITY_CORRUPTION

Example:

```text
subject identifier acquires whitespace
```

**Risk:** wrong subject linkage.

**Severity posture:** high; must not auto-trust.

---

## F-304 — TABLE_STRUCTURE_CORRUPTION

Separators/columns are lost or shifted.

**Risk:** result attaches to wrong test/range/flag.

**Required behavior:** parse failure or verification; no guessed realignment.

---

## F-305 — RESULT_TOKEN_CORRUPTION

Examples:

```text
1+ → 1
<5 → 5
0-2 → 02
```

**Risk:** semantic value changes.

**Required behavior:** raw source preservation + exact-field eval.

---

## F-306 — UNIT_CORRUPTION

Example:

```text
/HPF → /HPE
```

**Risk:** wrong normalization/comparison.

**Required behavior:** do not silently normalize invalid unit.

---

## F-307 — REFERENCE_RANGE_CORRUPTION

**Risk:** abnormal assessment wrong.

**Required behavior:** preserve raw, flag ambiguity.

---

## F-308 — SOURCE_FLAG_CORRUPTION

**Risk:** abnormal marker lost or invented.

**Required behavior:** source flag measured separately.

---

## F-309 — METADATA_DATE_CORRUPTION

**Risk:** wrong longitudinal ordering.

**Required behavior:** invalid/ambiguous date must not be silently coerced.

---

## F-310 — STRUCTURAL_VALID_SEMANTIC_WRONG

JSON Schema passes but extracted content is wrong.

**Lesson:**

```text
contract validation
≠
extraction correctness
```

---

## F-311 — UNSUPPORTED_LAYOUT

Parser cannot reliably identify fields.

**Required behavior:** explicit unsupported/verification state.

---

## F-312 — UNCALIBRATED_CONFIDENCE

Engine returns numeric confidence but relationship to critical-field correctness is unknown.

**Required behavior:** treat as feature/evidence, not clinical authority.
