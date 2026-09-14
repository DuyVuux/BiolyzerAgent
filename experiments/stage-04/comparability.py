from __future__ import annotations
from units import normalize_unit, can_convert

RELATED_GROUPS = [
    {"5799-2", "60026-2"},
    {"5803-2", "50560-2"},
    {"25428-4", "50555-2"},
]


def classify(left: dict, right: dict) -> str:
    if left.get("status") != "validated" or right.get("status") != "validated":
        return "INDETERMINATE"
    lc, rc = left.get("code"), right.get("code")
    if lc == rc:
        lu, ru = left.get("unit"), right.get("unit")
        if lu is None and ru is None:
            return "EXACT_COMPARABLE"
        lnu, rnu = normalize_unit(lu), normalize_unit(ru)
        if lnu == rnu and lnu is not None:
            return "EXACT_COMPARABLE"
        if lu is not None and ru is not None and can_convert(lu, ru):
            return "CONVERTIBLE_COMPARABLE"
        return "RELATED_NOT_COMPARABLE"
    for group in RELATED_GROUPS:
        if lc in group and rc in group:
            return "RELATED_NOT_COMPARABLE"
    return "RELATED_NOT_COMPARABLE"
