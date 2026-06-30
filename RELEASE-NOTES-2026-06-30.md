# ow-cursor-config release notes — 2026-06-30

Source: cursor-config-generic `public/` → publish-ow-cursor-config.sh
Hub reconcile: pass (profile synced; some ARCHIVE_SKIP on alt archive paths — permission on existing archive dirs)

## Summary

Aligns the published tree with the hub’s current `public/` classification: retired slash commands and legacy rules/skills removed; consolidated GitHub, ITRS/Opsview, and diagnostic rules added; cursor rule validate/improve skills and repo-convention-change refreshed. Commands folder is index-only (all commands retired 2026-06-12).

## Added

- `rules/diagnose-issues.mdc` — issue investigation and root-cause reporting norms
- `rules/github-and-remotes.mdc` — GitHub read order, commit/PR prose, repo write policy
- `rules/itrs-engineer.mdc` — ITRS engineer product and internal-doc context
- `rules/opsview-context.mdc` — Opsview wording and invalid-source guardrails
- `rules/technical-why.mdc` — mechanism/root-cause explanations for “why/how” questions

## Removed

- `commands/*` (all former slash commands) — retired to hub archive 2026-06-12; workflows covered by rules and Cursor built-ins
- `rules/commit-and-pr-style.mdc` — superseded by `github-and-remotes.mdc`
- `rules/copy-files-with-cp.mdc` — tooling philosophy moved to per-repo `AGENTS.md`
- `rules/github-repo-links-read-via-mcp-then-ssh-then-http.mdc` — merged into `github-and-remotes.mdc`
- `rules/opsview-monitoring.mdc`, `rules/opsview-sources-not-valid.mdc` — merged into `opsview-context.mdc`
- `rules/owilliamson-vendor-context.mdc` — personal/vendor context stays in hub `private/`
- `rules/remote-repo-approval.mdc`, `rules/replicated-vendor-portal-read-only.mdc` — folded into `external-systems-read-only.mdc` / domain rules
- `rules/repo-tooling-invariants.mdc` — archived pending rethink; use repo `AGENTS.md` tooling profile
- `rules/version-format.mdc` — hub-only maintenance policy
- `skills/cursor-test-skill/` — not in current public classification
- `skills/plan-check-cursor/` — plan skills retired from public export

## Changed

- `rules/external-systems-read-only.mdc` — umbrella default-deny with domain-rule pointers
- `skills/cursor-improve-rule/` — updated norms, examples, and SKILL workflow
- `skills/cursor-validate-rule/` — updated norms, examples, and SKILL workflow
- `skills/cursor-convert-ui-rules/reference-hub.md` — hub path references refreshed
- `skills/cursor-workflow-review/reference.md` — policy inventory and helper notes
- `skills/repo-convention-change/` — SKILL, README, and reference aligned to current hub policy
- `hooks.json` — formatting only (same hook events and `agent-retro-meter` registration)

## README updates

- `README.md` — commands folder marked retired (index-only)
- `commands/README.md` — retirement status and recovery path
- `rules/README.md` — current rule inventory table
- `skills/README.md` — removed `cursor-test-skill` and `plan-check-cursor`; tooling philosophy note updated

## Verify locally

```bash
cd /home/owilliamson/Documents/Cursor/ow-cursor-config
git status
git diff
```

## Not included

- `private/` hub content
- `**/state.json` (runtime hook state; publish excludes)
