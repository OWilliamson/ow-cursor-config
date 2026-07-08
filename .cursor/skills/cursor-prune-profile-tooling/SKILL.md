---
name: cursor-prune-profile-tooling
description: >-
  Project skill for ow-cursor-config only: prunes profile rules or skills previously
  installed from this bundle but no longer in the catalog. Use when the user invokes
  cursor-prune-profile-tooling with input rules or skills in the ow-cursor-config workspace.
disable-model-invocation: true
---

# Prune profile tooling (ow-cursor-config)

**Project skill** — `.cursor/skills/cursor-prune-profile-tooling/` in **ow-cursor-config** only. **Not** in `~/.cursor/skills/`.

## Invocation

**Manual only:** `/cursor-prune-profile-tooling` or `@cursor-prune-profile-tooling` in the ow-cursor-config workspace.

## Required input

**`rules`** or **`skills`**.

## Workspace guard

```bash
test -f scripts/prune-profile-rules.sh
test -f catalog/bundle-manifest.json
test -f .cursor/skills/cursor-prune-profile-tooling/SKILL.md
```

## Definition of done

- Input `rules` or `skills` confirmed.
- Prune script ran (or dry-run report).
- Only manifest-managed retired names removed.

## Non-goals

- Do not install (use `@cursor-install-profile-rules` or `@cursor-install-profile-skills`).
- Do not prune hooks, commands, or subagents.
- Do not remove user-authored profile tooling.

## Workflow

1. Confirm input `rules` or `skills`.
2. Run workspace guard.
3. Resolve paths per [reference-platform.md](reference-platform.md).
4. Dry-run when user asks what would be removed; else confirm unless "prune now".
5. Run `prune-profile-<kind>`.
6. Report removed paths.

## Boundaries

- Manifest-gated deletes only under `$CURSOR_PROFILE/rules/` or `skills/`.
