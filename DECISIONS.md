# Decisions

Why the Scribe Exchange Protocol is the way it is. One numbered entry per decision; a later entry may amend an earlier one but never deletes it. Plain words; the jargon term is given with its explanation the first time.

## D1. Format: prose for people, schemas for machines
`spec/*.md` is the prose. `schemas/*.json` (JSON Schema: a file describing the exact shape of a JSON object) is the machine source of truth; when prose and schema disagree, the schema wins. `examples/*.json` are checked against the schemas in CI. `openapi.yaml` is generated from schemas plus the endpoint list, never hand-written. *Open:* whether the endpoint list is Markdown only or also a small YAML so OpenAPI can be generated fully.

## D2. Vendor-neutral, field-neutral, implementation-neutral
The spec describes a *client* and a *scribe service*. It never names an implementation; Lipi is the reference implementation, one of many. Nothing field-specific (healthcare, law, government) and nothing vendor-specific in the base; fields are served by **profiles** (D14).

## D3. Licence
Apache-2.0 for prose and schemas alike: one licence, its patent clause reassures implementers, and schema files can be copied into client code. No patents are sought on the protocol (defensive publication).

## D4. Major version in the path, minor pinned by header
`/v1/…`. Within a major only additive changes: new optional fields, endpoints, event types, values in open lists. Closed lists (statuses, error codes) never gain values within a major. An optional `Scribe-Exchange-Version: 1.2` request header pins a minor; every response carries the minor used. Deprecation: announce in discovery, warn with `Scribe-Exchange-Deprecated` / `-Sunset` headers for 6 months, remove after 12.

## D5. Header names are product-prefixed, never `X-`
`Scribe-Exchange-*`, following RFC 6648 and current practice. A profile prefixes its own headers with its own name.

## D6. Open lists and closed lists
"Open" means a service may add values and clients must ignore unknown ones (source kinds, document forms, export formats, delivery modes). "Closed" means only the listed values exist in this major (statuses, error codes, warning codes). This is what makes minors safe.

## D7. Authentication stops at the token
The protocol says two things: send a bearer token in `Authorization`; discovery names the OpenID Connect / OAuth 2 authorization server(s) that issue tokens (`auth.authorization_servers`, as the Model Context Protocol does). People use authorization code + PKCE; servers use client credentials. Everything else (login screens, passwords, cookies, API keys, roles, who may see what, settings, admin, audit) is implementation. Consequence: a small deployment with no identity system needs an implementation that ships a built-in authorization server. *Amends an earlier draft that specified login methods, API keys and cookie sessions in the protocol.*

## D8. Discovery declares capabilities, not vendors
`/.well-known/scribe-exchange`. Models are listed as the deployer's enabled models in two lists, `stt` (speech-to-text) and `structuring`, with ids opaque to clients; no tiers. Document forms (`markdown`, `json`, …), export formats, delivery modes, source kinds and limits are all declared here. The protocol mandates no particular document form; a service produces at least one of the forms it declares for every document.

## D9. Sessions are folders; inputs are sources
A session has no outcome: `active | archived`, never times out. Everything put in is a **source** with a `kind` from an open list; v0.1 defines `audio`, `text`, `file`, `reference`. Only `audio` has a lifecycle (`created → recording → processing → success | failed | cancelled`); others are `ready | failed`. Any number of sources, any time while active; a second recording is a second audio source. Sources are immutable except `label`, so a document's record of which sources it used stays true. What a service does with a text/file/reference when writing is implementation. Shortcut: a session may be created with its first sources in the same call. Rejected: "audio is the session, the rest are attachments"; a `role: primary | context` label (a template concern).

## D10. Audio lifecycle
Chunks are numbered from 0 and sent to a URL the service hands out (`transport`); the client never builds upload URLs. Audio format is declared per chunk with `Content-Type`; all chunks of one recording share it. `end` carries an optional `chunks_total`; the service answers with what it has and the gaps; the client fills gaps and ends again. The service ends a recording itself at the maximum length or after inactivity and processes what it has, with a warning; a recording that never received audio is `cancelled` (`no_audio`). No "expired" state anywhere. Two models are chosen separately: `stt_model` on the audio source, the structuring model on the document.

## D11. One status vocabulary
`success | failed` for things that run (audio sources, documents, jobs); `cancelled` for a recording with no result; `ready` for sources that need no work; `active | archived` for sessions. Problems that did not stop a thing are `warnings[]`, never a `partial` state.

## D12. Documents: current content and a revision number, no mandated history
A document holds its current content plus a `revision` that rises on every save. Save sends `If-Match: <revision>`; a stale one gets `409` with the current revision and the client decides; `If-Match: *` skips the check. `document.saved` fires on every save so clients or plugins may keep history; a service that keeps it says `document_history: true`.

## D13. Deletion of a session is required
Every compliant service can delete a session and everything in it (sources, audio, transcripts, documents). Deleting people is the implementation's job.

## D14. Profiles add, never change
A profile is a named extension for one field: optional fields on base objects, extra objects and routes under `/v1/profiles/{name}/`, template packs with strict output schemas, event types. It may not change a base object. Discovery lists installed profiles. The base spec names no profile.

## D15. Home
The protocol has its own repository from the start, separate from any implementation, so that its independence is visible and others can work on it without pulling a server. Implementations pin it by tag.
