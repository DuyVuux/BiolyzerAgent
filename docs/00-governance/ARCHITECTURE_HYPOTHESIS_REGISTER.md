# Architecture Hypothesis Register

> **Purpose:** Tracks architectural hypotheses that must be empirically tested during the project's evolution rather than assumed upfront.

---

## Registered Hypotheses

| ID | Hypothesis | Target Stage | Verification Method | Status |
|---|---|---|---|---|
| **HYP-01** | Multi-page PDF lab reports can be parsed to structured observations with >95% precision without requiring an external proprietary OCR platform. | Stage 3 | Benchmark on `testdata/synthetic/lab-reports/` vs ground truth in `evals/datasets/extraction/`. | OPEN |
| **HYP-02** | Terminology and unit normalization (LOINC / UCUM) can be achieved with a deterministic alias dictionary backed by LLM disambiguation fallback. | Stage 4 | Normalization evaluation harness in `evals/datasets/normalization/`. | OPEN |
| **HYP-03** | A single root Go module is sufficient for the entire backend surface and avoids multi-module coordination overhead. | Stage 9 | Dependency graph analysis and build times during API creation. | OPEN |
| **HYP-04** | ByteDance's Eino framework provides sufficient composability for our Go clinical agent pipeline without requiring Python runtime services. | Stage 9 | Pipeline latency, memory profile, and error-handling benchmarks. | OPEN |
| **HYP-05** | Relational SQL schema with JSONB support is adequate for patient longitudinal timelines without introducing specialized time-series databases. | Stage 10 | Query latency benchmark on longitudinal aggregations over 1,000 synthetic patient histories. | OPEN |
| **HYP-06** | Durable execution runtimes (e.g. DBOS, Temporal) are only justified if pipeline latency or step recovery requirements exceed standard idempotency patterns. | Stage 12 | Failure-injection and retry experiments in `experiments/stage-11-failure-recovery/`. | OPEN |
| **HYP-07** | Clinical claim grounding can be deterministically verified against extracted biomarker observations and PubMed citations before presentation. | Stage 7 | Safety benchmark in `evals/datasets/safety/`. | OPEN |
