from __future__ import annotations
from units import normalize_unit


def _norm(s):
    if s is None:
        return None
    return str(s).strip().lower().replace("-", "_").replace(" ", "_")


def map_observation(obs: dict, catalog: dict) -> dict:
    local = str(obs.get("local_test_name", "")).strip().lower()
    system = _norm(obs.get("system"))
    scale = _norm(obs.get("scale"))
    method = _norm(obs.get("method"))
    unit = normalize_unit(obs.get("unit_source")) if obs.get("unit_source") else None

    alias_candidates = []
    for concept in catalog["concepts"]:
        aliases = {a.lower() for a in concept.get("aliases", [])}
        if local in aliases:
            alias_candidates.append(concept)

    if not alias_candidates:
        return {"status":"unmapped", "candidate_codes":[], "validated_code":None, "matched_dimensions":[], "missing_dimensions":[]}

    filtered = []
    diagnostics = []
    for c in alias_candidates:
        matched = []
        failed = []
        missing = []
        for key, actual in [("system", system), ("scale", scale), ("method", method)]:
            expected = _norm(c.get(key))
            if expected is None:
                continue
            if actual is None:
                missing.append(key)
            elif actual == expected:
                matched.append(key)
            else:
                failed.append(key)
        expected_unit = c.get("unit_ucum")
        if expected_unit is not None:
            if unit is None:
                missing.append("unit")
            elif unit == expected_unit:
                matched.append("unit")
            else:
                failed.append("unit")
        if not failed:
            filtered.append(c)
        diagnostics.append({"code":c["code"],"matched":matched,"failed":failed,"missing":missing})

    if not filtered:
        return {"status":"unmapped", "candidate_codes":[], "validated_code":None, "matched_dimensions":[], "missing_dimensions":[]}

    # A concept is validated only if exactly one candidate remains and every required
    # catalog dimension available for that concept was supplied by the observation.
    if len(filtered) == 1:
        c = filtered[0]
        required_missing = []
        for key in ["system","scale","method"]:
            if c.get(key) is not None and obs.get(key) is None:
                required_missing.append(key)
        if c.get("unit_ucum") is not None and obs.get("unit_source") is None:
            required_missing.append("unit")
        if not required_missing:
            return {
                "status":"validated",
                "candidate_codes":[c["code"]],
                "validated_code":c["code"],
                "display":c["display"],
                "terminology_version":catalog["terminology_version"],
                "matched_dimensions":["alias","system","scale"] + (["method"] if c.get("method") is not None else []) + (["unit"] if c.get("unit_ucum") is not None else []),
                "missing_dimensions":[],
            }

    return {
        "status":"candidate",
        "candidate_codes":sorted(c["code"] for c in filtered),
        "validated_code":None,
        "matched_dimensions":["alias"],
        "missing_dimensions":sorted({m for d in diagnostics for m in d["missing"]}),
    }
