# BioMarker Agent — Master Roadmap (16 Stages)

> **Document Type:** Governance Specification  
> **Source:** [BIOMARKER_PROJECT_SKELETON_V0.1.md](../../BIOMARKER_PROJECT_SKELETON_V0.1.md)  
> **Rule:** Folders and runtime dependencies are only materialized when the corresponding Stage is active.

---

## 1. 16-Stage Evolution Matrix

| Stage | Stage Name | Focus Area | Deliverables & Artifacts | Status |
|---|---|---|---|---|
| **0** | **Root Governance & Tooling** | Workspace baseline, governance, toolchain | Root config, `docs/00-governance/`, `experiments/`, `evals/`, `testdata/` | **IN PROGRESS** |
| **1** | **Product Context & Safety Envelope** | Clinical problem definition, boundaries | `docs/01-product/` (Use cases, intended use, non-goals, risk bounds) | Queued |
| **2** | **Domain Modeling & Schemas** | Clinical concepts, observations, reports | `docs/02-domain/`, first `contracts/schemas/` | Queued |
| **3** | **Ingestion Proof-of-Concept** | Parsing lab documents (PDF, text, OCR) | `experiments/stage-03-ingestion/`, synthetic fixtures in `testdata/` | Queued |
| **4** | **Normalization & Terminology** | Units, reference intervals, LOINC/SNOMED | `experiments/stage-04-normalization/`, normalization contracts | Queued |
| **5** | **Longitudinal Timeline** | Tracking patient biomarker trends across time | Timeline domain specs, state model | Queued |
| **6** | **Evidence Retrieval & Provenance** | Grounded medical claims, citation retrieval | `experiments/stage-06-evidence/`, evidence contracts | Queued |
| **7** | **Clinical Reasoning & Safety Gates** | Deterministic safety checking, guardrails | `experiments/stage-07-reasoning-safety/`, safety specifications | Queued |
| **8** | **Executable Clinical Evaluations** | AI and clinical quality measurement | `evals/datasets/`, `evals/scorers/`, `evals/harness/` | Queued |
| **9** | **Go Production Runtime & API** | Minimum backend service, Eino evaluation | `go.mod`, `apps/api/`, `internal/` bounded contexts | Queued |
| **10** | **Persistence & State Store** | Database adapter, migrations | Relational / document storage (only if needed), `infra/local/` | Queued |
| **11** | **Failure Modes & Recovery** | Circuit breakers, retries, degradation | `experiments/stage-11-failure-recovery/`, integration tests | Queued |
| **12** | **Durability & Async Workers** | Long-running tasks, durable execution | `apps/worker/` (only if background orchestration is justified) | Queued |
| **13** | **Reproducibility & Attestation** | Execution provenance, audit logs | Versioning contracts, execution hashes | Queued |
| **14** | **User Interface & API Client** | Frontend application & typed client | `apps/web/` (React/Vite), `packages/api-client/`, OpenAPI spec | Queued |
| **15** | **Mia Platform Integration** | Controlled integration with Mia ecosystem | Mia adapter, deployment manifests, operational runbooks | Queued |

---

## 2. Stage Quality Gates

Before advancing from Stage $N$ to Stage $N+1$, the following criteria must be satisfied:
1. All stage-specific documentation is reviewed and committed.
2. If code was written, tests pass and verify all required behavior.
3. No speculative architecture for future stages was introduced.
4. An ADR is recorded if an architectural trade-off was made.
