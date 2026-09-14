# Stage 03 Experiment Run Report

## Environment

```json
{
  "python": "3.13.5",
  "PyMuPDF": "1.26.7",
  "pypdf": "5.9.0",
  "pdfplumber": "0.11.9",
  "reportlab": "4.4.9",
  "Pillow": "12.3.0",
  "pytesseract": "0.3.13",
  "jsonschema": "4.26.0",
  "tesseract": "tesseract 5.5.0"
}
```

## Benchmark

| Case | Backend | Mode | Meta | Row recall | Field exact | Kind | Comparator | Schema | Manual review |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
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

## Interpretation

- Native extractors should succeed on digital-born cases and fail to recover image-only text.
- OCR can recover image-only reports but exact metadata/identity must still be measured.
- Schema validity is structural evidence only.
- No confidence threshold is approved by this benchmark.
