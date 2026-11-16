# Specification chapters

Written one at a time, reviewed before the next. A chapter is "done" when its objects have schemas in `../schemas/` and valid examples in `../examples/`.

| # | File | Covers | Status |
|---|---|---|---|
| 01 | `01-introduction.md` | Purpose, scope, terms, conformance | draft |
| 02 | `02-architecture.md` | The two parties, the flow, the objects, the status vocabulary, profiles | draft |
| 03 | `03-versioning.md` | `/v1/` in the path, additive rule, deprecation | draft |
| 04 | `04-discovery.md` | `/.well-known/scribe-exchange`: versions, authorization servers, capabilities, models (stt + structuring), languages, profiles | draft |
| 05 | `05-authentication.md` | Bearer token; discovery names the authorization server (OpenID Connect / OAuth 2); nothing else | draft |
| 06 | `06-sessions.md` | Sessions as folders (`active` / `archived`) and **sources** (`audio`, `text`, `file`, `reference`); the audio source lifecycle, `end` with gaps, `transport` | draft |
| 07 | `07-audio-input.md` | Sending audio to the `transport` URL: chunk rules, single file, formats | draft |
| 08 | `08-transcripts.md` | Chunk text while recording, whole transcript at the end, timestamps | draft |
| 09 | `09-templates.md` | Template: instructions, output format, optional JSON schema; create, list, delete | draft |
| 10 | `10-documents.md` | Generate (a streamed call, nothing stored) and documents (saved text with `revision`) | draft |
| 11 | `11-errors.md` | One error shape, the closed code list, HTTP mapping, retry rules | draft |
| 12 | `12-security.md` | HTTPS, credentials only in headers, rate limits, isolation | draft |
| 13 | `13-profiles.md` | A named add-on for one field: what it may add, what it may not change, where it lives | draft |
| 14 | `14-conformance.md` | The service and client checklists, item by item, and the test suite | draft |

Fourteen chapters. Deletion is in chapter 6; everything that runs carries its own status or streams, so there is no job object. Users, roles, settings, administration and push notifications belong to implementations.
