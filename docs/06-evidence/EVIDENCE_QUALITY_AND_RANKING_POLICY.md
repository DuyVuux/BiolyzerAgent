# Evidence Quality & Ranking Policy

> **Status:** PROPOSED v0.1

---

## 1. Do not conflate three concepts

```text
retrieval priority
≠
study design
≠
certainty of evidence
```

---

## 2. Retrieval priority

A policy can rank likely-useful sources higher.

Example candidate ordering:

```text
official guideline
systematic review / evidence synthesis
meta-analysis
randomized trial
observational study
other relevant source
```

This only determines what is reviewed first.

---

## 3. Source-type metadata

Stage 06 records source type because it is useful for:

- search filtering;
- evidence presentation;
- conflict analysis;
- later appraisal.

---

## 4. Why no numeric source score?

A single number such as:

```text
systematic review = 5
RCT = 4
observational = 3
```

is misleading.

A systematic review can be weak.

An observational study can directly answer a diagnostic/prognostic question that an RCT does not.

The relevant question, population, outcome, bias and precision still matter.

---

## 5. GRADE boundary

GRADE requires explicit consideration of domains such as:

```text
risk of bias
imprecision
inconsistency
indirectness
publication bias
```

and assesses certainty by important outcome.

Stage 06 does not implement those judgments.

Therefore no artifact may label the current ranking:

```text
GRADE score
GRADE certainty
```

---

## 6. Candidate appraisal metadata

EvidenceSource/EvidenceClaim may later carry:

```text
population_match
outcome_match
study_design
sample_size
applicability_notes
risk_of_bias_reference
```

but those fields require explicit evidence and review.

---

## 7. Conflict handling

A lower-priority source is not deleted merely because a higher-priority source disagrees.

Bundle records conflict.

The physician-facing explanation later decides how to communicate it.
