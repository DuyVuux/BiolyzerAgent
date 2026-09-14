# Mia Reference Ledger

> **Purpose:** Tracks components and architectural patterns from the Mia Reference Architecture (`ai-studio`), classifying each as **KEEP**, **ADAPT**, **REJECT**, or **DEFER**.
>
> **Core Rule:** No pattern is copied blindly. Every pattern kept or adapted must earn its place through evidence and stage needs.

---

## Component Ledger

| Subsystem / Pattern | Mia Implementation | BioMarker Decision | Target Stage | Rationale |
|---|---|---|---|---|
| **Durable Execution Engine** | DBOS / Workers / Leases | **DEFER** | Stage 12 | Early stages are interactive, synchronous, or simple batch. Durability infrastructure adds massive cognitive and operational overhead before failure modes are proven. |
| **Worker / Queue** | Redis Streams / Distributed Worker Pool | **DEFER** | Stage 12 | Single-process API is sufficient for early prototyping. Add distributed workers only when task durations demand async decoupling. |
| **Manifest Compiler & Attestation** | Ed25519 cryptographic signing & manifest compiler | **DEFER** | Stage 13 | High production maturity pattern; not needed until multi-tenant auditability and runtime immutability become hard requirements. |
| **Agent Framework** | ByteDance Eino (Go) | **ADAPT** | Stage 9 | Eino is strong for Go-based agent pipelines. We adapt its core primitives while keeping business logic decoupled in `internal/observation/`, `internal/analysis/`. |
| **Model Context Protocol (MCP)** | Dynamic tool execution via MCP servers | **DEFER** | Stage 15 | BioMarker tools (terminology lookup, evidence retrieval) start as deterministic in-process ports/adapters before exposing via MCP. |
| **Canonical Contracts** | Centrally defined schemas | **KEEP** | Stage 2 | Contract-first discipline is invaluable for polyglot systems. Maintained in top-level `contracts/`. |
| **Longitudinal Timeline Model** | Patient observation history | **ADAPT** | Stage 5 | Adapted specifically for clinical biomarkers (units, reference ranges, specimen types) rather than generic events. |
| **Object Store for Documents** | MinIO / S3 document blob storage | **DEFER** | Stage 10 | Local filesystem storage (`var/uploads/`) is sufficient for Stage 3–9 experiments. |
| **Clinical Safety Gate** | Multi-layer validation | **KEEP & EXPAND** | Stage 7 | BioMarker elevates Clinical Safety to a first-class citizen (`docs/05-safety/`), distinct from technical security. |
| **Monorepo Task Orchestrator** | Turborepo + pnpm | **KEEP** | Stage 0 | Provides seamless developer ergonomics for cross-language building, linting, and testing. |

---

## Review Lifecycle

1. Before any deferred subsystem is materialized, an ADR must reference this ledger.
2. The author must demonstrate empirical evidence from an `experiments/` stage showing that simpler solutions fail to meet concrete requirements.
