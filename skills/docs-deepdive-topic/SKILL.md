---
name: docs-deepdive-topic
description: Use when the user invokes docs-deepdive-topic, asks for an exploration topic deep-dive or refresh, or wants web research merged into exploration/topics/. Covers AI/ML/DL/data-science topics and adjacent tooling; refreshes one topic with web-backed research and registry-backed citations.
disable-model-invocation: true
---

# Docs deep-dive (exploration topic)

## When to use

- User names this skill, `/docs-deepdive-topic`, or equivalent.
- User wants one `exploration/topics/<slug>/` folder brought up to date from the wider web.

## Required inputs

- **Topic slug**: directory name under `exploration/topics/` (e.g. `forge-flow`). If absent, infer from the message or list `exploration/topics/` and confirm before writing.

## Definition of done

- [ ] `exploration/README.md` was read before edits; citation and hygiene rules followed.
- [ ] `exploration/topics/<slug>/reference.md` lists sources, short quotes with trailing `SRC-###` on the quote line, scope/status/last reviewed.
- [ ] Every new `SRC-###` exists in `exploration/registry/sources.md` (and `authors.md` / `sites.md` if README requires).
- [ ] `exploration/topics/<slug>/info.md` includes all seven **verbatim** `###` headings in [reference.md](reference.md) (`info.md` skeleton; order fixed there); empty sections get one honest sentence after good-faith search.
- [ ] `exploration/topics/<slug>/deepdive.md` includes all four **verbatim** `###` headings in [reference.md](reference.md) (`deepdive.md` skeleton; order fixed there); empty sections get one honest sentence after good-faith search.
- [ ] New topic folder → topics table row added in `exploration/README.md`.
- [ ] Quotes stay short and tied to `SRC-###`; stable public URLs only; no long verbatim third-party copies; no secrets or private URLs.

## Non-goals

- Do not edit other topic slugs or unrelated repo areas.
- Do not mutate remote systems (read-only web research per `AGENTS.md` policy).
- Do not invent `SRC-###` rows or reuse IDs.

## Workflow

1. **Load hub rules** — Read `exploration/README.md` (registry model, quote rules, licensing).
2. **Resolve slug** — Confirm `exploration/topics/<slug>/` exists or will be created; read current `info.md`, `deepdive.md`, and `reference.md` if present.
3. **Reserve IDs** — Open `exploration/registry/sources.md`; note the next free `SRC-###` sequence; plan new rows before writing quotes that cite them.
4. **Research** — Run web search (and URL fetch when useful) across the channels in [reference.md](reference.md); prefer primary docs and official repos.
5. **Write reference** — Update `reference.md`; register sources; add `authors.md` / `sites.md` entries when README implies it.
6. **Write synthesis** — Update `info.md` and `deepdive.md` using the heading order and rubric in [reference.md](reference.md).
7. **Index** — If the folder is new, append the topics table row in `exploration/README.md`.
8. **Verify** — Re-read the Definition of done checklist; fix gaps.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| “I can paraphrase the doc without registering a source.” | Unregistered claims are not hub-auditable; add `SRC-###` or omit the claim. |
| “Sentiment is obvious from vibes.” | Tie sentiment bullets to cited threads/issues/papers or state uncertainty explicitly. |
| “I'll paste the README for completeness.” | Large paste violates exploration hygiene; link + short quote + summary. |

## Additional resources

- Query patterns, channel table, `info.md` / `deepdive.md` skeletons, section rubric: [reference.md](reference.md)
