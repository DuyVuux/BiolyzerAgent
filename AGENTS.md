# AI Agent Operational Guidelines (`AGENTS.md`)

> **Audience**: AI Coding Agents & Pair-Programming LLMs interacting with this repository.

---

## 1. Project Identity

This repository is **BioMarker Agent**, an intelligent clinical biomarker analysis system. It processes unstructured lab reports, normalizes clinical observations against terminology standards, tracks longitudinal trends, cites medical evidence, and provides deterministic safety-gated clinical insights.

Architecture Specification: [BIOMARKER_PROJECT_SKELETON_V0.1.md](./BIOMARKER_PROJECT_SKELETON_V0.1.md)

---

## 2. What Must Be Read First

Before generating, editing, or refactoring code in any stage, you MUST read:
1. [BIOMARKER_PROJECT_SKELETON_V0.1.md](./BIOMARKER_PROJECT_SKELETON_V0.1.md) — Fundamental architecture rules and stage evolution.
2. [docs/00-governance/MASTER_ROADMAP.md](./docs/00-governance/MASTER_ROADMAP.md) — The 16-stage roadmap and boundary checklist.
3. [docs/00-governance/SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md](./docs/00-governance/SOURCE_AUTHORITY_AND_CONFLICT_PROTOCOL.md) — Conflict resolution order.

---

## 3. Canonical Sources of Truth

1. **Human & Clinical Documentation** (`docs/`): Defines product scope, clinical safety rules, and architecture bounds.
2. **Machine Contracts** (`contracts/`): Canonical source for schemas (JSON Schema, OpenAPI, FHIR).
3. **Stage-Gated Code** (`apps/`, `internal/`): Must conform to `contracts/` and `docs/`. Implementation code is NEVER canonical over specifications.

---

## 4. What Must NEVER Be Assumed

- **NEVER assume future infrastructure**: Do NOT proactively generate code or configs for Redis, PostgreSQL, DBOS, Celery, Kafka, Docker, Kubernetes, or microservices until the specific Stage authorises it.
- **NEVER create empty placeholder directories**: Materialize folders only when they contain actual, functional files.
- **NEVER import `experiments/` into production code**: Code in `experiments/` is disposable and technical only.
- **NEVER treat clinical safety as just prompt engineering**: Deterministic safety gates, claim grounding, and risk bounds are mandatory.
- **NEVER use `latest` in package manifests**: Always pin exact versions for dependencies.

---

## 5. Where Code Can Be Created

- `apps/`: Deployable applications (only when stage gate opens).
- `internal/`: Go domain implementations (Stage 9+). Domain boundaries must be observed.
- `packages/`: Shared JS/TS utility libraries (only when multiple consumers exist).
- `contracts/`: Machine-readable schemas and specifications.
- `evals/`: Evaluators, clinical benchmarks, and scoring harnesses.
- `experiments/`: Standalone proof-of-concept scripts.
- `tools/`: Build, check, or fixture generation tools.

---

## 6. Verification Commands

Always run and verify these commands before concluding any task:
```bash
# Full repository integrity check
pnpm check

# Fast individual checks
pnpm lint
pnpm typecheck
pnpm test
```

---

## 7. Strict Data Safety & Privacy Rules

- **Zero Real Protected Health Information (PHI)**: Absolutely NO real patient data, medical record numbers, patient names, dates of birth, or clinical notes may be committed, cached, or logged.
- **Test Fixtures**: Only synthetic, de-identified datasets in `testdata/synthetic/` are permitted.
- **Secrets & Credentials**: Never hardcode or commit API keys, tokens, or environment credentials. Use `.env.example` for structural keys only.
