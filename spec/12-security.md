# 12. Security

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: none

---

## 12.1 Transport

Every endpoint, discovery included, is served over HTTPS. A service MUST NOT answer protocol requests over plain HTTP, and a client MUST NOT send them. TLS 1.2 or newer; certificate validation on.

The upload URLs a service hands out in a `transport` (chapter 6) follow the same rule.

## 12.2 Credentials

- A credential travels only in the `Authorization` header (chapter 5), never in a URL, a query string or a request body. A pre-signed upload URL is the one exception: there the signature in the URL is the credential, it is short-lived, and it opens one upload only.
- A service MUST NOT write a credential into a log, an error `message` or `details`.
- A client MUST treat a token as opaque and keep it where other code on the same device cannot read it.

## 12.3 Limits

A service MAY limit how often a caller may call it. When a call is over the limit, the service answers `429 rate_limited` with a `Retry-After` header (seconds), and the client waits at least that long. A service SHOULD count uploads of audio chunks separately from other calls, so a recording in progress is not starved by a burst of reads.

Every size and count limit a service enforces is one it declared in discovery (chapter 4); a request over a declared limit is refused with the code the defining chapter names, never silently truncated.

## 12.4 Isolation

A caller sees only what the service's policy allows: `404` for anything else, so an id alone reveals nothing (chapter 11). Ids are ULIDs (chapter 1): unguessable enough that a caller cannot enumerate another caller's sessions by trying values.

## 12.5 Errors

| Code | HTTP | When |
|---|---|---|
| `rate_limited` | 429 | Over the service's call limit. `Retry-After` says how long to wait. |

## 12.6 Summary

No endpoints.

---

**Previous:** [11. Errors](./11-errors.md) · **Next:** [13. Profiles](./13-profiles.md)
