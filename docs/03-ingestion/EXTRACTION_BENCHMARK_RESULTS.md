# Stage 03 — Extraction Benchmark Results

> **Status:** MEASURED SYNTHETIC BASELINE v0.1  
> **Important:** Đây là benchmark trên synthetic corpus, **không phải production accuracy claim**.

---

## 1. Experiment environment

Experiment được chạy trong environment:

```text
Python 3.x
PyMuPDF 1.26.7
pypdf 5.9.0
pdfplumber 0.11.9
ReportLab 4.4.9
Pillow 12.3.0
pytesseract 0.3.13
Tesseract 5.5.0
jsonschema 4.26.0
```

Exact environment snapshot nằm ở:

```text
experiments/stage-03/results/environment.json
```

---

## 2. Metric definitions

```text
metadata_accuracy
= exact matches / expected metadata fields

row_recall
= parsed observation rows / expected rows

field_exact_accuracy
= exact row-field matches /
  (expected rows × measured row fields)

value_kind_accuracy
= exact typed-result classification /
  expected observations

comparator_accuracy
= exact comparator classification /
  expected observations
```

Measured row fields:

```text
test_name
result_text
unit
reference
flag
```

---

## 3. Result table

The exact generated table is in:

```text
experiments/stage-03/results/benchmark.csv
experiments/stage-03/results/benchmark.json
experiments/stage-03/results/RUN_REPORT.md
```

### Key observed pattern

```text
Digital-born input
→ native extraction succeeds

Image-only PDF
→ native extraction gives no usable text

Clean scan
→ OCR recovers observation table strongly
→ timestamp transcription can still be wrong

Degraded scan
→ OCR introduces identity/table errors
→ manual verification remains necessary
```

---

## 4. Why native-text probe is necessary

Image-only PDF can still look perfect to a human.

But:

```text
looks like PDF with text
≠
contains machine text
```

Therefore ingestion must explicitly detect whether usable text exists.

A failure like:

```text
native extracted chars = 0
```

must trigger a defined fallback/error path.

---

## 5. Why field-level evaluation is necessary

Suppose OCR reads:

```text
2026-09-13T23:30:00Z
```

as:

```text
2026-09-13T23:30:002
```

Observation rows may still parse perfectly.

A single aggregate “document extraction succeeded” would hide the timestamp error.

Similarly:

```text
subject-synthetic-001
```

can become:

```text
sub ject-synthetic-001
```

and still be a syntactically valid string.

Thus:

```text
JSON Schema PASS
≠
subject identity correct
```

---

## 6. What schema validation proved

Stage 02 JSON Schemas successfully validate structurally well-formed parser output.

They catch:

- missing required structural fields;
- invalid variants;
- malformed contract shapes.

They do **not** catch:

- wrong test identity;
- OCR character substitutions;
- clinically incorrect mapping;
- wrong subject if the wrong string is syntactically valid.

This is expected.

---

## 7. Human verification conclusion

Stage 03 does not approve:

```text
confidence >= 0.95
→ auto-accept
```

Reason:

- OCR engine confidence is not automatically calibrated to field correctness;
- different field types have different risk;
- production-like corpus has not been evaluated;
- clinical risk tolerance is not yet encoded.

Instead, current candidate gate is:

```text
required metadata complete?
expected structure coherent?
all critical fields parsed?
source locator available?
any ambiguity/data-quality issue?
```

If not:

```text
REQUIRES_VERIFICATION
```

Numerical thresholds remain deferred to Stage 08 + clinical review.

---

## 8. Production claim limitation

This Stage proves:

> The architecture must support native-text and OCR paths and must evaluate extraction at field level.

It does **not** prove:

> Production urinalysis extraction accuracy is X%.

That requires an approved representative corpus.

---

## 9. Exact measured matrix generated in this run

| Case | Backend | Mode | Meta | Rows | Fields | Kind | Comparator | Schema | Review |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| digital_pipe | pymupdf_native | native | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | PASS | NO |
| digital_pipe | pypdf_native | native | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | PASS | NO |
| digital_pipe | pdfplumber_native | native | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | PASS | NO |
| digital_pipe | tesseract_ocr | ocr | 0.60 | 0.62 | 0.28 | 0.12 | 0.38 | PASS | YES |
| digital_pipe | hybrid_auto | native | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | PASS | NO |
| digital_fixed | pymupdf_native | native | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | PASS | NO |
| digital_fixed | pypdf_native | native | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | PASS | NO |
| digital_fixed | pdfplumber_native | native | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| digital_fixed | tesseract_ocr | ocr | 0.60 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| digital_fixed | hybrid_auto | native | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | PASS | NO |
| scan_clean | pymupdf_native | native | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| scan_clean | pypdf_native | native | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| scan_clean | pdfplumber_native | native | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| scan_clean | tesseract_ocr | ocr | 0.40 | 0.88 | 0.80 | 0.88 | 0.88 | PASS | YES |
| scan_clean | hybrid_auto | ocr | 0.40 | 0.88 | 0.80 | 0.88 | 0.88 | PASS | YES |
| scan_degraded | pymupdf_native | native | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| scan_degraded | pypdf_native | native | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| scan_degraded | pdfplumber_native | native | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | FAIL | YES |
| scan_degraded | tesseract_ocr | ocr | 0.40 | 1.00 | 0.88 | 1.00 | 1.00 | PASS | YES |
| scan_degraded | hybrid_auto | ocr | 0.40 | 1.00 | 0.88 | 1.00 | 1.00 | PASS | YES |

### Contract interpretation

- Runs with parsed observations validate against the Stage-02 canonical schema.
- Runs with zero parsed observations intentionally fail the canonical dataset contract because `observations` requires at least one item.
- This is fail-closed behavior, not a benchmark defect.
