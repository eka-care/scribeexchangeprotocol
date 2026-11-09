# 5. Authentication

**Scribe Exchange Protocol v0.1 (draft)**

---

## 5.1 Optional, but standardised when present

A service MAY require authentication. Discovery says whether it does:

```json
"auth": null
```
means every endpoint is open (a single-user install, a trusted network, a development setup).

```json
"auth": { "authorization_servers": ["https://auth.example.com"] }
```
means requests must carry a bearer token, and that is where tokens come from.

That is the whole of what the protocol says. How people sign in, how servers get credentials, who may see what, roles, cookies, API keys, timeouts, audit: all implementation. The protocol pins the *shape* so that one client works against every service; this is the same position the Model Context Protocol takes.

## 5.2 Bearer token

When `auth` is present:

```http
GET /v1/sessions
Authorization: Bearer eyJ…
```

- The token is **opaque**: clients treat it as a string and send it back as given.
- It MUST NOT appear in URLs, query strings or request bodies.
- A service MUST accept this header on every endpoint except discovery. It MAY accept other mechanisms in addition, for its own clients; protocol clients rely on the bearer token.
- The service decides what the token's holder may do. The protocol promises only that a caller can see what it created (chapter 2).

## 5.3 Where tokens come from

`auth.authorization_servers` lists one or more OpenID Connect / OAuth 2 issuers. A client fetches `{issuer}/.well-known/openid-configuration` (the standard OpenID Connect discovery document) and from there knows how to proceed:

| Who | Standard flow | In plain words |
|---|---|---|
| A person in an app | Authorization code with PKCE | The app sends the browser to the authorization server; the person signs in there; the app receives a token. |
| Another server | Client credentials | The backend presents its own id and secret to the authorization server and receives a token. |

`auth.scopes_supported` is optional: scopes the service understands, if it uses any.

The authorization server may be a product the deployment already runs (Keycloak, Google Workspace, Microsoft Entra, Authentik…) or one built into the scribe service.

## 5.4 Expiry

Token lifetime and refresh follow the authorization server's own metadata. When a token has expired the service answers `401 token_expired`; the client obtains a new one and retries once. Any other `401` (`authentication_failed`) means the credential is bad.

## 5.5 Errors

| Code | HTTP | When |
|---|---|---|
| `authentication_failed` | 401 | `auth` is required and the token is missing, malformed, unknown or revoked. |
| `token_expired` | 401 | Token past its expiry. Get a new one and retry. |
| `forbidden` | 403 | Valid token (or no auth required); the service's policy does not allow this action on this object. |

Full error shape: chapter 13.

---

**Previous:** [4. Discovery](./04-discovery.md) · **Next:** [6. Sessions and sources](./06-sessions.md)
