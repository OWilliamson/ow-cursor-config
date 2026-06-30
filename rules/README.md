# Cursor rules (`rules/`)

**What this is:** Files here are **Cursor rules** (`.mdc` = Markdown with optional **YAML frontmatter**). They give the agent **persistent, repo- or user-level guidance**: coding standards, safety constraints, product terminology, and workflow expectations. Frontmatter fields such as `description`, `globs`, and `alwaysApply` control when and how strongly a rule applies after the files are installed under `~/.cursor/rules/` or `.cursor/rules/`.

**Scope:** These rules are maintained as the generic **OWilliamson** baseline in `public/`; merge or replace carefully when syncing with a project's `.cursor/rules/`. Personal identity rule (`owilliamson-user.mdc`) lives in [`private/rules/`](../../private/rules/).

**Activation:** `alwaysApply: true` = always on. `alwaysApply: false` with `globs` = auto-attached when matching files are in context. `alwaysApply: false` with a `description` and no `globs` = apply intelligently (agent pulls in when relevant). No `description` and no `globs` = manual `@` mention only.

**Related:** Agent Skills (separate packages with `SKILL.md` and co-located references) live in the sibling [`../skills/`](../skills/) tree, not under this `rules/` folder.

## Contents

| Rule file | What it does |
|-----------|----------------|
| [external-systems-read-only.mdc](external-systems-read-only.mdc) | **Umbrella default-deny** for writes outside the workspace; allows read/explore. Points to domain rules (e.g. GitHub) for allow/deny detail. |
| [technical-why.mdc](technical-why.mdc) | **WHY / explain / understand** questions: mechanism, root cause, or design decision — not perception talk. Apply intelligently. |
| [diagnose-issues.mdc](diagnose-issues.mdc) | **Issue / investigate / diagnose** requests: credible reports, named causes, no minimization. Apply intelligently. |
| [itrs-engineer.mdc](itrs-engineer.mdc) | **ITRS engineer** first-party context, internal doc hierarchy (Confluence, Jira, Slack), product scope. Apply intelligently. |
| [opsview-context.mdc](opsview-context.mdc) | **Opsview monitoring** wording (Opsview not Nagios; OP5 exception) and **invalid opsview.com sources** — scoped by `globs`. |
| [github-and-remotes.mdc](github-and-remotes.mdc) | **GitHub** read order (MCP → SSH → HTTP), commit/PR prose, OWilliamson repo classes and write policy. Apply intelligently. |

Superseded rules: [`archive/superseded-rules/`](../../archive/superseded-rules/).
