# Stage 05 — Longitudinal Benchmark Results

> **Status:** MEASURED SYNTHETIC BASELINE v0.2  
> **Limitation:** Synthetic lineage keys and timestamps; not a production clinical-data accuracy claim.

## Metrics (v0.2 Benchmark Run)

| Metric | Result |
|---|---:|
| `scenario_pass_rate` | `1.0` (15/15 cases) |
| `false_merge_rate` | `0.0` |
| `snapshot_determinism` | `True` |
| `cross_subject_rejection` | `True` |
| `duplicate_resolution` | `True` |
| `revision_selection` | `True` |
| `chronology_ordering` | `True` |
| `comparability_split` | `True` |
| `candidate_mapping_exclusion` | `True` |
| `identity_collision_idempotent_duplicate` | `True` |
| `identity_collision_hard_conflict` | `True` |
| `reconciliation_required_exclusion` | `True` |
| `trend_boundary_cases` | `True` |

## Interpretation

The experiment demonstrates that the proposed v0.2 model can:

- sort by clinical time despite out-of-order arrival (domain-level chronology);
- collapse exact duplicate imports;
- select a corrected representation without creating a new measurement point;
- preserve distinct same-value/same-time clinical events;
- merge exact/approved-convertible quantity units;
- split different canonical methods/codes;
- exclude candidate terminology from validated series;
- reject mixed-subject input;
- compute only value-kind-safe trend features;
- handle identity collision with same payload via idempotent duplicate (`duplicate_collapsed`);
- fail closed on identity collision with different payload (`unresolved_conflict` / LONG-016);
- isolate incomplete/ambiguous observations into `reconciliation_required` without polluting active series;
- rebuild the same snapshot identity from the same logical inputs independent of input order.

## Non-conclusion

The benchmark does **not** prove real upstream deduplication correctness because the source-event identity in this corpus is synthetic.
Production lineage remains dependent on actual source-system identifiers and correction semantics (Stage 10).
