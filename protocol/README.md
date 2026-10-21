# Vaarta Protocol

The published rules for how a **client** (a web app, a mobile app, another server) talks to a **scribe service** (a server that turns recorded speech into a transcript and then into structured documents using templates).

The protocol is vendor-neutral. The Vaarta server is its reference implementation; any other server may implement it, and any client that follows it works against any compliant server.

> Status: **v0.1 draft, being written (Phase 0).** Nothing is stable before v1.0.

## Layout

| Folder | What | Who reads it |
|---|---|---|
| `spec/` | Numbered Markdown chapters, in plain words. Each object and endpoint is described in prose with its fields. | People |
| `schemas/` | One JSON Schema file per object (`session.schema.json`, `transcript.schema.json`, …). **This is the machine source of truth**: if prose and schema disagree, the schema wins and the prose is fixed. | Programs, and people checking exact shapes |
| `examples/` | Valid example payloads. Every example is checked against its schema in CI. | Both |
| `openapi.yaml` | Generated from `schemas/` plus the endpoint list. Never edited by hand. | Tools |

## Rules

1. **Versioning.** The version is in the path: `/v1/…`. Within a major version only additive changes are allowed (new optional fields, new endpoints); nothing is removed or renamed. A breaking change means `/v2/`.
2. **Profiles add, never change.** A *profile* is an extension for one field (the first is healthcare, MedScribeAlliance). It may add objects, fields, templates and routes under `/v1/profiles/<name>/`. It may not change a base object.
3. **Nothing medical, nothing vendor-specific** in the base. If a word only makes sense in one field or for one company, it belongs in a profile or in a product.
4. **RFC 2119 words.** MUST, SHOULD, MAY have their standard meaning: required, recommended, optional.
5. **Plain words.** Every technical term is explained the first time it appears in a chapter.

## Licence

Apache-2.0, same as the rest of the repository. Parts of the text derive from the MedScribeAlliance specification (CC BY 4.0, authored by Eka Care).
