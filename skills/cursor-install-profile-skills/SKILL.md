---
name: cursor-install-profile-skills
description: >-
  Installs or updates shipped Cursor skills from ow-cursor-config into the user
  profile (~/.cursor/skills). Use when the user invokes cursor-install-profile-skills
  to sync bundle skills, update profile skills from the repo, or bootstrap skills on
  Linux or Windows.
disable-model-invocation: true
---

# Install profile skills

## Invocation

**Manual only:** `/cursor-install-profile-skills` or `@cursor-install-profile-skills`.

Platform routing: **[reference-platform.md](reference-platform.md)**. Operator reference: **[../../scripts/profile-tooling.md](../../scripts/profile-tooling.md)**.

## Definition of done

- `install-profile-skills` script ran successfully (or `--dry-run` report shown).
- Each catalog skill directory exists under `$CURSOR_PROFILE/skills/<name>/` with `SKILL.md`.
- Manifest updated with current skill names (unless dry-run).

## Non-goals

- Do not install rules, hooks, commands, or subagents.
- Do not install into `~/.cursor/skills-cursor/` (Cursor internal).
- Do not prune removed skills (use `@cursor-prune-profile-tooling` with input `skills`).
- Do not commit, push, or mutate remotes.

## Workflow

1. Resolve repo root and profile per [reference-platform.md](reference-platform.md).
2. If preview requested, use `--dry-run` / `-DryRun`.
3. Run `install-profile-skills` for the detected platform.
4. Report script summary.
5. Remind: new **custom** skills use Cursor built-in **create-skill**; optional `@cursor-validate-skill` on one package.

## Boundaries

- Local filesystem only.
- Never delete extra profile skills not in the bundle manifest.

## Bootstrap note

First-time users can run this skill's script once to install **all** bundle skills (including this skill and the other install/prune skills) before using `@` invocation.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| "Copy one skill folder manually." | Use the script so manifest stays aligned for prune. |
| "Install rules in the same step." | Use `@cursor-install-profile-rules` separately. |
