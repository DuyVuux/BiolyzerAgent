from __future__ import annotations
import hashlib
from copy import deepcopy

def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def canonical_source_id(src: dict) -> str:
    ids = src.get("identifiers", {})
    if ids.get("doi"):
        return "doi:" + ids["doi"].lower()
    if ids.get("pmid"):
        return "pmid:" + ids["pmid"]
    return src["canonical_locator"]

def materialize_source(src: dict) -> dict:
    sid = canonical_source_id(src)
    body_digest = digest(src["content"])
    passages = []
    for idx, p in enumerate(src.get("passages", []), 1):
        text = p.get("text", "")
        passages.append({
            "passage_id": f"{sid}:p{idx}",
            "locator": p["locator"],
            "content_digest": digest(text),
            "text": text,
            "proposition_key": p["proposition_key"],
            "relation_direction": p["relation_direction"],
        })
    res = {
        "schema_version": "1.0",
        "source_id": sid,
        "canonical_locator": src["canonical_locator"],
        "identifiers": src.get("identifiers", {}),
        "title": src["title"],
        "publisher": src.get("publisher", ""),
        "publication_date": src.get("publication_date", ""),
        "source_type": src["source_type"],
        "version": src.get("version", ""),
        "content_digest": body_digest,
        "integrity_state": "verified",
        "post_publication_state": src.get("post_publication_state", "unknown"),
        "passages": passages,
    }
    # Raw source artifact hash separation (EVID-018 architectural principle)
    if "raw_content" in src or "raw_bytes" in src:
        raw_val = src.get("raw_bytes") if "raw_bytes" in src else src.get("raw_content")
        raw_b = raw_val if isinstance(raw_val, bytes) else str(raw_val).encode("utf-8")
        res["raw_content_sha256"] = hashlib.sha256(raw_b).hexdigest()
    elif "raw_content_sha256" in src:
        res["raw_content_sha256"] = src["raw_content_sha256"]
    return res

class SourceRegistry:
    def __init__(self):
        self.by_identity = {}
        self.conflicts = []

    def register(self, src: dict) -> dict:
        item = materialize_source(src)
        identity = item["source_id"]
        version = item.get("version", "")
        key = (identity, version)

        if key not in self.by_identity:
            self.by_identity[key] = item
            return item

        previous = self.by_identity[key]
        if previous["content_digest"] == item["content_digest"]:
            return previous

        conflict = deepcopy(item)
        conflict["integrity_state"] = "identity_conflict"
        self.conflicts.append({
            "source_id": identity,
            "version": version,
            "existing_digest": previous["content_digest"],
            "incoming_digest": item["content_digest"],
        })
        return conflict

    def all_verified(self):
        return [v for _, v in sorted(self.by_identity.items()) if v["integrity_state"] == "verified"]
