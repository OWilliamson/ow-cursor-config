# Tool picker

## Session and context

| Goal | Use | Not |
|------|-----|-----|
| Painful / slow agent session post-mortem | `@cursor-session-retro` | Re-litigating in same noisy thread |
| Automatic nudge after heavy turns | `agent-retro-meter` hook + retro skill | Manual guesswork |
| Hand off to a **new** chat (ephemeral) | `@chat-notation` (private profile) | chat-notes as long-term docs |
| Save durable personal session log | `@chat-lastresponse` (private) | chat-notes folder |
| Execute a saved plan | `@plan-build` (private) | chat-notation |

## Authoring and quality

| Goal | Use | Not |
|------|-----|-----|
| Audit skill package (read-only) | `@cursor-validate-skill` | Eyeball only |
| Refactor skill package (apply edits) | `@cursor-improve-skill` | validate skill |
| Audit rule `.mdc` (read-only) | `@cursor-validate-rule` | |
| Refactor rule `.mdc` | `@cursor-improve-rule` | |
| Red/Amber/Green workflow or policy inventory | `@cursor-workflow-review` | |
| Compress always-on context files | `@cursor-compress-context` | improve-skill alone |

## Review and repo hygiene

| Goal | Use | Not |
|------|-----|-----|
| Script / small tooling review | `@script-review` | Full app code review skill |
| Repo cruft / consolidation audit | `@repo-cleanup` | Ad-hoc deletes |
| Convention change without drift | `@repo-convention-change` | |
| PR / diff bug scan (Cursor built-in) | `@review-bugbot` | script-review |
| Security pass on local changes | `@review-security` | One-line nits only |

## Delegation

| Goal | Use | Not |
|------|-----|-----|
| When to spawn explore / shell / Task | `@cursor-delegate` | Vanilla explore without contract |
| Subagent notes in repo | `subagents/README.md` in this repo | |

## Profile install (ow-cursor-config)

| Goal | Use | Not |
|------|-----|-----|
| Install/update bundle rules to profile | `@cursor-install-profile-rules` | Manual one-off `cp` |
| Install/update bundle skills to profile | `@cursor-install-profile-skills` | `skills-cursor/` |
| Prune retired bundle rules or skills | `@cursor-prune-profile-tooling` (input `rules` or `skills`) | Deleting user-authored files |
| Personal identity rule | `@cursor-create-identity-rule` | Shipped rules tree |

Scripts: `scripts/profile-tooling.md` in this repo.

## Prefix cheat sheet

| Prefix | Meaning |
|--------|---------|
| `cursor-` | Cursor meta (validate, improve, retro, delegate, …) |
| `repo-` | Repository structure and policy |
| `script-` | Script and tooling review |
