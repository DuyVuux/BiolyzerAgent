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

## 2. Structure (to be materialized in Stage 8)

```text
evals/
├── datasets/          # Ground-truth benchmarks (synthetic/de-identified)
│   ├── extraction/    # Lab report extraction accuracy test cases
│   ├── normalization/ # LOINC, UCUM, and reference interval test cases
│   ├── evidence/      # Citation relevance and claim grounding datasets
│   └── safety/        # Adverse event, contraindicated advice, red-flag cases
├── rubrics/           # Multi-dimensional scoring rubrics (clinical correctness, tone)
├── scorers/           # Automated scorers (deterministic + LLM-as-a-judge)
├── harness/           # Runner to execute evaluations across model versions
└── reports/           # Evaluation execution results (historical benchmarks)
```

---

## 3. Contribution Policy

- All evaluation test samples must be strictly de-identified or synthetic.
- Eval reports committed to git must be consolidated summaries; raw per-token traces belong in local execution or ephemeral storage.
