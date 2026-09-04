# owcc-repo-cleanup — reference patterns

Use when the main [SKILL.md](SKILL.md) is not enough detail for a specific stack.

## Search hints (examples, not exhaustive)

- **Legacy / superseded:** `grep -RiE 'legacy|superseded|deprecated|see .*(instead|AGENTS|docs/)|TODO.*remove' --include='*.md' --include='*.mdc' .`
- **Duplicate hubs:** multiple `*REFERENCES*`, `*links*`, `upstream*` at repo root vs `docs/`.
- **Skills / rules:** `ls -la .cursor/skills/ .cursor/rules/ 2>/dev/null`
- **Large or binary noise:** `git ls-files | rg -i '\\.(zip|jar|class|pyc)$'` (policy: usually ignore or LFS).

## .gitignore checks

- `git status --ignored` (if supported) or spot-check known output dirs.
- `git ls-files '*.log' '**/target/**' '**/node_modules/**'` — expect empty for typical ignores.

## Merge documentation safely

- Add `<a id="stable-anchor"></a>` before a heading when replacing a deleted doc’s URL.
- Grep for old basename after merge: `rg -F 'old-file.md'`.

## User skill install reminder

Personal skills live under **`~/.cursor/skills/<name>/`** with a **`SKILL.md`** (YAML frontmatter). Never install team skills under **`~/.cursor/skills-cursor/`** (Cursor internal).

<a id="what-to-look-for"></a>

## What to look for

### A. Deletion candidates

- **Setup / bootstrap leftovers:** one-off notes (`initial-*`, `important-*`, `TODO-scratch`, migration dumps), duplicate link lists when a doc hub exists.
- **Fully redundant files:** same content or purpose as another tracked file; generated artifacts committed by mistake.
- **Superseded docs:** files that say “see X instead” or duplicate a canonical guide—**merge then delete** targets.
- **Unused directories:** empty trees, gitignored-only placeholders with no references, vendor/skeleton trees the team has decided not to maintain (policy call—flag, do not assume delete).
- **Obsolete process artifacts:** old CI configs, deprecated scripts, duplicate templates superseded by `templates/` or tooling.

### B. Merge / refactor candidates

- **Documentation:** thin pages that belong as a section inside `AGENTS.md`, `docs/README.md`, or a domain guide (preserve one anchor; add explicit HTML `id` if links must stay stable).
- **Scripts / templates:** two scripts doing adjacent steps where one entrypoint + subcommand would reduce drift; parallel `local/` vs `uploads/` style folders serving overlapping “drop files here” roles.
- **Directories with overlapping purpose:** flag consolidation **only** with a migration note (paths referenced in scripts, `.gitignore`, and docs).

### C. Rehome to user scope (or small change to allow it)

Evaluate **project** copies of:

- **Agent Skills** under `.cursor/skills/` that are portable philosophy or personal workflow (copy to `~/.cursor/skills/<name>/`, point rules/docs at user path, remove from repo).
- **Rules** that encode personal preference vs repo invariants—flag for user-level rule or slimmer project rule.
- **Commands / subagents / MCP wrappers** that are environment-specific—flag **Review** unless clearly duplicative of global config.

Prefer **rehome** when the artifact has **no repo-specific paths** or those paths can be generalized in one paragraph.

### D. `.gitignore` pass

- Read **`.gitignore`** (and `.git/info/exclude` if relevant). List **common build outputs** for stacks in the repo (e.g. `target/`, `node_modules/`, `.venv/`, `dist/`, `*.zip` under output dirs).
- Run **`git ls-files`** for patterns that **should** be ignored (build dirs, local exports, secrets filenames). Flag **tracked files that belong ignored** (`git rm --cached` candidates).
- Flag **gaps**: generated files appearing in `git status` that are not covered by ignore rules.

<a id="report-output-template"></a>

## Report output (template)

Deliver to the user (markdown):

```markdown
# Repo cleanup audit: <repo-name>

**Scope:** <paths or whole repo> · **Branch:** <current> · **Read-only:** yes

## Summary counts
| Bucket | Count |
|--------|-------|
| Delete | n |
| Merge / refactor | n |
| Rehome (user) | n |
| Review / uncertain | n |

## Indexed findings

### D1 — Delete (recommended)
| Id | Path | Rationale | Risk |
|----|------|-----------|------|

### M1 — Merge / refactor
| Id | Path(s) | Proposal | Depends on |

### R1 — Rehome to user scope
| Id | Object | Current location | Proposed user location | Doc/rule edits needed |

### Q1 — Review / uncertain
| Id | Path | Question for user |

## .gitignore
- **OK / gaps / tracked junk:** …
- **Suggested rule lines** (if any): …

## Recommended execution order
1. …
2. …

**Awaiting your choice:** which ids to execute (or “none”) and whether to use a new branch name: ___
```

Use stable ids (`D1`, `M2`, …) so the user can reply “execute D1, M2 only”.

<a id="execution-phase-after-approval"></a>

## Execution phase (only after approval)

- Create/use a **feature branch** for repo changes.
- For **merge-then-delete** docs: land merged text first, update all inbound links, then delete the old file in the same change set.
- For **rehome skills**: copy to `~/.cursor/skills/<skill-name>/`, update references to **`~/.cursor/skills/...`**, remove in-repo copy; do **not** put canonical team policy in the user skill unless agreed.
- Re-run **`git status`** and a minimal **smoke test** / CI the repo defines after tooling moves.
