# 5. Authentication

**Scribe Exchange Protocol v0.1 (draft)**

---

## 5.1 What the protocol says, and what it leaves out

The protocol says two things about authentication:

1. Every request carries a **bearer token** in the `Authorization` header.
2. The discovery document names the **authorization server** that issues those tokens.

Everything else is the implementation's business: how people sign in (passwords, single sign-on, passkeys), how servers get credentials, who may see what, roles, cookies for a web app, API keys, session timeouts, audit. Two compliant services may do all of that differently and still speak the same protocol.

## 5.2 Bearer token

```http
GET /v1/sessions
Authorization: Bearer eyJ…
```

- The token is **opaque** to the client: never parse it or depend on its format. It may be a JWT or anything else.
- It MUST NOT appear in URLs, query strings or request bodies.
- A service MUST accept this header on every endpoint except discovery.
- The service decides what the token's subject may do. The protocol promises only that a caller can see what it created (chapter 2).

## 5.3 Where tokens come from

Discovery (chapter 4) carries:

```json
"auth": {
  "authorization_servers": ["https://auth.example.com"],
  "scopes_supported": ["scribe-exchange"]
}
```

`authorization_servers` lists one or more OpenID Connect / OAuth 2 issuers. A client that knows nothing else about the deployment fetches `{issuer}/.well-known/openid-configuration` (the standard OpenID Connect discovery document) and from there knows how to sign a person in or how to obtain a server-to-server token. This is the same arrangement the Model Context Protocol uses for its servers.

| Who | Standard flow | In plain words |
|---|---|---|
| A person in an app | Authorization code with PKCE | The app sends the browser to the authorization server; the person signs in there; the app receives a token. |
| Another server | Client credentials | The backend presents its own id and secret to the authorization server and receives a token. No person involved. |

`scopes_supported` is optional: scopes the service understands, if it uses any. A client that requests none gets whatever the authorization server grants by default.

The authorization server may be a product the deployment already runs (Keycloak, Google Workspace, Microsoft Entra, Authentik…) or one built into the scribe service itself. The protocol does not care which; a small deployment with no identity system of its own is expected to use the built-in one.

## 5.4 Refresh and expiry

Token lifetime and refresh are the authorization server's affair and follow its OpenID Connect metadata. When a token has expired the service answers `401 token_expired`; the client obtains a new one and retries once. Any other `401` (`authentication_failed`) means the credential is bad; sign in again.

## 5.5 Errors

| Code | HTTP | When |
|---|---|---|
| `authentication_failed` | 401 | Missing, malformed, unknown or revoked token. |
| `token_expired` | 401 | Token past its expiry. Get a new one and retry. |
| `forbidden` | 403 | Valid token; the service's policy does not allow this action on this object. |

Full error shape: chapter 14.

---

**Previous:** [4. Discovery](./04-discovery.md) · **Next:** [6. Sessions and sources](./06-sessions.md)
