# repo-convention-change — reference

Optional detail. Read when the workflow needs templates, a longer checklist, or expanded phase notes.

<a id="phase-3-align"></a>

## Phase 3 — Align implementation (expanded)

1. **B (Restatement):** grep for violations of the **already-stated** rule; fix tooling/docs/tests until consistent **or** document a scoped exception in the canonical file.
2. **C (Redefinition):** produce a **short migration list** (files, scripts, CI, sample trees); execute in dependency order (generators before docs that show output names).
3. **Automation:** prefer checks in repo CI or smoke scripts that **fail** on regression (pattern ban, artifact shape)—policy-only text is not enough for safety-critical invariants.

<a id="phase-4-verify"></a>

## Phase 4 — Verify (expanded)

- [ ] No contradictory copy in handbook + rules + hub for the same rule (or contradiction explicitly marked “legacy until Qx”).
- [ ] Examples in canonical doc match at least one real path or command in the repo (or generic placeholder clearly labeled).
- [ ] If tooling changed: tests or script dry-run mentioned in handbook **Tooling** / **Contributing** section.

## Anti-patterns

- Treating **“human readable”** as permission to ignore **stated** machine constraints (e.g. underscores) without the user saying so.
- **B** mode work done as **A** mode (new parallel naming doc that disagrees with an older bullet in `AGENTS.md`).
- Large renames without an explicit **C** acknowledgment from the user.

## User prompt disambiguation (copy for the agent reply)

If unclear, ask the user **one** compact question:

> Is this **(A) a new convention**, **(B) restating an existing one** (fix drift only), or **(C) redefining** (breaking change)? If B or C, which file is the **single canonical** policy doc (path)?

## Canonical policy doc skeleton

Use in any repo’s `docs/` or root handbook as appropriate:

```markdown
# [Topic] convention

## Status
New | Restatement | Redefinition (supersedes: [link or “informal prior”])

## Scope
- Applies to: [paths, file types, generated vs hand-edited]
- Does not apply to: […]

## Rules
1. …
2. …

## Examples
| Wrong | Right |
| ----- | ----- |
| … | … |

## Tooling
- Enforced by: [script / CI job / none yet]
- Handbook link: [AGENTS.md section]

## Migration (C only)
- [ ] …
```

## Drift inventory (B mode)

```text
- [ ] Handbook: …
- [ ] .cursor/rules: …
- [ ] docs hub: …
- [ ] tools/README or scripts: …
- [ ] CI / smoke: …
- [ ] Sample / template trees: …
```

## Handoffs

| If the work is mostly… | Read next |
| ---------------------- | --------- |
| Flags, packagers, ZIP/build shape, “safe default” | Repo `AGENTS.md` → Tooling profile |
| Full agent handbook + rules audit | `cursor-workflow-review` |

## Install location

Personal (all repos): `~/.cursor/skills/repo-convention-change/`

Project copy (team shares it): copy the directory into `<repo>/.cursor/skills/repo-convention-change/` and mention it from that repo’s `AGENTS.md` if desired.
