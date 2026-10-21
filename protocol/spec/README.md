# Specification chapters

Written one at a time, reviewed before the next. A chapter is "done" when its objects have schemas in `../schemas/` and valid examples in `../examples/`.

| # | File | Covers | Status |
|---|---|---|---|
| 01 | `01-introduction.md` | Purpose, scope, terms, conformance | planned |
| 02 | `02-architecture.md` | Actors (client, scribe service, identity provider, webhook receiver), the flow, integration patterns | planned |
| 03 | `03-versioning.md` | `/v1/` in the path, additive rule, deprecation | planned |
| 04 | `04-discovery.md` | `/.well-known/vaarta`: versions, auth methods, capabilities, models (stt + structuring), languages, profiles | planned |
| 05 | `05-authentication.md` | Bearer tokens, refresh, API keys, login methods | planned |
| 06 | `06-sessions.md` | Session object, states, create / get / list / end / delete, `audio_input` and `transport` | planned |
| 07 | `07-audio-input.md` | Chunked, file, (stream v2); chunk rules; direct upload | planned |
| 08 | `08-transcripts.md` | Transcript and segment objects, transcript upload as input | planned |
| 09 | `09-templates.md` | Template object (sections, kinds, instructions, output language, tools, knowledge), CRUD, packs | planned |
| 10 | `10-documents.md` | Document object, forms (raw / editor / markdown), generate, save, versions, export | planned |
| 11 | `11-jobs.md` | Job object and status endpoint | planned |
| 12 | `12-webhooks-and-events.md` | Event catalogue, webhook CRUD, signing, retries, duplicate safety | planned |
| 13 | `13-users-and-workspace.md` | Users, roles, the one workspace, admin endpoints | planned |
| 14 | `14-deletion.md` | Delete a session or a user: what is removed, the event | planned |
| 15 | `15-errors.md` | Error shape, codes, HTTP mapping, retry guidance | planned |
| 16 | `16-security.md` | TLS, credentials, webhook verification, rate limits, audit | planned |
| 17 | `17-profiles.md` | How a profile declares itself, where it lives, the healthcare profile as the first | planned |
| 18 | `18-conformance.md` | What a server and a client must pass; the test suite | planned |

Chapters 01–12 and 15–16 correspond to MedScribeAlliance's twelve chapters, generalised. Chapters 08, 10, 11, 13, 14, 17, 18 are new.
