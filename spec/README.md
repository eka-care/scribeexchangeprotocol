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
| 08 | `08-transcripts.md` | Transcript and segment objects, paging, partial transcripts while recording | draft |
| 09 | `09-templates.md` | Template object (sections, kinds, instructions, output language, tools, knowledge), CRUD, packs | planned |
| 10 | `10-documents.md` | Document object, forms as declared in discovery, generate, save, `revision`, export | planned |
| 11 | `11-jobs.md` | Job object, status endpoint, how a client learns work is done | planned |
| 12 | `12-deletion.md` | Delete a session and everything in it: what is removed | planned |
| 13 | `13-errors.md` | Error shape, codes, HTTP mapping, retry guidance | planned |
| 14 | `14-security.md` | TLS, credentials, rate limits | planned |
| 15 | `15-profiles.md` | How a profile declares itself, where it lives, what it may add | planned |
| 16 | `16-conformance.md` | What a server and a client must pass; the test suite | planned |

Sixteen chapters. Users, roles, settings, administration and push notifications belong to implementations.
