# Stage 03 Handoff — Lab Ingestion Characterization

> **Status:** CANDIDATE COMPLETE WITH SYNTHETIC-CORPUS LIMITATION  
> **Next Stage:** 04 — Normalization & Clinical Terminology

---

## 1. What Stage 03 proved

Measured on a reproducible synthetic Urinalysis corpus:

```text
digital-born PDF
→ native text path works

image-only PDF
→ native path fails by construction
→ OCR fallback required

clean OCR
→ observation extraction can be strong
→ metadata characters can still fail

degraded OCR
→ identity/table errors appear
```

---

## 2. Architecture pressure

Candidate ingestion flow:

```text
Native text probe
→ native extract OR OCR fallback
→ deterministic parsing
→ canonical typed values
→ schema validation
→ semantic completeness checks
→ verification gate
```

---

## 3. Important non-conclusion

Stage 03 does NOT approve:

```text
a production parser library
a production OCR engine
a fixed confidence threshold
production accuracy claims
```

Synthetic corpus cannot justify those decisions.

---

## 4. Stage 04 input

Stage 04 now receives structured observations with:

```text
local test name
raw result
typed result
source unit
source range
source flag
specimen
method when available
provenance
mapping_status
verification state
```

Stage 04 must determine:

```text
test identity normalization
LOINC candidate/validated mapping
unit normalization/compatibility
safe conversion
semantic equivalence
```

---

## 5. Stage 04 must not hide Stage 03 uncertainty

If ingestion marks:

```text
ambiguous_test_identity
ambiguous_unit
source_conflict
```

normalization cannot simply “fix” it by guessing.

---

## 6. Real-corpus limitation

Current gate:

```text
SYNTHETIC_CHARACTERIZATION_GATE = PASS
REPRESENTATIVE_REAL_LAYOUT_GATE = NOT EXECUTED
```

Reason:

Project package is Zero-PHI and no approved de-identified representative corpus was provided.

This does not block Stage 04 domain/normalization experimentation.

It does block any production extraction-accuracy claim.

---

## 7. Next Stage

Stage 04 — Normalization & Clinical Terminology should:

- use Stage 03 synthetic parsed outputs;
- test LOINC mapping semantics;
- test UCUM normalization;
- distinguish local display name from canonical identity;
- define comparability rules;
- preserve mapping uncertainty.

No production runtime yet.
