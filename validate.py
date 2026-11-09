#!/usr/bin/env python3
"""Check every example in examples/ against its schema in schemas/.

Mapping: examples/<name>[.variant].json -> schemas/<name>.schema.json
(the part before the first dot is the schema name).
Usage: python3 validate.py   (needs: pip install jsonschema)
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

HERE = Path(__file__).parent
SCHEMAS = HERE / "schemas"
EXAMPLES = HERE / "examples"


def main() -> int:
    schemas = {}
    resources = []
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)
        name = path.name.removesuffix(".schema.json")
        schemas[name] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))
        # also allow bare relative refs like "principal.schema.json"
        resources.append((path.name, Resource.from_contents(schema)))
    registry = Registry().with_resources(resources)

    failures = 0
    checked = 0
    for path in sorted(EXAMPLES.glob("*.json")):
        name = path.name.split(".")[0]
        if name not in schemas:
            print(f"SKIP  {path.name}: no schema named {name}.schema.json")
            continue
        validator = Draft202012Validator(schemas[name], registry=registry, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(json.loads(path.read_text())), key=lambda e: list(e.path))
        checked += 1
        if errors:
            failures += 1
            print(f"FAIL  {path.name}")
            for e in errors:
                print(f"      at {'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}")
        else:
            print(f"ok    {path.name}")
    print(f"\n{checked} examples checked, {failures} failing, {len(schemas)} schemas")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
