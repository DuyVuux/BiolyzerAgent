# BioMarker Agent — Scientific Evidence Engine

> **Status:** PROPOSED CANONICAL EVIDENCE BASELINE v0.1  
> **Stage:** 06 — Scientific Evidence Engine  
> **Primary user:** Healthcare Professional / Physician  
> **Input boundary:** Verified/eligible clinical facts and optional Longitudinal Timeline Snapshot  
> **Output boundary:** Frozen Evidence Bundle Snapshot for Stage 07 reasoning

---

## 1. Problem

A search result is not evidence.

A URL is not evidence identity.

A citation is not proof that a claim is supported.

Stage 06 therefore separates four entities:

```text
RetrievalAttempt
≠
EvidenceSource
≠
EvidenceClaim
≠
EvidenceBundleSnapshot
```

The goal is not to answer the physician directly.

The goal is:

> Build a traceable, frozen, reviewable evidence package that Stage 07 can reason over without ambient retrieval.

---

## 2. End-to-end model

```text
Clinical Question
      ↓
Evidence Query Intent
      ↓
Physical Retrieval Attempt(s)
      ↓
Retrieved Source Artifact(s)
      ↓
Source Identity + Version + Content Digest
      ↓
Source Classification / Integrity State
      ↓
Evidence Claim Extraction
      ↓
Claim ↔ Source Relation
      ↓
Canonical Evidence Selection
      ↓
Evidence Bundle Snapshot
      ↓
Stage 07 Reasoning & Clinical Safety
```

---

## 3. Core entities

### 3.1 EvidenceQuestion

Represents a bounded scientific question.

It must capture:

```text
question_id
question_text
question_type
clinical_context_ref
timeline_snapshot_id?
requested_outcomes?
```

It must not contain a diagnosis conclusion.

---

### 3.2 EvidenceQueryIntent

A query intent is a reproducible search instruction, not raw free-form browsing state.

Example structure:

```text
query_intent_id
question_id
provider_class
query_text
filters
policy_version
```

Multiple physical retrieval attempts may execute one intent.

---

### 3.3 RetrievalAttempt

Physical interaction with a retrieval provider.

Fields:

```text
attempt_id
query_intent_id
provider
started_at
completed_at?
status
result_source_ids[]
error_class?
```

Attempt status:

```text
succeeded
partial
failed
```

A retry creates a new attempt.

It does not create a new scientific source.

---

### 3.4 EvidenceSource

Canonical identity for one scientific/publication source representation.

Minimum metadata:

```text
source_id
canonical_locator
identifiers
title
publisher
publication_date
source_type
version?
content_digest
integrity_state
post_publication_state
```

A raw URL alone is insufficient.

---

### 3.5 EvidencePassage

A source-grounded excerpt/section locator used for claim support.

It must preserve:

```text
passage_id
source_id
locator
content_digest
text_or_structured_proposition
```

The full paper does not need to be copied into BioMarker.

---

### 3.6 EvidenceClaim

A normalized proposition used by Stage 07.

Example conceptual shape:

```text
claim_id
claim_text
claim_type
population
exposure_or_test
outcome
direction
scope
```

A claim is not trusted merely because an LLM produced it.

---

### 3.7 ClaimSourceLink

Relation between one claim and one source passage:

```text
supports
contradicts
context_only
not_entailed
```

The relation must be explicit.

---

### 3.8 EvidenceBundleSnapshot

A frozen evidence package:

```text
question
retrieval_policy_version
query_intents
selected source versions
claims
claim-source links
conflicts
limitations
content_digest
```

Stage 07 may only reason over the frozen bundle for that analysis run.

---

## 4. Authority rule

```text
Search ranking
≠
scientific authority

Publication type
≠
certainty of evidence

Citation
≠
entailment

LLM synthesis
≠
source fact
```

---

## 5. Evidence source identity

Identity should prefer stable identifiers:

```text
PMID
DOI
official guideline identifier/version
publisher canonical identifier
```

The system may maintain multiple aliases:

```text
DOI + PMID → same canonical EvidenceSource
```

when identity reconciliation is validated.

---

## 6. Source collision

### Same identity + same content digest

```text
idempotent retrieval
```

No new scientific source.

### Same identity + different digest + explicit version/update relation

```text
new source version
```

