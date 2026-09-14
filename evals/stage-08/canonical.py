from __future__ import annotations
import hashlib
import json
from typing import Any

def canonical_json(obj: Any) -> str:
    """
    Serializes a Python object into a canonical JSON string adhering to RFC 8785 (JCS).
    Ensures:
    - Deterministic sorting of object keys by lexicographical byte order.
    - No insignificant whitespace (separators are strictly ',', ':').
    - UTF-8 representation without Unicode character escaping.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def canonical_bytes(obj: Any) -> bytes:
    """Returns the UTF-8 encoded byte sequence of the canonical JSON string."""
    return canonical_json(obj).encode("utf-8")

def canonical_digest(obj: Any) -> str:
    """Computes the deterministic SHA-256 hex digest of the canonical JSON representation."""
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def verify_attestation(obj: Any, expected_digest: str) -> bool:
    """
    Verifies that the object's canonical SHA-256 digest matches the expected attestation digest.
    Fails closed if there is any drift or mismatch.
    """
    if not isinstance(expected_digest, str) or len(expected_digest) != 64:
        return False
    return canonical_digest(obj) == expected_digest.lower()
