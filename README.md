# Scribe Exchange Protocol

The open rules for how a **client** talks to a **scribe service**: a server that takes recordings, notes and files, turns speech into text, and turns all of it into structured documents using templates.

The protocol is vendor-neutral and field-neutral. Any server may implement it; any client that follows it works against any compliant server. Lipi is the reference implementation, one of many.

> Status: **v0.1 draft, being written.** Nothing is stable before v1.0.

## Layout

| Folder | What | Who reads it |
|---|---|---|
| `spec/` | Numbered Markdown chapters, in plain words. Each object and endpoint is described in prose with its fields. Start at `spec/01-introduction.md`; the chapter plan is `spec/README.md`. | People |
| `schemas/` | One JSON Schema file per object. **The machine source of truth**: if prose and schema disagree, the schema wins and the prose is fixed. | Programs, and people checking exact shapes |
| `examples/` | Valid example payloads. Every example is checked against its schema in CI. | Both |
| `openapi.yaml` | Generated from `schemas/` plus the endpoint list. Never edited by hand. | Tools |
| `DECISIONS.md` | Why the protocol is the way it is, one numbered entry per decision. | Contributors |

## Checking

`python3 validate.py` checks every file in `examples/` against its schema (needs `pip install jsonschema referencing`). CI runs it on every change.

## Rules

1. **Versioning.** The major version is in the path: `/v1/…`. Within a major version only additive changes are allowed (new optional fields, new endpoints, new values in open lists); nothing is removed or renamed. A breaking change means `/v2/`.
2. **Profiles add, never change.** A *profile* is an extension for one field. It may add objects, fields, templates and routes under `/v1/profiles/<name>/`. It may not change a base object.
3. **Nothing field-specific, nothing vendor-specific** in the base. If a word only makes sense in one field or for one company, it belongs in a profile or in a product.
4. **The protocol stops at the wire.** How a service logs people in, who may see what, how it stores things, which models it runs: implementation. The protocol says what travels between client and service.
5. **RFC 2119 words.** MUST, SHOULD, MAY have their standard meaning: required, recommended, optional.
6. **Plain words.** Every technical term is explained the first time it appears in a chapter.

## Names

The short handle is `scribe-exchange` everywhere a short name is needed: `/.well-known/scribe-exchange`, `Scribe-Exchange-*` headers, package names. The spec does not use an acronym.

## Licence

Apache-2.0. Contributions under the Developer Certificate of Origin (DCO). Maintained by Eka Care.