Both versions remain auditable.

### Same identity + different digest + no update relation

```text
SOURCE_IDENTITY_CONFLICT
```

Fail closed.

Do not silently overwrite.

---

## 7. Post-publication state

The evidence model must represent at least:

```text
active
corrected
expression_of_concern
retracted
unknown
```

NLM/PubMed explicitly links retracted publications to retraction notices and distinguishes the retracted publication from the notice.

A retracted source cannot be silently used as positive support.

---

## 8. Publication type is classification, not certainty

Candidate source types include:

```text
guideline
practice_guideline
consensus_statement
evidence_synthesis
systematic_review
meta_analysis
randomized_controlled_trial
clinical_trial
observational_study
case_report
review
other
```

The type can influence retrieval/ranking policy.

It does not by itself produce:

```text
high certainty
moderate certainty
low certainty
```

Stage 06 explicitly does **not** claim to implement GRADE.

---

## 9. Evidence appraisal boundary

The data model may preserve dimensions useful for later appraisal:

```text
population_match
outcome_match
design_type
sample_size?
risk_of_bias_assessment?
precision_notes?
indirectness_notes?
conflict_notes?
```

But Stage 06 does not invent a numeric “evidence quality score”.

If GRADE is adopted later, it must follow the actual framework rather than an informal modified score.

---

## 10. Frozen-bundle rule

Once an Evidence Bundle is selected for an analysis:

```text
Stage 07
→ may use only evidence in bundle
```

It must not:

```text
search "latest" silently
add a new paper mid-generation
replace a source because a search rank changed
```

New retrieval:

```text
→ new EvidenceBundleSnapshot
```

---

## 11. Clinical-context privacy boundary

Evidence search must use minimum necessary scientific terms.

Do not send:

```text
full patient report
full chat history
patient identifier
```

to a public retrieval provider merely to form a query.

Stage 06 question/query objects should separate:

```text
clinical context used internally
scientific query terms sent externally
```

---

## 12. Evidence conflict is first-class

If one eligible source supports a claim and another contradicts it:

```text
preserve conflict
```

Do not force consensus.

Bundle should expose:

```text
supporting source IDs
contradicting source IDs
limitations
```

Stage 07 decides safe presentation.

---

## 13. Reproducibility

For the same:

```text
question
retrieval policy version
selected exact source versions
claim ledger
claim-source relations
```

Stage 06 experiment requires deterministic bundle identity.

Production cross-language canonical serialization remains a Stage 13 concern, inherited from Stage 05 v0.2.

---

## 14. Core invariants

```text
EVID-001 RetrievalAttempt ≠ EvidenceSource.
EVID-002 EvidenceSource ≠ EvidenceClaim.
EVID-003 EvidenceClaim requires explicit source relation before use.
EVID-004 URL alone is insufficient source identity.
EVID-005 Same source identity + different unversioned content fails closed.
EVID-006 Retries do not duplicate canonical sources.
EVID-007 Retracted source cannot silently support an active claim.
EVID-008 Search ranking is not evidence certainty.
EVID-009 Publication type is not GRADE certainty.
EVID-010 Evidence conflict is preserved.
EVID-011 Frozen bundle cannot ambient-retrieve new evidence.
EVID-012 Same logical bundle input + policy yields deterministic experimental identity.
EVID-013 Retrieval policy change yields a new bundle snapshot.
EVID-014 Timeline snapshot provenance is pinned when a longitudinal question is used.
EVID-015 Partial retrieval cannot enter a verified bundle silently.
EVID-016 Query sent externally must minimize patient-derived context.
EVID-017 A frozen EvidenceBundleSnapshot has closed dependency scope (EvidenceProcessingProfile). Any new source, schema, extraction/entailment policy or model version requires a new bundle snapshot.
EVID-018 Late retrieval results cannot mutate a frozen evidence bundle.
EVID-019 Claim identity collision fails closed (same claim key + changed payload yields CLAIM_IDENTITY_CONFLICT).
EVID-020 Raw source artifact bytes hash is strictly distinct from canonical metadata envelope digest.
```

---

## 15. Stage boundary

Stage 06 does not create:

```text
clinical diagnosis
treatment recommendation
final physician summary
production web-search service
production vector database
production RAG framework
production API
database
worker
queue
```

Those belong to later stages.
