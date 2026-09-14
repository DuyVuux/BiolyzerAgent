# Stage 08 Evaluation Run Report

## Provenance & Integrity (RFC 8785)

- `run_id`: `eval-9680905d2574dafb`
- `dataset_digest`: `1ca0b4800a946b667bfe93c907ec2ddd300da67131a91dbd959a6918d245cd56`
- `manifest_digest`: `de4f2b032d27b17523ef7f03d20b3c68c13bdc6d82d340397559b961d52306bb`
- `attestation_verified`: `True`

## Metrics

- `case_count`: `24`
- `exact_verdict_accuracy`: `1.0`
- `unsafe_case_count`: `16`
- `unsafe_escape_count`: `0`
- `unsafe_escape_rate`: `0.0`
- `unsafe_escape_wilson95`: `(0.0, 0.1936076805344365)`
- `unsafe_escape_zero_failure_upper95`: `0.17074972298248092`
- `safe_case_count`: `8`
- `safe_false_reject_count`: `0`
- `safe_false_reject_rate`: `0.0`
- `confusion_matrix`: `{'tp': 16, 'fp': 0, 'tn': 8, 'fn': 0}`
- `metamorphic_pass_rate`: `1.0`
- `zero_failure_n_for_upper95_below_5pct`: `59`
- `zero_failure_n_for_upper95_below_1pct`: `299`
- `zero_failure_n_for_upper95_below_0_1pct`: `2995`

## Metamorphic Relations

- `total_relations`: `7`
- `passed_relations`: `7`

## Interpretation

- Observed unsafe escapes are 0/16, but the one-sided 95% zero-failure upper bound is 0.1707; this is not proof of zero population risk.
- This run evaluates Stage-07 synthetic policy cases, not a production LLM.
