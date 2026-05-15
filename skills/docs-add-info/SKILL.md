---
name: docs-add-info
description: >-
  Adds new research or documentation information into a docs hub in a controlled
  way. Use when the user wants to capture a new source, expand a topic,
  or route new findings into hub docs such as external research notes or
  roadmap guidance.
disable-model-invocation: true
---

# Docs Add Info

## When to use

- The user asks to add new information to the docs hub.
- The user wants to record a source, synthesis, or research note cleanly.
- The user wants `<docs-dir>/` updated, but the information may also affect related hub docs.

Do not apply this skill proactively during ordinary research.

## Required inputs

- **Docs directory**: path to the docs root (e.g. `exploration/`). If absent, ask before proceeding.
- Source or location: URL, chat link, file path, or other exact reference.
- Purpose: what the information should help discover, explain, or improve.
- Destination: existing topic, new topic, registry entry, or hub doc.

If the destination is unclear, ask:

> Where should this information live: an existing topic, a new topic, or a hub doc?

## Definition of done

- The information is placed in the right file or files.
- `<docs-dir>/` citations use stable `SRC-###` IDs when quotations are added.
- Any topic index or registry entries are updated when new sources are recorded.
- Broader guidance changes are reflected in the relevant hub doc pages.
- No secrets, private URLs, or long copied passages are added.

## Non-goals

- Do not invent new source IDs or loosen the existing registry format.
- Do not add large verbatim excerpts.
- Do not modify external systems.
- Do not broaden scope into unrelated cleanup or refactors.
- Do not write any claim from a source you have not fetched in this session.

## Workflow

0. **Load hub rules** — Read `<docs-dir>/AGENTS.md` including the **Writing quality standards** (VFF contract). The source-in-hand rule is the most critical for single-item inserts: do not write any claim from a source you have not fetched in this session.
1. Identify the information type:
   - **One source or quote** → update an existing topic or create a new one.
   - **One synthesis point** → add or expand `info.md`.
   - **Hub guidance change** → update the closest hub doc page as well.
2. Route the content:
   - `<docs-dir>/topics/<slug>/reference.md` for sources, short quotes, and context.
   - `<docs-dir>/topics/<slug>/info.md` for synthesis, implementation notes, and use cases.
   - `<docs-dir>/registry/sources.md` for new `SRC-###` rows.
   - A hub landscape or notes doc when the result is a broad scan.
   - Roadmap, inventory, or related hub docs when the guidance itself changes.
3. Preserve the local hub conventions:
   - Keep quotes short and specific.
   - Link out instead of copying large blocks.
   - Keep `SRC-###` as the primary citation style.
4. If multiple destinations are needed, update the most specific source file first, then the supporting doc pages.

## Destination-specific guidance

### Existing topic

- Add the new source or note to `reference.md`.
- Update `info.md` only if the new information changes the synthesis.
- If the topic gets a new source, add or reuse the matching `SRC-###` row.

### New topic

- Create `<docs-dir>/topics/<slug>/reference.md` and `<docs-dir>/topics/<slug>/info.md`.
- Add the new row to `<docs-dir>/registry/sources.md`.
- Update the hand-maintained topic index in `<docs-dir>/README.md`.

### Hub docs update

- Update the closest hub doc with the takeaway, not the raw source text.
- Use the appropriate landscape or notes doc for broad scans and a roadmap doc for follow-up actions.
- Update an inventory doc if the new information changes the catalogue or install guidance.

## Validation

- Re-read every changed file.
- If `SRC-###` citations changed, run the hub's source-ID validation script (e.g. `python <docs-dir>/scripts/check_src_ids.py`).
- Check `git status --short` and review the diff for unintended files.

## Example prompts

- "Add this blog post to the relevant topic."
- "Capture this meeting note as a new research topic."
- "Turn these findings into a docs update and a topic synthesis."
