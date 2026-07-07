---
name: cursor-install-profile-rules
description: >-
  Installs or updates shipped Cursor rules from ow-cursor-config into the user
  profile (~/.cursor/rules). Use when the user invokes cursor-install-profile-rules
  to sync bundle rules, update profile rules from the repo, or bootstrap rules on
  Linux or Windows.
disable-model-invocation: true
---

# Install profile rules

## Invocation

**Manual only:** `/cursor-install-profile-rules` or `@cursor-install-profile-rules`.

Platform routing and script paths: **[reference-platform.md](reference-platform.md)**. Operator reference: **[../../scripts/profile-tooling.md](../../scripts/profile-tooling.md)**.

## Definition of done

- `install-profile-rules` script ran successfully (or `--dry-run` report shown).
- Shipped `.mdc` files exist under `$CURSOR_PROFILE/rules/`.
- `$CURSOR_PROFILE/.ow-cursor-config-manifest.json` lists current catalog rule names (unless dry-run).

## Non-goals

- Do not install skills, hooks, commands, or subagents.
- Do not prune removed rules (use `@cursor-prune-profile-tooling` with input `rules`).
- Do not write identity rules (`{handle}-user.mdc`) — use `@cursor-create-identity-rule`.
- Do not commit, push, or mutate remotes.

## Workflow

1. Resolve **repo root** (`OW_CURSOR_CONFIG` → walk up from this skill to repo root → ask user).
2. Resolve **profile** (`CURSOR_PROFILE` → OS default → ask if WSL/Windows ambiguous).
3. If the user asked to preview, pass `--dry-run` / `-DryRun`.
4. **Route platform** per [reference-platform.md](reference-platform.md) and run `install-profile-rules`.
5. Report summary lines from script output (installed / updated / unchanged; manifest path).
6. Remind: personal identity rule is separate (`@cursor-create-identity-rule`); optional spot-check with `@cursor-validate-rule`.

## Boundaries

- Local filesystem only under repo and `$CURSOR_PROFILE`.
- Never delete profile rules not managed by the bundle manifest.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| "I'll copy one .mdc by hand." | Use the script so manifest stays aligned for prune. |
| "Install skills too." | Use `@cursor-install-profile-skills` — separate skill and script. |
