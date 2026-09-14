# Stage 06 — Evidence Engine Benchmark Results (v0.2 Hardened)

> **Status:** MEASURED SYNTHETIC BASELINE v0.2  
> **Limitation:** This validates evidence-domain mechanics, not real biomedical retrieval/NLI accuracy.

## Metrics

| Metric | Result |
|---|---:|
| `scenario_pass_rate` | `1.0` |
| `false_source_merge_rate` | `0.0` |
| `unsupported_claim_acceptance_rate` | `0.0` |
| `retracted_positive_support_rate` | `0.0` |
| `bundle_determinism` | `True` |
| `source_collision_fail_closed` | `True` |
| `claim_collision_fail_closed` | `True` |
| `conflict_preserved` | `True` |
| `late_retrieval_isolated` | `True` |
| `bundle_closure_enforced` | `True` |

## What this proves

The synthetic experiment proves the hardened domain mechanics can:

- keep retrieval retries separate from source identity;
- make same-source/same-content retrieval idempotent;
- fail closed on unexplained identity/content collision;
- preserve explicit versions;
- isolate partial retrieval;
- exclude retracted positive support;
- preserve supporting and contradicting evidence simultaneously;
- reject unrelated/unsupported citation relations;
- build deterministic frozen bundle identity independent of input ordering;
- produce a new bundle when retrieval policy or timeline provenance changes;
- **[v0.2]** isolate late retrieval results from mutating a frozen bundle (`EVID-018`);
- **[v0.2]** enforce idempotent claim re-extraction when proposition payload matches;
- **[v0.2]** fail closed on claim identity collisions with differing proposition payloads;
- **[v0.2]** enforce closed dependency scope via `EvidenceProcessingProfile` (`EVID-017`);
- **[v0.2]** separate raw binary artifact hash from canonical structured metadata digest.

## What this does not prove

It does not establish:

- production PubMed/Crossref retrieval accuracy;
- production full-text licensing/access behavior;
- biomedical claim extraction accuracy;
- biomedical entailment model accuracy;
- GRADE certainty;
- clinical recommendation safety.

Those remain separate gates.
