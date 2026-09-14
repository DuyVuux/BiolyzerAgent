from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ParsedRow:
    test_name: str
    result_text: str
    unit: Optional[str]
    reference: Optional[str]
    flag: Optional[str]
    raw_line: str
    page: int = 1


@dataclass
class ParsedReport:
    metadata: dict
    rows: list[ParsedRow]
    parse_errors: list[str]


META_KEYS = {
    "SUBJECT": "subject",
    "SPECIMEN": "specimen",
    "COLLECTED": "collected",
    "ISSUED": "issued",
    "STATUS": "status",
}


def _clean_optional(value: str) -> Optional[str]:
    value = value.strip()
    if value in {"", "-"}:
        return None
    return value


def _parse_pipe(line: str):
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 5:
        return None
    return parts


def _parse_fixed(line: str):
    parts = [p.strip() for p in re.split(r"\s{2,}", line.strip()) if p.strip()]
    # trailing empty FLAG can disappear; accept 4 or 5 fields
    if len(parts) == 4:
        parts.append("")
    if len(parts) != 5:
        return None
    return parts


def parse_report(text: str) -> ParsedReport:
    metadata = {}
    rows = []
    errors = []
    in_table = False

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue

        upper = line.upper()
        matched_meta = False
        for source_key, target_key in META_KEYS.items():
            prefix = source_key + "="
            if upper.startswith(prefix):
                metadata[target_key] = line[len(prefix):].strip()
                matched_meta = True
                break
        if matched_meta:
            continue

        if "TEST" in upper and "RESULT" in upper and ("REFERENCE" in upper or "REF" in upper):
            in_table = True
            continue

        if not in_table:
            continue

        parts = _parse_pipe(line) if "|" in line else _parse_fixed(line)
        if parts is None:
            errors.append(f"ROW_PARSE_FAILURE:{line}")
            continue

        test_name, result_text, unit, reference, flag = parts
        if not test_name or not result_text:
            errors.append(f"ROW_REQUIRED_FIELD_MISSING:{line}")
            continue

        rows.append(
            ParsedRow(
                test_name=test_name,
                result_text=result_text,
                unit=_clean_optional(unit),
                reference=_clean_optional(reference),
                flag=_clean_optional(flag),
                raw_line=line,
            )
        )

    return ParsedReport(metadata=metadata, rows=rows, parse_errors=errors)


def classify_result(result_text: str, unit: Optional[str]) -> dict:
    raw = result_text.strip()

    m = re.fullmatch(r"([<>]=?)\s*(-?\d+(?:\.\d+)?)", raw)
    if m:
        out = {
            "kind": "quantity",
            "value": float(m.group(2)),
            "comparator": m.group(1),
            "source_text": raw,
        }
        if unit:
            out["unit_source"] = unit
            if unit == "/HPF":
                out["unit_ucum"] = "/[HPF]"
            elif unit == "/LPF":
                out["unit_ucum"] = "/[LPF]"
        return out

    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)", raw)
    if m:
        out = {
            "kind": "interval",
            "low": float(m.group(1)),
            "high": float(m.group(2)),
            "source_text": raw,
        }
        if unit:
            out["unit_source"] = unit
            if unit == "/HPF":
                out["unit_ucum"] = "/[HPF]"
            elif unit == "/LPF":
                out["unit_ucum"] = "/[LPF]"
        return out

    if re.fullmatch(r"\d+\+", raw):
        return {
            "kind": "ordinal",
            "source_text": raw,
            "normalized_code": raw.replace("+", "_plus"),
            "rank": int(raw[:-1]) + 1,
        }

    if re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        out = {
            "kind": "quantity",
            "value": float(raw),
            "source_text": raw,
        }
        if unit:
            out["unit_source"] = unit
        return out

    known_categories = {"negative", "positive", "yellow", "clear", "present", "absent"}
    if raw.lower() in known_categories:
        return {
            "kind": "categorical",
            "source_text": raw,
            "normalized_code": raw.lower(),
        }

    return {"kind": "text", "source_text": raw}
