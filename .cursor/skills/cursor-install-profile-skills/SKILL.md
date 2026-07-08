---
name: cursor-install-profile-skills
description: >-
  Project skill for ow-cursor-config only: installs or updates shipped skills into
  the user profile via scripts/install-profile-skills. Use when the user invokes
  cursor-install-profile-skills in the ow-cursor-config workspace on Linux or Windows.
disable-model-invocation: true
---

# Install profile skills (ow-cursor-config)

**Project skill** — `.cursor/skills/cursor-install-profile-skills/` in **ow-cursor-config** only. **Not** shipped to `~/.cursor/skills/`.

## Invocation

**Manual only:** `/cursor-install-profile-skills` or `@cursor-install-profile-skills` in the ow-cursor-config workspace.

Platform routing: **[reference-platform.md](reference-platform.md)**. Operator reference: **[../../../scripts/profile-tooling.md](../../../scripts/profile-tooling.md)**.

## Workspace guard

```bash
test -f scripts/install-profile-skills.sh
test -f catalog/bundle-manifest.json
test -f .cursor/skills/cursor-install-profile-skills/SKILL.md
```

## Definition of done

- Workspace guard passed.
- `install-profile-skills` script succeeded (or dry-run report shown).
- Catalog skills exist under `$CURSOR_PROFILE/skills/<name>/`.
- Manifest updated (unless dry-run).

## Non-goals

- Do not install this skill to `~/.cursor/skills/`.
- Do not install rules, hooks, commands, or subagents.
- Do not write into `~/.cursor/skills-cursor/`.
- Do not prune (use `@cursor-prune-profile-tooling` with input `skills`).

## Workflow

1. Run workspace guard.
2. Resolve paths per [reference-platform.md](reference-platform.md).
3. Optional `--dry-run` / `-DryRun`.
4. Run `install-profile-skills`.
5. Report summary.

## Boundaries

- Local filesystem only.
