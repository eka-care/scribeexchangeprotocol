# Specification chapters

Written one at a time, reviewed before the next. A chapter is "done" when its objects have schemas in `../schemas/` and valid examples in `../examples/`.

| # | File | Covers | Status |
|---|---|---|---|
| 01 | `01-introduction.md` | Purpose, scope, terms, conformance | draft |
| 02 | `02-architecture.md` | Actors (client, scribe service, authorization server, webhook receiver), the flow, integration patterns | draft |
| 03 | `03-versioning.md` | `/v1/` in the path, additive rule, deprecation | draft |
| 04 | `04-discovery.md` | `/.well-known/scribe-exchange`: versions, authorization servers, capabilities, models (stt + structuring), languages, profiles | draft |
| 05 | `05-authentication.md` | Bearer token; discovery names the authorization server (OpenID Connect / OAuth 2); nothing else | draft |
| 06 | `06-sessions.md` | Sessions as folders (`active` / `archived`) and **sources** (`audio`, `text`, `file`, `reference`); the audio source lifecycle, `end` with gaps, `transport` | draft |
| 07 | `07-audio-input.md` | Sending audio to an audio source: chunks, single file, (stream v2); direct upload; file-source upload | planned |
| 08 | `08-transcripts.md` | Transcript and segment objects, partial transcripts while recording | planned |
| 09 | `09-templates.md` | Template object (sections, kinds, instructions, output language, tools, knowledge), CRUD, packs | planned |
| 10 | `10-documents.md` | Document object, forms as declared in discovery, generate, save, `revision`, export | planned |
| 11 | `11-jobs.md` | Job object and status endpoint | planned |
| 12 | `12-webhooks-and-events.md` | Event catalogue, webhook CRUD, signing, retries, duplicate safety | planned |
| 13 | `13-deletion.md` | Delete a session and everything in it: what is removed, the event | planned |
| 14 | `14-errors.md` | Error shape, codes, HTTP mapping, retry guidance | planned |
| 15 | `15-security.md` | TLS, credentials, webhook verification, rate limits, audit | planned |
| 16 | `16-profiles.md` | How a profile declares itself, where it lives, what it may add | planned |
| 17 | `17-conformance.md` | What a server and a client must pass; the test suite | planned |

Seventeen chapters. Users, roles, settings and administration are deliberately absent: they belong to implementations.
