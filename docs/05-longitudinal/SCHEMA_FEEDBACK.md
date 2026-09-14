# Stage 05 — Canonical Schema Feedback

> **Status:** ADDITIVE FEEDBACK / NO SILENT BREAKING CHANGE

---

## 1. Stage 05 finding

Safe duplicate/revision handling is much stronger when upstream exposes stable source-side identities.

Candidate future provenance fields:

```text
source_report_key
source_result_key
source_event_key
source_version_key
```

These are not invented identifiers.

They must come from source-system evidence when available.

---

## 2. Why current hash is insufficient

Document SHA-256 tells:

```text
same document bytes?
```

It does not necessarily tell:

```text
same clinical measurement event?
```

Two corrected report files have different hashes but may describe the same clinical event.

---

## 3. Why same value/time is insufficient

Two real measurements may produce:

```text
same analyte
same timestamp granularity
same value
```

Deduplicating them by similarity can erase real data.

---

## 4. Current decision

Do not modify Stage 02 schemas in this package.

Stage 06 does not require these fields.

Before production persistence, Stage 10 should revisit provenance contract based on actual source interfaces.

---

## 5. Timeline contract added

Stage 05 adds:

```text
contracts/schemas/clinical/longitudinal-timeline.schema.json
```

This is a derived-output contract and does not replace Stage 02 observation contract.
