#!/usr/bin/env python3
"""Generate openapi.yaml from schemas/*.schema.json and tools/endpoints.yaml.

Usage:  python3 tools/gen_openapi.py          (writes openapi.yaml)
        python3 tools/gen_openapi.py --check  (fails if openapi.yaml is stale)
Needs:  pip install pyyaml openapi-spec-validator
"""
import copy
import json
import sys
from pathlib import Path

import yaml


class Dumper(yaml.SafeDumper):
    """No YAML anchors: repeated blocks are written out in full so the file reads plainly."""

    def ignore_aliases(self, data):
        return True

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
ENDPOINTS = ROOT / "tools" / "endpoints.yaml"
OUT = ROOT / "openapi.yaml"
VERSION = "0.1.0"

HEADER_VERSION = {
    "name": "Scribe-Exchange-Version", "in": "header", "required": False,
    "description": "Pin the minor version to behave as (chapter 3).",
    "schema": {"type": "string", "example": "1.0"},
}
HEADER_IF_MATCH = {
    "name": "If-Match", "in": "header", "required": True,
    "description": "The revision the client started from, or * to skip the check (chapter 10).",
    "schema": {"type": "string"},
}
RESP_HEADERS = {
    "Scribe-Exchange-Version": {"description": "The minor version that served the call.", "schema": {"type": "string"}},
}


def load_schemas():
    """Return {file-stem: schema}, with $ref URNs rewritten to #/components/schemas/<Title>."""
    raw = {}
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        raw[path.name.removesuffix(".schema.json")] = json.loads(path.read_text())
    urn_to_title = {s["$id"]: s["title"] for s in raw.values()}

    extra = {}  # hoisted $defs: "<Title>.<def>" -> schema

    def rewrite(node, title):
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                if k in ("$schema", "$id", "$comment"):
                    continue
                if k == "$defs":
                    for name, sub in v.items():
                        extra[f"{title}.{name}"] = rewrite(sub, title)
                    continue
                if k == "$ref" and isinstance(v, str):
                    if v.startswith("urn:"):
                        out[k] = "#/components/schemas/" + urn_to_title[v]
                    elif v.startswith("#/$defs/"):
                        out[k] = f"#/components/schemas/{title}.{v.removeprefix('#/$defs/')}"
                    else:
                        out[k] = v
                else:
                    out[k] = rewrite(v, title)
            return out
        if isinstance(node, list):
            return [rewrite(v, title) for v in node]
        return node

    schemas = {stem: rewrite(s, s["title"]) for stem, s in raw.items()}
    titles = {stem: s["title"] for stem, s in raw.items()}
    return schemas, titles, extra


def ref(title):
    return {"$ref": "#/components/schemas/" + title}


def expand_params(spec, common):
    out = []
    for p in spec.get("params", []):
        if isinstance(p, str) and p.startswith("$"):
            c = common[p[1:]]
            out.extend(c if isinstance(c, list) else [c])
        else:
            out.append(p)
    return [
        {"name": p["name"], "in": p["in"], "required": p["in"] == "path",
         "description": p.get("description", ""), "schema": {"type": p["type"]}}
        for p in out
    ]


def error_response(status, codes_for_status):
    return {
        "description": "Error. Codes: " + ", ".join(sorted(codes_for_status)) + " (chapter 11).",
        "headers": RESP_HEADERS,
        "content": {"application/json": {"schema": ref("Error")}},
    }


