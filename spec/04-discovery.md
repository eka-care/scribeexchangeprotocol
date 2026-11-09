# 4. Discovery

**Scribe Exchange Protocol v0.1 (draft)** · Schema: [`04-discovery.schema.json`](../schemas/04-discovery.schema.json) · Example: [`04-discovery.json`](../examples/04-discovery.json)

---

## 4.1 The well-known endpoint

A service MUST publish a **discovery document** at:

```http
GET /.well-known/scribe-exchange
```

- No authentication. Anyone may read it.
- `Content-Type: application/json`.
- SHOULD be cacheable: `Cache-Control: max-age=3600` (one hour) is recommended.
- A client MUST read it before its first call and SHOULD cache it for the time the service says. A client SHOULD re-read it after an `unsupported_version` or `capability_not_supported` error.

`/.well-known/` is a standard place (RFC 8615) for a site to publish information about itself, so clients can find it without being told the path.

## 4.2 What it contains

```json
{
  "protocol": "scribe-exchange",
  "protocol_version": "0.1",
  "supported_versions": ["0.1"],
  "deprecated_versions": [],

  "service": {
    "name": "Example Scribe",
    "documentation_url": "https://docs.example.com",
    "support_email": "support@example.com",
    "security_contact": "security@example.com"
  },

  "endpoints": {
    "base_url": "https://scribe.example.com/v1"
  },

  "auth": {
    "authorization_servers": ["https://auth.example.com"],
    "scopes_supported": ["scribe-exchange"]
  },

  "capabilities": {
    "sources": {
      "max_per_session": 20,
      "kinds": {
        "audio": {
          "max": 3,
          "input": ["chunked", "file"],
          "formats": ["audio/webm;codecs=opus", "audio/wav", "audio/ogg;codecs=opus"],
          "max_chunk_seconds": 25,
          "max_seconds": 7200,
          "inactivity_seconds": 300
        },
        "text":      { "max": 10, "max_chars": 20000 },
        "file":      { "max": 10, "max_bytes": 26214400, "content_types": ["application/pdf", "image/jpeg", "image/png"], "url_fetch": false },
        "reference": { "max": 10 }
      }
    },
    "document_history": false,
    "document_forms": ["json", "markdown"],
    "document_delivery": ["poll"],
    "export_formats": ["markdown", "pdf"]
  },

  "models": {
    "stt": [
      { "id": "whisper-large-v3", "display_name": "Whisper large v3", "languages": ["en", "hi", "ta"], "features": { "timestamps": true, "diarization": false }, "default": true }
    ],
    "structuring": [
      { "id": "llama-3.3-70b", "display_name": "Llama 3.3 70B (local)", "features": { "streaming": false }, "default": true },
      { "id": "claude-sonnet", "display_name": "Claude Sonnet", "features": { "streaming": true } }
    ]
  },

  "languages": {
    "supported": ["en", "hi", "ta", "te", "kn", "ml", "bn", "mr", "gu", "pa"],
    "auto_detection": true
  },

  "profiles": []
}
```

## 4.3 Fields

Required unless marked optional. "Closed list" means only the listed values are allowed in this version; "open list" means a service may ADD values (base values remain), and clients must ignore ones they do not know.

### Top level

| Field | Type | Meaning |
|---|---|---|
| `protocol` | string | MUST be `"scribe-exchange"`. |
| `protocol_version` | string | Newest version implemented, `MAJOR.MINOR`. |
| `supported_versions` | string[] | Every major version still served (chapter 3). |
| `deprecated_versions` | object[] | Optional. One entry per **major** version being retired (minors are never removed). `version` is that line's newest minor, written exactly as in `supported_versions`, so a client can match them; `sunset_date` (date); `migration_guide` (URL, optional). |

### `service`

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Human-readable name of this deployment. |
| `documentation_url` | URL | Optional. |
| `support_email` | string | Optional. |
| `security_contact` | string | Optional. Where to report a vulnerability. A `/.well-known/security.txt` is RECOMMENDED as well. |

### `endpoints`

| Field | Type | Meaning |
|---|---|---|
| `base_url` | URL | Where `/v1/` lives. Every path in this spec is relative to it. Clients MUST use it rather than guessing from the discovery URL. |

### `auth`

| Field | Type | Meaning |
|---|---|---|
| `auth` | object \| null | `null`: no authentication required; every endpoint is open. An object: a bearer token is required on every endpoint except discovery (chapter 5). |
| `auth.authorization_servers` | URL[] | One or more OpenID Connect / OAuth 2 issuers that mint the bearer tokens this service accepts. A client fetches `{issuer}/.well-known/openid-configuration` to learn how to sign in or obtain a server token. At least one. |
| `auth.scopes_supported` | string[] | Optional. Scopes the service understands, if it uses any. |


