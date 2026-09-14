# Contributing to BioMarker Agent

Thank you for contributing to BioMarker Agent. This repository has strict governance standards to maintain domain clarity, clinical safety, and architectural integrity.

---

## 1. Core Engineering Principles

1. **Stage-Gated Materialization**: Never add directories, frameworks, databases, or runtime components that belong to future stages. Every directory and dependency must have a direct justification in the current active Stage.
2. **Zero Real Patient Data**: Never commit Protected Health Information (PHI) or real medical records. All test fixtures in `testdata/` must be completely synthetic or irreversibly de-identified.
3. **Canonical Contracts First**: API models and clinical schemas must be defined in `contracts/` before backend or frontend implementations.
4. **ADRs Required for Architecture Shifts**: Any structural change (introducing a new database, queue, external service, or top-level package) requires an Architecture Decision Record (ADR) in `docs/07-decisions/adr/`.

---

## 2. Development Workflow

### Prerequisites
- Node.js `22.x` (see `.node-version`)
- pnpm `11.10.0`
- Go `1.27+` (when Stage 9 begins)

### Setup & Commands
```bash
# Install dependencies
pnpm install

# Run all linting, typechecking, and tests
pnpm check

# Run specific tasks
pnpm lint
pnpm typecheck
pnpm test
```

---

## 3. Pull Request Guidelines

1. **Branch Naming**:
   - `feat/stage-XX-<feature-name>`
   - `fix/<issue-name>`
   - `docs/<topic-name>`
   - `experiment/stage-XX-<name>`
2. **Verification Checklist Before Submitting**:
   - [ ] `pnpm check` passes cleanly with zero errors.
   - [ ] No unapproved dependencies added to `package.json` or `go.mod`.
   - [ ] No sensitive credentials, tokens, or environment files committed.
   - [ ] Relevant documentation updated in `docs/`.
   - [ ] If changing schemas, validation tests updated.

---

## 4. Code Ownership & Boundaries

- `apps/` — Deployable entrypoints. Must remain thin composition roots.
- `internal/` — Core business and domain logic (Go backend, from Stage 9). Platform adapters strictly separated from clinical domains.
- `contracts/` — Shared machine-readable contracts (JSON Schema, OpenAPI).
- `evals/` — Dedicated to AI and clinical quality metrics. Distinct from unit tests.
- `experiments/` — Disposable prototypes. Code in `experiments/` must **never** be imported into production code (`apps/` or `internal/`).
