# Source Authority & Conflict Protocol

> **Purpose:** Establishes the authoritative hierarchy of documents and code, and the conflict resolution protocol when discrepancies arise.

---

## 1. Authority Hierarchy

When two sources within this repository express conflicting statements, models, or constraints, authority is resolved in the following strict order:

```text
Level 1: Regulatory & Clinical Safety Specifications
         (docs/05-safety/, docs/01-product/INTENDED_USE_AND_SAFETY_ENVELOPE.md)
              ↓
Level 2: Canonical Machine Contracts
         (contracts/schemas/, contracts/openapi/)
              ↓
Level 3: Domain & Architecture Specifications
         (docs/02-domain/, docs/03-architecture/, docs/07-decisions/adr/)
              ↓
Level 4: Implementation Code
         (apps/, internal/, packages/)
              ↓
Level 5: Experiments & Scratch Code
         (experiments/, tools/)
```

---

## 2. Rules of Authority

1. **Implementation Code is Never Canonical**: If Go/TypeScript code disagrees with a schema in `contracts/` or a specification in `docs/`, the code is considered buggy and must be fixed, unless an approved ADR explicitly states otherwise.
2. **Clinical Safety Trumps Feature Convenience**: Clinical safety gates and claim grounding constraints cannot be bypassed for UX simplicity or latency optimization.
3. **Contracts are Single Sources of Truth for Cross-Language Types**: Data shapes exchanged between Go and TypeScript are governed by `contracts/`, never by private internal Go structs or TypeScript interfaces.

---

## 3. Conflict Resolution Protocol

If an engineer or AI agent discovers an inconsistency:
1. **Identify the Conflict**: Pinpoint the conflicting files and line ranges.
2. **Determine Hierarchy**: Check which source holds higher authority per Section 1.
3. **Escalate / Document**:
   - If the higher authority is clear, update the lower authority source to align.
   - If two documents at the same level conflict (e.g. two conflicting ADRs or specs), open an issue / create an ADR draft and resolve before proceeding with code changes.
