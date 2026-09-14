from __future__ import annotations

UNIT_ALIASES = {
    "mg/dL": "mg/dL",
    "mg/dl": "mg/dL",
    "MG/DL": "mg/dL",
    "g/L": "g/L",
    "/HPF": "/[HPF]",
    "/[HPF]": "/[HPF]",
    "/LPF": "/[LPF]",
    "/[LPF]": "/[LPF]",
    "pH": "[pH]",
    "[pH]": "[pH]",
    "{Spec grav}": "{Spec grav}",
}

# factor means: target_value = source_value * factor
CONVERSIONS = {
    ("mg/dL", "g/L"): 0.01,
    ("g/L", "mg/dL"): 100.0,
}


def normalize_unit(source):
    if source is None:
        return None
    return UNIT_ALIASES.get(source)


def convert_value(value, source_unit, target_unit):
    src = normalize_unit(source_unit) or source_unit
    dst = normalize_unit(target_unit) or target_unit
    if src == dst:
        return {"status":"identity", "value": float(value), "unit": dst, "rule_id":"identity"}
    factor = CONVERSIONS.get((src, dst))
    if factor is None:
        return {"status":"rejected", "value": None, "unit": None, "rule_id": None}
    return {"status":"converted", "value": float(value) * factor, "unit": dst, "rule_id": f"{src}_to_{dst}"}


def can_convert(source_unit, target_unit):
    src = normalize_unit(source_unit) or source_unit
    dst = normalize_unit(target_unit) or target_unit
    return src == dst or (src, dst) in CONVERSIONS
