# Stage 08 — ai-studio Reference Reconciliation

> **Method:** BioMarker evaluation design first → ai-studio reference second.

The available architecture/history indicates ai-studio already values:

```text
contract tests
integration tests
security/isolation tests
failure injection
idempotency/replay verification
deterministic harnesses
version-pinned manifests
```

## KEEP

```text
testable invariants
failure-first scenarios
reproducible manifests
negative security tests
explicit PASS/FAIL/NOT EXECUTED evidence
```

## ADAPT

```text
runtime failure-injection mindset
→ clinical/evidence/safety red-team evaluation (MR-01 to MR-07)

manifest pinning & RFC 8785 JCS attestation
→ EvaluationRun provenance & tamper-proof cryptographic dataset digests

AST boundary scanning & mock elimination
→ static analysis forbidding premature runtime imports, dynamic eval/exec, and tautological assertions

candidate adapter fairness
→ same frozen cases across model candidates with anti-circular oracle guardrails
```

## REJECT

```text
runtime throughput as clinical quality metric
one global pass score
circular assertions / pseudo-oracles (e.g., verifying presence of arbitrary non-empty string as success)
```

## DEFER

```text
distributed load/fencing/worker evaluation (DBOS, PostgreSQL triggers, Redis, Celery)
```

until runtime stages (Stages 09-12) make those mechanisms real.

---

# Implemented Architectural Upgrades (Post-Survey)

Based on the deep code survey of `ai-studio`, the following upgrades have been implemented in `evals/stage-08/`:

1. **RFC 8785 JSON Canonicalization Scheme (JCS) & Attestation**:
   - Implemented [`evals/stage-08/canonical.py`](file:///workspace/projects/MialyzerAgent/evals/stage-08/canonical.py).
   - Guarantees deterministic key ordering, float/separator formatting, SHA-256 digest computation, and digital signature/attestation verification.

2. **AST-Level Static Boundary & Anti-Tautology Verification**:
   - Implemented [`evals/stage-08/tests/test_ast_boundaries.py`](file:///workspace/projects/MialyzerAgent/evals/stage-08/tests/test_ast_boundaries.py).
   - Prevents forbidden imports (`apps`, `redis`, `dbos`, `celery`, `requests`, `urllib`).
   - Prevents dangerous dynamic evaluation (`eval`, `exec`).
   - Analyzes test ASTs to reject trivial/tautological assertions (`self.assertEqual('a', 'a')`).

3. **Metamorphic Safety Red-Teaming (MR-01 to MR-07)**:
   - Expanded metamorphic relations with `MR-06` (ambient tool invocation injection -> `REJECT`) and `MR-07` (policy closure digest tamper -> `DEFER`).
   - Hardened `experiments/stage-07/harness.py` to ensure input closure gate G0 violations correctly defer evaluation.
   - Evaluated across 24 synthetic cases and 7 metamorphic relations with 100% pass rate.

4. **Anti-Circular Oracle Guardrails**:
   - Added explicit verification in `test_evaluator.py` ensuring ungrounded statements with invalid or hallucinated references cannot falsely pass evaluation.
