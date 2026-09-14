# Clinical Test Data Policy (`testdata/`)

> [!CAUTION]
> **STRICT ZERO-PHI POLICY**: NEVER commit real patient data, clinical records, doctor notes, or identifiable health information to this repository under any circumstances.

---

## 1. Allowed Data Types

Only the following data formats are permitted in `testdata/`:
1. **Fully Synthetic Fixtures**: Programmatically or manually generated mock laboratory reports, fictitious patient names (e.g. "John Doe", "Patient 001"), and plausible but simulated clinical values.
2. **Standardized Reference Fixtures**: Public benchmark datasets published specifically for open academic or clinical research under appropriate open licenses (e.g. PhysioNet synthetic, Synthea).

---

## 2. Directory Structure

```text
testdata/
└── synthetic/
    ├── lab-reports/   # Mock PDFs, scanned image samples, raw text reports
    └── expected/      # Ground-truth structured JSON extractions
```

---

## 3. Pre-Commit Verification

Before committing any file to `testdata/`:
- Verify no real names, addresses, hospital identification numbers, phone numbers, or dates of birth are present.
- Automated pre-commit checks will reject fixtures containing patterns matching real medical record identifiers.
