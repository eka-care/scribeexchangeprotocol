# 7. Audio input

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: the `transport` object is defined in [`06-source.schema.json`](../schemas/06-source.schema.json)

---

## 7.1 Where audio goes

Audio belongs to an **audio source** inside a session (chapter 6). When the source is created the service returns a `transport` (6.9) that says where and how to send the bytes. The client sends the bytes there, then calls `end` (6.8). That is the whole exchange, for every service.

The upload URL is the service's choice: its own API, or an object store (S3, GCS, Azure Blob and the like) with a pre-signed URL. The client treats both the same way. The examples in this chapter use the service's own API only to have something concrete to show.

Audio **formats** are declared in discovery (`capabilities.sources.kinds.audio.formats`) as MIME types. The client picks one and names it on every upload with `Content-Type`.

## 7.2 Using the transport

| `kind` | What the client does |
|---|---|
| `put` | `PUT` the raw audio to `url` (file) or to `url_template` with `{n}` replaced by the chunk index (chunked). Send every entry of `headers` as a request header. |
| `post-form` | `POST` `multipart/form-data` to `url`: every entry of `fields` as a form field first, then the audio as the field named `file`. |

**Authentication.** When the URL is under the service's API, the client sends its `Authorization` header as on any other call (chapter 5). When it is a pre-signed storage URL, the signature in the URL or `fields` is the credential and no `Authorization` header is sent. A client tells the two apart by the origin of the URL against `endpoints.base_url` in discovery.

**Expiry.** `expires_at`, when present, is when the URL stops accepting uploads. A client that still has bytes to send after that fetches the source again (`GET …/sources/{sid}`): while the source is `created` or `recording`, the service returns a `transport` that is valid at that moment.

**Success.** A `2xx` response from the URL means the bytes are stored. The body is whatever the receiving end returns; the protocol does not define it. The client's view of what the service holds is `chunks.received` on the source, and the answer to `end`.

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
- **One format per recording.** The first chunk fixes the format; every later chunk uses the same `Content-Type`.
- **Each chunk stands alone.** A chunk is a complete, playable audio file in its format (its own container header), so the service can transcribe it on its own. A client that records continuously cuts the stream into such files; pauses in speech are good places to cut.
- **Length.** A chunk is at most `max_chunk_seconds` long (default 25).
- **Idempotent.** Sending the same index again replaces the earlier bytes. A client retries a failed upload by sending the same index.
- **Order of arrival is free.** Chunks may arrive out of order; the service orders them by index.

The service may start transcribing a chunk as soon as it arrives. A chunk that proves unusable (wrong format, too long, undecodable) is skipped with a `chunk_skipped` warning on the source (6.8); when the service hosts the upload URL it may refuse such a chunk at once with the errors in 7.6.

When the recording is over the client calls `end` (6.8) with `chunks_total`. The service reports `gaps`; the client re-sends those indexes and calls `end` again.

## 7.4 Single-file upload

One complete recording in one request (`input: file`).

```http
PUT https://scribe.example.com/v1/sessions/01J9ZM1A…/sources/01J9ZN8C…/file
Authorization: Bearer …
Content-Type: audio/wav
Content-Length: 18432044

<binary audio>
```

Then `end` (6.8), which moves the source to `processing`. The service cuts the file into pieces itself where it needs to (long files are transcribed in parts); how it cuts is its own affair. Maximum length is `max_seconds`; a longer file fails the source with `audio_too_long` in `failure`, or is refused at upload with `422 audio_too_long` when the service hosts the URL.

## 7.5 Format and encoding

| Format | MIME type | Note |
|---|---|---|
| WebM / Opus | `audio/webm;codecs=opus` | RECOMMENDED for browsers |
| Ogg / Opus | `audio/ogg;codecs=opus` | |
| WAV (PCM) | `audio/wav` | large; simplest to produce |
| MP4 / AAC | `audio/mp4` | common on phones |

Recommended encoding for speech: 16 kHz or higher, mono, 32 kbps or more for compressed formats. A service lists what it accepts; a client picks from that list.

## 7.6 Errors

When the service hosts the upload URL itself, it answers an upload with these codes. When an object store hosts it, errors arrive in the store's own format (7.2) and the service reports what it finds as warnings or `failure` on the source after `end`.

| Code | HTTP | When |
|---|---|---|
| `source_not_recording` | 422 | Audio sent to an audio source that is past `recording`. |
| `unsupported_format` | 415 | `Content-Type` is outside `formats`. |
| `format_mismatch` | 422 | `Content-Type` differs from the first chunk's. |
| `chunk_too_long` | 422 | Chunk longer than `max_chunk_seconds`. |
| `audio_too_long` | 422 | File longer than `max_seconds`. |
| `payload_too_large` | 413 | Bytes beyond the service's request-size limit. |
| `payload_required` | 400 | Empty body. |

## 7.7 Summary

This chapter adds no endpoints. Audio goes to the URL in `transport`; `end` and `cancel` are in chapter 6.

---

**Previous:** [6. Sessions and sources](./06-sessions.md) · **Next:** [8. Transcripts](./08-transcripts.md)
