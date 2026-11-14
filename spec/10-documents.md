# 10. Generation and documents

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: [`10-generate-request.schema.json`](../schemas/10-generate-request.schema.json), [`10-document.schema.json`](../schemas/10-document.schema.json), [`10-document-create-request.schema.json`](../schemas/10-document-create-request.schema.json)

---

## 10.1 Two separate things

**Generation** is a call: take a session's sources, a template and a model, and write. The service streams the text back as it is written. Nothing is stored; to get it again, call again.

A **document** is a place to save text. The first save creates it; every later save replaces its content and raises a counter, the `revision`, that stops two writers from overwriting each other unknowingly.

The client joins the two: it generates, lets the user read or edit, and saves what it wants kept. The document does not need to know where its text came from.

## 10.2 Generate

```http
POST /v1/sessions/{id}/generate
Content-Type: application/json

{ "template_id": "01J9ZR4D5E6F7G8H9J0K1M2N3P", "structuring_model": "llama-3.3-70b", "source_ids": ["01J9ZN7B8C9D0E1F2G3H4J5K6M", "01J9ZN9D0E1F2G3H4J5K6M7N8P"] }
```

| Field | Required | Meaning |
|---|---|---|
| `template_id` | yes | The template to apply (chapter 9). |
| `structuring_model` | no | An id from `models.structuring`. Default: the one marked `default`. |
| `source_ids` | no | Which sources to read. Default: every source in the session that is `ready` or `success`. When given, each id MUST be a source of this session in one of those states. |

The response is a stream of events (`Content-Type: text/event-stream`, one JSON object per event):

```
200
event: started
data: {"template_id":"01J9ZR4D5E6F7G8H9J0K1M2N3P","structuring_model":"llama-3.3-70b","output_format":"markdown","source_ids":["01J9ZN7B8C9D0E1F2G3H4J5K6M","01J9ZN9D0E1F2G3H4J5K6M7N8P"]}

event: delta
data: {"text":"## Chief complaint\n"}

event: delta
data: {"text":"Headache for three days, no fever.\n"}

event: done
data: {"content":"## Chief complaint\nHeadache for three days, no fever.\n…","warnings":[]}
```

| Event | Sent | Data |
|---|---|---|
| `started` | always, first | What is being applied to what: `template_id`, `structuring_model`, `output_format`, `source_ids` (the ones actually read). |
| `delta` | zero or more | `text`: the next piece of the output, in order. For `json` the pieces are fragments of the JSON text. Joined, the deltas equal `content`. A service whose writer does not stream sends none. |
| `done` | on success, last | `content`: the whole output, a string for `markdown`, `text`, `html` and an object for `json` (validated against the template's `output_json_schema` when there is one). `warnings`: problems that did not stop it, closed list `no_sources`, `source_ignored` (`code`, `message`, optional `source_id`). |
| `error` | on failure, last | `code`, `message`. Codes: `generation_failed`, `output_invalid` (the writer could not satisfy the schema), `internal_error`. |

A session with no usable source still produces output (`warnings: [no_sources]`): whatever the template makes of nothing. Refused with `409 invalid_state` on an `archived` session, before any event.

If the connection drops, the output is lost; the client calls again.

## 10.3 The document object

```json
{
  "id": "01J9ZP3C4D5E6F7G8H9J0K1M2N",
  "session_id": "01J9ZM1A2B3C4D5E6F7G8H9J0K",
  "output_format": "markdown",
  "content": "## Chief complaint\nHeadache for three days, no fever. Worse in the evening.\n\n## History\n…",
  "revision": 2,
  "created_at": "2026-10-22T06:25:41.300Z",
  "updated_at": "2026-10-22T06:31:05.000Z"
}
```

| Field | Type | Meaning |
|---|---|---|
| `id` | ULID | |
| `session_id` | ULID | The session it belongs to; documents live under their session. |
| `output_format` | string | What `content` is: one of discovery's `output_formats`. Fixed at creation. |
| `content` | string \| object | A string for `markdown`, `text`, `html`; an object for `json`. Up to `capabilities.documents.max_content_bytes`. |
| `revision` | integer | `1` when created; rises by one on every save. |
| `created_at`, `updated_at` | timestamp | `updated_at` moves on every save. |

## 10.4 Create

```http
POST /v1/sessions/{id}/documents
Content-Type: application/json

{ "output_format": "markdown", "content": "## Chief complaint\n…" }
```

`201` with the document, `revision: 1`. Refused with `409 invalid_state` on an `archived` session. A session may hold any number of documents.

## 10.5 Save

The client holds the whole `content` and sends it back:

```http
PUT /v1/sessions/{id}/documents/{did}
If-Match: 1
Content-Type: application/json

{ "content": "## Chief complaint\nHeadache for three days, no fever. Worse in the evening.\n…" }
```

`If-Match` carries the `revision` the client started from. If it is still current, the service stores the content, raises `revision` by one and answers `200` with the document. If not, `409 revision_conflict` with the current document in the body; the client merges and tries again. `If-Match: *` skips the check and accepts last-write-wins knowingly. Without the header: `428 precondition_required`.

`content` MUST be of the document's `output_format`. The service keeps the current content only; earlier revisions are the client's to keep if it wants them.

## 10.6 Read, list, delete

```http
GET /v1/sessions/{id}/documents
GET /v1/sessions/{id}/documents/{did}
DELETE /v1/sessions/{id}/documents/{did}
```

List returns the session's documents that are visible to the caller, newest first. Pagination as for sessions.

A document's visibility is its own, not inherited from its session: a service may let a caller see a document without letting it see the session (the session then answers `404` to that caller, the document `200`). What "visible" means is the service's policy. Delete answers `204`; chapter 12 says what "removed" means.

## 10.7 Limits come from discovery

`capabilities.documents.max_content_bytes` (chapter 4): the largest `content` accepted on create or save, and the largest a generation will produce.

## 10.8 Errors

| Code | HTTP | When |
|---|---|---|
| `template_not_found` | 404 | `template_id` names no template the caller may see. |
| `document_not_found` | 404 | Unknown id, or not visible to this caller. |
| `invalid_request` | 400 | Missing field; `structuring_model` or `output_format` not in discovery; a `source_ids` entry not in this session or not usable; `content` not of the document's format. |
| `content_too_large` | 413 | `content` over `max_content_bytes`. |
| `revision_conflict` | 409 | `If-Match` is not the current revision. Body: the current document. |
| `invalid_state` | 409 | Generate on, or create a document in, an archived session. |
| `precondition_required` | 428 | `PUT` without `If-Match`. |

## 10.9 Summary of endpoints

| Method | Path | Required? |
|---|---|---|
| POST | `/v1/sessions/{id}/generate` | yes |
| POST, GET | `/v1/sessions/{id}/documents` | yes |
| GET, PUT, DELETE | `/v1/sessions/{id}/documents/{did}` | yes |

---

**Previous:** [9. Templates](./09-templates.md) · **Next:** [11. Jobs](./11-jobs.md)
