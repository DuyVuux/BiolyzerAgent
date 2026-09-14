from __future__ import annotations
from collections import Counter

def compute_trend(series):
    pts = series["points"]
    if len(pts) < 2:
        return {"status":"insufficient_points"}

    times = [p["effective_at"] for p in pts]
    if any(count > 1 for count in Counter(times).values()):
        return {"status":"indeterminate_same_time"}

    kind = series["value_kind"]
    values = [p["value"] for p in pts]

    if kind == "quantity":
        if any(v.get("comparator") for v in values):
            return {"status":"not_computed_censored_value"}
        first = values[0]["value"]
        last = values[-1]["value"]
        delta = last - first
        direction = "increased" if delta > 0 else "decreased" if delta < 0 else "unchanged"
        return {
            "status":"computed_numeric",
            "direction":direction,
            "absolute_delta":round(delta, 10),
        }

    if kind == "ordinal":
        if any("rank" not in v for v in values):
            return {"status":"insufficient_points"}
        delta = values[-1]["rank"] - values[0]["rank"]
        direction = "increased" if delta > 0 else "decreased" if delta < 0 else "unchanged"
        return {"status":"computed_ordinal","direction":direction,"rank_delta":delta}

    if kind == "categorical":
        first = values[0].get("normalized_code", values[0].get("source_text"))
        last = values[-1].get("normalized_code", values[-1].get("source_text"))
        return {
            "status":"computed_categorical",
            "direction":"unchanged" if first == last else "changed",
        }

    if kind == "interval":
        return {"status":"history_only_interval"}

    return {"status":"insufficient_points"}
