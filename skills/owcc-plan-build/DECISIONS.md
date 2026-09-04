# Build decisions

Enumerated decisions for `/owcc-plan-build`, in **[SKILL.md](SKILL.md)** workflow order. Rubric: [VALIDATION.md](VALIDATION.md). Examples: [EXAMPLES.md](EXAMPLES.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target and preflight](#1-target-and-preflight) | 5.3.1 |
| 2 | [Four intents](#2-four-intents) | 5.3.1 |
| 3 | [Two layers](#3-two-layers) | 5.3.3 |
| 4 | [Execution rule](#4-execution-rule) | 5.3.3 |
| 5 | [Plan file discipline](#5-plan-file-discipline) | 5.3.3–5.3.4 |
| 6 | [Conflict resolution](#6-conflict-resolution) | 5.3.3 |
| 7 | [Native Build pairing](#7-native-build-pairing) | When to use / EXAMPLES |

---

## 1. Target and preflight

**Workflow:** 5.3.1

### Target

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use given path or `@`** | Build that plan | User `@` tags a file or gives absolute/relative path | That file |
| **Session native plan** | Build the `.plan.md` saved this session | Cursor native plan created in chat | Path once saved |
| **Open file in IDE** | Use the file the user means | “Build this plan”, file open, chat subject matches | That path IF unambiguous |
| **Chat default** | Most recently discussed plan in this chat | `/owcc-plan-build` only, no path | Paths, `@`, or edits cited in this thread |
| **Ask operator** | One-line ask for path | Two+ plans in play; or none identified | Do NOT guess |

**Not valid targets:** IDE Recently viewed unrelated to chat; newest plan in workspace without chat link; older topic’s plan unless still active.

Prefer `@`-attached plan when present.

### Preflight (all intents)

**Cursor-native detection:** plan path ends with `.plan.md` (no profile/runtime detection).

| Path class | Preflight |
|------------|-----------|
| **Cursor-native** (`.plan.md`) | Skip `.validation.json`. Proceed to orient. |
| **Non-cursor-native** (any other plan path) | Require passing `.validation.json` (steps below). |

**Non-cursor-native JSON checks:**

1. Derive report path: `<workspace>/.cursor/plans/reports/<plan-name>.validation.json` where `<plan-name>` IS slugified frontmatter `name:` (fallback: plan file stem).
2. READ the JSON from disk. Parse `plan`, `result`, `issued_at`, `schema`, `failures`.
3. Require: file exists; `plan` matches attached absolute path; `result === "pass"`; `schema === 1`; `issued_at` ≥ plan file mtime.
4. On fail: stop with report path + `failures[]` — do NOT name other skills.

Artifact contract (non-cursor-native only): workspace `.cursor/plans/reports/<plan-name>.validation.json` schema `1` with `plan`, `result`, `issued_at`, `failures`.

---

## 2. Four intents

**Workflow:** 5.3.1

| Intent | When | What owcc-plan-build does |
|--------|------|----------------------|
| **Named todo** | User names a todo **id** | Match `id` IN flat `todos` or `phases[].todos`. Run **implement + verify pair** only. Update YAML `status` for those ids. Stop-if / frozen decisions before writes. |
| **Named phase** | User names a **phase** — **case-insensitive** match on `phases[].name` | All todos IN that phase only, IN listed order. IF flat (`isProject: false`), say phase does not apply. |
| **Incomplete plan** | No todo or phase named; any todo `pending` / `in_progress` | First pending IN phase order or list order. One todo at a time. |
| **Complete plan** | No todo or phase named; all todos `completed` or `cancelled` | RUN `plan-validate-close.py`, final validation, completion-audit, `**Plan build:** complete — YYYY-MM-DD`. Fix YAML only where evidence contradicts `completed`. |

**Disambiguation:** `/owcc-plan-build` with only `@plan.md` attached → choose **incomplete** vs **complete** from frontmatter + diff; state which intent IN one line.

**Scoped invoke rule:** When scope IS not whole-plan, user must name a **todo id** or **phase name**.

Decision tree: user names **todo id** → named todo; names **phase** → named phase; else all todos done → complete; else → incomplete.

---

## 3. Two layers

**Workflow:** 5.3.3

| Layer | What it is | Who updates it |
|-------|------------|----------------|
| **A. Plan file YAML** | `status:` on each todo IN frontmatter | **/owcc-plan-build** (canonical); native Build may also update when **Plan file edit rule** IS IN the plan body — `status:` only |
| **B. Session todos** | Cursor todo tool IN active Agent chat | Native Build and **/owcc-plan-build** — ids must match plan todo ids |

Cursor native Build discourages plan-file edits. Plans with **Plan file edit rule** (status-only exception — never quote the injected prohibition IN the plan body) permit YAML `status:` updates during Build. Always run `/owcc-plan-build` after native chunks to reconcile layer A.

---

## 4. Execution rule

**Workflow:** 5.3.3

**One todo at a time** within scope:

1. Layer A: `status: in_progress` (status line only).
2. Layer B: mirror id IN session todo tool when available.
3. Implement + verify per todo `content`.
4. Layer A: `status: completed` after verify passes.
5. Layer B: mirror `completed`.

Resume at **first `pending`** IN scope.

When a todo's `content` names `plan-verify-close-cursor.py`, RUN those commands and follow pass/fail rules IN the todo. Do not mark the verify todo complete until the script exits 0.

---

## 5. Plan file discipline

**Workflow:** 5.3.3–5.3.4

| Allowed | Forbidden without approval |
|---------|------------------------------|
| `status:` on todos IN scope | Plan body, todo `content`, order, new todos |
| **Plan build:** line on **complete** intent | Arbitrary prose |

---

## 6. Conflict resolution

**Workflow:** 5.3.3

| Conflict | Rule |
|----------|------|
| Plan vs user chat | User wins **scope**; plan wins **verification** unless user overrides |
| Plan file vs session todos | **Layer A** wins for resume |
| Chat memory vs YAML | Trust **plan file** + **git diff** |

---

## 7. Native Build pairing

| Plan shape | Native chunk | Then |
|------------|--------------|------|
| **Flat** (`isProject: false`) | Select **one implement + verify pair** → Build IN new agent | Reconcile YAML on disk (incomplete intent) |
| **Project** (`isProject: true`) | Select **all todos IN one phase** → Build IN new agent | Reconcile YAML for phase or whole plan |

| Layer | Native Build | owcc-plan-build governor |
|-------|--------------|---------------------|
| A — plan YAML `status` | May update when status-only edit rule present | **Canonical** — govern/sync after each chunk |
| B — composer todos | Updates | Mirrors when implementing IN owcc-plan-build |

Copy-paste `phases[].name` from YAML into native selection and named-phase build intent.
