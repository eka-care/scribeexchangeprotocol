# Changelog — Scribe Exchange Protocol

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow the protocol version.

## [Unreleased]

### Added
- Repository layout: `spec/`, `schemas/`, `examples/`, `validate.py`, `tools/`, generated `openapi.yaml`.
- Chapters 01–14: introduction, architecture, versioning, discovery, authentication, sessions and sources, audio input, transcripts, templates, generation and documents, errors, security, profiles, conformance.
- Schemas and examples for every object and request body; one error shape.
- `tools/gen_openapi.py` and `tools/endpoints.yaml`: `openapi.yaml` is generated from the schemas and the endpoint list, and validated as OpenAPI 3.1.

### Shape of v0.1, in short
- A session is a folder of sources; audio is the one required kind. Sources are immutable; a session is archived with `PATCH` and is then read-only.
- Audio goes to the URL in a source's `transport`; `put` (under the service's API) is always offered, `post-form` (straight to a store) is a service's option the client opts into. The audio format is fixed on the source.
- A transcript is read chunk by chunk while recording and whole once the source is `success`; timestamps are `audio_offset_ms` (audio timeline), `received_at` (service clock) and `recorded_at` (client clock, sent with `end`).
- A template is instructions plus an output format. Generation is a streamed call that stores nothing; a document is text the client saved, with a `revision` guarded by `If-Match`.
- Deletion covers the service's own store only. No job object, no export, no webhooks: anything that takes time carries its own status or streams.
- Nine HTTP statuses; the error code is the contract.

### Notes
- Decisions behind the design are in `DECISIONS.md`.
