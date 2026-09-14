from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from parser import ParsedReport, classify_result


def _valid_iso_z(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            datetime.fromisoformat(value[:-1] + "+00:00")
            return value
        datetime.fromisoformat(value)
        return value
    except ValueError:
        return None


def build_dataset(pdf_path: Path, parsed: ParsedReport, extraction_mode: str) -> dict:
    content_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    subject = parsed.metadata.get("subject", "unknown-subject")
    doc_id = "doc-" + pdf_path.stem
    report_id = "report-" + pdf_path.stem

    observations = []
    obs_ids = []

    for idx, row in enumerate(parsed.rows, 1):
        obs_id = f"obs-{pdf_path.stem}-{idx:02d}"
        obs_ids.append(obs_id)
        obs = {
            "schema_version": "1.0",
            "observation_id": obs_id,
            "report_id": report_id,
            "subject_ref": subject,
            "local_test_name": row.test_name,
            "status": "unknown",
            "mapping_status": "unmapped",
            "specimen": {"source_text": parsed.metadata.get("specimen", "Unknown")},
            "result": classify_result(row.result_text, row.unit),
            "verification": {"status": "unverified"},
            "data_quality": {"issues": []},
            "provenance": {
                "source_document_id": doc_id,
                "source_locator": {
                    "page": row.page,
                    "row_label": row.test_name,
                    "field_label": "Result row",
                    "raw_text": row.raw_line,
                },
                "extraction_method": ("parser" if extraction_mode == "native" else "ocr" if extraction_mode == "ocr" else "hybrid"),
            },
        }
        if row.reference:
            parsed_range = (
                {
                    "kind": "categorical_expected",
                    "expected_source_values": [row.reference],
                }
                if row.reference.lower() == "negative"
                else {"kind": "textual", "text": row.reference}
            )
            obs["source_reference_ranges"] = [{
                "range_id": f"range-{pdf_path.stem}-{idx:02d}",
                "origin": "source_report",
                "raw_text": row.reference,
                "parsed": parsed_range,
            }]
        if row.flag:
            normalized = "abnormal" if row.flag.upper() == "ABN" else "other"
            obs["source_interpretations"] = [{
                "raw_text": row.flag,
                "normalized_code": normalized,
            }]
        observations.append(obs)

    report = {
        "schema_version": "1.0",
        "report_id": report_id,
        "subject_ref": subject,
        "source_document_id": doc_id,
        "report_type": {"local_name": "Synthetic Urinalysis Panel"},
        "status": parsed.metadata.get("status", "unknown")
        if parsed.metadata.get("status", "unknown") in {
            "registered", "partial", "preliminary", "modified", "final",
            "amended", "corrected", "appended", "cancelled", "entered_in_error", "unknown"
        } else "unknown",
        "diagnostic_service_label": "Synthetic Laboratory",
        "specimen": {"source_text": parsed.metadata.get("specimen", "Unknown")},
        "observation_ids": obs_ids,
    }
    effective = _valid_iso_z(parsed.metadata.get("collected"))
    issued = _valid_iso_z(parsed.metadata.get("issued"))
    if effective:
        report["effective_at"] = effective
    if issued:
        report["issued_at"] = issued

    return {
        "schema_version": "1.0",
        "dataset_snapshot_id": "ds-" + pdf_path.stem,
        "subject_ref": subject,
        "created_at": "2026-09-14T06:00:00Z",
        "verification_status": "unverified",
        "source_documents": [{
            "schema_version": "1.0",
            "document_id": doc_id,
            "media_type": "application/pdf",
            "integrity": {"sha256": content_hash},
            "provenance": {
                "source_system_label": "stage-03-synthetic-corpus",
                "received_at": "2026-09-14T05:59:00Z",
            },
            "retention_class": "ephemeral_development",
        }],
        "reports": [report],
        "observations": observations,
    }
