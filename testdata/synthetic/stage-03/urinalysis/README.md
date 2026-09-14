# Stage 03 Synthetic Urinalysis Corpus

All artifacts in this directory are synthetic.

They are created to measure ingestion mechanics only.

They are **not** clinical reference data and must not be used as medical guidance.

## Cases

```text
digital_pipe.pdf
digital_fixed.pdf
scan_clean.pdf
scan_degraded.pdf
```

Gold truth:

```text
gold_report.json
```

Corpus metadata:

```text
corpus_manifest.yaml
```

Regenerate:

```bash
python experiments/stage-03/generate_corpus.py --repo-root .
```
