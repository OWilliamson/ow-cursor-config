---
name: cursor-install-profile-rules
description: >-
  Project skill for ow-cursor-config only: installs or updates shipped rules into
  the user profile via scripts/install-profile-rules. Use when the user invokes
  cursor-install-profile-rules in the ow-cursor-config workspace on Linux or Windows.
disable-model-invocation: true
---

# Install profile rules (ow-cursor-config)

**Project skill** — lives at `.cursor/skills/cursor-install-profile-rules/` in the **ow-cursor-config** checkout only. **Not** installed to `~/.cursor/skills/`.

## Invocation

**Manual only:** `/cursor-install-profile-rules` or `@cursor-install-profile-rules` when the workspace is **ow-cursor-config**.

Platform routing: **[reference-platform.md](reference-platform.md)**. Operator reference: **[../../../scripts/profile-tooling.md](../../../scripts/profile-tooling.md)**.

## Workspace guard

Before running scripts, verify:

```bash
test -f scripts/install-profile-rules.sh
test -f catalog/bundle-manifest.json
test -f .cursor/skills/cursor-install-profile-rules/SKILL.md
```

If any check fails, stop — this skill is for the **ow-cursor-config** repo root, not the hub or profile.

## Definition of done

- Workspace guard passed.
- `install-profile-rules` script ran successfully (or `--dry-run` report shown).
- Shipped `.mdc` files exist under `$CURSOR_PROFILE/rules/`.
- Manifest updated (unless dry-run).

## Non-goals

- Do not install this skill package to `~/.cursor/skills/`.
- Do not install skills, hooks, commands, or subagents.
- Do not prune (use `@cursor-prune-profile-tooling` with input `rules`).
- Do not write identity rules — use shipped `@cursor-create-identity-rule` from profile after install.

## Workflow

1. Run workspace guard.
2. Resolve repo root and profile per [reference-platform.md](reference-platform.md).
3. If preview requested, use `--dry-run` / `-DryRun`.
4. Run `install-profile-rules` for the detected platform.
5. Report script summary.

## Boundaries

- Local filesystem only under repo and `$CURSOR_PROFILE`.
