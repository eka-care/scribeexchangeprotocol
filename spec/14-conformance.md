# 14. Conformance

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: none

---

## 14.1 What conformance means

A **scribe service** conforms when every item in 14.2 holds for it. A **client** conforms when every item in 14.3 holds for it. Each item names the chapter that defines it; this chapter adds nothing new, it collects.

A service may conform to the base and to any number of profiles (chapter 13); each profile has its own list.

## 14.2 A conformant scribe service

| # | Requirement | Chapter |
|---|---|---|
| S1 | Serves `/.well-known/scribe-exchange` over HTTPS with a document valid against `04-discovery.schema.json`. | 4, 12 |
| S2 | Serves every endpoint marked REQUIRED under `/v1/`; answers every call with `Scribe-Exchange-Version`. | 3, 6–10 |
| S3 | Accepts an optional `Scribe-Exchange-Version` on requests; answers `400 unsupported_version` for a minor it does not know. | 3 |
| S4 | If `auth` is not `null` in discovery: accepts `Authorization: Bearer <token>` and refuses calls without one with `401`. If `auth` is `null`: answers calls with no `Authorization` header. | 5 |
| S5 | Creates sessions, lists and reads them, archives with `PATCH`, deletes with `DELETE`; an archived session refuses every change with `409 invalid_state`. | 6 |
| S6 | Accepts the `audio` source kind with `chunked` or `file` input; declares in discovery every kind it accepts and every limit it enforces. | 4, 6 |
| S7 | Returns a `transport` of kind `put` on every audio source for a client that lists only `put`. | 6, 7 |
| S8 | Accepts chunks in any order, replaces a re-sent index, refuses a `Content-Type` other than the source's `format`. | 7 |
| S9 | Answers `end` with the gaps it sees; keeps the source `recording` while gaps remain; moves it on when none do; ends a recording itself at `max_seconds` and after `inactivity_seconds`. | 6 |
| S10 | Serves a chunk's text by index once transcribed, and the whole transcript once the source is `success`. | 8 |
| S11 | Creates, lists, reads and deletes templates; refuses `output_json_schema` without `json`. | 9 |
| S12 | Streams generation as `started`, `delta`*, then `done` or `error`; the joined deltas equal `content`; `json` content validates against the template's schema. | 10 |
| S13 | Creates, reads, lists, saves and deletes documents under their session; `PUT` without `If-Match` is `400 precondition_required`; a stale `If-Match` is `409 revision_conflict` with the current document. | 10 |
| S14 | Deleting a session makes it and everything in it answer `404`. | 6 |
| S15 | Every error is the shape of chapter 11 with a code from its list and one of its nine statuses. | 11 |
| S16 | Serves nothing over plain HTTP; never puts a credential in a URL, log line or error message. | 12 |
| S17 | Adds nothing field-specific to the base; profiles live under `/v1/profiles/{name}/`. | 13 |

## 14.3 A conformant client

| # | Requirement | Chapter |
|---|---|---|
| C1 | Reads discovery before its first call and stays within the capabilities it declares (formats, chunk length, counts, sizes). | 4 |
| C2 | Sends `Authorization: Bearer <token>` when discovery's `auth` is not `null`; obtains the token from an authorization server discovery names. | 5 |
| C3 | Ignores fields it does not know and does not fail on an unknown value in an open list. | 3 |
| C4 | Sends audio only to the URL in the source's `transport`, with `Content-Type` equal to the source's `format`; cuts chunks at or under `max_chunk_seconds`, each a complete file in its format. | 7 |
| C5 | Ends every recording it started, re-sends the gaps `end` reports, and ends again. | 6 |
| C6 | Reads the whole transcript only once the source is `success`; reads chunk texts by index before that. | 8 |
| C7 | Asks only for output formats discovery lists. | 4, 9 |
| C8 | Consumes a generation stream to `done` or `error`; on a lost connection, calls again. | 10 |
| C9 | Sends `If-Match` on every save; on `409 revision_conflict`, reads the current document before saving again. | 10 |
| C10 | Branches on `error.code`, not on `message`; honours `Retry-After`. | 11, 12 |

## 14.4 The test suite

A conformance test suite runs against a service's discovery URL and a credential, exercises each item in 14.2 in order, and reports pass or fail per item. It is code, kept beside this specification, and versioned with it; a service claims conformance to a base version by passing that version's suite. Client conformance is checked by review against 14.3; a reference service may offer a mode that logs each client requirement as it is met.

---

**Previous:** [13. Profiles](./13-profiles.md) · **Next:** none; this is the last chapter.
