# Schemas

One JSON Schema (draft 2020-12) per protocol object. These files are the machine source of truth for the protocol: the prose in `../spec/` describes them; `../openapi.yaml` is generated from them; CI checks `../examples/` against them.

Naming: `<object>.schema.json`, lower-case, singular: `session.schema.json`, `transcript-segment.schema.json`, `error.schema.json`.

Rules:
- Every property has a `description` in plain words.
- Every schema has at least one example in `../examples/`.
- Additive changes only within a major version.
- Profile schemas live in the profile's own folder, not here.
