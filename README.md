# Vaarta

**Open-source scribe software: a spoken conversation → a structured, editable document, in any field, using templates you choose, on servers you control.**

"Vaarta" (वार्ता) means "conversation" in Hindi.

> Status: **pre-1.0, under construction.** Nothing here is stable yet. The protocol, plugin API and SDK are promised stable from v1.0 onward, not before.

## What is in this repository

| Folder | What it holds | Status |
|---|---|---|
| `protocol/` | The **Vaarta Protocol**: the published rules for how any client talks to any scribe service. Written spec (`spec/`), JSON schemas (`schemas/`), examples (`examples/`). Vendor-neutral; the Vaarta server is its reference implementation. | Phase 0, being written |
| `docs/` | Design documents: what Vaarta is, architecture (overall, backend, frontend), the phased plan, and the running decision log. Read `docs/00-start-here.md` first. | Current |
| `packages/` | Server, plugin SDK, bundled plugins, client SDK, design system, reference web app. | Not started (Phase 1+) |

## The five pieces (each usable alone)

1. **Vaarta Protocol** — spec + schemas. No code.
2. **Server** — Python, built on [echo](https://github.com/eka-care/echo-sdk), Postgres + file storage.
3. **Client SDK** — TypeScript, speaks the protocol against any compliant server.
4. **Reference UI** — React web app built only from the Client SDK.
5. **Plugin SDK** — what plugin authors import.

## Who it is for

- **Deployers** who need documents from conversations and cannot send recordings to someone else's cloud (hospitals, government, courts, anyone under data-residency rules).
- **Builders** who extend Vaarta with plugins, or fork it to make their own product.
- **Protocol implementers** who write their own server or client against the protocol without using this code.

Medical is one use of Vaarta, not Vaarta itself. The healthcare version (MedScribeAlliance profile, Aarogya Vaarta, EkaScribe) is built on top as plugins. Nothing medical lives in the core.

## How the docs are organised

Everything is written in plain words on purpose. Each technical term is explained the first time it appears. Decisions are numbered once across all documents and never renumbered; the log is `docs/decisions.md`.

## Licence

Apache-2.0, for everything in this repository including the protocol text and schemas. Contributions under the Developer Certificate of Origin (DCO). Maintained by Eka Care.
