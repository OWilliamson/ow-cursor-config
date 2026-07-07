# ow-cursor-config release notes

Release history for this repository. Newest day at top.

## 2026-07-07

### Summary

Added profile install/prune scripts and catalog manifest, plus skills for context compression, subagent delegation, tooling picker, customer-facing explanations, and bundle rule/skill install. Added **itrs-org-routing** for ITRS information-source routing. Updated several rules and cursor meta skills (identity rule, validate/improve norms).

### Added

- `rules/itrs-org-routing.mdc` — topic-first routing for ITRS Confluence, Jira, Slack, GitHub, and public docs
- `catalog/bundle-manifest.yaml`, `catalog/bundle-manifest.json` — shipped rule and skill inventory for install/prune scripts
- `scripts/` — profile install and prune wrappers (`install-profile-*.sh`/`.ps1`, `prune-profile-*.sh`/`.ps1`, `profile-tooling.md`)
- `skills/cursor-compress-context/` — compress always-on context files while preserving code, paths, and URLs
- `skills/cursor-delegate/` — when to use Task subagents and structured return contracts
- `skills/cursor-install-profile-rules/`, `skills/cursor-install-profile-skills/` — install bundle rules or skills into `~/.cursor/`
- `skills/cursor-prune-profile-tooling/` — prune profile rules or skills retired from the bundle
- `skills/cursor-tooling-help/` — one-shot tool picker for skills, rules, hooks, and workflows
- `skills/customer-explanation/` — draft customer-facing technical explanations from internal context

### Changed

- `rules/external-systems-read-only.mdc` — precedence and domain-rule pointers clarified
- `rules/github-and-remotes.mdc` — identity-rule binding and write-policy wording
- `rules/itrs-engineer.mdc` — engineer stance and doc hierarchy updates
- `rules/opsview-context.mdc` — Opsview wording and invalid-source guardrails
- `skills/cursor-create-identity-rule/` — SKILL, examples, and hub reference aligned to current norms
- `skills/cursor-improve-rule/`, `skills/cursor-validate-rule/` — authoring norms reference updates
- `skills/cursor-improve-skill/`, `skills/cursor-validate-skill/` — authoring norms reference updates

### README updates

- `README.md` — add `catalog/` and `scripts/` to layout table
- `rules/README.md` — add `itrs-org-routing.mdc`
- `skills/README.md` — add new skill packages and profile-install row in supporting assets

## 2026-06-30

### Summary

Retired all slash commands (commands folder is index-only). Added rules for diagnostics, GitHub remotes, ITRS engineering context, Opsview wording, and technical “why/how” answers. Added **cursor-create-identity-rule** skill to scaffold a personal identity rule for GitHub policy. Removed legacy rules merged into the new set and retired cursor-test-skill and plan-check-cursor. Updated github-and-remotes to read the GitHub account from the identity rule, and refreshed cursor-improve-rule, cursor-validate-rule, repo-convention-change, and cursor-workflow-review.

### Added

- `skills/cursor-create-identity-rule/` — scaffold personal always-on identity rule with GitHub bindings for `github-and-remotes.mdc`
- `rules/diagnose-issues.mdc` — issue investigation and root-cause reporting norms
- `rules/github-and-remotes.mdc` — GitHub read order, commit/PR prose, repo write policy
- `rules/itrs-engineer.mdc` — ITRS engineer product and internal-doc context
- `rules/opsview-context.mdc` — Opsview wording and invalid-source guardrails
- `rules/technical-why.mdc` — mechanism/root-cause explanations for “why/how” questions

### Removed

- `commands/*` — all slash commands retired; workflows covered by rules and Cursor built-ins
- `rules/commit-and-pr-style.mdc` — superseded by `github-and-remotes.mdc`
- `rules/copy-files-with-cp.mdc` — tooling philosophy belongs in per-repo `AGENTS.md`
- `rules/github-repo-links-read-via-mcp-then-ssh-then-http.mdc` — merged into `github-and-remotes.mdc`
- `rules/opsview-monitoring.mdc`, `rules/opsview-sources-not-valid.mdc` — merged into `opsview-context.mdc`
- `rules/owilliamson-vendor-context.mdc` — personal vendor context; use a local identity rule instead
- `rules/remote-repo-approval.mdc`, `rules/replicated-vendor-portal-read-only.mdc` — folded into `external-systems-read-only.mdc` and domain rules
- `rules/repo-tooling-invariants.mdc` — use repo `AGENTS.md` tooling profile instead
- `rules/version-format.mdc` — repo-local versioning policy
- `skills/cursor-test-skill/` — removed from bundle
- `skills/plan-check-cursor/` — removed from bundle

### Changed

- `rules/github-and-remotes.mdc` — personal GitHub account from identity rule; generic repo-class wording
- `rules/external-systems-read-only.mdc` — umbrella default-deny with domain-rule pointers
- `skills/cursor-improve-rule/` — updated norms, examples, and SKILL workflow
- `skills/cursor-validate-rule/` — updated norms, examples, and SKILL workflow
- `skills/cursor-convert-ui-rules/reference-hub.md` — portable path references
- `skills/cursor-workflow-review/reference.md` — policy inventory and helper notes
- `skills/repo-convention-change/` — SKILL, README, and reference aligned to current policy
- `hooks.json` — formatting only (same hook events and `agent-retro-meter` registration)

### README updates

- `README.md` — commands folder marked retired (index-only)
- `commands/README.md` — retirement status
- `rules/README.md` — current rule inventory; identity rule + `github-and-remotes` pairing note
- `skills/README.md` — added `cursor-create-identity-rule`; removed retired skills; updated tooling note
