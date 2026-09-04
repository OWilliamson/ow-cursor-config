---
name: owcc-skill-modify
description: >-
  Targeted maintenance of a Cursor skill already in the owcc-skill-improve
  package shape. Use when changing behaviour, scope, or siblings without a full
  improve rewrite; requires META.md.
disable-model-invocation: true
---

# 1. Modify Cursor skills

The aim of invoking owcc-skill-modify is to apply operator-requested changes to a skill already in the improve-skill semantic-sibling format — META + WORKFLOW orientation first, plan-before-edit, alignment, then maintainer sync of `META.md` and `WORKFLOW.yaml`.

Explicit-only. Invoke with `/owcc-skill-modify`.

## 2. When to use

- Target already has §1–7 + semantic siblings (post-`/owcc-skill-improve`).
- Focused behaviour, wording, scope, or sibling update — NOT a full rewrite.
- Maintenance when improve would over-touch the package.

## 3. Inputs

| Signal | How to act |
|--------|------------|
| Absolute path to skill directory | Target ([DECISIONS §1](DECISIONS.md#1-target-skill-directory)) |
| `@` on `SKILL.md` or skill folder | Resolve package root as target |
| Change request (what to alter) | Plan loci ([DECISIONS §3](DECISIONS.md#3-change-class)) |
| No path / ambiguous target | Ask once; do NOT guess |
| No change request | Ask once what to MODIFY; do NOT invent edits |

## 4. Scope

**In scope:** READ target `META.md` then `WORKFLOW.yaml` before other target files; gate on META; orient from META tree/rules AND WORKFLOW steps; plan loci before edits; MODIFY only planned loci; alignment sweep; always sync `WORKFLOW.yaml` AND `META.md` after other edits; OUTPUT per [RESPONSE.md](RESPONSE.md).

**Out of scope:** Full `/owcc-skill-improve` reshape; create-from-scratch; rename `name:`/folder unless asked; invent requirements; edit when `META.md` absent; leave META/WORKFLOW stale after edits; copy CS-* tables from improve; link META from SKILL.

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | Conditional test | IF META missing, THEN stop |
| THEN | Consequence of IF | IF plan clear, THEN MODIFY |
| ELSE | Alternate branch | ELSE ask once |
| AND | Conjoin requirements | plan loci AND apply |
| NOT | Negation / forbid | do NOT edit without plan |
| IS | Equality / state check | IF class IS aims-scope |
| IN | Location / membership | change IN DECISIONS.md |
| CREATE | Make a new file | CREATE sibling IF planned |
| MODIFY | Change existing content | MODIFY SKILL §4 |
| DELETE | Remove from package | DELETE only IF planned |
| RUN | Execute a check | RUN alignment sweep |
| READ | Load a document | READ META.md then WORKFLOW.yaml |
| WRITE | Produce content at a path | WRITE RESPONSE section |
| REWRITE | Replace to a new shape | prefer MODIFY |
| SKIP TO | Jump forward | SKIP TO 5.3.8 IF zero primary edits |
| RETURN TO | Go back | RETURN TO 5.3.4 IF plan incomplete |
| WHILE | Repeat while true | WHILE loci remain, apply |
| DECIDE | Choose via matrix | DECIDE class per DECISIONS §3 |
| OUTPUT | Emit completion | OUTPUT §7 |

### 5.2. Workflow Rules

- Steps top to bottom; meet each **Outcome** before continuing.
- Stay within §4; READ linked docs for the step; apply §5.1 capitalisation only as operators.
- READ target `META.md` then `WORKFLOW.yaml` before any other target file; IF META absent, THEN stop with zero edits.
- Do NOT MODIFY until the plan lists each locus (file + section/role).
- After primary edits: RUN alignment ([DECISIONS §5](DECISIONS.md#5-alignment-sweep)), THEN maintainer sync ([DECISIONS §7](DECISIONS.md#7-maintainer-sync)).
- Prefer surgical MODIFY; defer reshape to `/owcc-skill-improve`.
- Do NOT link META.md from SKILL (this package or target).

| Excuse | Reality |
|--------|---------|
| “Skip META — I know the layout.” | META mandatory; IF missing, stop AND recommend improve. |
| “Skip WORKFLOW — steps are in SKILL.” | READ WORKFLOW with META; keep it synced after edits. |
| “Small tweak — no plan.” | Every edit needs a locus IN the plan first. |
| “Aims changed — siblings later.” | Aims/scope changes need whole-package alignment. |
| “Body drifted — ignore §1/§4.” | Non-aim edits must still fit current aim AND scope. |
| “META/WORKFLOW can wait.” | After other edits, sync both before claiming done. |

### 5.3. Workflow Steps

#### 5.3.1. Resolve target

1. DECIDE target per [DECISIONS §1](DECISIONS.md#1-target-skill-directory).
2. Confirm `SKILL.md` EXISTS at package root.

**Outcome:** Absolute path to target skill directory.

#### 5.3.2. META + WORKFLOW gate

1. READ target `META.md` **before** any other target file.
2. DECIDE gate per [DECISIONS §2](DECISIONS.md#2-meta-gate).
3. IF META.md IS absent OR unreadable, THEN OUTPUT hard-stop per [RESPONSE.md](RESPONSE.md) (recommend `/owcc-skill-improve`) with **no** edits AND stop.
4. ELSE extract directory tree, update rules, scripts table, References.
5. Immediately READ target `WORKFLOW.yaml` (same orientation pass as META).
6. IF WORKFLOW.yaml IS absent OR unreadable, THEN OUTPUT hard-stop per [RESPONSE.md](RESPONSE.md) (recommend `/owcc-skill-improve`) with **no** edits AND stop.
7. ELSE note `skill:` name AND step ids/titles/outcomes for later sync.

**Outcome:** META AND WORKFLOW loaded, OR hard stop with zero edits.

#### 5.3.3. Orient from META + WORKFLOW

1. List package files; compare to META directory tree.
2. Compare WORKFLOW.yaml step ids to SKILL §5.3 (note pre-existing drift; do NOT fix until planned).
3. Note update rules (WORKFLOW sync, META tree/References, no SKILL→META, archive).
4. IF reshape needed (legacy spine, live `reference-*`, missing required siblings), THEN DECIDE [DECISIONS §6](DECISIONS.md#6-reshape-vs-modify).
5. IF reshape required, THEN OUTPUT hard-stop per [RESPONSE.md](RESPONSE.md) with **no** edits AND stop.

**Outcome:** Orientation notes; proceed, OR hard stop with zero edits.

#### 5.3.4. Build change plan

1. Parse operator input into requested changes.
2. DECIDE change class per [DECISIONS §3](DECISIONS.md#3-change-class).
3. Map each change to locus: file role + section/id (META tree + SKILL/siblings).
4. IF ambiguous, THEN DECIDE [DECISIONS §4](DECISIONS.md#4-ambiguity).
5. Do NOT edit yet.

**Outcome:** Written change plan (class, loci, exclusions).

#### 5.3.5. Apply planned edits

1. WHILE plan loci remain, MODIFY (CREATE/DELETE only IF planned).
2. Honor target META update rules for primary loci.
3. Do NOT treat maintainer sync as optional here — full META/WORKFLOW sync IS 5.3.7.
4. IF zero primary edits, THEN SKIP TO 5.3.8.

**Outcome:** Only planned primary loci changed.

#### 5.3.6. Alignment sweep

1. DECIDE sweep mode per [DECISIONS §5](DECISIONS.md#5-alignment-sweep).
2. IF non-aim/scope content changed, THEN verify package still fits current §1 AND §4; fix or RETURN TO 5.3.4.
3. IF §1 OR §4 changed, THEN verify workflow, siblings, description, VALIDATION, AND RESPONSE match; fix or RETURN TO 5.3.4.
4. IF both kinds of edit, THEN RUN both directions.

**Outcome:** Package aligned (or blockers listed).

#### 5.3.7. Maintainer sync (META + WORKFLOW)

1. After any other package edits IN this run, DECIDE sync actions per [DECISIONS §7](DECISIONS.md#7-maintainer-sync).
2. MODIFY `WORKFLOW.yaml` so it mirrors current SKILL §5.3 (`skill` name, step ids, titles, outcomes, decisions).
3. MODIFY `META.md`: directory tree, update rules IF needed, scripts table, References, **Updated** timestamp (and version IF the change warrants it).
4. Confirm META still IS NOT linked from SKILL.md.

**Outcome:** META.md AND WORKFLOW.yaml correct relative to the post-edit package.

#### 5.3.8. Validate AND complete

1. RUN §6 against the modified target (AND this package when self-modifying).
2. IF fail, THEN RETURN TO the failing step, fix, re-validate.
3. IF pass, THEN OUTPUT §7.

**Outcome:** Validation pass (or blockers) AND completion chat.

## 6. Validation

On failure, re-READ §5, resolve, re-check.

### 6.1. Scripted validation

None bundled. RUN checks IN [VALIDATION.md](VALIDATION.md). Confirm target `WORKFLOW.yaml` mirrors §5.3 AND `META.md` matches the package tree after any edit run.

### 6.2. Agent questions

Answer every [VALIDATION.md](VALIDATION.md) Agent question against this run’s target.

### 6.3. Interrogation agent

None by default. IF operator requests, THEN read-only subagent: plan-vs-diff, META+WORKFLOW gate, alignment sweep, maintainer sync only.

**Pass when:** META+WORKFLOW gate respected; plan preceded edits; alignment done; maintainer sync done after other edits; Critical checks clear or blockers reported; chat matches [RESPONSE.md](RESPONSE.md).

## 7. Completion

OUTPUT chat per [RESPONSE.md](RESPONSE.md). Do NOT claim a pressure test unless done.
