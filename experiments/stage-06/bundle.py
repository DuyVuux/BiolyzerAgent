from __future__ import annotations
import hashlib, json
from claim_ledger import ClaimRegistry

DEFAULT_POLICY = "evidence-retrieval-policy-v1"

DEFAULT_PROCESSING_PROFILE = {
    "profile_id": "evidence-profile-v1",
    "retrieval_policy": {
        "policy_id": "evidence-retrieval-policy",
        "version": "1.0",
        "digest": hashlib.sha256(b"evidence-retrieval-policy-v1-content").hexdigest(),
    },
    "source_selection_policy": {
        "policy_id": "evidence-selection-policy",
        "version": "1.0",
        "digest": hashlib.sha256(b"evidence-selection-policy-v1-content").hexdigest(),
    },
    "claim_schema": {
        "schema_id": "https://schemas.biomarker.local/evidence/evidence-claim.schema.json",
        "version": "1.0",
        "digest": hashlib.sha256(b"evidence-claim-schema-v1-content").hexdigest(),
    },
    "entailment_policy": {
        "policy_id": "claim-entailment-and-conflict-policy",
        "version": "1.0",
        "digest": hashlib.sha256(b"claim-entailment-and-conflict-policy-v1-content").hexdigest(),
    },
}

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def build_bundle(
    question,
    query_intents,
    attempts,
    sources,
    claim_candidates,
    policy_version=DEFAULT_POLICY,
    processing_profile=None,
    frozen_at=None,
):
    profile = processing_profile or DEFAULT_PROCESSING_PROFILE

    # EVID-018: Late retrieval results cannot mutate a frozen bundle.
    # If frozen_at is provided, attempts completed strictly after frozen_at are excluded from this bundle.
    valid_attempts = []
    for a in attempts:
        if frozen_at and a.get("completed_at") and a["completed_at"] > frozen_at:
            continue
        valid_attempts.append(a)

    eligible_sources = sorted(
        [
            s for s in sources
            if s["integrity_state"] == "verified"
            and s["post_publication_state"] != "expression_of_concern"
        ],
        key=lambda x: (x["source_id"], x.get("version", ""), x["content_digest"])
    )

    claim_registry = ClaimRegistry()
    for c in claim_candidates:
        claim_registry.register(c, eligible_sources)

    all_claims = claim_registry.all_claims()
    selected_claims = claim_registry.all_selected()

    conflicts = []
    for c in selected_claims:
        sup = sorted({x["source_id"] for x in c["links"] if x["relation"] == "supports"})
        con = sorted({x["source_id"] for x in c["links"] if x["relation"] == "contradicts"})
        if sup and con:
            conflicts.append({
                "claim_id": c["claim_id"],
                "supporting_source_ids": sup,
                "contradicting_source_ids": con,
            })

    status = "conflicted" if conflicts else "verified"
    if any(a["status"] == "partial" for a in valid_attempts) and not any(a["status"] == "succeeded" for a in valid_attempts):
        status = "incomplete"

    payload = {
        "schema_version": "1.0",
        "question_id": question["question_id"],
        "question_text": question["question_text"],
        **({"timeline_snapshot_id": question["timeline_snapshot_id"]} if question.get("timeline_snapshot_id") else {}),
        **({"frozen_at": frozen_at} if frozen_at else {}),
        "retrieval_policy_version": policy_version,
        "processing_profile": profile,
        "query_intents": sorted(query_intents, key=lambda x: x["query_intent_id"]),
        "retrieval_attempt_ids": sorted(a["attempt_id"] for a in valid_attempts),
        "selected_sources": eligible_sources,
        "claims": sorted(selected_claims, key=lambda x: x["claim_id"]),
        "conflicts": sorted(conflicts, key=lambda x: x["claim_id"]),
        "limitations": [
            "Synthetic Stage-06 entailment uses structured proposition keys.",
            "Publication type is not treated as certainty of evidence.",
            "Closed dependency scope enforced under EVID-017.",
            "Late retrieval cannot mutate frozen bundle under EVID-018."
        ],
        "status": status,
    }
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return {
        "schema_version": "1.0",
        "bundle_id": "evidence-" + digest[:16],
        "experimental_content_sha256": digest,
        **{k: v for k, v in payload.items() if k != "schema_version"},
    }, all_claims
