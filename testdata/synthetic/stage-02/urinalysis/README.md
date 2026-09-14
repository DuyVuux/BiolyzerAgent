# Stage 02 Synthetic Urinalysis Fixtures

All data in this directory is synthetic and exists only to test contract shape. It is **not** a source of clinical reference ranges or medical guidance.

- `valid_mixed_values.json`: quantity, ordinal, categorical, interval, comparator, source range, source flag, candidate LOINC mapping, UCUM, provenance and verification state.
- `invalid_missing_provenance.json`: intentionally removes required provenance; schema validation must fail.
