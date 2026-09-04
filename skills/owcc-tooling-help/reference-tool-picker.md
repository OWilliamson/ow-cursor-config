# Tool picker (public skills only)

Routes skills shipped in this repository (`owcc-*`). Unprefixed profile skills (plan, chat, worklog) are out of scope here.

## Session and hooks

| Goal | Use | Not |
|------|-----|-----|
| Painful / slow agent session post-mortem | `/owcc-session-retro` | Re-litigating in same noisy thread |
| Automatic nudge after heavy turns | `agent-retro-meter` hook + `/owcc-session-retro` | Manual guesswork |

## Authoring and quality

| Goal | Use | Not |
|------|-----|-----|
| Audit skill package (read-only; improve VALIDATION norms) | `/owcc-skill-validate` | `/owcc-skill-improve` (mutates) |
| Refactor skill package (full reshape) | `/owcc-skill-improve` | validate skill; modify for surgical edits |
| Maintain improved skill (META-first surgical edits) | `/owcc-skill-modify` | improve (full rewrite); validate (read-only) |
| Audit rule `.mdc` (read-only) | `/owcc-rule-validate` | |
| Refactor rule `.mdc` | `/owcc-rule-improve` | |
| Red/Amber/Green workflow or policy inventory | `/owcc-workflow-review` | |
| Compress always-on context files | `/owcc-context-compress` | improve-skill alone |
| Migrate Settings User Rules → `.mdc` | `/owcc-ui-convert-rules` | Hand-splitting without template |
| Scaffold personal identity rule | `/owcc-identity-create-rule` | Ad-hoc rule files |
| Strip LLM writing tropes (audit or rewrite) | `/owcc-prose-strip-tropes` | Restyling code/config; inventing “soul” |

## Review and repo hygiene

| Goal | Use | Not |
|------|-----|-----|
| Script / small tooling review | `/owcc-script-review` | Full app code review |
| Repo cruft / consolidation audit | `/owcc-repo-cleanup` | Ad-hoc deletes |
| Convention change without drift | `/owcc-repo-convention-change` | |
| PR / diff bug scan (Cursor built-in) | `/review-bugbot` | owcc-script-review |
| Security pass on local changes (Cursor built-in) | `/review-security` | One-line nits only |

## Delegation

| Goal | Use | Not |
|------|-----|-----|
| When to spawn explore / shell / Task | `/owcc-agent-delegate` | Vanilla explore without contract |
| Subagent notes in repo | `subagents/README.md` in this repo | |

## Customer / domain

| Goal | Use | Not |
|------|-----|-----|
| Customer-facing explanation draft | `/owcc-customer-explanation` | Internal runbooks or Jira comments |

## Meta

| Goal | Use | Not |
|------|-----|-----|
| Which public skill or hook fits? | `/owcc-tooling-help` | Guessing from memory |

## Profile kit install (ow-cursor-config)

Open **ow-cursor-config** as the Cursor workspace. Project skills in `.cursor/skills/` (not `~/.cursor/skills/`):

| Goal | Use | Not |
|------|-----|-----|
| Install default kit (`owcc-kit-starter`) | `bash scripts/install-profile-kit.sh` | Ad-hoc `cp` of individual skills/rules |
| Install all shippable kits | `bash scripts/install-profile-kit.sh --all` | |
| Install one kit | `bash scripts/install-profile-kit.sh --kit owcc-kit-author` | |
| Prune a kit | `bash scripts/prune-profile-kit.sh --kit NAME` | Deleting user-authored files |

Scripts: [scripts/profile-tooling.md](../scripts/profile-tooling.md) in ow-cursor-config.

## Prefix cheat sheet

| Prefix / shape | Meaning |
|----------------|---------|
| `owcc-kit-*` | Profile install kit (not a skill) |
| `owcc-<target>-*` | Public profile skill (`target` = plan, skill, rule, …) |
| (unprefixed) | Private skill — no `owcc-` |
