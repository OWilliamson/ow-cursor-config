# Cursor Agent Skills (`skills/`)

**What this is:** Each skill lives in **its own subdirectory**. That directory is the skill’s package: **`SKILL.md`** (YAML frontmatter: `name`, `description`, optional flags) plus **all supporting files shipped with the skill**—scripts, checklists, reference markdown, nested folders such as `scripts/`—**co-located** under that same folder. Skills are **on-demand playbooks**—the agent loads them when the user `@`-mentions the skill or when the description matches the task.

**Install note:** Use [`scripts/install-profile-kit.sh`](../scripts/install-profile-kit.sh) to install kits into `~/.cursor/`. See [scripts/profile-tooling.md](../scripts/profile-tooling.md).

## Naming prefixes

| Prefix | Meaning |
|--------|---------|
| **`owcc-kit-*`** | Profile install kit (not a skill; see `bundles/`) |
| **`owcc-<target>-*`** | Public profile skill (`target` = plan, skill, rule, repo, …) |

## Skill packages

| Skill folder | What it does |
|--------------|----------------|
| [owcc-agent-delegate/](owcc-agent-delegate/) | When to spawn Task subagents vs stay on the main thread, and structured return contracts. |
| [owcc-context-compress/](owcc-context-compress/) | Compress always-on context files while preserving code, paths, and URLs. |
| [owcc-customer-explanation/](owcc-customer-explanation/) | Draft customer-facing technical explanations from internal context (public doc links only). |
| [owcc-identity-create-rule/](owcc-identity-create-rule/) | Scaffold a personal always-on `{handle}-user.mdc` with GitHub bindings for `github-and-remotes.mdc`. |
| [owcc-plan-build/](owcc-plan-build/) | Build or complete a Cursor plan from intake through closeout. |
| [owcc-plan-improve/](owcc-plan-improve/) | Reshape an existing plan. |
| [owcc-plan-review-execution/](owcc-plan-review-execution/) | Review whether a plan succeeded as specified. |
| [owcc-plan-triage/](owcc-plan-triage/) | Harvest and patch plan problems. |
| [owcc-plan-validation-report/](owcc-plan-validation-report/) | Write plan validation report artifacts. |
| [owcc-plan-verification-cursor/](owcc-plan-verification-cursor/) | Cursor-native plan verification and closeout helpers. |
| [owcc-prose-strip-tropes/](owcc-prose-strip-tropes/) | Audit or rewrite common LLM writing tropes. |
| [owcc-repo-cleanup/](owcc-repo-cleanup/) | Audit Cursor-oriented repos for cruft and consolidation; report first. |
| [owcc-repo-convention-change/](owcc-repo-convention-change/) | Apply a convention change without doc/tooling drift. |
| [owcc-rule-improve/](owcc-rule-improve/) | Refactor a rule `.mdc` for clarity before shipping. |
| [owcc-rule-validate/](owcc-rule-validate/) | Read-only audit of a rule `.mdc` against authoring norms. |
| [owcc-script-review/](owcc-script-review/) | Structured review of scripts and small tooling. |
| [owcc-session-retro/](owcc-session-retro/) | Post-mortem for painful agent sessions. |
| [owcc-skill-improve/](owcc-skill-improve/) | Full reshape of a skill package. |
| [owcc-skill-modify/](owcc-skill-modify/) | Surgical META-first edits to an existing skill package. |
| [owcc-skill-validate/](owcc-skill-validate/) | Read-only audit of a skill package against CS-* norms. |
| [owcc-tooling-help/](owcc-tooling-help/) | One-shot picker for which skill, rule, or hook fits a goal. |
| [owcc-ui-convert-rules/](owcc-ui-convert-rules/) | Migrate Settings User Rules paste into `.mdc` files. |
| [owcc-workflow-review/](owcc-workflow-review/) | Red/Amber/Green workflow review or policy inventory. |

Install/prune project skills live in [`.cursor/skills/`](../.cursor/skills/) — not under this `skills/` tree.

### Supporting assets (by skill)

| Location | Role |
|----------|------|
| `owcc-workflow-review/scripts/` | Path and frontmatter helpers for workflow review. |
| `owcc-workflow-review/reference.md` | Scoring, inventory fast path, helper invocations. |
| `owcc-rule-validate/` | Rule authoring norms, report skeleton, examples. |
| `owcc-plan-*/` | `DECISIONS.md`, `VALIDATION.md`, `WORKFLOW.yaml`; some packages include `scripts/`. |
| `owcc-skill-improve/`, `owcc-skill-modify/`, `owcc-skill-validate/` | Spine files (`DECISIONS`, `VALIDATION`, `META`, `WORKFLOW.yaml`). |
| `owcc-agent-delegate/reference-delegation.md` | Subagent routing and output contracts. |
| `owcc-tooling-help/reference-tool-picker.md` | Decision tables for skills, rules, hooks, and kit install. |
| `owcc-customer-explanation/` | `reference-public-docs.md`, `examples.md`. |
| `owcc-session-retro/` | `reference.md`, `reference-hooks.md`. |
| `scripts/` (repo root) | Kit install/prune — [../scripts/profile-tooling.md](../scripts/profile-tooling.md). |
