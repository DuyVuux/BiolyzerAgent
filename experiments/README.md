# Technical Experiments (`experiments/`)

> **Boundary Rule:** Code in `experiments/` is **strictly disposable and isolated**. It must **NEVER** be imported into production packages (`apps/`, `internal/`, `packages/`).

---

## 1. Purpose

The `experiments/` directory hosts targeted proofs-of-concept, performance benchmarks, and tool explorations across project stages. Each experiment tests an architectural hypothesis before decisions are codified.

---

## 2. Structure by Stage

As stages progress, subdirectories will be created:

```text
experiments/
├── stage-03/                # Ingestion PoC (PDF parsing, OCR, table extraction)
├── stage-04/                # Terminology & unit alignment experiments
├── stage-05/                # Longitudinal model & timeline experiments
├── stage-06/                # Retrieval & citation verification experiments
├── stage-07/                # Reasoning & deterministic safety gate experiments
├── stage-09/                # Eino pipeline benchmarks (planned)
├── stage-11/                # Chaos & circuit-breaking experiments (planned)
└── stage-12/                # Durability/worker experiments (conditional)
```

---

## 3. Experiment Lifecycle

1. **Hypothesis**: Reference an open ID from `docs/00-governance/ARCHITECTURE_HYPOTHESIS_REGISTER.md`.
2. **Implementation**: Self-contained script or executable.
3. **Outcome**: Document findings in a markdown report within the experiment folder.
4. **Resolution**: If successful, productionize clean domain logic in `internal/` (from Stage 9) under guidance of an ADR.
