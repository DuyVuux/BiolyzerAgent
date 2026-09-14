from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import fitz
import pdfplumber
from PIL import Image
from pypdf import PdfReader
import pytesseract


@dataclass
class ExtractionResult:
    text: str
    mode: str
    backend: str
    ocr_mean_confidence: Optional[float] = None


def pymupdf_native(path: Path) -> ExtractionResult:
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    return ExtractionResult(text=text, mode="native", backend="pymupdf_native")


def pypdf_native(path: Path) -> ExtractionResult:
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return ExtractionResult(text=text, mode="native", backend="pypdf_native")


def pdfplumber_native(path: Path) -> ExtractionResult:
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return ExtractionResult(text=text, mode="native", backend="pdfplumber_native")


def tesseract_ocr(path: Path) -> ExtractionResult:
    doc = fitz.open(path)
    texts = []
    confidences = []
    for page in doc:
        pix = page.get_pixmap(dpi=220, alpha=False)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        texts.append(pytesseract.image_to_string(image, config="--psm 6"))
        data = pytesseract.image_to_data(
            image, config="--psm 6", output_type=pytesseract.Output.DICT
        )
        for raw in data.get("conf", []):
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            if value >= 0:
                confidences.append(value)
    mean_conf = sum(confidences) / len(confidences) if confidences else None
    return ExtractionResult(
        text="\n".join(texts),
        mode="ocr",
        backend="tesseract_ocr",
        ocr_mean_confidence=mean_conf,
    )


def hybrid_auto(path: Path) -> ExtractionResult:
    native = pymupdf_native(path)
    usable = len(native.text.strip()) >= 80 and "SYNTHETIC URINALYSIS REPORT" in native.text
    if usable:
        native.backend = "hybrid_auto"
        native.mode = "native"
        return native
    ocr = tesseract_ocr(path)
    ocr.backend = "hybrid_auto"
    ocr.mode = "ocr"
    return ocr


BACKENDS = {
    "pymupdf_native": pymupdf_native,
    "pypdf_native": pypdf_native,
    "pdfplumber_native": pdfplumber_native,
    "tesseract_ocr": tesseract_ocr,
    "hybrid_auto": hybrid_auto,
}
