from __future__ import annotations
import hashlib
from datetime import datetime

INVALID = {"entered_in_error", "cancelled"}
REVISION_STATUSES = {"corrected", "amended", "superseded"}

def _logical_id(subject, key):
    raw = f"{subject}|{key}".encode()
    return "lm-" + hashlib.sha256(raw).hexdigest()[:16]

def _canonical_payload(o):
    canonical_test = o.get("canonical_test") or {}
    val = o.get("value") or {}
    return (
        canonical_test.get("system"),
        canonical_test.get("code"),
        val.get("kind"),
        val.get("value"),
        val.get("unit_ucum"),
        val.get("comparator"),
        val.get("rank"),
        val.get("normalized_code"),
        val.get("low"),
        val.get("high"),
        o.get("effective_at"),
        o.get("mapping_status"),
    )

def _is_reconciliation_required(o):
    if o.get("reconciliation_required") is True:
        return True, "explicit_reconciliation_flag"
    if o.get("source_status") == "reconciliation_required" or o.get("status") in ("preliminary", "unknown", "reconciliation_required"):
        return True, f"status_{o.get('source_status') or o.get('status')}"
    if o.get("missing_predecessor") is True:
        return True, "missing_revision_predecessor"
    if o.get("partial_payload") is True or o.get("truncated_message") is True:
        return True, "partial_payload_or_truncated_message"
    issues = o.get("issues") or o.get("data_quality", {}).get("issues") or []
    for issue in issues:
        if issue in ("partial_payload", "truncated_message", "missing_predecessor", "reconciliation_required", "low_extraction_confidence", "source_conflict"):
            return True, f"data_quality_issue_{issue}"
    return False, None

def resolve_lineage(observations):
    # One subject only.
    subjects = {o["subject_ref"] for o in observations}
    if len(subjects) != 1:
        raise ValueError("CROSS_SUBJECT_INPUT")
    subject = next(iter(subjects))

    # Grouping by source identity.
    # Priority for logical source identity:
    # 1. external_observation_id (scoped to source_system if present)
    # 2. source_event_key
    # 3. source_fingerprint
    # 4. observation_id
    grouped = {}
    for o in observations:
        if o.get("external_observation_id"):
            sys_name = o.get("source_system", "default")
            key = ("external", f"{sys_name}:{o['external_observation_id']}")
            grouped.setdefault(key, []).append(o)
        elif o.get("source_event_key"):
            key = ("event", o["source_event_key"])
            grouped.setdefault(key, []).append(o)
        elif o.get("source_fingerprint"):
            key = ("fp", o["source_fingerprint"])
            grouped.setdefault(key, []).append(o)
        else:
            key = ("obs", o["observation_id"])
            grouped.setdefault(key, []).append(o)

    groups = []
    selected = []
    excluded = []

    for (kind, key), members in sorted(grouped.items(), key=lambda x: str(x[0])):
        lm = _logical_id(subject, f"{kind}:{key}")
        member_ids = sorted(o["observation_id"] for o in members)

        # 1. Check if reconciliation is required (incomplete/partial message, ambiguous state, missing predecessor)
        reconcile_reasons = []
        for o in members:
            needed, reason_detail = _is_reconciliation_required(o)
            if needed:
                reconcile_reasons.append(reason_detail)
        if reconcile_reasons:
            groups.append({
                "logical_measurement_id": lm,
                "member_observation_ids": member_ids,
                "resolution": "reconciliation_required",
                "evidence_basis": f"reconciliation_required:{','.join(sorted(set(reconcile_reasons)))}",
            })
            for o in members:
                excluded.append({
                    "observation_id": o["observation_id"],
                    "reason": "reconciliation_required"
                })
            continue

        # 2. Evaluate identity & semantic payload
        if len(members) == 1:
            chosen = members[0]
            resolution = "unique"
            evidence = "single_representation"
        else:
            payloads = {_canonical_payload(o) for o in members}
            if len(payloads) == 1:
                # Same logical identity + same semantic payload -> idempotent duplicate
                chosen = sorted(members, key=lambda o: o["observation_id"])[0]
                resolution = "duplicate_collapsed"
                evidence = "same_source_identity_idempotent_payload"
            else:
                # Same logical identity + different semantic payload
                # Invariant LONG-016: Identity Collision Fails Closed
                # Requires explicit revision/correction lineage to prove superseding.
                has_revision_status = any(
                    o.get("source_status") in REVISION_STATUSES
                    or o.get("status") in REVISION_STATUSES
                    or o.get("replaces_observation_id")
                    or o.get("supersedes_id")
                    for o in members
                )
                issued_times = [o.get("issued_at") for o in members]
                all_have_issued = all(t is not None for t in issued_times)
                distinct_issued = len(set(issued_times)) == len(members)

                is_valid_revision = (
                    kind in ("event", "external")
                    and all_have_issued
                    and distinct_issued
                    and has_revision_status
                )

                if is_valid_revision:
                    chosen = max(members, key=lambda o: datetime.fromisoformat(o["issued_at"].replace("Z","+00:00")))
                    resolution = "revision_selected"
                    evidence = "same_source_event_key_latest_issued_at"
                else:
                    # Identity collision with different payload and no valid revision lineage -> HARD CONFLICT
                    groups.append({
                        "logical_measurement_id": lm,
                        "member_observation_ids": member_ids,
                        "resolution": "unresolved_conflict",
                        "evidence_basis": "identity_collision_different_payload_no_revision_lineage",
                    })
                    for o in members:
                        excluded.append({
                            "observation_id": o["observation_id"],
                            "reason": "unresolved_lineage_conflict"
                        })
                    continue

        # 3. Check source invalidation (entered_in_error, cancelled)
        if chosen.get("source_status") in INVALID or chosen.get("status") in INVALID:
            groups.append({
                "logical_measurement_id": lm,
                "member_observation_ids": member_ids,
                "selected_observation_id": chosen["observation_id"],
                "resolution": "source_invalidated",
                "evidence_basis": evidence + "_latest_invalidated",
            })
            excluded.append({
                "observation_id": chosen["observation_id"],
                "reason": "source_invalidated"
            })
            continue

        groups.append({
            "logical_measurement_id": lm,
            "member_observation_ids": member_ids,
            "selected_observation_id": chosen["observation_id"],
            "resolution": resolution,
            "evidence_basis": evidence,
        })
        selected.append((lm, chosen))

    return subject, groups, selected, excluded
