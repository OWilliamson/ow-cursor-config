# Create identity rule — examples

## Example: full identity rule

**Inputs:**

| Field | Value |
|-------|-------|
| Handle | `acme-dev` |
| GitHub | `acme-dev` |
| Legal name | Alex Martin |
| GitHub variant | AcmeDev |
| Systems | Jira, Confluence, Slack, email |

**Output:** `~/.cursor/rules/acme-dev-user.mdc`

```markdown
---
description: Identity for the user acme-dev in every session.
alwaysApply: true
---

# AcmeDev user

## Identity

The user is **acme-dev** (GitHub: `acme-dev`; also **Alex Martin** in Jira, Confluence, Slack, and email).

## GitHub (personal account)

Bindings for [github-and-remotes.mdc](github-and-remotes.mdc) (sibling under `~/.cursor/rules/`):

- **Personal GitHub user/org:** `acme-dev` (also **AcmeDev** — match remotes case-insensitively).
- **Repo create defaults:** owner = this account; default branch `main`; visibility `private`.

## Stance

- **Peer engineer**: direct; assume technical competence.
- **Unknown user-specific facts** (policy, secrets, environment, unreleased detail): one focused question — do not guess.
```

## Example: minimal identity rule

**Inputs:** handle `jdoe`, GitHub `jdoe` — no legal name or variants.

**Output:** `~/.cursor/rules/jdoe-user.mdc`

```markdown
---
description: Identity for the user jdoe in every session.
alwaysApply: true
---

# Jdoe user

## Identity

The user is **jdoe** (GitHub: `jdoe`).

## GitHub (personal account)

Bindings for [github-and-remotes.mdc](github-and-remotes.mdc) (sibling under `~/.cursor/rules/`):

- **Personal GitHub user/org:** `jdoe`.
- **Repo create defaults:** owner = this account; default branch `main`; visibility `private`.

## Stance

- **Peer engineer**: direct; assume technical competence.
- **Unknown user-specific facts** (policy, secrets, environment, unreleased detail): one focused question — do not guess.
```
