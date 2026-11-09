# 1. Introduction

**Scribe Exchange Protocol v0.1 (draft)**

---

## 1.1 Purpose

The Scribe Exchange Protocol is an open, vendor-neutral set of rules for how a **client** talks to a **scribe service**.

A *scribe service* is a server that takes recorded speech (or an already-written transcript), turns it into a transcript, and then turns that transcript into one or more **documents** using **templates**. A *client* is anything that uses such a service: a web app, a mobile app, a desktop app, or another backend.

The protocol exists so that:

- a client written once works against any compliant scribe service;
- a scribe service written once can be used by any compliant client;
- different fields (healthcare, government, law, education…) can add what they need on top without changing the base.

Lipi is the reference implementation. It is one implementation among others, not the owner of the protocol. This specification never names an implementation; it says "the scribe service".

## 1.2 Scope

### In scope

- Discovery: how a client learns what a service supports.
- Authentication: how a client presents a credential, and how it learns where credentials come from.
- Sessions: a folder of **sources** (recordings, notes, files, references to earlier work) and everything made from them.
- Audio input: chunked recording, single-file upload; streaming is reserved for a later version.
- Transcripts: the text of what was said in a recording, with timestamps, speakers and language where available.
- Templates: the recipe that says what a document should contain.
- Documents: the structured result, its forms, versions and export.
- Jobs: how a client follows work that runs in the background.
- Events and webhooks: how a service tells a client that something happened.
- Deletion: removing a session and everything in it.
- Errors, security, profiles, conformance (chapters 14–17).

### Out of scope

- How the service does transcription or structuring internally, or which AI models it uses.
- Billing.
- Users, roles, login screens, permissions, settings, administration, plugins, audit logs, health checks. These belong to the implementation (Lipi has all of them); the protocol only requires a bearer token and says where to get one.
- The editor's own document format. A service declares which document forms it produces (chapter 4); the protocol does not pick one.
- Anything specific to one field. That is what **profiles** are for (chapter 16).
- Live (real-time) transcription. The objects leave room for it; the endpoints come in a later version.

## 1.3 Terms

| Term | Meaning in this specification |
|---|---|
| **Client** | Any program that calls the service: an app, an SDK inside an app, or another server. |
| **Scribe service** (or just **service**) | The server that implements this protocol. |
| **Caller** | Whoever holds the bearer token on a request: a person through an app, or another server. The token's subject identifies the caller; what the caller may see is the service's policy. |
| **Session** | A folder: the sources put into it over time, and the documents made from them. Stays active as long as its owner wants. |
| **Source** | One thing put into a session: a recording (`audio`), a pasted note (`text`), a file (`file`), or a pointer to an earlier session or document (`reference`). Only `audio` has a lifecycle; the others are simply there. |
| **Chunk** | A short piece of audio (a few seconds). Recordings are sent as numbered chunks. |
| **Transcript** | The text of what was said in one recording, as an ordered list of **segments**. |
| **Segment** | One piece of a transcript: text, start and end time, and, when known, speaker, language, confidence. |
| **Template** | The recipe for a document: its sections, what each section should contain, the output language, and what the writer may use. A template never chooses an AI model. |
| **Document** | The structured result of applying a template to a transcript. Has one or more **forms** (markdown, JSON, HTML…); which forms, the service declares in discovery. |
| **Revision** | A number on a document that rises on every save. Clients send the revision they edited so two people cannot overwrite each other unknowingly. |
| **Job** | A piece of work the service runs in the background (transcribing, structuring). The client can ask for its status. |
| **Event** | A record that something happened (`session.success`, `document.success`…). Delivered to webhooks. |
| **Webhook** | A URL the client registers; the service calls it when an event happens. |
| **Discovery document** | A public JSON file the service publishes saying what it supports. |
| **Profile** | An extension of this protocol for one field. It adds; it never changes the base. |
| **Model** | An AI model the service can use. Two kinds: **STT** (speech-to-text) and **structuring** (writes the document). |

## 1.4 Conformance

The key words MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are to be read as in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119): MUST is required, SHOULD is recommended, MAY is optional.

### A conformant scribe service

- MUST publish a valid discovery document at `/.well-known/scribe-exchange` (chapter 4).
- MUST serve all endpoints marked REQUIRED under `/v1/` (chapters 5–13).
- MUST accept a bearer token in the `Authorization` header and MUST say in discovery where tokens come from (chapter 5).
- MUST accept the `audio` source kind with at least one input mode, `chunked` or `file`, and MUST declare every accepted source kind and its limits in discovery (chapters 4, 6, 7).
- MAY accept other source kinds (`text`, `file`, `reference`), each declared in discovery.
- MUST produce a transcript for every audio source that reaches `success`.
- MUST declare in discovery which document forms it produces (`capabilities.document_forms`) and MUST produce at least one of the declared forms for every document (chapter 10).
- MUST follow the error shape and codes (chapter 14).
- MUST sign every webhook delivery and include an event id (chapter 12).
- MUST offer deletion of a session and everything in it (chapter 13).
- SHOULD support webhooks; MAY support only polling.
- MUST NOT add field-specific objects to the base; those go in a profile (chapter 16).

### A conformant client

- MUST read the discovery document before its first call and MUST respect the capabilities it declares (audio formats, chunk limit, input modes).
- MUST send its credential as `Authorization: Bearer <token>` and nowhere else (chapter 5).
- MUST explicitly end a recording it started (chapter 6).
- MUST read `capabilities.document_forms` and work with the forms the service produces.
- A client with a server-side part (another backend, an integration) SHOULD receive results through webhooks; it MUST verify their signatures and MUST treat a repeated event id as the same event (chapter 12). Browser and mobile clients have no server to receive a webhook; they poll (chapter 11).
- SHOULD handle a document that failed without discarding the others in the same session.

The conformance test suite (chapter 17) is the executable form of these lists.

## 1.5 Conventions

- **HTTP examples** show method, path and the relevant headers only. `{id}` is a path parameter.
- **JSON** field names are `snake_case`. Unknown fields MUST be ignored by both sides (this is what makes additive changes safe).
- **Identifiers** are ULIDs (26 characters, sortable by creation time, safe in URLs), for example `01J9ZK3M8QW4R2T6V8X0Y1Z2A3`. Clients MUST treat them as opaque strings.
- **Timestamps** are ISO 8601 in UTC with millisecond precision: `2026-10-21T09:30:00.000Z`. Durations and offsets inside audio are integers in **milliseconds** (`start_ms`, `end_ms`), never floating seconds.
- **Languages** are BCP 47 tags (`en`, `hi`, `ta`, `en-IN`).
- **Audio formats** are MIME types (`audio/webm;codecs=opus`).
- `example.com` and `01J…` values in examples are placeholders.
- The JSON Schema files in `../schemas/` are the source of truth for every object. If prose and schema disagree, the schema is right and the prose has a bug.

---

**Next:** [2. Architecture](./02-architecture.md)
