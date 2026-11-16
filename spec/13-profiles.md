# 13. Profiles

**Scribe Exchange Protocol v0.1 (draft)** · Schemas: none in the base; a profile brings its own

---

## 13.1 What a profile is

The base protocol knows nothing about any one field: a session, a recording, a template, a document. A **profile** is a named add-on for one field, written as its own specification in the same format as this one (prose chapters, JSON Schemas, examples), kept in its own repository, with its own version.

A service that implements a profile says so in discovery (`profiles[]`, chapter 4). A client that needs it looks for the name and version there and otherwise carries on with the base alone.

This specification defines no profile.

## 13.2 What a profile may add

| It may | Where | Rule |
|---|---|---|
| Optional fields on base objects | `session.metadata` is already free for the client; beyond that, a profile may define optional fields on any base object, named with the profile's name as a prefix (`healthcare_patient_ref`). | Optional, ignored by clients that do not know the profile. A base object with the fields removed is still a valid base object. |
| Its own objects and endpoints | Under `/v1/profiles/{name}/`, the `base_url` discovery gives for it. | Same conventions as the base (chapter 1): ULIDs, timestamps, the error shape of chapter 11, versioning of chapter 3. |
| Templates | A set of templates a service installs with the profile, listed through the base `GET /v1/templates` like any other. | A profile may give a template an `output_json_schema` (chapter 9) so its documents have a fixed shape. |
| Meanings for open-list values | A profile may define additional values for an open list (a source `kind`, an output format) and say what they mean. | Base values keep their meaning. |

## 13.3 What a profile may not do

A profile adds; it does not change. It MUST NOT remove, rename or make required anything in the base, change the meaning of a base field or status, add a value to a closed list, or require a client to call a profile endpoint to complete a base flow. A client that knows only the base MUST be able to record, read a transcript, generate and save a document on a service that implements any number of profiles.

## 13.4 Versions

A profile has its own version and names the base version it requires. Discovery lists both (chapter 4). A profile's additive and breaking changes follow chapter 3, applied to the profile alone: a breaking change in a profile is a new major of that profile, not of the base.

## 13.5 Errors

A profile's own endpoints use the error shape of chapter 11 and MAY define their own codes, prefixed with the profile's name (`healthcare_consent_missing`). Base endpoints never return a profile code.

## 13.6 Summary

No endpoints in the base. A profile lives under `/v1/profiles/{name}/`.

---

**Previous:** [12. Security](./12-security.md) · **Next:** [14. Conformance](./14-conformance.md)
