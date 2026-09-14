# Clinical & AI Quality Evaluations (`evals/`)

> **Boundary Rule:** `evals/` is a **top-level citizen** dedicated to measuring clinical correctness, extraction precision, and AI safety. It is separate from software unit and integration tests.

---

## 1. Why `evals/` is not `tests/`

```text
Software Correctness (tests/)    ≠    Clinical & AI Quality (evals/)
- Does the code run?                  - Is the extracted lab value accurate?
- Does the API return HTTP 200?       - Are clinical claims grounded in evidence?
- Does the parser crash on EOF?       - Does the system flag dangerous contraindications?
- Deterministic pass/fail             - Probabilistic, rubric-scored, benchmark-driven
```

---

## 2. Directory Structure

```text
evals/
├── stage-08/          # Materialized Stage 08: Evaluation & Quality Architecture
│   ├── results/       # EvaluationRun artifacts, metrics, slices, metamorphic results
│   ├── tests/         # Unit tests for statistical helpers & metamorphic evaluator
│   ├── metrics.py     # Multi-dimensional metric computation & safety confusion matrix
│   ├── metamorphic.py # Metamorphic relation transformations (MR-01 to MR-05)
│   ├── stats.py       # Wilson CI, exact zero-failure upper bound, Cohen's kappa
│   ├── run_evaluation.py # Evaluation runner replaying Stage-07 fixtures against gold labels
│   └── README.md
```

### Running Stage 08 Evaluations

```bash
# Run unit tests for statistical helpers & evaluator logic
python3 -m unittest discover -s evals/stage-08/tests -v

# Execute full evaluation replay and produce benchmark artifacts
python3 evals/stage-08/run_evaluation.py --repo-root .
```

---

## 3. Contribution Policy

- All evaluation test samples must be strictly de-identified or synthetic.
- Eval reports committed to git must be consolidated summaries; raw per-token traces belong in local execution or ephemeral storage.
