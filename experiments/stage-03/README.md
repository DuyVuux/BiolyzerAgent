# Stage 03 Experimental Harness

> **NOT PRODUCTION CODE**

Purpose:

```text
characterize PDF/native/OCR ingestion failure modes
against Stage-02 canonical contracts
```

## Run

From repository root:

```bash
python experiments/stage-03/run_benchmark.py --repo-root .
```

## Unit tests

```bash
python -m unittest discover -s experiments/stage-03/tests -v
```

## Generated results

```text
experiments/stage-03/results/
```

## Data

Only synthetic fixtures under:

```text
testdata/synthetic/stage-03/
```
