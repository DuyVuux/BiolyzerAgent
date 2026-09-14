# Stage 02 Handoff — Canonical Biomarker Domain Model & Schemas

> **Status:** CANDIDATE COMPLETE  
> **Next Stage:** 03 — Lab Ingestion Characterization  
> **Primary vertical slice:** Urinalysis

## 1. Stage 02 established

Canonical concepts:

```text
SourceDocument
LabReport
BiomarkerObservation
ObservationValue
ReferenceRange
SourceInterpretation
DerivedRangeAssessment
ClinicalDatasetSnapshot
```

Machine-readable contracts:

```text
contracts/schemas/clinical/source-document.schema.json
contracts/schemas/clinical/lab-report.schema.json
contracts/schemas/clinical/biomarker-observation.schema.json
contracts/schemas/clinical/clinical-dataset.schema.json
```

Synthetic fixtures:

```text
testdata/synthetic/stage-02/urinalysis/
```

## 2. Key decisions

```text
Document ≠ Report ≠ Observation
Observation value is a tagged union
Raw/source value is always preserved
LOINC mapping is optional + stateful
UCUM unit is stored beside source unit
Source flag ≠ derived range assessment
Missing ≠ normal
Unknown remains unknown
FHIR is semantic reference, not persistence model
```

## 3. Urinalysis stress-test

Model biểu diễn được quantity, comparator quantity, interval, ordinal, categorical và text.

## 4. Stage 03 được phép làm

Experimental code chỉ trong `experiments/stage-03/`; synthetic data trong `testdata/`. Stage 03 được experiment PDF/image parsing, OCR nếu cần, table/field extraction, value-kind classification, range/unit/source-flag extraction, source locator và confidence measurement.

## 5. Stage 03 vẫn chưa được làm

Không production `apps/api`, `apps/web`, production runtime, database, worker, queue, Redis hoặc Kubernetes.

## 6. Contract evolution rule

Nếu experiment phát hiện schema thiếu:

```text
experiment evidence
→ schema change proposal
→ decision update
→ contract version change if needed
```

Không sửa schema chỉ để parser dễ code.

## 7. Metrics pressure

Stage 03 phải đo riêng test-name, value, value-kind, comparator, unit, reference-range, source-flag, date và source-locator extraction.

## 8. Deferred

LOINC auto-mapping, UCUM conversion policy, equivalence/comparability, longitudinal model, evidence, clinical safety gates và persistence/runtime vẫn deferred.

## 9. Gate

```text
DOMAIN_MODEL_GATE             = PASS
SCHEMA_SYNTAX_GATE            = PASS
VALID_FIXTURE_GATE            = PASS
NEGATIVE_FIXTURE_GATE         = PASS
URINALYSIS_COVERAGE_GATE      = PASS
ZERO_PHI_GATE                 = PASS
STAGE_BOUNDARY_GATE           = PASS
ROOT_CONFIG_INTEGRITY         = PASS_BY_PACKAGE_CONTENT
PNPM_CHECK                    = NOT_EXECUTED
HUMAN_LEARNING_GATE           = NOT_EXECUTED_BY_AI
CLINICAL_REVIEW_GATE          = REVIEW_RECOMMENDED
```
