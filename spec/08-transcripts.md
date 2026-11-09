# 8. Transcripts

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: [`08-transcript.schema.json`](../schemas/08-transcript.schema.json), [`08-transcript-segments-page.schema.json`](../schemas/08-transcript-segments-page.schema.json)

---

## 8.1 What a transcript is

A **transcript** is the text of one recording: what was said, in order, with the time each piece was said and, where the speech-to-text model provides them, who said it, in which language, and how sure the model is. It is made from one audio source and belongs to it (`source.transcript_id`).

The transcript grows while the recording is in progress and is complete when the audio source reaches `success`.

## 8.2 The transcript object

```json
{
  "id": "01J9ZM9Q8R7S6T5V4W3X2Y1Z0A",
  "session_id": "01J9ZM1A2B3C4D5E6F7G8H9J0K",
  "source_id": "01J9ZN7B8C9D0E1F2G3H4J5K6M",
  "complete": true,
  "stt_model": "whisper-large-v3",
  "language_detected": "hi",
  "duration_ms": 871240,
  "segment_count": 212,
  "text": "S1: Namaste, kya takleef hai?\nS2: Teen din se sar dard hai…",
  "created_at": "2026-10-22T06:10:09.004Z",
  "updated_at": "2026-10-22T06:24:58.402Z"
}
```

| Field | Type | Meaning |
|---|---|---|
| `id` | ULID | |
| `session_id`, `source_id` | ULID | Where it belongs. |
| `complete` | boolean | `true` once every chunk is transcribed and joined. `false` while the recording is in progress. |
| `stt_model` | string | The speech-to-text model that produced it. |
| `language_detected` | string \| null | BCP 47 tag of the main spoken language, once known. |
| `duration_ms` | integer | Length of audio transcribed so far. |
| `segment_count` | integer | Number of segments so far. |
| `text` | string | A plain-text rendering of the segments in order, one segment per line, prefixed with the speaker label when there is one. Convenient for display; the segments are the data. |
| `created_at`, `updated_at` | timestamp | `updated_at` moves every time segments are added. |

## 8.3 Segments

A **segment** is one piece of speech.

```json
{
  "index": 17,
  "text": "Teen din se sar dard hai.",
  "start_ms": 64120,
  "end_ms": 66880,
  "speaker": "S2",
  "language": "hi",
  "confidence": 0.93,
  "chunk_index": 2
}
```

| Field | Type | Meaning |
|---|---|---|
| `index` | integer | Position in the transcript, from 0, in time order. |
| `text` | string | What was said. |
| `start_ms`, `end_ms` | integer | Offsets from the start of the recording, in milliseconds. |
| `speaker` | string \| null | A label the model assigned to tell speakers apart (`S1`, `S2`, …). Present when the model separates speakers (`features.diarization`). The label is opaque; a profile may define meanings. |
| `language` | string \| null | BCP 47 tag for this segment, when the model reports it. |
| `confidence` | number \| null | 0 to 1, when the model reports it. |
| `chunk_index` | integer | Which uploaded chunk this came from. |

A service fills what its model provides and leaves the rest `null`. The fields are there so that every client reads one shape whatever the model.

## 8.4 Reading a transcript

```http
GET /v1/transcripts/{id}
```
Returns the transcript object. `200`.

```http
GET /v1/transcripts/{id}/segments?after_index=16&limit=200
```
Returns a page of segments in order:

```json
{ "segments": [ … ], "next_after_index": 216, "complete": true }
```

`after_index` (default: from the start) and `limit` (default 200, max 1000) page through long transcripts. `next_after_index` is the value to pass for the next page, or `null` when there are no more segments *yet*; `complete` says whether more may still arrive.

**While recording**, segments appear as chunks are transcribed; a client polls `/segments` with the last `next_after_index` it saw. Segments already returned keep their index and content.

The transcript is also reachable through its source: `GET /v1/sessions/{id}/sources/{sid}/transcript` returns the same object.

## 8.5 Lifecycle

| Audio source status | Transcript |
|---|---|
| `created` | none yet (`transcript_id` is `null`) |
| `recording` | exists once the first chunk is transcribed; `complete: false`; grows |
| `processing` | last chunks being transcribed and joined; `complete: false` |
| `success` | `complete: true`; `language_detected` and `duration_ms` final |
| `failed` | whatever was transcribed stays readable, `complete: false`; `source.failure` says why |
| `cancelled` | none, or whatever existed stays readable |

Deleting the source or the session deletes the transcript (chapter 12).

> **[OPEN]** Whether a client may edit a transcript (correct a word, relabel a speaker) through the protocol, and how a document generated earlier records which version it read.

## 8.6 Errors

| Code | HTTP | When |
|---|---|---|
| `transcript_not_found` | 404 | Unknown id, or outside what the caller may see. |
| `invalid_range` | 400 | `after_index` below 0 or `limit` outside 1–1000. |

## 8.7 Summary of endpoints

| Method | Path |
|---|---|
| GET | `/v1/transcripts/{id}` |
| GET | `/v1/transcripts/{id}/segments` |
| GET | `/v1/sessions/{id}/sources/{sid}/transcript` |

---

**Previous:** [7. Audio input](./07-audio-input.md) · **Next:** [9. Templates](./09-templates.md)
