from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz
from PIL import Image, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


ROWS = [
    ["SYNTH_PH", "6.0", "-", "SYNTH_RANGE", ""],
    ["SYNTH_PROTEIN", "Negative", "-", "Negative", ""],
    ["SYNTH_LE", "1+", "-", "Negative", "ABN"],
    ["SYNTH_RBC", "0-2", "/HPF", "SYNTH_RANGE", ""],
    ["SYNTH_WBC", "<5", "/HPF", "SYNTH_RANGE", ""],
    ["SYNTH_COLOR", "Yellow", "-", "-", ""],
    ["SYNTH_CLARITY", "Clear", "-", "-", ""],
    ["SYNTH_NITRITE", "Negative", "-", "Negative", ""],
]

METADATA = {
    "subject": "subject-synthetic-stage03-001",
    "specimen": "Urine",
    "collected": "2026-09-13T23:30:00Z",
    "issued": "2026-09-14T00:00:00Z",
    "status": "final",
}

GOLD = {
    "metadata": METADATA,
    "rows": [
        {
            "test_name": r[0],
            "result_text": r[1],
            "unit": None if r[2] == "-" else r[2],
            "reference": None if r[3] == "-" else r[3],
            "flag": None if r[4] == "" else r[4],
        }
        for r in ROWS
    ],
}


def draw_report(path: Path, layout: str) -> None:
    c = canvas.Canvas(str(path), pagesize=A4)
    x = 15 * mm
    y = 280 * mm
    c.setFont("Courier-Bold", 13)
    c.drawString(x, y, "SYNTHETIC URINALYSIS REPORT")
    y -= 8 * mm
    c.setFont("Courier", 9.5)
    header_lines = [
        f"SUBJECT={METADATA['subject']}",
        f"SPECIMEN={METADATA['specimen']}",
        f"COLLECTED={METADATA['collected']}",
        f"ISSUED={METADATA['issued']}",
        f"STATUS={METADATA['status']}",
    ]
    for line in header_lines:
        c.drawString(x, y, line)
        y -= 5 * mm
    y -= 3 * mm

    if layout == "pipe":
        c.drawString(x, y, "TEST | RESULT | UNIT | REFERENCE | FLAG")
        y -= 5 * mm
        for row in ROWS:
            c.drawString(x, y, " | ".join(row))
            y -= 5 * mm
    elif layout == "fixed":
        c.drawString(x, y, f"{'TEST':<20}{'RESULT':<14}{'UNIT':<10}{'REFERENCE':<18}{'FLAG':<6}")
        y -= 5 * mm
        for row in ROWS:
            c.drawString(
                x,
                y,
                f"{row[0]:<20}{row[1]:<14}{row[2]:<10}{row[3]:<18}{row[4]:<6}",
            )
            y -= 5 * mm
    else:
        raise ValueError(layout)
    c.save()


def to_image_pdf(source_pdf: Path, target_pdf: Path, degraded: bool) -> None:
    doc = fitz.open(source_pdf)
    pix = doc[0].get_pixmap(dpi=180, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if degraded:
        img = img.resize((int(img.width * 0.55), int(img.height * 0.55)))
        img = img.rotate(1.2, expand=True, fillcolor="white")
        img = img.filter(ImageFilter.GaussianBlur(0.45))
        resolution = 100
    else:
        resolution = 180
    img.convert("RGB").save(target_pdf, "PDF", resolution=resolution)


def main(repo_root: Path) -> None:
    out = repo_root / "testdata/synthetic/stage-03/urinalysis"
    out.mkdir(parents=True, exist_ok=True)

    digital_pipe = out / "digital_pipe.pdf"
    digital_fixed = out / "digital_fixed.pdf"
    scan_clean = out / "scan_clean.pdf"
    scan_degraded = out / "scan_degraded.pdf"

    draw_report(digital_pipe, "pipe")
    draw_report(digital_fixed, "fixed")
    to_image_pdf(digital_pipe, scan_clean, degraded=False)
    to_image_pdf(digital_pipe, scan_degraded, degraded=True)

    (out / "gold_report.json").write_text(
        json.dumps(GOLD, indent=2), encoding="utf-8"
    )
    manifest = {
        "synthetic_only": True,
        "cases": [
            {"id": "digital_pipe", "file": "digital_pipe.pdf", "kind": "digital"},
            {"id": "digital_fixed", "file": "digital_fixed.pdf", "kind": "digital"},
            {"id": "scan_clean", "file": "scan_clean.pdf", "kind": "image_only"},
            {"id": "scan_degraded", "file": "scan_degraded.pdf", "kind": "image_only_degraded"},
        ],
    }
    import yaml
    (out / "corpus_manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    main(args.repo_root.resolve())
