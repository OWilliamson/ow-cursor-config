# Validation-report decisions

Enumerated decisions for `/owcc-plan-validation-report`, in **[SKILL.md](SKILL.md)** workflow order. Artifact contract: [OUTPUTS.md](OUTPUTS.md). Rubric: [VALIDATION.md](VALIDATION.md).

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Target plan](#1-target-plan) | 5.3.1 |
| 2 | [Sizing flag](#2-sizing-flag) | 5.3.1 |
| 3 | [Pass/fail semantics](#3-pass-fail-semantics) | 5.3.2 |

---

## 1. Target plan

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Use given path or paste** | Validate that plan | User `@` tags a file, gives path, or pastes content | That file (prefer saved path for scripts) |
| **Session native plan** | Validate `.plan.md` saved this session | Cursor native plan created in chat | Path once saved |
| **Open file in IDE** | Use the file the user means | “Validate this plan”, file open, chat subject matches | That path IF unambiguous |
| **Chat default** | Most recently discussed plan in this chat | `/owcc-plan-validation-report` only, no path | Paths, `@`, or edits cited in this thread |
| **Ambiguous / none** | Ask once | Two+ candidates or none | Do NOT guess |

**Do not use:** IDE Recently viewed unrelated to this chat; arbitrary latest plan file without chat linkage.

---

## 2. Sizing flag

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **lean** | Pass `--sizing lean` (script default) | Default; user omitted sizing | Write script |
| **full** | Pass `--sizing full` | User said `full` on invoke line | Write script |
| **auto** | Pass `--sizing auto` | User said `auto` on invoke line | Write script |

Sizing affects how internal checks interpret lean/full shape expectations. It does **not** edit the plan.

---

## 3. Pass/fail semantics

**Workflow:** 5.3.2

| Signal | Meaning | Agent action |
|--------|---------|--------------|
| Exit `0` + `result: pass` | Qualitative errors = 0 AND structure pass | OUTPUT pass line |
| Exit `1` + `result: fail` | One or more error-severity qualitative or structure failures | OUTPUT fail line; do NOT edit plan |
| Exit `2` | Runtime / I/O error | OUTPUT error; do NOT invent a report |
| Chunk advisory only | Never fails validation | Ignored for pass/fail; may appear IN JSON `chunk_advisory` |

**Build gate (non-cursor-native only):** When the plan path does **not** end with `.plan.md`, build preflight expects `result: pass`, matching `plan` path, `schema: 1`, and fresh `issued_at`. Cursor-native `.plan.md` skips this artifact.
