# 3. Versioning

**Scribe Exchange Protocol v0.1 (draft)**

---

## 3.1 Version numbers

The protocol version is `MAJOR.MINOR`.

| Part | Changes when | Example |
|---|---|---|
| MAJOR | Something is removed, renamed, or changes meaning. Clients must change. | `1.0` → `2.0` |
| MINOR | Something is added: a new optional field, a new endpoint, a new value in an open list. Old clients keep working. | `1.0` → `1.1` |

Stability is promised from `1.0`: from then on the additive rule below is a guarantee. `0.x` versions may change between minors.

## 3.2 The version is in the path

Every endpoint lives under `/v{MAJOR}/`: `/v1/sessions`, `/v1/documents/{id}`. A breaking change means a new prefix (`/v2/`) served alongside the old one for the deprecation period.

Minor versions are additive, so any `1.x` client works against any `1.y` server. A client that wants to pin a minor MAY send:

```http
Scribe-Exchange-Version: 1.2
```

If present, the service MUST behave as that minor, or answer `400 unsupported_version` if it does not know it. If absent, the service uses the newest minor it implements. Every response MUST carry the minor actually used:

```http
Scribe-Exchange-Version: 1.3
```

The major is always the path.

## 3.3 The additive rule

Within one major version a service MAY:

- add an optional field to any object;
- add an endpoint;
- add a value to an open list (for example a new `audio_input` mode), as long as it is declared in discovery.

Within one major version a service MUST NOT:

- remove or rename a field or endpoint;
- make an optional field required;
- change a field's type or meaning;
- add a value to a **closed** list (status values, error codes are closed; chapters 6, 10, 11, 15 say which).

Because of this rule, **clients MUST ignore fields they do not know** and MUST NOT fail on an unknown value in an open list.

## 3.4 Declaring versions

The discovery document says what the service speaks:

```json
{
  "protocol": "scribe-exchange",
  "protocol_version": "1.1",
  "supported_versions": ["1.1"],
  "deprecated_versions": []
}
```

- `protocol_version` — the newest version implemented.
- `supported_versions` — every major version still served, with its newest minor (`["1.1", "2.0"]` while both prefixes exist).
- `deprecated_versions` — see 3.5.

## 3.5 Deprecation

When a major version is going away:

1. **Announce** it in discovery:
   ```json
   "deprecated_versions": [
     { "version": "1.1", "sunset_date": "2028-01-01", "migration_guide": "https://docs.example.com/migrate-1-to-2" }
   ]
   ```
2. **Warn** on every response under the old prefix for at least 6 months:
   ```http
   Scribe-Exchange-Deprecated: true
   Scribe-Exchange-Sunset: 2028-01-01
   ```
3. **Remove** the prefix no earlier than 12 months after the announcement.

Clients SHOULD log the `Scribe-Exchange-Deprecated` header when they first see it.

## 3.6 Profiles and the base

A profile has its own version and declares which base version it requires. A profile may move faster than the base. Discovery lists both (chapter 4, chapter 15).

## 3.7 Header names

Every header this protocol defines carries the product name as its prefix, following current practice (`Stripe-Signature`, `GitHub-Api-Version`) and RFC 6648. The prefix keeps these names distinct from everyone else's. Header names are case-insensitive.

| Header | Direction | Chapter |
|---|---|---|
| `Scribe-Exchange-Version` | request (optional) and response (always) | 3 |
| `Scribe-Exchange-Deprecated`, `Scribe-Exchange-Sunset` | response, during a deprecation period | 3 |

A profile that needs its own headers prefixes them with its own name.

---

**Previous:** [2. Architecture](./02-architecture.md) · **Next:** [4. Discovery](./04-discovery.md)
