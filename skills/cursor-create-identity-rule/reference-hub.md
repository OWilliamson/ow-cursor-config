# Create identity rule — paths, template, and checks

## Profile paths

| What | Path |
|------|------|
| Personal identity rules | `~/.cursor/rules/` |
| `github-and-remotes.mdc` (sibling contract) | `~/.cursor/rules/github-and-remotes.mdc` |

## Where to write files

Unless the user specifies another directory, write to **`~/.cursor/rules/`** (live profile rules).

**Never** write identity rules to a shared or export-staged rules tree — identity is personal.

## Filename

`{handle}-user.mdc` where `{handle}` is the user's short username in **kebab-case** (lowercase; non-alphanumeric runs become `-`).

On collision with an existing file: stop and ask whether to **update in place** or **archive then replace** (timestamped backup when the user wants history kept).

## Discovery fields

| Field | Required | Default / notes |
|-------|----------|-----------------|
| Handle | Yes | Drives filename and `# {Title} user` heading |
| GitHub username | Yes | Personal account for remote matching |
| Legal / display name | No | Omit identity clause if not supplied |
| GitHub casing variants | No | e.g. `AcmeDev` for case-insensitive remote match |
| Jira / Confluence / Slack / email name | No | Use legal name when same; list only systems the user names |
| Default branch | No | `main` |
| Repo visibility | No | `private` |
| Stance bullets | No | Peer engineer + ask-don't-guess defaults (see template) |
| Destination | If ambiguous | Ask once |

## Preflight

- [ ] Confirm `{handle}-user.mdc` does not already exist, or user chose update vs archive-replace.
- [ ] Confirm `github-and-remotes.mdc` is installed as a sibling under `~/.cursor/rules/` (identity rule binds to it).
- [ ] List other `alwaysApply: true` rules in the destination directory; sum line counts — flag if combined total is disproportionate (target: identity rule body under ~25 lines).

## Emit template

Substitute placeholders. Keep `description` on **one physical line** (no YAML `>-` or `|`).

```markdown
---
description: Identity for the user {handle} in every session.
alwaysApply: true
---

# {title} user

## Identity

The user is **{handle}** (GitHub: `{github_handle}`{identity_clause}).

## GitHub (personal account)

Bindings for [github-and-remotes.mdc](github-and-remotes.mdc) (sibling under `~/.cursor/rules/`):

- **Personal GitHub user/org:** `{github_handle}`{casing_note}.
- **Repo create defaults:** owner = this account; default branch `{default_branch}`; visibility `{visibility}`.

## Stance

{stance_bullets}
```

### Placeholder rules

| Placeholder | Rule |
|-------------|------|
| `{title}` | Title-case form of handle for the `#` heading (e.g. `acme-dev` → `AcmeDev`) |
| `{identity_clause}` | If legal/display name or named systems supplied: `; also **{name}** in Jira, Confluence, Slack, and email` — list only systems the user named; omit clause entirely if only handle + GitHub |
| `{casing_note}` | If variants supplied: ` (also **{Variant}** — match remotes case-insensitively)` — else omit |
| `{stance_bullets}` | Default unless user overrides: `- **Peer engineer**: direct; assume technical competence.` and `- **Unknown user-specific facts** (policy, secrets, environment, unreleased detail): one focused question — do not guess.` |

## After writing (tell the user)

1. Do **not** duplicate identity prose in **Settings → Rules → User Rules** — clear that field if it overlaps.
2. If the user keeps rules in git, commit the new file from their profile or dotfiles repo.
3. Smoke-check in a fresh chat: agent should know handle and GitHub account without re-asking.
4. Optionally run `cursor-validate-rule` on the new file.

## Agent checklist

- [ ] Required inputs gathered; nothing invented.
- [ ] File written to `~/.cursor/rules/` or agreed live profile path — not a shared export rules tree.
- [ ] Filename is `{handle}-user.mdc`.
- [ ] Frontmatter: `alwaysApply: true`, one-line `description`.
- [ ] GitHub section links `github-and-remotes.mdc`.
- [ ] Post-write reminders delivered.
