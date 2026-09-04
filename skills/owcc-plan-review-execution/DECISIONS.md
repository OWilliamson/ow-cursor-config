# Success-review decisions

Enumerated decisions for `/owcc-plan-review-execution`, IN **[SKILL.md](SKILL.md)** workflow order. Rubric: [VALIDATION.md](VALIDATION.md). Chat shape: [RESPONSE.md](RESPONSE.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target plan](#1-target-plan) | 5.3.1 |
| 2 | [Review scope](#2-review-scope) | 5.3.1 |
| 3 | [Git baseline](#3-git-baseline) | 5.3.1 |
| 4 | [Closeout finding class](#4-closeout-finding-class) | 5.3.10 (optional appendix) |
| 5 | [Success dimensions](#5-success-dimensions) | 5.3.3–5.3.7 |
| 6 | [Per-todo verdict](#6-per-todo-verdict) | 5.3.8 |
| 7 | [Workspace rules](#7-workspace-rules) | 5.3.7 |
| 8 | [Bugbot gate](#8-bugbot-gate) | 5.3.9 |
| 9 | [Security Review](#9-security-review) | 5.3.9 |
| 10 | [Failure why and action](#10-failure-why-and-action) | 5.3.10 |
| 11 | [Better-than-start](#11-better-than-start) | 5.3.10 |
| 12 | [Overall verdict](#12-overall-verdict) | 5.3.10 |
| 13 | [A/M/R inventory severity](#13-amr-inventory-severity) | 5.3.2 |
| 14 | [Plan-edit severity](#14-plan-edit-severity) | 5.3.7 / residual |
| 15 | [Specified-but-undone](#15-specified-but-undone) | 5.3.3–5.3.8 |

---

## 1. Target plan

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use @ / path / paste** | Review that plan file or pasted body | User provides `@path`, absolute path, or pasted plan | That plan |
| **Open file + chat link** | Use the open file | File IS open AND clearly discussed IN this chat as the subject | That file |
| **Most recent IN chat** | Plan this conversation has been about | `/owcc-plan-review-execution` only; one clear subject | Paths cited, @ attachments, or named plan subject |
| **Ask operator** | One-line ask listing candidates | Two+ plans discussed OR none identified | Do not guess |

**Not valid:** IDE Recently viewed lists; arbitrary newest `.plan.md` IN workspace without chat linkage; a prior-topic plan unless still the active subject.

---

## 2. Review scope

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Todo only** | Success review for one todo id | User names a todo id | That todo; Aims/Target/Scope/Better relative to it |
| **Phase** | All todos IN `phases[].name` (case-insensitive) | User names a phase AND plan IS project (`isProject: true`) | That phase's todos; success dims relative to phase |
| **Whole plan** | All todos | Neither todo nor phase named | Full matrix; whole-plan success dims |
| **Phase → whole/todo** | Fall back | Phase named but plan IS flat | Say so; use whole plan or named todo |

Partial scope: Aims / Target shape / Scope / Better are judged relative to the todo/phase/whole IN scope — not the entire plan when scoped down.

---

## 3. Git baseline

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Operator `--base` / named rev** | Use that rev | User names a baseline | Preflight diff + Better-than-start |
| **merge-base main/master** | `git merge-base HEAD main` or `master` | Default when that branch exists | Preflight + Better |
| **HEAD + working tree** | Uncommitted + last commit only | No main/master | Preflight; note ambiguity IN Residual risks |
| **Blocked** | Cannot resolve | No git repo or merge-base fails hard | Overall **incomplete_review**; wrong/ambiguous baseline → Residual risks |

---

## 4. Closeout finding class

**Workflow:** 5.3.10 (optional appendix only)

Run peer closeout scripts only when the operator asks OR `**Plan build:** complete` IS present. Closeout answers *"is bookkeeping correct?"* Success review answers *"did execution meet Aims and related criteria?"*

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Execution** | Affects whether claimed work happened | Missing deliverable; premature `**Plan build:** complete` while success dims fail | May raise overall to **fail** / **warn** |
| **Authoring** | About plan shape / gates, not executed success | `missing_verify`; `missing_final_validation`; YAML closeout-gate shape | Appendix / Residual only; do **NOT** force Overall **fail** alone |
| **Informational** | Context only | Registry attribution; skip when script N/A | Note briefly |

IF unsure whether a closeout code means "work missing" vs "plan never had that gate", THEN prefer **Authoring** AND state the ambiguity IN Residual risks.

---

## 5. Success dimensions

**Workflow:** 5.3.3–5.3.7

Mark each dimension **pass** / **warn** / **fail** / **n/a** for the review scope.

| Dimension | Pass when | Fail when | n/a when |
|-----------|-----------|-----------|----------|
| **Aims** | In-scope Aim **Result** rows met on disk/diff | Aim Result unmet despite files or YAML ([§15](#15-specified-but-undone)) | No Aims section / no in-scope rows |
| **Target shape** | End-state matches §4 narrative/layout | Clear mismatch to Target shape | Section `None.` or absent |
| **Scope** | In-scope covered; no material out-of-scope drift | Required in-scope missing OR significant drift | Empty Scope (rare) — warn preferred |
| **Stop-if** | No stop-if met-and-ignored; no workaround past halt | Stop-if ignored or worked around | No Stop-if gates |
| **Rules / §9** | Plan Rules + §9 + bounded workspace rules honored by work | Clear violation IN diff/files | §9 `None.` AND no applicable workspace rules |

A/M/R inventory gaps feed Scope and todo correctness; they do not alone replace Aims judgment. Apply [§15](#15-specified-but-undone) when plan text names a deliverable or check.

---

## 6. Per-todo verdict

**Workflow:** 5.3.8

Judge **correctness** for that todo against its Aim Result row (IF any) and Stages Key actions / Definition of done — not YAML alone. Do **NOT** paste the whole-plan Aims dimension verdict onto every todo row; each todo needs its own judgment ([§15](#15-specified-but-undone)).

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **pass** | Correctly done | Disk/diff supports Aim Result + Key actions for that todo | That todo |
| **warn** | Soft gap only | Ambiguous outcome; blocked check; partial-but-usable; cancelled with documented reason | That todo |
| **fail** | Incorrect or unmet | Specified-but-undone ([§15](#15-specified-but-undone)); claimed complete but Aim Result unmet; wrong change; decision/stop-if violated | That todo |
| **blocked** | Could not check | Ambiguous path; no git; missing baseline | That todo |
| **n/a** | No claim to audit | Todo NOT IN scope; pending with no completion claim | That todo |

---

## 7. Workspace rules

**Workflow:** 5.3.7

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Plan Rules + §9** | Always check | Always (skip §9 IF `None.`) | Rules dimension |
| **Bounded workspace** | Always-on / project rules that apply to touched paths or Scope | Path/glob / Scope names clearly match | Rules dimension |
| **Skip broad profile** | Do not audit whole `~/.cursor/rules` | Default | Do NOT fail for unrelated always-on rules |

---

## 8. Bugbot gate

**Workflow:** 5.3.9

| Signal | Action |
|--------|--------|
| Operator `bugbot=off` / `skip-bugbot` | Skip — record operator skip; Bugs **n/a** |
| Operator `bugbot=on` / `run-bugbot` | Run — overrides LOC default |
| No signal; `code_loc` ∈ [1, 5000] | Run (default on) |
| No signal; `code_loc` > 5000 | Skip (default off) — record LOC; Bugs **n/a** |
| No code IN diff (`code_loc` = 0) | Skip — record no code; Bugs **n/a** |

**Code LOC:** added+removed lines on code paths only (`.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.go`, `.rs`, `.java`, `.c`/`.cpp`/`.h`, `.cs`, `.rb`, `.php`, program shell). Not code: `.md`, plans, lockfiles, generated junk.

When run — Task `bugbot`, `run_in_background: false`, prompt:

```text
Full Repository Path: <workspace root under review>
Diff: uncommitted changes
Custom Instructions: Review code changes only. Ignore markdown, plan files, and documentation-only edits. Report defects in program source.
```

Use `Diff: branch changes` when review IS clearly branch-wide. Do NOT pre-compute Bugbot's diff beyond the LOC gate.

Spawn failure when gated on → **incomplete_review** / warn — NOT Bugs **pass**.

---

## 9. Security Review

**Workflow:** 5.3.9

Independent of Bugbot.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Run** | Task `security-review`, same shape as Bugbot (code-focused Custom Instructions) | Diff touches auth, secrets, network, or external writes | Subagent findings |
| **Skip** | Record reason | None of those surfaces touched | Security **n/a** |

Spawn failure when required → incomplete_review/warn — not Security pass.

---

## 10. Failure why and action

**Workflow:** 5.3.10

For every fail or warn — assign a sequential **F-id** (F1, F2, …):

| Field | Required content |
|-------|------------------|
| **ID** | F1, F2, … — stable for operator reply |
| **Source** | Success dim, todo id, or subagent |
| **Severity** | **fail** or **warn** |
| **Why** | Root cause: criterion → workspace outcome → why verdict (not a lone path/snippet) |
| **Action needed?** | **yes** / **no** |
| **Next step** | IF yes: recommended remediation (re-open todo, fix path, re-run build/closeout) — do NOT execute IN this skill |

Per-todo fail/warn rows MUST cite the matching Failure ID.

---

## 11. Better-than-start

**Workflow:** 5.3.10

Compares workspace **since the git baseline** ([§3](#3-git-baseline)) — progress and non-regression. Do **NOT** re-judge Aims, Target shape, Scope, Stop-if, Rules, todos, Bugbot, or Security here; those dims already own their verdicts. Better does **not** copy Aims pass/fail.

| Verdict | When |
|---------|------|
| **pass** | Usable baseline (operator `--base` or merge-base `main`/`master`); since baseline, in-scope claimed paths are not worse than at baseline (no unexplained loss/break of in-scope deliverables that existed at baseline); AND when A/M/R or Stages claimed file work, the diff since baseline is non-empty on relevant paths |
| **warn** | Baseline ambiguous (HEAD+WT only, or merge-base unclear) OR empty/near-empty diff when the plan claimed file changes OR soft regression signals (unclear whether worse) |
| **fail** | Clear regression vs baseline on in-scope paths (e.g. required deliverable present at baseline now missing/broken without Removals; in-scope artifact clearly worse) |
| **n/a** | No git repo OR baseline blocked ([§3](#3-git-baseline) Blocked) |

**Not Better's job:** Aim Result rows (Aims dim); end-state narrative (Target shape); unplanned drift (Scope); halt honesty (Stop-if); Bugbot/Security findings (subagents / Overall).

---

## 12. Overall verdict

**Workflow:** 5.3.10

| Overall | When |
|---------|------|
| **pass** | All success dims pass/n/a; no fail-severity findings |
| **pass_with_warnings** | No fails; one or more warns |
| **fail** | Fail on Aims, Target shape (IF applicable), Scope, Stop-if, Rules/§9, todo correctness, Better, or Bugbot/Security when run |
| **incomplete_review** | Missing git, blocked baseline, or gated-on Task failed before findings |

Authoring-class closeout alone does **NOT** force **fail**. Skipped Bugbot = **n/a**.

---

## 13. A/M/R inventory severity

**Workflow:** 5.3.2

Inventory script emits statuses only — NOT verdicts. Agent severity after disk/diff judgment ([§15](#15-specified-but-undone)):

| Signal | Severity | Notes |
|--------|----------|-------|
| Claimed path **missing** when Aim/Stages/A/M/R required it | **fail** | Specified-but-undone |
| Claimed path **missing** when only loosely referenced | **warn** | Tie to Scope |
| **wrong_change_type** when plan named change type | **fail** | e.g. modified when Removals claimed delete |
| **wrong_change_type** minor / unclear | **warn** | Agent reads file |
| **unplanned** path | **warn** (minor drift) or **fail** (large/out-of-scope) | Tie to Scope dimension |
| **inventory_incomplete** | **warn** | Abbreviated A/M/R table |
| Content/Change/Reason mismatch | Agent judgment after reading files | Script does not judge prose columns |

One inventory gap → one primary dim (usually Scope **or** the affected todo). Do not fail both Scope and that todo for the same path without distinct reasons.

---

## 14. Plan-edit severity

**Workflow:** residual / Rules integrity

During build, only frontmatter todo `status:` lines should change. Inspect `git diff` on the plan file when relevant.

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **pass** | No unexpected plan body edits | Diff limited to expected `status:` updates | Integrity |
| **warn** | Minor non-substance edits | Timestamp or `**Plan build:**` line only | Finding severity |
| **fail** | Unauthorized substance change | Decisions, todo wording, or structure changed without user approval | Finding severity |

---

## 15. Specified-but-undone

**Workflow:** 5.3.3–5.3.8

When the plan **names** a requirement and execution does not show it on disk/diff, verdict IS **fail** — not **warn**.

| Plan names | Workspace shows | YAML `status:` | Verdict |
|------------|-----------------|----------------|---------|
| Aim **Result** row | Result unmet | completed | **fail** |
| Stages **Key actions** / **Definition of done** | Action/DoD absent or wrong | completed | **fail** |
| A/M/R path + Content/Change claim | Path missing or wrong change type | (any) | **fail** when Aim/Stages tied |
| Same, loosely referenced | Gap unclear | completed | **warn** or **blocked** |

**warn** only when: outcome ambiguous; check **blocked** (no git, secret-gated command); partial-but-usable with documented operator skip; or cancelled with reason IN plan/chat.

**Not specified-but-undone:** polish gaps; inventory abbreviate; minor unplanned drift — those stay **warn** per §5/§13.

Do NOT mark **pass** because a file exists when Aim Result or DoD text is unmet (see EXAMPLES Example 2).
