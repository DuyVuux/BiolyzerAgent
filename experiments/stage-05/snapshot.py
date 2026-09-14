from __future__ import annotations
import hashlib, json
from lineage import resolve_lineage
from series import build_series
from trend import compute_trend

POLICY_VERSION = "longitudinal-policy-v1"

def canonical_json(obj):
    """
    Experimental deterministic JSON serializer for Stage 05.
    
    NOTE ON CANONICAL IDENTITY BOUNDARY:
    This sorting serializer provides deterministic experimental identity within Python runtimes.
    In accordance with ai-studio lessons and production governance, cross-language canonical
    identity REQUIRES a formally specified profile (RFC 8785 / JCS, duplicate-key rejection,
    strict RFC 7493 I-JSON numeric domain, and canonical timestamp formatting).
    That formal Canonical Clinical Payload Profile is frozen in Stage 13 before production persistence.
    """
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False)

def build_snapshot(observations):
    subject, lineage_groups, selected, excluded = resolve_lineage(observations)
    series, series_excluded = build_series(selected)
    excluded.extend(series_excluded)

    for s in series:
        s["trend"] = compute_trend(s)

    source_ids = sorted({o["source_dataset_snapshot_id"] for o in observations})
    payload = {
        "schema_version":"1.0",
        "subject_ref":subject,
        "policy_version":POLICY_VERSION,
        "source_dataset_snapshot_ids":source_ids,
        "lineage_groups":sorted(lineage_groups,key=lambda x:x["logical_measurement_id"]),
        "series":sorted(series,key=lambda x:x["series_id"]),
        "excluded_observations":sorted(excluded,key=lambda x:(x["observation_id"],x["reason"])),
    }
    digest = hashlib.sha256(canonical_json(payload).encode()).hexdigest()
    return {
        "schema_version":"1.0",
        "timeline_snapshot_id":"timeline-"+digest[:16],
        "content_sha256":digest,
        "subject_ref":subject,
        "policy_version":POLICY_VERSION,
        "source_dataset_snapshot_ids":source_ids,
        "lineage_groups":payload["lineage_groups"],
        "series":payload["series"],
        "excluded_observations":payload["excluded_observations"],
    }
