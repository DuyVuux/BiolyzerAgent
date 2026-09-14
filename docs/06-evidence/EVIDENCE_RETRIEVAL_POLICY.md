# Evidence Retrieval Policy

> **Status:** PROPOSED v0.1  
> **Policy baseline:** `evidence-retrieval-policy-v1`

---

## 1. Retrieval sources

Stage 06 external research confirms useful metadata/retrieval interfaces:

### PubMed / NCBI E-utilities

Useful for:

```text
biomedical citation search
PMID identity
publication type
publication status/linkage
```

NCBI documents ESearch/EFetch and rate-control requirements.

### Crossref REST API

Useful for:

```text
DOI metadata
publisher metadata
licenses
post-publication updates
Retraction Watch-linked metadata
```

Crossref metadata is not automatically full text.

---

## 2. Provider role

Provider result ordering is discovery input only.

No provider is itself clinical authority.

---

## 3. Query policy

An intent records:

```text
question_id
query_text
filters
provider_class
policy_version
```

Examples of filters:

```text
date window
publication type
language
human studies
guideline/systematic review preference
```

Filters must be explicit and reproducible.

---

## 4. Minimum necessary query

External query should contain scientific concepts, not full patient context.

Preferred:

```text
"urinary biomarker X association Y systematic review"
```

Not:

```text
full patient's values, identifier, medications and chat transcript
```

unless an approved private retrieval architecture later allows it.

---

## 5. Retrieval prioritization

Candidate discovery priority:

```text
official guideline / consensus
evidence synthesis / systematic review / meta-analysis
controlled/interventional clinical evidence
large observational evidence
other relevant literature
```

This is a **search prioritization policy**, not a certainty rating.

---

## 6. PubMed publication types

NLM distinguishes types such as:

```text
Guideline
Practice Guideline
Consensus Statement
Meta-Analysis
Systematic Review
Clinical Trial
Observational Study
Case Reports
Retraction Notice
```

PubMed's 2026 update also added `Evidence Synthesis` to article-type filters.

---

## 7. Retrieval attempts

Each attempt records:

```text
provider
query intent
status
result IDs
timing
error
```

Partial attempts do not become verified evidence merely because they returned some records.

---

## 8. No ambient latest

After bundle freeze:

```text
search providers are out of scope for current Stage-07 reasoning
```

A freshness refresh creates a new bundle.

---

## 9. API operational notes

For future implementation:

- NCBI asks scripted clients to identify `tool` and `email`;
- without an API key, NCBI documents a 3 requests/second limit;
- Crossref recommends responsible API use and offers a polite pool.

These are adapter requirements, not domain semantics.
