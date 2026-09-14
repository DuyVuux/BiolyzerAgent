# Stage 04 Experiment Run Report

## Summary

| Metric | Value |
|---|---:|
| mapping_status_accuracy | 1.0 |
| validated_code_exact_accuracy | 1.0 |
| false_validation_rate | 0.0 |
| unit_normalization_accuracy | 1.0 |
| safe_conversion_accuracy | 1.0 |
| comparability_accuracy | 1.0 |
| stage03_unknown_label_no_guess | True |

## Interpretation

- Ambiguous method cases remain `candidate` instead of being force-validated.
- Unknown Stage-03 synthetic labels remain non-validated.
- Exact unit conversions are allowlisted; chemistry-specific conversion is rejected.
- Comparability requires validated identity before unit conversion is considered.
