---
name: cursor-create-identity-rule
description: >-
  Scaffolds a personal always-on identity rule (.mdc) with handle, legal name,
  GitHub bindings for github-and-remotes, and communication stance. Use when the
  user manually invokes cursor-create-identity-rule to bootstrap an identity rule,
  user identity rule, or {handle}-user.mdc for a new Cursor profile.
disable-model-invocation: true
---

# Create identity rule

## Invocation

**Manual only:** load by **name** (`cursor-create-identity-rule`) or **`@cursor-create-identity-rule`**. Do **not** infer this workflow from ambient chat alone.

Discovery fields, emit template, hub paths, preflight, post-steps, and checklist: **[reference-hub.md](reference-hub.md)**.

Worked example: **[reference-examples.md](reference-examples.md)**.

## Required inputs

Gather from the user (or infer only when unambiguous from context):

1. **Handle** — short username (drives filename and rule title).
2. **GitHub username** — personal GitHub account for `github-and-remotes.mdc` bindings.
3. **Optional:** legal or display name; GitHub casing variants; names in Jira, Confluence, Slack, or email; repo-create defaults; custom stance bullets; destination directory.

If any required field is missing, ask **once** with a focused question. Do not invent employer, org, or email details.

## Definition of done

- One `{handle}-user.mdc` written to the agreed destination with `alwaysApply: true`.
- Body matches the template in `reference-hub.md` (Identity, GitHub, Stance sections).
- Preflight checks in `reference-hub.md` completed.
- User reminded per post-steps in `reference-hub.md`.

## Non-goals

- Do not write identity rules to `public/rules/` (identity is personal, not export staging).
- Do not fold in coding standards, external-systems policy, or domain rules.
- Do not invent GitHub orgs, emails, or employer context.
- Do not duplicate identity prose in **Settings → Rules → User Rules** after the file exists.

## Workflow

1. Read [reference-hub.md](reference-hub.md) and [reference-examples.md](reference-examples.md).
2. Gather required and optional inputs per `reference-hub.md`.
3. Run preflight checks (existing file, `github-and-remotes.mdc` sibling, always-on budget).
4. Emit `{handle}-user.mdc` from the template in `reference-hub.md`.
5. Finish with post-write reminders in `reference-hub.md`.

## Excuse → Reality

| Excuse | Reality |
|--------|---------|
| "I'll put identity in Settings User Rules instead." | File-backed identity belongs in `{handle}-user.mdc`; clear Settings after sync to avoid duplicate always-on context. |
| "Public rules is fine for identity." | Identity is personal; use `~/.cursor/rules/` (live profile) — never a shared or export-staged rules tree. |
| "I can guess the GitHub handle." | Required input; `github-and-remotes.mdc` reads the account from this rule — wrong handle breaks remote policy. |
