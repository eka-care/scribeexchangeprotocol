# Schemas

One JSON Schema (draft 2020-12) per protocol object. These files are the machine source of truth: the prose in `../spec/` describes them, `../openapi.yaml` is generated from them, and CI checks `../examples/` against them.

## Naming

`NN-<object>.schema.json`, where `NN` is the spec chapter that defines the object and `<object>` is lower-case, singular: `06-session.schema.json`, `08-transcript.schema.json`. Files therefore sort in chapter order.

Inside each file:
- `$id` is a stable URN, `urn:scribe-exchange:schema:<object>`. Every `$ref` between schemas uses the URN, so a file can be renamed (for example when chapters are renumbered) with nothing else to change.
- `$comment` names the chapter and section that define the object.

## Schemas in this version

| File | Object | Defined in |
|---|---|---|
| `04-discovery.schema.json` | DiscoveryDocument | 04 §4.2–4.3 |
| `06-session.schema.json` | Session | 06 §6.2 |
| `06-session-create-request.schema.json` | SessionCreateRequest | 06 §6.3 |
| `06-session-update-request.schema.json` | SessionUpdateRequest | 06 §6.3 |
| `06-source.schema.json` | Source (all kinds; audio fields) | 06 §6.4, §6.7 |
| `06-source-create-request.schema.json` | SourceCreateRequest | 06 §6.5 |
| `06-source-end-response.schema.json` | SourceEndResponse | 06 §6.8 |
| `08-transcript.schema.json` | Transcript, Segment (`$defs/segment`) | 08 §8.2–8.3 |
| `08-transcript-segments-page.schema.json` | TranscriptSegmentsPage | 08 §8.4 |

## Rules

- Every property has a `description` in plain words.
- Every schema has at least one example in `../examples/`.
- Additive changes only within a major version.
- Profile schemas live in the profile's own repository.
