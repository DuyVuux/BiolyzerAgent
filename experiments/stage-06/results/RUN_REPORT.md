# Stage 06 Experiment Run Report (v0.2 Hardened)

## Metrics

- `scenario_pass_rate`: `1.0`
- `false_source_merge_rate`: `0.0`
- `unsupported_claim_acceptance_rate`: `0.0`
- `retracted_positive_support_rate`: `0.0`
- `bundle_determinism`: `True`
- `source_collision_fail_closed`: `True`
- `claim_collision_fail_closed`: `True`
- `conflict_preserved`: `True`
- `late_retrieval_isolated`: `True`
- `bundle_closure_enforced`: `True`

## Scenarios

- `retry_does_not_duplicate_source`: **PASS**
- `same_identity_same_digest_idempotent`: **PASS**
- `same_identity_different_digest_conflict`: **PASS**
- `explicit_source_version_preserved`: **PASS**
- `partial_attempt_not_verified`: **PASS**
- `retracted_source_not_positive_support`: **PASS**
- `supported_claim_linked`: **PASS**
- `contradiction_preserved`: **PASS**
- `unrelated_citation_not_entailed`: **PASS**
- `unsupported_claim_rejected`: **PASS**
- `retrieval_order_bundle_deterministic`: **PASS**
- `policy_change_new_bundle`: **PASS**
- `timeline_change_new_bundle`: **PASS**
- `late_retrieval_cannot_mutate_frozen_bundle`: **PASS**
- `claim_identity_same_payload_idempotent`: **PASS**
- `claim_identity_different_payload_conflict`: **PASS**
- `processing_profile_change_yields_new_bundle`: **PASS**
- `raw_artifact_digest_independent_from_envelope`: **PASS**
