# Validation rubric

Completion checks for `/owcc-skill-improve`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

None. (This package has no `scripts/`. Mechanical checks below are agent-run commands.)

### Mechanical commands (agent-run)

- `wc -l SKILL.md` — expect under 500 (suggestion).
- Word count excluding frontmatter:

```bash
python3 -c "import re,sys; t=open('SKILL.md').read(); print(len(re.sub(r'^---\n.*?\n---\n','',t,1,re.DOTALL).split()))"
```

- For `CS-WORDS-GENERAL`: IF §5.3 has 5+ top-level steps THEN budget 900 ELSE 500 (suggestion).
- Compare frontmatter `name` to folder basename.
- Inventory package files; verify every SKILL.md link resolves inside the package **OR** is listed under META References → Reference To.
- Confirm META.md has ## References with Referenced From and Reference To tables.
- Confirm no live `reference-*.md` remains IN the improved package.

## Agent questions

- [ ] Target path unambiguous; no unauthorized rename of `name:` or folder?
- [ ] Target `SKILL.md` has numbered sections 1–7 matching [OUTPUTS.md](OUTPUTS.md) SKILL contract?
- [ ] Required siblings present: RESPONSE.md, VALIDATION.md, META.md, WORKFLOW.yaml?
- [ ] WORKFLOW.yaml `skill` matches `name` AND step ids cover SKILL §5.3?
- [ ] Optional siblings match [DECISIONS.md §4](DECISIONS.md#4-optional-siblings-for-target)?
- [ ] META.md EXISTS AND IS NOT linked from SKILL.md?
- [ ] META.md has References (Referenced From + Reference To); every SKILL peer path IS listed under Reference To?
- [ ] No substance dropped without user-approved drop ([DECISIONS §8](DECISIONS.md#8-fidelity-disposition))?
- [ ] Description IS trigger-only (no workflow summary)?
- [ ] Workflow has §5.1 operator table; steps use multilevel numbering, **Outcome:** lines, AND §5.1 operators (capitalised only as operators)?
- [ ] DECIDE points resolve to DECISIONS.md sections when branching exists?
- [ ] Chat OUTPUT ready per [RESPONSE.md](RESPONSE.md)?
- [ ] CS-* norms below applied; Critical findings cleared or blocked explicitly?

## Interrogation agent

None by default. IF operator requests a subagent audit, THEN scope it to: package inventory vs OUTPUTS roles, fidelity gate, AND Critical CS-* norms only.

## Authoring norms (CS-*)

Principles:

- Verifiable checks (binary pass/fail) preferred over advisory notes.
- Mechanical checks confirm structure; behavioural effectiveness requires a pressure test IN a fresh session.
- Keep `SKILL.md` procedural; deeper reference IN sibling files one hop away (DECISIONS may link to OUTPUTS/VALIDATION).
- One term per concept; avoid synonym drift.
- Descriptions describe when to use the skill — NOT workflow steps.

| Norm ID | Check | Severity default |
|---------|-------|-----------------|
| `CS-NAME-FOLDER` | `name` field matches folder basename | Critical |
| `CS-DESC-LEN` | `description` char count under 1024 | Critical |
| `CS-DESC-WHEN` | description starts with "Use when" or equivalent trigger form; not first-person | Suggestion |
| `CS-DESC-WORKFLOW-SUMMARY` | description does not summarise skill's own workflow steps | Critical |
| `CS-DESC-BODY-ALIGN` | description claims match what the body actually instructs | Critical |
| `CS-LINES-500` | `wc -l SKILL.md` under 500 | Suggestion |
| `CS-WORDS-FREQ` | IF `disable-model-invocation` omitted or false: body word count under 200 | Suggestion |
| `CS-WORDS-GENERAL` | IF `disable-model-invocation: true`: body under 500 words (single-task) or 900 (multi-step, 5+ top-level §5.3 steps) | Suggestion |
| `CS-DISABLE-INTENT` | `disable-model-invocation` matches length and niche intent | Suggestion |
| `CS-LINKS-ONE-HOP` | links IN `SKILL.md` resolve within package; no SKILL→A→B chains required to act (DECISIONS→OUTPUTS allowed) | Suggestion |
| `CS-NO-FORCE-LOAD` | no `@path` links IN body unless intentionally force-loaded | Suggestion |
| `CS-PATHS-SCOPE` | file-type-specific skills declare `paths` glob IN frontmatter | Nice to have |
| `CS-PORTABLE-PATHS` | no absolute personal paths that break for other installers | Suggestion |
| `CS-SCRIPT-SAFETY` | `scripts/` (IF present) has no network calls or raw shell with user-supplied input | Critical |
| `CS-PKG-NO-ORPHANS` | non-generated files cited from `SKILL.md` OR marked archive/deprecated OR **exempt: META.md** | Suggestion |
| `CS-PKG-REFS-EXIST` | every file referenced by `SKILL.md` exists within the package **OR** is listed under META.md References → Reference To (peer allowlist) | Critical |
| `CS-PKG-META-REFS` | META.md has References (Referenced From + Reference To tables); peer SKILL links match Reference To | Suggestion |
| `CS-PKG-SCRIPTS-DOCUMENTED` | each script has dependency notes AND execute-vs-read guidance | Suggestion |
| `CS-PKG-SIBLINGS-LEAN` | sibling files are single-purpose AND avoid unused bulk | Suggestion |
| `CS-PKG-SHAPE` | required roles present (SKILL, RESPONSE, VALIDATION, META, WORKFLOW.yaml); no live `reference-*.md` | Critical |
| `CS-PKG-WORKFLOW-SYNC` | WORKFLOW.yaml mirrors §5.3 step ids; `skill` matches frontmatter `name` | Critical |
| `CS-PKG-SKILL-SPINE` | SKILL.md has numbered `# 1.` … `## 7.` sections per OUTPUTS | Critical |
| `CS-INVOKE-SLASH` | explicit-only: invoke `/skill-name` only; `@` reserved for file attachment | Suggestion |
| `CS-ANTI-WIN-PATHS` | no Windows-style backslash paths IN docs or scripts | Suggestion |
| `CS-TERMINOLOGY` | one term per concept throughout | Suggestion |
| `CS-NO-TIME-BOMBS` | no time-sensitive phrases unless IN a dated legacy section | Suggestion |
| `CS-BOUNDARIES-EXPLICIT` | skill states what it does **not** do IN §4 Scope (or equivalent) | Suggestion |
| `CS-AUTO-CLARITY` | mode/format skills include when to drop the mode | Suggestion |
| `CS-NO-FAKE-ABBREV` | prose does not invent shorthands for token savings | Nice to have |

### Frontmatter and description guidance

- `name`: lowercase hyphens only, under 64 characters.
- `description`: third person; answers when to use.
- Explicit-only: `disable-model-invocation: true` when long, narrow, or purposeful invoke.
- Invoke line: `/skill-name` only.

### Structure guidance (new spine)

- SKILL sections: §1 Aim, §2 When to use, §3 Inputs, §4 Scope, §5 Workflow (5.1 Operators, 5.2 Rules, 5.3 Steps), §6 Validation, §7 Completion.
- Boundaries live IN §4 Out of scope.
- Workflows ordered by dependency; Outcomes per step; DECIDE → DECISIONS.
- Semantic siblings per [OUTPUTS.md](OUTPUTS.md) (including required WORKFLOW.yaml); legacy `reference-*` not allowed after improve.

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
- Acknowledge passes; do not omit checks silently.
- Cap detailed findings; list remaining norm IDs IF many.
- Final sanity: only flag items worth fixing.
