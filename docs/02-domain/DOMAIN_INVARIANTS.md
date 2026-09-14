# BioMarker Domain Invariants

> **Status:** PROPOSED NORMATIVE BASELINE v0.1  
> **Stage:** 02

## DATA-001 — Raw source is preserved
Normalized representation không được xóa source representation.

## DATA-002 — Document, report and observation are distinct
`SourceDocument ≠ LabReport ≠ BiomarkerObservation`.

## DATA-003 — Observation is not diagnosis
Canonical observation không chứa autonomous diagnosis field.

## DATA-004 — Mixed result types are first-class
Canonical value không numeric-only.

## DATA-005 — Comparator is data
`<5` không được silently biến thành `5`.

## DATA-006 — Interval is data
`0–2` không được silently biến thành midpoint.

## DATA-007 — Negative is not missing
Categorical/ordinal negative result không serialize thành absence.

## DATA-008 — Missing is not normal
Không có observation không chứng minh normal result.

## DATA-009 — Unknown remains unknown
Không infer missing specimen/method/date/context nếu source không support.

## DATA-010 — Source range has provenance
Reference range phải trace về source.

## DATA-011 — Source flag and derived flag are separate
Lab flag không merge với system-computed assessment.

## DATA-012 — Clinical risk flag is separate again
Critical/escalation không dùng chung semantics với simple range comparison.

## DATA-013 — Local identity survives canonical mapping
LOINC/canonical code không overwrite source/local test name.

## DATA-014 — Candidate mapping is not validated mapping
Downstream phải phân biệt mapping status.

## DATA-015 — Source unit survives normalization
UCUM mapping không overwrite source unit.

## DATA-016 — Dataset snapshot has provenance closure
Mọi observation trong snapshot phải reference report/source artifact hợp lệ.

## DATA-017 — IDs are locators, not authority
Possession của IDs không chứng minh permission.

## DATA-018 — Synthetic data only in Stage 02 artifacts
Không real patient data.

## DATA-019 — Clinical summary is downstream
AI/physician summary không nằm trong canonical observation schema.

## DATA-020 — Storage implementation is not domain semantics
Canonical model không phụ thuộc PostgreSQL/JSONB/object storage/runtime.
