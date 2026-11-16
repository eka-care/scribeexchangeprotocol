# 11. Errors

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: [`11-error.schema.json`](../schemas/11-error.schema.json)

---

## 11.1 One shape

Every error response, from every endpoint, is JSON of this shape with one of the nine HTTP statuses in 11.2:

```json
{
  "error": {
    "code": "revision_conflict",
    "message": "Document is at revision 3; you sent If-Match: 2.",
    "details": { "current_revision": 3 }
  }
}
```

| Field | Type | Meaning |
|---|---|---|
| `code` | string | A name from the closed list in 11.3. This is what a client branches on. |
| `message` | string | For a person reading logs. Plain words, in English, no secrets. Clients MUST NOT parse it. |
| `details` | object | Optional. Extra facts about this error; the chapter that defines the code says what goes in it (for `revision_conflict`, the current document). Absent when there is nothing to add. |

A client reads `code` first and the HTTP status second. The status is there for proxies, logs and generic HTTP libraries; the code is the contract.

Streamed responses (chapter 10) carry a failure as an `error` event with the same `code` and `message` instead of an HTTP status, because the status was already sent.

## 11.2 HTTP status

| Status | Used for |
|---|---|
| `400` | The request is malformed or names something discovery does not list. Fix the request. |
| `401` | No usable credential. Get one (chapter 5). |
| `403` | The credential is fine; the action is not allowed on this object. |
| `404` | The thing does not exist, or the caller may not see it; the two are not distinguished. |
| `409` | The thing exists but is in a state where this action does not apply, or someone else changed it first. |
| `413` | The body is bigger than what is accepted. |
| `429` | Too many requests; wait as long as `Retry-After` says (chapter 12). |
| `500` | The service failed. Retry later. |
| `503` | The service is not available right now. Retry after `Retry-After` when present. |

`400` covers everything wrong with the request itself, including a missing `If-Match` and a value over a limit the service declared in discovery; the code says which. `413`, `429` and `503` may also come from infrastructure in front of the service (a proxy, a load balancer), without the JSON body; a client treats a bodiless one of these by status alone.

## 11.3 Codes

The list is closed: a service MUST NOT invent codes, and a new code is a new minor version (chapter 3). A client that meets a code it does not know treats it by HTTP status.

| Code | HTTP | Defined in | Retry? |
|---|---|---|---|
| `unsupported_version` | 400 | 3 | no |
| `invalid_request` | 400 | 6, 10 | no |
| `invalid_source` | 400 | 6 | no |
| `invalid_template` | 400 | 9 | no |
| `metadata_too_large` | 400 | 6 | no |
| `payload_required` | 400 | 7 | no |
| `authentication_failed` | 401 | 5 | after a new credential |
| `token_expired` | 401 | 5 | after a new credential |
| `forbidden` | 403 | 5 | no |
| `session_not_found` | 404 | 6 | no |
| `source_not_found` | 404 | 6, 8 | no |
| `chunk_not_found` | 404 | 8 | yes, shortly, while recording |
| `template_not_found` | 404 | 9, 10 | no |
| `document_not_found` | 404 | 10 | no |
| `invalid_state` | 409 | 6, 8, 10 | after the state changes |
| `revision_conflict` | 409 | 10 | after reading the current document |
| `payload_too_large` | 413 | 7 | no |
| `content_too_large` | 413 | 10 | no |
| `kind_not_supported` | 400 | 6 | no |
| `source_limit_reached` | 400 | 6 | no |
| `source_too_large` | 400 | 6 | no |
| `source_not_recording` | 400 | 6, 7 | no |
| `format_mismatch` | 400 | 7 | no |
| `chunk_too_long` | 400 | 7 | no |
| `audio_too_long` | 400 | 7 | no |
| `template_limit_reached` | 400 | 9 | no |
| `precondition_required` | 400 | 10 | with `If-Match` |
| `rate_limited` | 429 | 12 | after `Retry-After` |
| `internal_error` | 500 | 11 | yes, with backoff |
| `unavailable` | 503 | 11 | yes, after `Retry-After` |

Codes that arrive inside a stream rather than as an HTTP response: `generation_failed`, `output_invalid`, `internal_error` (chapter 10, `error` event). Codes that arrive inside an object rather than as a response: `failure.code` on an audio source (chapter 6).

## 11.4 Retrying

- A `5xx`, or a dropped connection with no response, MAY be retried based on the service's capabilities / instructions. Uploads of chunks and saves with `If-Match` are safe to repeat: a chunk index is idempotent, and a stale `If-Match` is refused rather than applied twice.
- A `429` or `503` with `Retry-After` is retried no sooner than the header says.
- A `4xx` other than those is not retried unchanged; the table in 11.3 says what has to change first.

## 11.5 Summary

No endpoints. Every chapter's error table lists the codes it uses; this chapter is the index.

---

**Previous:** [10. Generation and documents](./10-documents.md) · **Next:** [12. Security](./12-security.md)
