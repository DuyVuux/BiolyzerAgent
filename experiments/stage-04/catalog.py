from __future__ import annotations
import json
from pathlib import Path


def load_catalog(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_token(value):
    if value is None:
        return None
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")
