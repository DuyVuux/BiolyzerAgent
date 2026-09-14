from __future__ import annotations

from difflib import SequenceMatcher


META_FIELDS = ["subject", "specimen", "collected", "issued", "status"]
ROW_FIELDS = ["test_name", "result_text", "unit", "reference", "flag"]


def expected_kind(result: str) -> str:
    import re
    if re.fullmatch(r"([<>]=?)\s*(-?\d+(?:\.\d+)?)", result):
        return "quantity"
    if re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)", result):
        return "interval"
    if re.fullmatch(r"\d+\+", result):
        return "ordinal"
    if re.fullmatch(r"-?\d+(?:\.\d+)?", result):
        return "quantity"
    if result.lower() in {"negative", "positive", "yellow", "clear", "present", "absent"}:
        return "categorical"
    return "text"


def expected_comparator(result: str):
    import re
    m = re.fullmatch(r"([<>]=?)\s*(-?\d+(?:\.\d+)?)", result)
    return m.group(1) if m else None


def score(gold: dict, parsed, canonical_dataset: dict, raw_text: str, canonical_gold_text: str) -> dict:
    metadata_hits = sum(parsed.metadata.get(k) == gold["metadata"][k] for k in META_FIELDS)
    metadata_accuracy = metadata_hits / len(META_FIELDS)

    expected_rows = gold["rows"]
    parsed_rows = parsed.rows
    row_recall = min(len(parsed_rows), len(expected_rows)) / len(expected_rows)

    field_hits = 0
    field_total = len(expected_rows) * len(ROW_FIELDS)
    kind_hits = 0
    comparator_hits = 0

    observations = canonical_dataset["observations"]

    for i, grow in enumerate(expected_rows):
        if i < len(parsed_rows):
            prow = parsed_rows[i]
            pmap = {
                "test_name": prow.test_name,
                "result_text": prow.result_text,
                "unit": prow.unit,
                "reference": prow.reference,
                "flag": prow.flag,
            }
            for field in ROW_FIELDS:
                if pmap[field] == grow[field]:
                    field_hits += 1

        if i < len(observations):
            result_obj = observations[i]["result"]
            if result_obj["kind"] == expected_kind(grow["result_text"]):
                kind_hits += 1
            if result_obj.get("comparator") == expected_comparator(grow["result_text"]):
                comparator_hits += 1

    field_accuracy = field_hits / field_total
    kind_accuracy = kind_hits / len(expected_rows)
    comparator_accuracy = comparator_hits / len(expected_rows)

    similarity = SequenceMatcher(
        None,
        "".join(raw_text.split()),
        "".join(canonical_gold_text.split()),
    ).ratio()

    manual_review_required = not (
        metadata_accuracy == 1.0
        and row_recall == 1.0
        and field_accuracy == 1.0
        and kind_accuracy == 1.0
        and comparator_accuracy == 1.0
        and not parsed.parse_errors
    )

    return {
        "metadata_accuracy": metadata_accuracy,
        "row_recall": row_recall,
        "field_exact_accuracy": field_accuracy,
        "value_kind_accuracy": kind_accuracy,
        "comparator_accuracy": comparator_accuracy,
        "text_character_similarity": similarity,
        "parse_error_count": len(parsed.parse_errors),
        "manual_review_required": manual_review_required,
    }
