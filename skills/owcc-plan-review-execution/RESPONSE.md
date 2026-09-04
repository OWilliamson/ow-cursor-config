# Completion response

Chat/session OUTPUT when `/owcc-plan-review-execution` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Plan success review

**Plan:** <path>
**Scope:** whole plan | phase <name> | todo <id>
**Baseline:** <rev or merge-base summary>
**Overall:** pass | pass_with_warnings | fail | incomplete_review

### Success judgments

| Dimension | Verdict | Judgment |
|-----------|---------|----------|
| Aims | pass/warn/fail/n/a | <criterion → workspace outcome → why verdict> |
| Target shape | pass/warn/fail/n/a | <criterion → workspace outcome → why verdict> |
| Scope | pass/warn/fail/n/a | <criterion → workspace outcome → why verdict> |
| Stop-if | pass/warn/fail/n/a | <criterion → workspace outcome → why verdict> |
| Rules / §9 | pass/warn/fail/n/a | <criterion → workspace outcome → why verdict> |
| Better than start | pass/warn/fail/n/a | <baseline / regression / forward-change — not Aims> |

### Failures — why and action

| ID | Source | Severity | Why | Action needed? | Next step |
|----|--------|----------|-----|----------------|-----------|
| F1 | <dim or todo> | fail/warn | <cause> | yes/no | <recommendation or none> |

### Per-todo correctness

| Todo | YAML | Judgment | Verdict | Failure ID |
|------|------|----------|---------|------------|
| <id> | completed | <criterion → outcome → why> | pass/warn/fail/blocked/n/a | F<n> or — |

### Subagent findings

- Bugbot: <summary or n/a — skip reason>
- Security Review: <summary or n/a — skip reason>

### A/M/R inventory

- A/M/R: <claimed missing/wrong / unplanned summary>
- code_loc: <n> — bugbot_default: <on|off>

### Residual risks

<ambiguities, baseline caveats, authoring-only closeout notes IF appendix run>
```

## Sections

### Header (Plan / Scope / Baseline / Overall)

#### Use

Always.

#### Empty Allowance

No.

### Success judgments

#### Use

Always — lead the report after the header.

#### Empty Allowance

No — every row present (use n/a with reason IN Judgment when needed).

#### Judgment cell contract

Each Judgment cell MUST state: **plan criterion** (Aim Result, Target shape clause, Scope item, etc.) → **workspace outcome** (what disk/diff shows) → **why** the verdict follows. Do NOT fill with a lone path, snippet, or inventory line.

### Failures — why and action

#### Use

Always when any fail or warn exists across success dims, todos, or subagents.

#### Empty Allowance

Yes — write `none` IF Overall IS pass with no warns needing action.

#### ID contract

Assign sequential **F1**, **F2**, … to every fail and warn. Operator may reply by F-id (e.g. "F2 fixed — re-review"). Subagent defects that affect Overall get F-ids here.

### Per-todo correctness

#### Use

Always for todos IN scope.

#### Empty Allowance

No IF any todo IN scope — one row per todo. Judgment IS criterion → outcome → why, not YAML alone. Fail/warn rows MUST cite Failure ID.

### A/M/R inventory

#### Use

Always after inventory assist RUN (brief).

#### Empty Allowance

No — include A/M/R summary + code_loc / bugbot_default. Do NOT dump full JSON. Place after Subagent findings.

### Subagent findings

#### Use

Always.

#### Empty Allowance

No — Bugbot and Security each present as summary or **n/a** with skip reason.

### Residual risks

#### Use

Always.

#### Empty Allowance

No — write `none` explicitly IF empty. Prefer parking optional authoring-class closeout notes here.

### Closeout appendix (optional)

#### Use

Only when operator asked OR `**Plan build:** complete` present — after Residual or under Residual. Not a mandatory Objective-checks block.

#### Empty Allowance

Yes — omit entirely when not run.

## Section Contract

### Content

- Absolute plan path, scope, baseline, overall verdict ([DECISIONS §12](DECISIONS.md#12-overall-verdict)).
- Success judgments first ([DECISIONS §5](DECISIONS.md#5-success-dimensions), [§11](DECISIONS.md#11-better-than-start)).
- Failures with F-ids, why + action ([DECISIONS §10](DECISIONS.md#10-failure-why-and-action)).
- Per-todo correctness with Failure ID column ([DECISIONS §6](DECISIONS.md#6-per-todo-verdict)).
- Brief A/M/R inventory + Bugbot/Security ([DECISIONS §8](DECISIONS.md#8-bugbot-gate)–[§9](DECISIONS.md#9-security-review)).
- Remediation as recommendations only (this skill does not fix).

### Authoring

- Concise operator chat; do NOT dump full inventory JSON unless debugging.
- Operator may respond to enumerated F-ids.
- Do NOT suggest unrelated skills IN the report (naming a remediation invoke IN Failures next-step IS allowed).
- Do NOT MODIFY the plan or implement remediation IN this invocation.
- Lead with plan success; do NOT headline closeout authoring or YAML theater as if they were the product.