### `capabilities`

| Field | Type | Meaning |
|---|---|---|
| `sources` | object | What may be put into a session (chapter 6). |
| `sources.max_per_session` | integer | Total sources of all kinds one session may hold. |
| `sources.kinds` | object | One entry per accepted source kind, keyed by kind name. A kind not listed is refused with `kind_not_supported`. `audio` MUST be present. Every entry has `max` (how many of that kind per session); the rest depends on the kind, below. |
| `sources.kinds.audio.input` | string[] | Open list: `chunked` (numbered chunks as recording happens), `file` (one complete recording), `stream` (reserved). At least one of `chunked`, `file`. |
| `sources.kinds.audio.formats` | string[] | MIME types accepted. `audio/webm;codecs=opus` is RECOMMENDED for browsers. |
| `sources.kinds.audio.max_chunk_seconds` | integer | Longest chunk accepted. Default 25. Clients MUST NOT send longer chunks. |
| `sources.kinds.audio.max_seconds` | integer | Longest single recording. |
| `sources.kinds.audio.inactivity_seconds` | integer | If no chunk arrives for this long, the service ends the recording itself (chapter 6). |
| `sources.kinds.text.max_chars` | integer | Longest text source. |
| `sources.kinds.file.max_bytes` | integer | Largest file. |
| `sources.kinds.file.content_types` | string[] | Accepted MIME types for files. |
| `sources.kinds.file.url_fetch` | boolean | Whether a file may be given as a URL for the service to fetch, instead of uploaded. |
| `document_history` | boolean | Whether the service keeps old revisions of documents and serves them (chapter 10). `false` means only the current content is kept. |
| `document_forms` | string[] | Open list, at least one. The forms **every** document from this service carries (chapter 10). Known ids: `markdown`, `json` (typed sections), `html`, `text`. A deployment may add its own (an editor's native form, for example). A client reads this list and works with what is there. |
| `document_delivery` | string[] | Open list: `poll` (always present), `stream` (reserved). How a client can learn a document is ready. |
| `export_formats` | string[] | Open list, at least one. Export formats available (`markdown`, `pdf`, `docx`, …); depends on the deployment's exporters. |

### `models`

Two lists, one per kind. A client shows these to users or passes an `id` when creating a session (`stt_model`) or a document (`model`). If a client passes nothing, the service uses the one marked `default`.

| Field | Type | Meaning |
|---|---|---|
| `stt[]` / `structuring[]` | object[] | At least one in each list. |
| `[].id` | string | The identifier to send. Opaque to clients. |
| `[].display_name` | string | What to show. |
| `[].languages` | string[] | Optional. BCP 47 tags this model handles. Absent means "any in `languages.supported`". |
| `[].features` | object | Optional. For `stt`: `timestamps`, `diarization` (speaker separation). For `structuring`: `streaming`. All booleans. Open list of keys. |
| `[].default` | boolean | Optional. Exactly one per list SHOULD be `true`. |

Model identifiers are chosen by the deployment and are opaque to clients.

### `languages`

| Field | Type | Meaning |
|---|---|---|
| `supported` | string[] | BCP 47 tags the service can transcribe. |
| `auto_detection` | boolean | Whether the service can detect the spoken language when the client gives no hint. |

### `profiles`

| Field | Type | Meaning |
|---|---|---|
| `profiles[]` | object[] | Installed profiles. Empty array when none. |
| `[].name` | string | Profile name, e.g. `medscribealliance`. |
| `[].version` | string | The profile's own version. |
| `[].base_url` | URL | Where the profile's routes live, normally `{base_url}/profiles/{name}`. |
| `[].documentation_url` | URL | Optional. |

A profile MAY add further keys inside its own entry. It MUST NOT add keys at the top level of the discovery document.

## 4.4 How a client uses it

1. Fetch once; cache for `max-age`.
2. Read `auth`. If it is `null`, call freely; otherwise get a token from one of `auth.authorization_servers` (chapter 5).
3. Before offering ways to add material, read `sources.kinds`: which kinds exist, how many of each, and for audio which `input` modes and `formats` are accepted and the `max_chunk_seconds`.
4. Before offering a model choice, read `models.stt` and `models.structuring`.
5. Read `document_forms` to know what every document will carry, and `export_formats` to know what to offer in an export menu.
6. If it needs a profile, check `profiles[]` for the name and version.


---

**Previous:** [3. Versioning](./03-versioning.md) · **Next:** [5. Authentication](./05-authentication.md)
