from __future__ import annotations
import hashlib
from datetime import datetime

PREFERRED_UNIT = {"5804-0": "mg/dL"}

def convert_quantity(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "g/L" and to_unit == "mg/dL":
        return value * 100.0
    if from_unit == "mg/dL" and to_unit == "g/L":
        return value * 0.01
    raise ValueError("UNSAFE_OR_UNKNOWN_CONVERSION")

def _series_id(code, kind, unit):
    raw = f"{code}|{kind}|{unit or '-'}".encode()
    return "series-" + hashlib.sha256(raw).hexdigest()[:16]

def build_series(selected):
    excluded = []
    buckets = {}

    for logical_id, o in selected:
        if o.get("mapping_status") != "validated" or not o.get("canonical_test"):
            excluded.append({"observation_id":o["observation_id"],"reason":"mapping_not_validated"})
            continue
        if not o.get("effective_at"):
            excluded.append({"observation_id":o["observation_id"],"reason":"missing_effective_time"})
            continue

        code = o["canonical_test"]["code"]
        kind = o["value"]["kind"]
        normalized_unit = None
        val = dict(o["value"])

        if kind == "quantity":
            src_unit = val.get("unit_ucum")
            preferred = PREFERRED_UNIT.get(code, src_unit)
            if not src_unit or not preferred:
                excluded.append({"observation_id":o["observation_id"],"reason":"unit_not_normalized"})
                continue
            try:
                val["value"] = convert_quantity(val["value"], src_unit, preferred)
            except ValueError:
                excluded.append({"observation_id":o["observation_id"],"reason":"unit_not_normalized"})
                continue
            val["unit_ucum"] = preferred
            normalized_unit = preferred
        elif kind == "interval":
            normalized_unit = val.get("unit_ucum")

        key = (code, kind, normalized_unit)
        buckets.setdefault(key, {"test":o["canonical_test"], "points":[]})
        buckets[key]["points"].append({
            "logical_measurement_id": logical_id,
            "selected_observation_id": o["observation_id"],
            "effective_at": o["effective_at"],
            **({"issued_at":o["issued_at"]} if o.get("issued_at") else {}),
            "source_dataset_snapshot_id": o["source_dataset_snapshot_id"],
            "value": val,
        })

    series = []
    for (code, kind, unit), data in sorted(buckets.items()):
        points = sorted(
            data["points"],
            key=lambda p: (
                datetime.fromisoformat(p["effective_at"].replace("Z","+00:00")),
                p["logical_measurement_id"],
            )
        )
        item = {
            "series_id": _series_id(code, kind, unit),
            "canonical_test": data["test"],
            "value_kind": kind,
            "points": points,
        }
        if unit:
            item["normalized_unit"] = unit
        series.append(item)
    return series, excluded
