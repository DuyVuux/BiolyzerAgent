# Stage 07 — Reasoning & Clinical Safety Benchmark Results

> **Status:** MEASURED SYNTHETIC SAFETY-HARNESS BASELINE v0.1  
> **Limitation:** This validates deterministic safety-gate mechanics against synthetic reasoning candidates. It does not establish production model clinical reasoning quality.

## Metrics

| Metric | Result |
|---|---:|
| `scenario_pass_rate` | `1.0` |
| `grounded_allowed_acceptance_rate` | `1.0` |
| `prohibited_behavior_escape_rate` | `0.0` |
| `unsupported_statement_acceptance_rate` | `0.0` |
| `ambient_action_escape_rate` | `0.0` |
| `conflict_nondisclosure_acceptance_rate` | `0.0` |
| `critical_policy_escape_rate` | `0.0` |
| `unverified_clinical_fact_escape_rate` | `0.0` |
| `approved_output_review_basis_complete` | `True` |
| `safety_decision_determinism` | `True` |


## Covered safety behaviors

The synthetic benchmark covers:

```text
grounded measured fact
grounded deterministic derived fact
supported evidence context
bounded interpretation

diagnosis rejection
treatment rejection
dose-change rejection
emergency-triage rejection

unknown clinical reference
unsupported evidence
hidden evidence conflict
disclosed evidence conflict

incomplete evidence
reconciliation-required clinical input
candidate terminology
unverified measured fact

ambient retrieval/tool requests
source instruction attempting to grant tool access
evidence-claim identity collision

missing-context acknowledgement
patient-specific causal overclaim

source-provided critical flag with no approved escalation policy
independent physician-review basis in safe output
```

## What this proves

```text
SAFETY_GATE_MECHANICS = PASS_SYNTHETIC
```

It shows that the current deterministic harness can enforce the encoded safety contract on structured candidates.

## What this does not prove

It does not establish:

```text
production LLM clinical reasoning accuracy
safety-gate sensitivity/specificity on natural model outputs
biomedical hallucination rate
clinical usefulness
physician acceptance
critical-value workflow validity
regulatory classification
```

Those become empirical Stage-08 evaluation requirements.
