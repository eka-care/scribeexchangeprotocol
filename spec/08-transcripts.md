# 8. Transcripts

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: [`08-transcript-chunk.schema.json`](../schemas/08-transcript-chunk.schema.json), [`08-transcript.schema.json`](../schemas/08-transcript.schema.json)

---

## 8.1 What a transcript is

A **transcript** is the text of one recording. It belongs to its audio source (chapter 6) and is read under it. There are two views:

- **Chunk by chunk, while recording** — each uploaded chunk gets its own text as soon as the service has transcribed it. This is the live view.
- **Whole, at the end** — once the source is `success`, one object holds the complete text.

For `input: file` only the whole view applies.

## 8.2 The chunk object

```http
GET /v1/sessions/{id}/sources/{sid}/transcript/chunks/{n}
```

```json
{
  "index": 3,
  "status": "success",
  "audio_offset_ms": 64120,
  "received_at": "2026-10-22T06:11:40.210Z",
  "recorded_at": "2026-10-22T06:11:14.000Z",
  "text": "Teen din se sar dard hai. Bukhar nahi hai."
}
```

| Field | Type | Meaning |
|---|---|---|
| `index` | integer | The chunk's upload index (chapter 7). |
| `status` | string | Closed list: `queued` (received, not yet transcribed), `success` (text ready), `failed` (could not be transcribed; the source carries a `chunk_skipped` warning). |
| `audio_offset_ms` | integer \| null | Where this chunk starts on the audio timeline: the summed length of chunks `0 … n−1`, from decoding them. `null` while any earlier chunk is missing. Pauses between chunks are not audio and are not counted. |
| `received_at` | timestamp | When the bytes reached the service's storage (service clock). |
| `recorded_at` | timestamp \| null | The client's own clock for when the chunk was recorded, as sent with `end` (6.8). `null` until then, or when the client sent none. |
| `text` | string \| null | What was said in this chunk. `null` unless `success`. |

Rules:

- `404 chunk_not_found` until the service holds the chunk. Right after an upload under `post-form` the service may not have noticed the bytes yet; a client retries after a moment.
- Once `success`, the object does not change (except `recorded_at` being filled at `end`). A client fetches each index once and keeps it.
- The service SHOULD transcribe chunks as they arrive. `chunks.transcribed` on the source counts how many are `success` or `failed`.

A client building a live view: upload chunk `n`, poll `…/chunks/{n}` until `success` or `failed`, append the text. Under `put` the upload response is already this object (7.2), often with `status: success`, in which case there is nothing to poll.

## 8.3 The transcript object

```http
GET /v1/sessions/{id}/sources/{sid}/transcript
```

```json
{
  "source_id": "01J9ZN7B8C9D0E1F2G3H4J5K6M",
  "stt_model": "whisper-large-v3",
  "language_detected": "hi",
  "duration_ms": 871240,
  "text": "Namaste, kya takleef hai?\nTeen din se sar dard hai. Bukhar nahi hai.\n…",
  "created_at": "2026-10-22T06:24:58.402Z"
}
```

| Field | Type | Meaning |
|---|---|---|
| `source_id` | ULID | The audio source. |
| `stt_model` | string | The speech-to-text model that produced it. |
| `language_detected` | string \| null | BCP 47 tag of the main spoken language, when the model reports one. |
| `duration_ms` | integer | Length of the audio transcribed. |
| `text` | string | The whole recording as plain text, chunks joined in index order, skipped chunks omitted. |
| `created_at` | timestamp | When the service joined it. |

Available once the source is `success`; before that `409 invalid_state`. The service writes it once, when the source completes, and it does not change. A `failed` source has no transcript object; its chunk objects stay readable.

> **[OPEN]** Whether a client may correct a transcript through the protocol, and how a document generated earlier records which text it read.

## 8.4 Errors

| Code | HTTP | When |
|---|---|---|
| `source_not_found` | 404 | Unknown source, or not an `audio` source. |
| `chunk_not_found` | 404 | No chunk with that index held by the service. |
| `invalid_state` | 409 | Transcript object requested before the source is `success`. |

## 8.5 Summary of endpoints

| Method | Path | Required? |
|---|---|---|
| GET | `/v1/sessions/{id}/sources/{sid}/transcript/chunks/{n}` | yes |
| GET | `/v1/sessions/{id}/sources/{sid}/transcript` | yes |

---

**Previous:** [7. Audio input](./07-audio-input.md) · **Next:** [9. Templates](./09-templates.md)
