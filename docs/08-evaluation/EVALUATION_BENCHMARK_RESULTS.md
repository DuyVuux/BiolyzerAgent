# Stage 08 — Evaluation Benchmark Results

> **Status:** MEASURED SYNTHETIC EVALUATOR BASELINE v0.1  
> **Important:** This evaluates Stage-07 synthetic policy fixtures through the actual Stage-07 harness. It is **not** a production LLM benchmark.

## Measured results

```text
case_count                       = 24
exact_verdict_accuracy           = 1.0
unsafe_case_count                = 16
unsafe_escape_count              = 0
unsafe_escape_rate               = 0.0
safe_case_count                  = 8
safe_false_reject_count          = 0
safe_false_reject_rate           = 0.0
metamorphic_pass_rate            = 1.0 (7/7 relations)
manifest_attestation_verified    = true (RFC 8785 JCS + SHA-256)
ast_boundary_checks_passed       = true (no forbidden imports, no eval/exec)
```

## Statistical interpretation

Observed unsafe escapes:

```text
0 / 16
```

One-sided 95% zero-failure upper bound:

```text
0.1707
```

Therefore:

```text
observed 0% escape
≠
proven 0% population risk
```

Sample-size planning with zero observed failures:

```text
upper95 < 5%   → n >= 59
upper95 < 1%   → n >= 299
upper95 < 0.1% → n >= 2995
```

These are statistical planning values, not approved clinical release thresholds.

## Scope limitation

This run proves:

```text
Stage-08 evaluator mechanics
statistical reporting
Stage-07 replay integration
metamorphic test mechanics
```

It does not prove:

```text
production model quality
clinical usefulness
real-world safety
```
