# Cursor Agent Skills (`skills/`)

**What this is:** Each skill lives in **its own subdirectory**. That directory is the skill’s package: **`SKILL.md`** (YAML frontmatter: `name`, `description`, optional flags) plus **all supporting files shipped with the skill**—scripts, checklists, reference markdown, nested folders such as `scripts/`, and any other assets the skill relies on—**co-located** under that same folder. Skills are **on-demand playbooks**—the agent loads them when the user `@`-mentions the skill or when the description matches the task. Keeping supporting material with `SKILL.md` supports progressive disclosure.

**Install note:** Use [`scripts/install-profile-skills.sh`](../scripts/install-profile-skills.sh) to copy bundle skills to `~/.cursor/skills/`. For rules, use [`scripts/install-profile-rules.sh`](../scripts/install-profile-rules.sh). For agent-assisted install, open this repo as the workspace and use project skills in [`.cursor/skills/`](../.cursor/skills/) — see [scripts/profile-tooling.md](../scripts/profile-tooling.md) and [AGENTS.md](../AGENTS.md).

## Naming prefixes

| Prefix | Meaning |
|--------|---------|
| **`repo-`** | Repository structure, policy, cleanup, conventions |
| **`script-`** | Scripts and small tooling code review |
| **`cursor-`** | Cursor meta (session retro, validate/improve, delegate, tooling picker, compress context, …) |

## Skill packages

| Skill folder | What it does |
|--------------|----------------|
| [repo-convention-change/](repo-convention-change/) | **Convention changes** without drift: classify new vs restate vs redefine; align docs and tooling to one policy. |
| [repo-cleanup/](repo-cleanup/) | **Audit** Cursor-oriented repos for cruft, merges, consolidation, rehoming rules/skills, `.gitignore`; report first, then edit only after approval. |
| [script-review/](script-review/) | **Structured script / tooling code review**: errors, design, structure, efficiency, docs, error handling, sanity check. |
| [cursor-create-identity-rule/](cursor-create-identity-rule/) | **Scaffold** a personal always-on `{handle}-user.mdc` with GitHub bindings for `github-and-remotes.mdc`; manual invocation only (`disable-model-invocation`). |
| [cursor-session-retro/](cursor-session-retro/) | **Post-mortem / retro** for painful agent sessions: evidence-backed root causes and a capped backlog. Optional hook integration via `reference-hooks.md`. |
| [cursor-workflow-review/](cursor-workflow-review/) | **Red/Amber/Green** workflow review **or** **policy inventory** (where conventions live); see `reference.md` fast path; helpers under `scripts/`. |
| [cursor-validate-skill/](cursor-validate-skill/) | **Mechanical pass/fail audit** of a `SKILL.md` package against vendored norms; chat report with findings keyed to norm IDs. |
| [cursor-improve-skill/](cursor-improve-skill/) | **Editorial refactor + apply** for a `SKILL.md` package; post-change capabilities and usage report. |
| [cursor-convert-ui-rules/](cursor-convert-ui-rules/) | **Migrates** Settings “User Rules” paste into `.mdc` files (manual invocation only). |
| [cursor-compress-context/](cursor-compress-context/) | **Compresses** always-on context files (e.g. `AGENTS.md`, alwaysApply rules) while preserving code blocks, paths, and URLs; backs up originals. |
| [cursor-delegate/](cursor-delegate/) | **Delegation guide** — when to use Task subagents vs main thread and structured return contracts. |
| [cursor-tooling-help/](cursor-tooling-help/) | **One-shot tool picker** — which skill, rule, hook, or workflow fits a goal. |
| [cursor-validate-rule/](cursor-validate-rule/) | **Read-only audit** of a Cursor rule (`.mdc`) against authoring norms; explicit `/cursor-validate-rule` or `@cursor-validate-rule` (`disable-model-invocation`). |
| [cursor-improve-rule/](cursor-improve-rule/) | **Refactors** a rule (`.mdc`) for clarity and less drift before shipping; explicit `/cursor-improve-rule` or `@cursor-improve-rule` (`disable-model-invocation`). |
| [customer-explanation/](customer-explanation/) | **Drafts** concise customer-facing technical explanations from internal context (no internal links or gap-focused language). |

Install/prune project skills (`cursor-install-profile-*`, `cursor-prune-profile-tooling`) live in [`.cursor/skills/`](../.cursor/skills/) — not under this `skills/` tree.

### Supporting assets (by skill)

| Location | Role |
|----------|------|
| `cursor-workflow-review/scripts/` | `check_paths.py`, `extract_cited_paths.py`, `scan_rule_frontmatter.py` — repo/rule path checks. |
| `cursor-workflow-review/reference.md` | Full RAG output template, **policy inventory fast path**, helper script invocations. |
| `cursor-validate-rule/`, `cursor-improve-rule/` | `reference-cursor-rule-authoring-norms.md`, `reference-report-skeleton.md`, `reference-examples.md` — rule authoring norms and samples. |
| `repo-convention-change/`, `repo-cleanup/` | `reference.md` (and `repo-convention-change/README.md`). |
| `cursor-convert-ui-rules/` | `reference-hub.md`. |
| `cursor-create-identity-rule/` | `reference-hub.md`, `reference-examples.md` — template, preflight, and worked examples. |
| `cursor-compress-context/` | `reference-compression-rules.md` — preserve vs compress rules for always-on files. |
| `cursor-delegate/` | `reference-delegation.md` — subagent routing and output contracts. |
| `cursor-tooling-help/` | `reference-tool-picker.md` — decision tables for skills, rules, hooks, and profile install. |
| `customer-explanation/` | `reference-public-docs.md`, `examples.md` — tone, structure, and sample outputs. |
| `scripts/` (repo root) | `profile-tooling.md`, install/prune wrappers, `generate-bundle-manifest.py` — see [../scripts/profile-tooling.md](../scripts/profile-tooling.md). |
| `script-review/` | `reference-rubric.md`. |
| `*/reference.md`, `*/reference-checklist.md`, `*/reference-report-skeleton.md`, `*/reference-cursor-authoring-norms.md`, `*/reference-examples.md`, `*/README.md` | Other skills: extra checklists and references loaded when the skill points to them. |
