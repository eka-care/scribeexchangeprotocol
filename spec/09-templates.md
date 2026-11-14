# 9. Templates

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: [`09-template.schema.json`](../schemas/09-template.schema.json), [`09-template-create-request.schema.json`](../schemas/09-template-create-request.schema.json)

---

## 9.1 What a template is

A **template** says what to write and in which format. The service applies it to the sources of a session and streams the text back (chapter 10). The same template may be applied to any number of sessions, and to the same session more than once.

## 9.2 The template object

```json
{
  "id": "01J9ZR4D5E6F7G8H9J0K1M2N3P",
  "name": "OPD consultation note",
  "instructions": "Write a consultation note in English with the headings Chief complaint, History, Examination, Assessment, Plan. Use only what was said; leave a heading empty rather than guess. Record drug names and doses exactly as spoken.",
  "output_format": "markdown",
  "output_json_schema": null,
  "created_at": "2026-10-20T09:00:00.000Z"
}
```

| Field | Type | Meaning |
|---|---|---|
| `id` | ULID | |
| `name` | string | Display name. 1–200 characters. |
| `instructions` | string | What the writer is told, in plain language: headings, tone, language, what to include and leave out. Up to `capabilities.templates.max_instruction_chars`. |
| `output_format` | string | The format of the text produced: one of discovery's `output_formats` (chapter 4). Known ids: `markdown`, `json`, `text`, `html`. |
| `output_json_schema` | object \| null | With `output_format: json` only: a JSON Schema the output MUST satisfy. The service shapes the writer's output to it and validates before sending `done` (chapter 10). `null` means any JSON object. |
| `created_at` | timestamp | |

**Templates are immutable.** To change one, create a new template and delete the old; ids already in use elsewhere keep meaning what they meant.

## 9.3 Endpoints

### Create

```http
POST /v1/templates
Content-Type: application/json

{ "name": "OPD consultation note", "instructions": "…", "output_format": "markdown" }
```

`201` with the template. `output_json_schema` is accepted only with `output_format: json`.

### List, get

```http
GET /v1/templates
GET /v1/templates/{id}
```

List returns the templates visible to the caller (at least the ones it created; anything wider is the service's policy), newest first. Pagination: `limit` (default 50, max 200) and an opaque `cursor`; the response carries `next_cursor` or `null`.

### Delete

```http
DELETE /v1/templates/{id}
```

`204`. A later `GET` is `404`.

## 9.4 Limits come from discovery

`capabilities.templates` (chapter 4): `max_instruction_chars` and `max_per_caller`.

## 9.5 Errors

| Code | HTTP | When |
|---|---|---|
| `template_not_found` | 404 | Unknown id, or not visible to this caller. |
| `invalid_template` | 400 | Missing or malformed field; `output_format` not in discovery; `output_json_schema` given without `json`, or not a valid JSON Schema. |
| `template_limit_reached` | 422 | `max_per_caller` hit. |

## 9.6 Summary of endpoints

| Method | Path | Required? |
|---|---|---|
| POST, GET | `/v1/templates` | yes |
| GET, DELETE | `/v1/templates/{id}` | yes |

---

**Previous:** [8. Transcripts](./08-transcripts.md) · **Next:** [10. Generation and documents](./10-documents.md)