def build():
    schemas, titles, extra = load_schemas()
    cfg = yaml.safe_load(ENDPOINTS.read_text())
    code_status = cfg["codes"]
    common = cfg["common_params"]

    components = {titles[stem]: schemas[stem] for stem in sorted(schemas)}
    components.update(sorted(extra.items()))
    # Page wrapper for list endpoints.
    def page_of(stem):
        return {"type": "object", "required": ["items", "next_cursor"],
                "properties": {"items": {"type": "array", "items": ref(titles[stem])},
                               "next_cursor": {"type": ["string", "null"]}}}

    paths = {}
    for ep in cfg["endpoints"]:
        op = {
            "summary": ep["summary"],
            "description": f"Defined in spec chapter {ep['chapter']}.",
            "operationId": ep["method"] + "".join(
                part.strip("{}").title() for part in ep["path"].replace("/.well-known/", "/wellKnown/").split("/") if part
            ),
            "parameters": expand_params(ep, common),
            "responses": {},
        }
        if not ep.get("no_version"):
            op["parameters"].append(HEADER_VERSION)
        if ep.get("if_match"):
            op["parameters"].append(HEADER_IF_MATCH)
        if ep.get("no_auth"):
            op["security"] = []
        if not op["parameters"]:
            del op["parameters"]

        if "request" in ep:
            body = {"application/json": {"schema": ref(titles[ep["request"]])}}
            if ep.get("multipart"):
                body["multipart/form-data"] = {"schema": {"type": "object", "properties": {
                    "source": ref(titles[ep["request"]]),
                    "file": {"type": "string", "format": "binary"}}}}
            op["requestBody"] = {"required": True, "content": body}
        elif "request_inline" in ep:
            op["requestBody"] = {"required": True, "content": {"application/json": {"schema": ep["request_inline"]}}}

        r = ep["response"]
        resp = {"description": "OK", "headers": RESP_HEADERS}
        if "schema" in r:
            resp["content"] = {"application/json": {"schema": ref(titles[r["schema"]])}}
        elif "list_of" in r:
            resp["content"] = {"application/json": {"schema": page_of(r["list_of"])}}
        elif r.get("stream"):
            resp["description"] = "Server-sent events: started, delta*, then done or error (chapter 10)."
            resp["content"] = {"text/event-stream": {"schema": {"type": "string"}}}
        else:
            resp["description"] = "No content"
        if ep.get("no_version"):
            del resp["headers"]
        op["responses"][str(r["status"])] = resp

        by_status = {}
        for code in ep.get("errors", []):
            by_status.setdefault(str(code_status[code]), set()).add(code)
        if not ep.get("no_auth"):
            by_status.setdefault("401", set()).update({"authentication_failed", "token_expired"})
            by_status.setdefault("403", set()).add("forbidden")
        by_status.setdefault("429", set()).add("rate_limited")
        by_status.setdefault("500", set()).add("internal_error")
        by_status.setdefault("503", set()).add("unavailable")
        for status in sorted(by_status):
            op["responses"][status] = error_response(status, by_status[status])

        paths.setdefault(ep["path"], {})[ep["method"]] = op

    doc = {
        "openapi": "3.1.0",
        "info": {
            "title": "Scribe Exchange Protocol",
            "version": VERSION,
            "description": "Generated from spec/ and schemas/ by tools/gen_openapi.py. Do not edit by hand. "
                           "Audio bytes go to the URL in a source's transport (chapters 6, 7), which is not a fixed path and is not listed here.",
            "license": {"name": "Apache-2.0"},
        },
        "servers": [{"url": "https://scribe.example.com", "description": "endpoints.base_url from discovery, without /v1"}],
        "security": [{"bearer": []}, {}],
        "paths": paths,
        "components": {
            "securitySchemes": {"bearer": {"type": "http", "scheme": "bearer",
                                           "description": "Required only when discovery's auth is not null (chapter 5)."}},
            "schemas": components,
        },
    }
    return doc


def main():
    doc = build()
    text = "# Generated by tools/gen_openapi.py from schemas/ and tools/endpoints.yaml. Do not edit.\n" + \
        yaml.dump(doc, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=120)
    if "--check" in sys.argv:
        if OUT.exists() and OUT.read_text() == text:
            print("openapi.yaml is up to date")
            return 0
        print("openapi.yaml is stale; run python3 tools/gen_openapi.py")
        return 1
    OUT.write_text(text)
    try:
        from openapi_spec_validator import validate
        validate(yaml.safe_load(text))
        print(f"wrote {OUT.name}: {sum(len(v) for v in doc['paths'].values())} operations, "
              f"{len(doc['components']['schemas'])} schemas, valid OpenAPI 3.1")
    except ImportError:
        print(f"wrote {OUT.name} (install openapi-spec-validator to validate)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
