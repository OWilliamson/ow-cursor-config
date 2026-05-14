---
name: docs-deepdive-topic
description: Use when the user invokes docs-deepdive-topic, asks for a topic deep-dive or refresh against a docs directory, or wants web research merged into a topics folder. Refreshes one topic with web-backed research and registry-backed citations.
disable-model-invocation: true
---

# Docs deep-dive (topic)

## When to use

- User names this skill, `/docs-deepdive-topic`, or equivalent.
- User wants one `<docs-dir>/topics/<slug>/` folder brought up to date from the wider web.

## Required inputs

- **Docs directory**: path to the docs root (e.g. `exploration/`). If absent, ask before proceeding.
- **Topic slug**: directory name under `<docs-dir>/topics/` (e.g. `transformers`). If absent, infer from the message or list `<docs-dir>/topics/` and confirm before writing.

## Definition of done

- [ ] `<docs-dir>/README.md` was read before edits; citation and hygiene rules followed.
- [ ] `<docs-dir>/topics/<slug>/reference.md` lists sources, short quotes with trailing `SRC-###` on the quote line, scope/status/last reviewed.
- [ ] Every new `SRC-###` exists in `<docs-dir>/registry/sources.md` (and `authors.md` / `sites.md` if README requires).
- [ ] `<docs-dir>/topics/<slug>/info.md` includes all seven **verbatim** `###` headings in [reference.md](reference.md) (`info.md` skeleton; order fixed there); empty sections get one honest sentence after good-faith search.
- [ ] `<docs-dir>/topics/<slug>/deepdive.md` includes all four **verbatim** `###` headings in [reference.md](reference.md) (`deepdive.md` skeleton; order fixed there); empty sections get one honest sentence after good-faith search.
- [ ] New topic folder → topics table row added in `<docs-dir>/README.md`.
- [ ] Quotes stay short and tied to `SRC-###`; stable public URLs only; no long verbatim third-party copies; no secrets or private URLs.

## Non-goals

- Do not edit other topic slugs or unrelated repo areas.
- Do not mutate remote systems (read-only web research per `AGENTS.md` policy).
- Do not invent `SRC-###` rows or reuse IDs.

## Workflow

1. **Load hub rules** — Read `<docs-dir>/README.md` (registry model, quote rules, licensing).
2. **Resolve slug** — Confirm `<docs-dir>/topics/<slug>/` exists or will be created; read current `info.md`, `deepdive.md`, and `reference.md` if present.
3. **Reserve IDs** — Open `<docs-dir>/registry/sources.md`; note the next free `SRC-###` sequence; plan new rows before writing quotes that cite them.
4. **Research** — Run web search (and URL fetch when useful) across the channels in [reference.md](reference.md); prefer primary docs and official repos.
5. **Write reference** — Update `reference.md`; register sources; add `authors.md` / `sites.md` entries when README implies it.
6. **Write synthesis** — Update `info.md` and `deepdive.md` using the heading order and rubric in [reference.md](reference.md).
7. **Index** — If the folder is new, append the topics table row in `<docs-dir>/README.md`.
8. **Verify** — Re-read the Definition of done checklist; fix gaps.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| “I can paraphrase the doc without registering a source.” | Unregistered claims are not hub-auditable; add `SRC-###` or omit the claim. |
| “Sentiment is obvious from vibes.” | Tie sentiment bullets to cited threads/issues/papers or state uncertainty explicitly. |
| “I'll paste the README for completeness.” | Large paste violates exploration hygiene; link + short quote + summary. |

## Additional resources

- Query patterns, channel table, `info.md` / `deepdive.md` skeletons, section rubric: [reference.md](reference.md)
