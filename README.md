# BioMarker Agent

> **Clinical Biomarker Analysis, Longitudinal Tracking & Safe Clinical Intelligence**

## 1. Overview

BioMarker Agent is a specialized system designed to ingest diagnostic laboratory reports, extract and normalize biomarker observations, maintain longitudinal patient timelines, retrieve medical evidence, and generate safe, clinically-grounded analyses.

This repository follows a **Stage-Gated Polyglot Monorepo** architecture (TypeScript/React for frontend, Go for backend services, canonical JSON Schemas/OpenAPI contracts, and first-class evaluation harnesses).

Current Architecture Specification: [BIOMARKER_PROJECT_SKELETON_V0.1.md](./BIOMARKER_PROJECT_SKELETON_V0.1.md)

---

## 2. Project Status: Stage 0

The project is currently at **Stage 0** (Baseline Tooling, Workspace Orchestration & Governance). 

In accordance with our architecture principles, folders and components are materialized **only when justified by the active Stage**.

| Stage | Focus Area | Status |
|---|---|---|
| **Stage 0** | Root governance, toolchain baseline, docs structure | **IN PROGRESS / BASELINE** |
| **Stage 1** | Product context, intended use & safety envelope | Queued |
| **Stage 2** | Domain model & initial canonical contracts | Queued |
| **Stage 3–8** | Ingestion, normalization, evidence, safety & evals | Queued |
| **Stage 9** | Go production runtime & backend API | Queued |
| **Stage 14** | Web frontend & client package | Queued |
| **Stage 15** | Controlled ai-studio Platform integration | Queued |

See [MASTER_ROADMAP.md](./docs/00-governance/MASTER_ROADMAP.md) for full 16-stage roadmap details.

---

## 3. Architecture Principles

1. **Earned Complexity**: Do not prematurely introduce databases, message queues, workers, or microservices until concrete stage requirements demonstrate their need.
2. **Polyglot Monorepo**: Managed via `pnpm` workspace + `turbo` for unified task execution, with a single root Go module (introduced at Stage 9).
3. **Contract-First**: Machine-readable schemas in `contracts/` serve as canonical source-of-truth across languages.
4. **Evaluation-First**: `evals/` is a top-level citizen measuring clinical correctness and AI performance, distinct from software unit tests.
5. **Clinical Safety First-Class**: Clinical safety (`docs/05-safety/`) is treated as a distinct concern from technical security (`docs/04-security/`).

---

## 4. Getting Started

### Prerequisites
- **Node.js**: `>=22.0.0` (Pinned in `.node-version`)
- **pnpm**: `11.10.0`
- **Go**: `1.27+` (required from Stage 9)

### Setup
```bash
# Install workspace dependencies
pnpm install

# Run workspace checks
pnpm check
```

---

## 5. Repository Guide

- [CONTRIBUTING.md](./CONTRIBUTING.md) — Contribution guidelines, branch policy, and verification workflows.
- [AGENTS.md](./AGENTS.md) — Mandatory guidance and operational boundaries for AI coding agents.
- [docs/00-governance/](./docs/00-governance/) — Architectural governance, decision protocols, and reference ledgers.
- [experiments/](./experiments/) — Disposable, technical investigations and proofs-of-concept.
- [evals/](./evals/) — Benchmark datasets, clinical rubrics, and automated evaluators.
- [testdata/](./testdata/) — Synthetic and de-identified clinical test fixtures.
