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

**Structural gates:**

- [ ] `<docs-dir>/README.md` was read before edits; citation and hygiene rules followed.
- [ ] `<docs-dir>/topics/<slug>/reference.md` lists sources, short quotes with trailing `SRC-###` on the quote line, scope/status/last reviewed.
- [ ] Every new `SRC-###` exists in `<docs-dir>/registry/sources.md` (and `authors.md` / `sites.md` if README requires).
- [ ] `<docs-dir>/topics/<slug>/info.md` includes all seven **verbatim** `###` headings in [reference.md](reference.md) (`info.md` skeleton; order fixed there); empty sections get one honest sentence after good-faith search.
- [ ] `<docs-dir>/topics/<slug>/deepdive.md` includes all four **verbatim** `###` headings in [reference.md](reference.md) (`deepdive.md` skeleton; order fixed there); empty sections get one honest sentence after good-faith search.
- [ ] New topic folder → topics table row added in `<docs-dir>/README.md`.
- [ ] Quotes stay short and tied to `SRC-###`; stable public URLs only; no long verbatim third-party copies; no secrets or private URLs.

**Quality gates (must also pass):**

- [ ] At least **three distinct search channel types** were attempted before writing (primary source + implementation artifact + practitioner forum); failed searches are documented in `reference.md`.
- [ ] `deepdive.md` `### How it works (in depth)` explains named mechanisms (components, data flow, design decisions) — not a summary of what a source covers. Cites ≥2 independent sources.
- [ ] `deepdive.md` `### Implementation notes` contains at least one concrete artifact (command, config snippet, hardware number, model-hub ID) — or documents explicitly why none can be provided.
- [ ] `deepdive.md` `### Research Backing` cites ≥2 distinct source types with specific results or stated limitations — not just source existence.
- [ ] `deepdive.md` `### Public Sentiment` is not blank: either cites named threads/issues with `SRC-###`, or documents the search attempt and null result with date and channels tried.

## Non-goals

- Do not edit other topic slugs or unrelated repo areas.
- Do not mutate remote systems (read-only web research per `AGENTS.md` policy).
- Do not invent `SRC-###` rows or reuse IDs.

## Workflow

1. **Load hub rules** — Read `<docs-dir>/AGENTS.md` (registry model, quote rules, licensing, and the **Writing quality standards** — the VFF contract that governs all hub content). Also read `<docs-dir>/README.md` for the topics index and heading contract.
2. **Resolve slug** — Confirm `<docs-dir>/topics/<slug>/` exists or will be created; read current `info.md`, `deepdive.md`, and `reference.md` if present.
3. **Reserve IDs** — Open `<docs-dir>/registry/sources.md`; note the next free `SRC-###` sequence; plan new rows before writing quotes that cite them.
4. **Research** — Run web search (and URL fetch when useful) across **all three required channel types** in [reference.md](reference.md): primary technical source, implementation artifact, and practitioner forum. Prefer primary docs and official repos.
5. **Write reference** — Update `reference.md`; register sources; add `authors.md` / `sites.md` entries when README implies it; record failed search attempts.
6. **Write synthesis** — Update `info.md` and `deepdive.md` using the heading order and rubric in [reference.md](reference.md).
7. **Index** — If the folder is new, append the topics table row in `<docs-dir>/README.md`.
8. **Verify** — Re-read the full Definition of done checklist (structural **and** quality gates); fix gaps.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| "I can paraphrase the doc without registering a source." | Unregistered claims are not hub-auditable; add `SRC-###` or omit the claim. |
| "Sentiment is obvious from vibes." | Tie sentiment bullets to cited threads/issues/papers or state uncertainty explicitly. |
| "I'll paste the README for completeness." | Large paste violates exploration hygiene; link + short quote + summary. |
| "The paper analyses architecture, datasets, and training." | That is not a deep dive; that is a table of contents. Name the actual components, data flow, or design trade-offs in your own words and cite where. |
| "Implementation detail is in the paper, not duplicated here." | Extract the relevant step, config, or number. If a paywall blocks reproduction, quote the accessible abstract claim and note the limitation. |
| "Research Backing: primary backing is SRC-034." | A single survey is a starting point. Add a second independent source (benchmark, model card, replication) with specific results before the section is done. |
| "Public Sentiment: no specific thread cited yet." | Search `site:reddit.com`, Hacker News, and the project issue tracker. If nothing substantive is found, write that with the date and channels tried — do not leave a placeholder. |

## Additional resources

- Query patterns, channel table, minimum coverage rules, `info.md` / `deepdive.md` skeletons, section rubric: [reference.md](reference.md)
