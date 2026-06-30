# Cursor workflow review — reference

## Helper scripts (from repository under review)

Set `REPO` to the repository root. Set `SKILL` to this skill directory (where `scripts/` lives).

```bash
REPO=/path/to/target/repo
SKILL="$HOME/.cursor/skills/cursor-workflow-review"

# 1) Collect cited repo-relative paths from hub files (edit file list)
python3 "$SKILL/scripts/extract_cited_paths.py" --repo "$REPO" \
  --files AGENTS.md README.md docs/README.md

# 2) Save paths to a file and verify existence
python3 "$SKILL/scripts/extract_cited_paths.py" --repo "$REPO" \
  --files AGENTS.md README.md docs/README.md \
  | python3 "$SKILL/scripts/check_paths.py" --repo "$REPO" --from-stdin

# 3) Rule coverage snapshot (frontmatter only)
python3 "$SKILL/scripts/scan_rule_frontmatter.py" --repo "$REPO"
# If rules live outside `.cursor/rules`, pass a relative path:
# python3 "$SKILL/scripts/scan_rule_frontmatter.py" --repo "$REPO" --rules-dir path/to/rules
```

**Finding hub files:** if `docs/README.md` is missing, pass whatever paths the handbook actually links (e.g. `CONTRIBUTING.md`, `docs/index.md`).

<a id="workflow-review-scoring"></a>

## Scoring rules (per question)

| Status | Meaning |
|--------|---------|
| **Green** | No meaningful improvement needed for this criterion. |
| **Amber** | **One major** issue, **or** **up to three minor** issues (list each). |
| **Red** | **Two or more major** issues, **or** **four or more minor** issues (list each). |

**Major** = wrong or missing entrypoint, contradictory instructions, unsafe guidance, or a workflow that reliably misleads the agent.  
**Minor** = unclear wording, missing cross-link, small inconsistency, or polish that would reduce friction.

## Questions (evaluate in this order)

Answer **one question at a time** in the response, with status then bullets.

### 1. Purpose and use case

Is it obvious **what** each workflow is for and **when** to use it (vs out of scope)?

### 2. Human entry points

Is it clear **how a human** starts each workflow (first file to open, branch or policy gates, commands from repository root)?

### 3. Ease of follow

Are steps **ordered**, **actionable**, and free of unexplained jargon or internal identifiers without pointers?

### 4. Documentation for Cursor agents

Is there **enough** linked, authoritative markdown for an agent to execute without guessing (golden path, constraints, “do not” list)?

### 5. Naming and discoverability

Do **paths, rule names, and headings** read consistently so an agent can find the right doc from the handbook or rules without ambiguity?

### 6. Dead ends

Any **broken links**, references to missing files, or instructions that stop without a next step or validation?

### 7. Redundancies

Do **multiple** places repeat the same policy **without** a single canonical link (risk of drift)?

### 8. Option surface

Are there **more branches/options** than needed (confusing defaults vs escape hatches), without a clear **default path**?

When scripts, packagers, or generated artifacts appear in the review surface, score Q8 against the target repo’s **`AGENTS.md` → Tooling profile** for named invariants—do not invent a separate bar in this review.

## Efficiency notes (workflow review)

- Prefer **hub-first** reading; expand only along the **cited path graph** from hubs.
- Treat the **handbook** (`AGENTS.md` or named equivalent) as the contract; flag drift when root `README.md` or rules contradict it.
- On large repos, trace **one vertical slice** (the main contributor journey) end-to-end for questions 2–5 and 8—reuse the same slice per question.
- For **Q7**, weight “duplicate policy, no pointer to canonical” more than harmless hub-to-doc cross-links.

## Repository policy report (inventory-only fast path)

Use this when the user wants **where policies live** and **one-line summaries**, not Red/Amber/Green per workflow question.

### Goal

Produce a **single markdown report** that inventories **where** the repo states policies and **what** each area covers, without duplicating full policy text (link + one-line summary per item).

### Assumptions

- Workspace root is the **git repository root** (or monorepo package root if the user scopes a subfolder—state the root you used in the report header).
- Prefer **read-only** inspection unless the user also asked for fixes.

### Scan order (check what exists; skip missing paths)

1. **Handbook / contract** — `AGENTS.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `CODEOWNERS`, root `README.md` (whichever exist).
2. **Documentation hub** — `docs/README.md` and linked index tables; high-signal guides under `docs/` (naming, deploy/import, versioning, layout, checklists, baseline/catalog policy).
3. **Cursor / AI guidance** — `.cursor/rules/*.mdc`, `.cursor/rules/*.md`, `AGENTS.md` cross-links; project skills under `.cursor/skills/**/SKILL.md` if present (do not read `~/.cursor/skills-cursor/`).
4. **Baselines and catalogs** — `baselines/README.md`, `baselines/*/README.md` when present.
5. **Tooling contract** — `tools/README.md`, smoke scripts, validators named in handbook (e.g. `test-*.sh`, `verify-*.sh`, `check-*.py`).
6. **Repo-specific roots** — `reports/README.md`, `templates/README.md`, `packages/README.md`, `NOTICE`, `LICENSE*` when they encode redistribution or output policy.

### What to extract

For each discovered policy source: **path** (repo-relative); **audience** if obvious; **topic tags**; **one-line summary**; **canonical?** (yes if claimed single source of truth, else supporting).

### Output skeleton

```markdown
# Repository policy report

**Workspace root:** `<path or .>`
**Generated:** `<ISO date>`

## Executive summary

- `<N>` primary policy sources, `<M>` supporting docs.
- **Highest-risk gaps:** `<bullets if any contradictions or missing handbook>`

## Policy sources (table)

| Path | Role | Topics | Summary |
|------|------|--------|---------|
| … | … | … | … |

## Tooling and automation

| Script / check | Invoked from | What it enforces |
|----------------|--------------|------------------|

## Contradictions or drift (if any)

- …

## Suggested follow-ups (optional)

- …
```

### Quality bar

- **No wall of pasted policy:** tables + short summaries; link paths with backticks.
- **Deduplicate:** if two files repeat the same rule, list the **canonical** one first and note “also stated in …”.
- **Unknowns:** if a path is referenced but missing, list under **Gaps** with the referrer path.

### Optional deep pass

If the user asks for **full** policy text extraction, add **Appendix: verbatim excerpts** with small quoted blocks only where necessary—default is index style above.

## Output template — full workflow review (RAG questions 1–8)

```markdown
## Cursor workflow review — <repo name>

### Per-question results

**1. Purpose and use case — <R|A|G>**  
…

**2. Human entry points — <R|A|G>**  
…

… (through 8)

### Summary (point by point)

1. Purpose: …
2. Human entry: …
…
8. Options: …

### Recommended follow-ups (optional)

- …
```

## Inventory table (optional, during triage)

| Workflow (neutral label) | Defining files (2–5) | Default path | Escape hatch |
|--------------------------|----------------------|----------------|---------------|
| … | … | … | … |

## `rg` triage (optional)

From `$REPO`:

```bash
rg -n "AGENTS|\\.cursor/rules|SKILL\\.md" AGENTS.md README.md 2>/dev/null || true
rg --files -g "*.mdc" .cursor/rules 2>/dev/null || true
```

Adjust paths if the repo stores rules elsewhere (document finding in the review).
