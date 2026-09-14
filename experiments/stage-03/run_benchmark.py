from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import platform
import subprocess
from pathlib import Path

import yaml

from backends import BACKENDS
from parser import parse_report
from canonical import build_dataset
from evaluate import score
from schema_validation import build_validator, validate_dataset


def package_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def tesseract_version():
    try:
        out = subprocess.check_output(["tesseract", "--version"], text=True)
        return out.splitlines()[0].strip()
    except Exception:
        return None


def environment_snapshot():
    return {
        "python": platform.python_version(),
        "PyMuPDF": package_version("PyMuPDF"),
        "pypdf": package_version("pypdf"),
        "pdfplumber": package_version("pdfplumber"),
        "reportlab": package_version("reportlab"),
        "Pillow": package_version("Pillow"),
        "pytesseract": package_version("pytesseract"),
        "jsonschema": package_version("jsonschema"),
        "tesseract": tesseract_version(),
    }


def canonical_gold_text(gold):
    lines = [
        "SYNTHETIC URINALYSIS REPORT",
        f"SUBJECT={gold['metadata']['subject']}",
        f"SPECIMEN={gold['metadata']['specimen']}",
        f"COLLECTED={gold['metadata']['collected']}",
        f"ISSUED={gold['metadata']['issued']}",
        f"STATUS={gold['metadata']['status']}",
        "TEST | RESULT | UNIT | REFERENCE | FLAG",
    ]
    for r in gold["rows"]:
        lines.append(" | ".join([
            r["test_name"],
            r["result_text"],
            r["unit"] or "-",
            r["reference"] or "-",
            r["flag"] or "",
        ]))
    return "\n".join(lines)


def main(repo_root: Path):
    corpus_dir = repo_root / "testdata/synthetic/stage-03/urinalysis"
    results_dir = repo_root / "experiments/stage-03/results"
    raw_dir = results_dir / "raw_text"
    canonical_dir = results_dir / "canonical_outputs"
    results_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    canonical_dir.mkdir(parents=True, exist_ok=True)

    gold = json.loads((corpus_dir / "gold_report.json").read_text(encoding="utf-8"))
    manifest = yaml.safe_load((corpus_dir / "corpus_manifest.yaml").read_text(encoding="utf-8"))
    validator = build_validator(repo_root)
    gold_text = canonical_gold_text(gold)

    rows = []
    for case in manifest["cases"]:
        pdf_path = corpus_dir / case["file"]
        for backend_name, backend in BACKENDS.items():
            extraction = backend(pdf_path)
            parsed = parse_report(extraction.text)
            dataset = build_dataset(pdf_path, parsed, extraction.mode)
            schema_errors = validate_dataset(validator, dataset)

            metrics = score(gold, parsed, dataset, extraction.text, gold_text)
            row = {
                "case": case["id"],
                "case_kind": case["kind"],
                "backend": backend_name,
                "mode_used": extraction.mode,
                "native_or_ocr_chars": len(extraction.text.strip()),
                "ocr_mean_confidence": (
                    round(extraction.ocr_mean_confidence, 3)
                    if extraction.ocr_mean_confidence is not None else None
                ),
                **{k: round(v, 4) if isinstance(v, float) else v for k, v in metrics.items()},
                "schema_valid": len(schema_errors) == 0,
                "schema_error_count": len(schema_errors),
                "parsed_rows": len(parsed.rows),
                "expected_rows": len(gold["rows"]),
            }
            rows.append(row)

            (raw_dir / f"{case['id']}__{backend_name}.txt").write_text(
                extraction.text, encoding="utf-8"
            )
            (canonical_dir / f"{case['id']}__{backend_name}.json").write_text(
                json.dumps(dataset, indent=2), encoding="utf-8"
            )

    env = environment_snapshot()
    (results_dir / "environment.json").write_text(json.dumps(env, indent=2), encoding="utf-8")
    (results_dir / "benchmark.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    columns = list(rows[0].keys())
    with (results_dir / "benchmark.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    # Human-readable report
    lines = [
        "# Stage 03 Experiment Run Report",
        "",
        "## Environment",
        "",
        "```json",
        json.dumps(env, indent=2),
        "```",
        "",
        "## Benchmark",
        "",
        "| Case | Backend | Mode | Meta | Row recall | Field exact | Kind | Comparator | Schema | Manual review |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['case']} | {r['backend']} | {r['mode_used']} | "
            f"{r['metadata_accuracy']:.2f} | {r['row_recall']:.2f} | "
            f"{r['field_exact_accuracy']:.2f} | {r['value_kind_accuracy']:.2f} | "
            f"{r['comparator_accuracy']:.2f} | "
            f"{'PASS' if r['schema_valid'] else 'FAIL'} | "
            f"{'YES' if r['manual_review_required'] else 'NO'} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "- Native extractors should succeed on digital-born cases and fail to recover image-only text.",
        "- OCR can recover image-only reports but exact metadata/identity must still be measured.",
        "- Schema validity is structural evidence only.",
        "- No confidence threshold is approved by this benchmark.",
        "",
    ]
    (results_dir / "RUN_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    print("Stage 03 benchmark complete")
    for r in rows:
        print(
            f"{r['case']:16} {r['backend']:20} "
            f"meta={r['metadata_accuracy']:.2f} rows={r['row_recall']:.2f} "
            f"fields={r['field_exact_accuracy']:.2f} kind={r['value_kind_accuracy']:.2f} "
            f"schema={'PASS' if r['schema_valid'] else 'FAIL'} "
            f"review={'YES' if r['manual_review_required'] else 'NO'}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    main(args.repo_root.resolve())
