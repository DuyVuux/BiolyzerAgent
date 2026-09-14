# Stage 06 Handoff — Scientific Evidence Engine v0.2

> **Status:** CANDIDATE COMPLETE (v0.2 SURGICALLY HARDENED)  
> **Next Stage:** 07 — Reasoning & Clinical Safety

---

## 1. Canonical Stage 06 entities

```text
EvidenceQuestion
EvidenceQueryIntent
RetrievalAttempt
EvidenceSource
EvidencePassage
EvidenceClaim
ClaimSourceLink
EvidenceBundleSnapshot
```

---

## 2. Core separation

```text
RetrievalAttempt
≠
EvidenceSource
≠
EvidenceClaim
≠
EvidenceBundleSnapshot
```

---

## 3. Core safety semantics & invariants

```text
URL ≠ evidence identity
citation ≠ entailment
publication type ≠ certainty
search rank ≠ authority
retracted source ≠ active positive support
EVID-017: frozen bundle has closed dependency scope (EvidenceProcessingProfile)
EVID-018: late retrieval results cannot mutate a frozen bundle
raw source artifact hash ≠ canonical envelope hash
claim identity collision fails closed (same key + changed payload -> CLAIM_IDENTITY_CONFLICT)
```

---

## 4. Frozen Stage-07 input contract

Stage 07 must strictly consume:

```text
Canonical Clinical Dataset Snapshot
+
Longitudinal Timeline Snapshot (if relevant)
+
Evidence Bundle Snapshot
  ├── exact source versions + digests
  ├── claim ledger + links
  ├── conflicts + limitations
  └── closed processing profile (PolicyDescriptors)
+
Reasoning & Clinical Safety Policy
```

**Absolute Invariant:** Zero ambient retrieval during current reasoning generation. The LLM cannot expand its evidence universe during reasoning.

---

## 5. Experiment gates (18/18 PASS)

Synthetic experiment verifies:

- retry attempts do not duplicate sources;
- same source identity + same digest is idempotent;
- source identity collision fails closed;
- explicit source versioning is preserved;
- partial retrieval is excluded;
- retracted support is excluded;
- unsupported citation does not become support;
- contradiction is preserved;
- retrieval order does not change bundle identity;
- retrieval-policy version changes bundle identity;
- timeline provenance changes bundle identity;
- **[v0.2]** late retrieval cannot mutate frozen bundle (EVID-018);
- **[v0.2]** claim identity collision: same key + same payload is idempotent;
- **[v0.2]** claim identity collision: same key + different payload fails closed;
- **[v0.2]** closed dependency scope: processing profile digest change yields new bundle (EVID-017);
- **[v0.2]** raw source artifact digest is independent from structured metadata envelope.

---

## 6. Important limitation

Claim entailment in Stage 06 experiment uses controlled structured propositions.

Therefore:

```text
EVIDENCE_LEDGER_MECHANICS_GATE = PASS
PRODUCTION_BIOMEDICAL_ENTAILMENT_GATE = NOT EXECUTED
```

Stage 08 must evaluate real claim-source entailment quality before production.

---

## 7. External retrieval adapter status

PubMed/NCBI and Crossref interfaces were researched from official documentation.

No production API adapter was created.

No live external retrieval benchmark is claimed.

---

## 8. ai-studio lesson & reconciliation

Stage 06 v0.2 adapts the verified architectural principles from `ai-studio`:

```text
many physical attempts
→ canonical logical selection
→ immutable provenance
→ closed dependency scope (manifest closure)
→ frozen snapshot
```

without importing runtime leases, worker mechanics, or premature database schemas.

Decisions:
- Transient network timeouts on read operations allow safe physical retries under the same query intent (not forced into clinical reconciliation).
- PostgreSQL schema, `ON CONFLICT`, and worker fencing are deferred to Stages 10, 11, and 12.
- RFC 8785 (JCS) production canonicalization is deferred to Stage 13.
- Scope creep (genomics/WGS, giant DICOM files, US-specific 6-year HIPAA retention) is explicitly rejected.

---

## 9. Stage 07 is allowed to begin

Yes, provided Stage 07:

- reasons only from pinned clinical/timeline/evidence snapshot inputs;
- distinguishes source fact from LLM inference;
- preserves uncertainty and scientific conflicts;
- enforces physician-facing safety boundary (Level A/B only, zero autonomous diagnosis);
- does not convert evidence ranking into diagnosis authority.
