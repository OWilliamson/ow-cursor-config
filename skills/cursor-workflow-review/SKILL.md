---
name: cursor-workflow-review
description: >-
  Reviews Cursor-oriented repository workflows (AGENTS.md, .cursor/rules, doc hubs,
  skills) with Red/Amber/Green scoring per criterion, or emits a policy inventory
  report (where conventions live, tables + short summaries) when the user only needs
  an index—not scored criteria. Use for workflow review, agent guidance audit,
  repo policy inventory, handbook summary, rules index, or full agent-oriented repo review.
disable-model-invocation: true
---

# Cursor workflow review

Structured pass over **Cursor-facing** artifacts: handbook, `.cursor/rules/*.mdc`, optional `.cursor/skills/**/SKILL.md`, linked doc hubs, and handbook-named scripts.

**Skill root:** this directory. Human install / copy: [README.md](README.md). Helpers: [`scripts/`](scripts/) — Python 3 stdlib, run from **target repo root** (`REPO`/`SKILL` in [reference.md](reference.md)). Scoring, questions 1–8, efficiency: [reference.md#workflow-review-scoring](reference.md#workflow-review-scoring).

## When to run

- Workflow / agent-guidance review, full repo agent-oriented review, or policy inventory / rules index / handbook summary requests.
- Use the **inventory fast path** when the user only needs **where** expectations live—not scored R/A/G per question.

## Deliverables (pick one per request)

| User intent | What to produce | How |
|-------------|-----------------|-----|
| **Index only** | **Repository policy report** | [reference.md — Inventory fast path](reference.md#repository-policy-report-inventory-only-fast-path). Skip questions 1–8 unless the user also wants a quality review. |
| **Quality review** | **Cursor workflow review** (questions 1–8) | Steps below; [scoring + questions](reference.md#workflow-review-scoring); output template in `reference.md`. |

If unclear, ask once: **index-style report** vs **scored workflow review** (or both—in that order: inventory first, then scores).

## How to run (agent behavior)

1. **Triage** — identify the review surface:
   - Read handbook first (`AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING.md`); if missing, treat `.cursor/rules/` + root `README.md` as hubs.
   - Scan `.cursor/rules/*.mdc` frontmatter for all rules; read full bodies only for `alwaysApply: true` and rules whose `globs` match this session's work.
   - Read the documentation hub the handbook names.
   - List `.cursor/skills/**/SKILL.md` by frontmatter `description` unless a skill is clearly central.
   - Review surface = paths cited from handbook + rules + hub only; optionally run [`scripts/extract_cited_paths.py`](scripts/extract_cited_paths.py) from repo root per [reference.md](reference.md). Do not read unrelated docs.

2. **Inventory (one short list)** — Name each **workflow** (neutral label, e.g. “land change → validate → open PR”) and the **2–5 files** that define it. Omit orphan docs unless the user asked for a full documentation audit.

3. **Evaluate** — For **each question** in [reference.md — Questions 1–8](reference.md#questions-evaluate-in-this-order), assign **Red / Amber / Green** using the [scoring rules](reference.md#scoring-rules-per-question), then list concrete findings for Amber and Red (bullet + file path or section).

4. **Dead-link / dead-end spot check (scoped)** — Only for paths **cited from** the review surface: verify they exist under the repo. Use [`scripts/check_paths.py`](scripts/check_paths.py) with a path list (from step 1). Do not crawl the entire repository for links.

5. **Optional rule index** — For a fast view of rule coverage, run [`scripts/scan_rule_frontmatter.py`](scripts/scan_rule_frontmatter.py) from the repository root.

6. **Summarize** — Use the output template in [reference.md](reference.md). End with **prioritized fixes**; each fix should name the **single canonical file** to edit when possible.

Do not edit the target repository unless the user separately asks for changes.
