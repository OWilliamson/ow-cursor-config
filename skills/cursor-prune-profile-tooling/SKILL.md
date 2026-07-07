---
name: cursor-prune-profile-tooling
description: >-
  Removes profile rules or skills previously installed from ow-cursor-config that are
  no longer in the bundle catalog. Use when the user invokes cursor-prune-profile-tooling
  with input rules or skills to prune retired bundle tooling on Linux or Windows.
disable-model-invocation: true
---

# Prune profile tooling

## Invocation

**Manual only:** `/cursor-prune-profile-tooling` or `@cursor-prune-profile-tooling`.

## Required input

**`rules`** or **`skills`** — which manifest slice to prune. Do not run both in one invocation unless the user explicitly asks for two sequential runs.

## Definition of done

- User specified `rules` or `skills`.
- Prune script ran (or dry-run report shown).
- Only manifest-managed names absent from current catalog were removed.
- Manifest updated to match current catalog (unless dry-run).

## Non-goals

- Do not prune hooks, commands, or subagents.
- Do not remove user-authored rules/skills never installed via this bundle.
- Do not install or update (use `@cursor-install-profile-rules` or `@cursor-install-profile-skills`).

## Workflow

1. Confirm required input: `rules` or `skills`. If missing, ask once.
2. Resolve repo root and profile per [reference-platform.md](reference-platform.md).
3. Default to **dry-run** when the user asks what would be removed; otherwise confirm before delete unless they said "prune now".
4. Run `prune-profile-<kind>` for the platform.
5. If manifest missing for that kind, stop and tell user to run install first.
6. Report removed paths and counts.

## Boundaries

- Deletes only under `$CURSOR_PROFILE/rules/` or `$CURSOR_PROFILE/skills/` for names in the managed manifest that left the catalog.
- No git or network operations.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| "Delete all rules not in the repo." | Prune only removes names previously installed from this bundle (manifest-gated). |
| "Prune rules and skills together." | Two script invocations — one per kind — unless user explicitly requests both in sequence. |
