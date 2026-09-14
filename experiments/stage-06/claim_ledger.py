from __future__ import annotations
from copy import deepcopy

POSITIVE_ELIGIBLE = {"active", "corrected", "unknown"}

def build_claim(claim: dict, sources: list[dict]) -> dict:
    links = []
    for src in sources:
        if src.get("integrity_state") != "verified":
            continue
        for p in src.get("passages", []):
            if p["proposition_key"] != claim["proposition_key"]:
                relation = "not_entailed"
            else:
                relation = p["relation_direction"]
                if relation == "supports" and src.get("post_publication_state") == "retracted":
                    relation = "not_entailed"
            links.append({
                "source_id": src["source_id"],
                "passage_id": p["passage_id"],
                "relation": relation,
            })

    supports = [x for x in links if x["relation"] == "supports"]
    contradicts = [x for x in links if x["relation"] == "contradicts"]
    context = [x for x in links if x["relation"] == "context_only"]

    if supports and contradicts:
        status = "conflicted"
    elif supports:
        status = "supported"
    elif context:
        status = "context_only"
    else:
        status = "unsupported"

    return {
        "schema_version": "1.0",
        "claim_id": claim["claim_id"],
        "claim_text": claim["claim_text"],
        "proposition_key": claim["proposition_key"],
        "status": status,
        "links": links,
    }

class ClaimRegistry:
    """Canonical Claim Ledger enforcing idempotent re-extraction and fail-closed collision semantics."""
    def __init__(self):
        self.by_identity = {}
        self.conflicts = []

    def register(self, claim: dict, sources: list[dict]) -> dict:
        built = build_claim(claim, sources)
        key = claim["claim_id"]

        if key not in self.by_identity:
            self.by_identity[key] = built
            return built

        previous = self.by_identity[key]
        # Check if identical proposition key and claim text (Idempotent replay)
        if previous["proposition_key"] == built["proposition_key"] and previous["claim_text"] == built["claim_text"]:
            return previous

        # Identity collision: same claim_id, but different proposition payload -> FAIL CLOSED
        conflict = deepcopy(built)
        conflict["status"] = "claim_identity_conflict"
        self.conflicts.append({
            "claim_id": claim["claim_id"],
            "existing_proposition_key": previous["proposition_key"],
            "incoming_proposition_key": built["proposition_key"],
            "existing_claim_text": previous["claim_text"],
            "incoming_claim_text": built["claim_text"],
        })
        # Conflict does not overwrite the canonical selection, but marks as conflicted
        return conflict

    def all_claims(self) -> list[dict]:
        return [v for _, v in sorted(self.by_identity.items())]

    def all_selected(self) -> list[dict]:
        return [
            v for _, v in sorted(self.by_identity.items())
            if v["status"] in {"supported", "conflicted", "context_only"}
        ]
