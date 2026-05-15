---
name: docs-widedive-topic
description: Use when the user invokes docs-widedive-topic, wants to broaden a topic with new sources not already in its reference.md, or wants new information added under existing headings in info.md and deepdive.md without restructuring. Distinct from docs-deepdive-topic: widedive augments breadth; deepdive creates or rewrites depth.
disable-model-invocation: true
---

# Docs wide-dive (topic)

## When to use

- User names this skill, `/docs-widedive-topic`, or equivalent.
- User wants one `<docs-dir>/topics/<slug>/` folder broadened with sources not already cited.
- User wants new bullets added under existing headings without a full rewrite.

## Required inputs

- **Docs directory**: path to the docs root (e.g. `exploration/`). If absent, ask before proceeding.
- **Topic slug**: directory name under `<docs-dir>/topics/` (e.g. `transformers`). If absent, infer from the message or list `<docs-dir>/topics/` and confirm before writing.

## Definition of done

- [ ] `<docs-dir>/README.md` was read before edits; citation and hygiene rules followed.
- [ ] Existing `reference.md` sources were inventoried; new sources are distinct from already-cited ones.
- [ ] At least one new `SRC-###` added to `<docs-dir>/registry/sources.md` (and `authors.md` / `sites.md` where README implies it).
- [ ] New sources appear in `<docs-dir>/topics/<slug>/reference.md` with short quotes and trailing `SRC-###` on the quote line.
- [ ] New bullets added under at least one existing heading in `info.md` or `deepdive.md`; no headings renamed, reordered, or removed.
- [ ] No existing content removed or rewritten; only appended.
- [ ] Quotes stay short; stable public URLs only; no long verbatim third-party copies; no secrets or private URLs.

## Non-goals

- Do not create a new topic from scratch — use `docs-deepdive-topic` for that.
- Do not rewrite or restructure existing sections; leave that to `docs-deepdive-topic`.
- Do not enforce missing headings or migrate legacy layouts.
- Do not edit other topic slugs.
- Do not mutate remote systems (read-only web research per `AGENTS.md` policy).
- Do not invent `SRC-###` rows or reuse IDs.

## Workflow

1. **Load hub rules** — Read `<docs-dir>/AGENTS.md` (registry model, quote rules, licensing, and the **Writing quality standards** — the VFF contract that governs all hub content). Also read `<docs-dir>/README.md` for the topics index and heading contract.
2. **Resolve slug** — Confirm `<docs-dir>/topics/<slug>/` exists; read current `info.md`, `deepdive.md`, and `reference.md`.
3. **Inventory existing sources** — List all `SRC-###` IDs already cited in `reference.md`; note which channels (Reddit, arXiv, GitHub, official docs, etc.) are already covered and which are absent or thin.
4. **Identify gaps** — Use the channel table in [reference.md](reference.md) to decide which under-represented channels to target first.
5. **Reserve IDs** — Open `<docs-dir>/registry/sources.md`; note the next free `SRC-###` sequence; plan new rows before writing any quote that cites them.
6. **Research** — Run web searches targeting under-represented channels; prefer primary docs and official repos. See [reference.md](reference.md) for query patterns and gap-finding guidance.
7. **Write reference** — Append new sources to `reference.md`; register in `sources.md`; add `authors.md` / `sites.md` entries where README implies it.
8. **Enrich docs** — For each new source, identify which existing `###` headings in `info.md` and `deepdive.md` it supports; append new bullets there. Do not remove or reorder existing content.
9. **Verify** — Re-read the Definition of done checklist; fix gaps.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| "I can add another source from the same channel already in reference.md." | Widedive's primary goal is channel breadth; same-channel additions need a higher bar — state explicitly what this new source adds that existing ones do not. |
| "I'll restructure the section while I'm here." | Restructuring is deepdive's job; append only. |
| "I can paraphrase without registering a source." | Unregistered claims are not hub-auditable; add `SRC-###` or omit the claim. |
| "The heading is missing so I'll add it." | Missing headings are a deepdive concern; skip that heading or note the gap without creating it. |
| "I added a bullet — I'll add the citation later." | Every new bullet must carry its `SRC-###` inline on the same line it is written. Deferred citation creates unauditable content that cannot be distinguished from invention. |
| "This thread supports the same point; I'll add it from memory." | Fetch the URL and quote it directly before writing the bullet. Paraphrase-from-memory is the fabrication path even for low-stakes additions. |

## Additional resources

- Search channels, query patterns, gap-finding guidance, and sentiment guardrails: [reference.md](reference.md)
