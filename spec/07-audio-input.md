# 7. Audio input

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: the `transport` object is defined in [`06-source.schema.json`](../schemas/06-source.schema.json)

---

## 7.1 Where audio goes

Audio belongs to an **audio source** inside a session (chapter 6). When the source is created the service returns a `transport` (6.9) that says where and how to send the bytes. The client sends the bytes there, reads the text back as chunks are transcribed (chapter 8), then calls `end` (6.8).

Which `transport` comes back depends on what the client said it can handle (`transports` on the create request) and what the service offers. `put` is always available and points at the service's own API; `post-form` sends the bytes straight to an object store and is offered only by services that have set that up. The examples in this chapter show `put`.

The audio **format** is fixed on the source at creation (`format`, one of `capabilities.sources.kinds.audio.formats`). Every upload carries it as `Content-Type`.

## 7.2 Using the transport

| `kind` | What the client does |
|---|---|
| `put` | `PUT` the raw audio to `url` (file) or to `url_template` with `{n}` replaced by the chunk index (chunked). Send every entry of `headers` as a request header. |
| `post-form` | `POST` `multipart/form-data` to `url`: every entry of `fields` as a form field first, then the audio as the field named `file`. |

**Authentication.** When the URL is under the service's API, the client sends its `Authorization` header as on any other call (chapter 5). When it is a pre-signed storage URL, the signature in the URL or `fields` is the credential and no `Authorization` header is sent. A client tells the two apart by the origin of the URL against `endpoints.base_url` in discovery.

**Expiry.** `expires_at`, when present, is when the URL stops accepting uploads. A client that still has bytes to send after that fetches the source again (`GET …/sources/{sid}`): while the source is `created` or `recording`, the service returns a `transport` that is valid at that moment.

**Response.** Under `put` the service answers an upload with the **chunk object** (chapter 8): `status: queued`, or already `success` with `text` when the service transcribed it in the same request. Under `post-form` the response is the store's; the client treats any `2xx` as stored and ignores the body. In both cases the client's view of what the service holds is `chunks.received` on the source, the chunk objects (chapter 8), and the answer to `end`.

**Failure.** A `4xx` means the request is wrong or the URL expired: fetch the source for a fresh transport and send again. A `5xx` is retryable.

## 7.3 Chunked upload

A recording is sent as a series of short pieces while it happens.

```http
PUT https://scribe.example.com/v1/sessions/01J9ZM1A…/sources/01J9ZN7B…/chunks/3
Authorization: Bearer …
Content-Type: audio/webm;codecs=opus
Content-Length: 61440

<binary audio>
```

Rules:

- **Index.** Chunks are numbered from `0` in recording order; the index replaces `{n}` in `url_template`.
- **One format per recording.** `Content-Type` on every chunk equals the source's `format`.
- **Each chunk stands alone.** A chunk is a complete, playable audio file in its format (its own container header), so the service can transcribe it on its own. A client that records continuously cuts the stream into such files; pauses in speech are good places to cut.
- **Length.** A chunk is at most `max_chunk_seconds` long (default 25).
- **Idempotent.** Sending the same index again replaces the earlier bytes. A client retries a failed upload by sending the same index.
- **Order of arrival is free.** Chunks may arrive out of order; the service orders them by index.

The service SHOULD transcribe a chunk as soon as it arrives, so the client can read its text while recording (chapter 8). A chunk that proves unusable (wrong format, too long, undecodable) is skipped with a `chunk_skipped` warning on the source (6.8); under `put` the service may refuse such a chunk at once with the errors in 7.6.

When the recording is over the client calls `end` (6.8) with `chunks_total` and, if it has them, its own `recorded_at` times. The service reports `gaps`; the client re-sends those indexes and calls `end` again.

## 7.4 Single-file upload

One complete recording in one request (`input: file`).

```http
PUT https://scribe.example.com/v1/sessions/01J9ZM1A…/sources/01J9ZN8C…/file
Authorization: Bearer …
Content-Type: audio/wav
Content-Length: 18432044

<binary audio>
```

Under `put` the response is the source. Then `end` (6.8), which moves the source to `processing`; only the full transcript applies (chapter 8), there are no chunk objects. The service cuts the file into pieces itself where it needs to; how it cuts is its own affair. Maximum length is `max_seconds`; a longer file fails the source with `audio_too_long` in `failure`, or is refused at upload with `422 audio_too_long` under `put`.

## 7.5 Format and encoding

| Format | MIME type | Note |
|---|---|---|
| WebM / Opus | `audio/webm;codecs=opus` | RECOMMENDED for browsers |
| Ogg / Opus | `audio/ogg;codecs=opus` | |
| WAV (PCM) | `audio/wav` | large; simplest to produce |
| MP4 / AAC | `audio/mp4` | common on phones |

Recommended encoding for speech: 16 kHz or higher, mono, 32 kbps or more for compressed formats. A service lists what it accepts; a client picks from that list.

## 7.6 Errors

Under `put` the service answers an upload with these codes. Under `post-form` errors arrive in the store's own format (7.2) and the service reports what it finds as warnings or `failure` on the source.

| Code | HTTP | When |
|---|---|---|
| `source_not_recording` | 422 | Audio sent to an audio source that is past `recording`. |
| `format_mismatch` | 422 | `Content-Type` differs from the source's `format`. |
| `chunk_too_long` | 422 | Chunk longer than `max_chunk_seconds`. |
| `audio_too_long` | 422 | File longer than `max_seconds`. |
| `payload_too_large` | 413 | Bytes beyond the service's request-size limit. |
| `payload_required` | 400 | Empty body. |

## 7.7 Summary

This chapter adds no endpoints. Audio goes to the URL in `transport`; `end` and `cancel` are in chapter 6; reading the text is chapter 8.

---

**Previous:** [6. Sessions and sources](./06-sessions.md) · **Next:** [8. Transcripts](./08-transcripts.md)
