from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


def build_validator(repo_root: Path):
    schema_dir = repo_root / "contracts/schemas/clinical"
    names = [
        "source-document.schema.json",
        "lab-report.schema.json",
        "biomarker-observation.schema.json",
        "clinical-dataset.schema.json",
    ]
    schemas = {}
    registry = Registry()
    for name in names:
        schema = json.loads((schema_dir / name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schemas[name] = schema
        registry = registry.with_resource(
            schema["$id"],
            Resource.from_contents(schema, default_specification=DRAFT202012),
        )
    return Draft202012Validator(schemas["clinical-dataset.schema.json"], registry=registry)


def validate_dataset(validator, dataset: dict):
    errors = list(validator.iter_errors(dataset))
    return [e.message for e in errors]
