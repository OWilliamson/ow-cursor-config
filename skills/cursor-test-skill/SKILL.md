---
name: cursor-test-skill
description: >-
  Tests whether a Cursor skill package changes agent behaviour. Use when you
  want to verify a SKILL.md package against realistic pressure scenarios before
  treating it as effective.
disable-model-invocation: true
---

# Test Cursor skills

This skill is explicit-only. Invoke it with `/cursor-test-skill` or `@cursor-test-skill`.

## When to use

- The user wants to know whether a skill actually changes agent behaviour.
- The user has a skill package and one or more pressure scenarios to test.
- The user wants a behavioural test, not a mechanical validation pass.

## Required inputs

- **Target**: absolute path to the skill directory under test.
- **Skill type**: discipline-enforcing, technique, pattern, or reference.
- **Pressure scenario(s)**: realistic situations that should expose failure modes.

## Definition of done

- A baseline run without the skill is documented: exact agent output and any rationalizations captured verbatim.
- A second run with the skill attached is documented in the same format.
- Behaviour difference (or absence of one) is explicitly stated.
- Any loopholes the skill did not close are recorded as inputs for future improve work.
- The report is produced using `reference-report-skeleton.md`.

## Non-goals

- Do not modify the target skill.
- Do not replace validate or improve.
- Do not link this skill to validate or improve at runtime.

## Principles

0. Treat the package as the unit, not `SKILL.md` alone. List and classify every file before setting up the test.
1. Skipping the baseline run invalidates the test.
2. If the skill does not change behaviour, the package still has a gap.
3. Observed rationalizations are inputs for future improve work.

## Skill type taxonomy

| Type | Examples | Test approach |
|------|----------|---------------|
| Discipline-enforcing | always-ask-before-rename, TDD rules | Combined-pressure scenarios and rationalization checks |
| Technique | how-to workflows, step-by-step guides | Application scenarios and edge cases |
| Pattern | mental models, decision frameworks | Recognition and counter-example scenarios |
| Reference | API docs, command lists | Retrieval and correct-application scenarios |

## Package member types

Read all package members before testing. Each type affects what to load and verify.

| Type | Examples | Testing implication |
|------|----------|---------------------|
| Entry point | `SKILL.md` | Primary artefact under test; must be attached for the with-skill run |
| Reference doc | `reference-*.md`, `reference.md` | Load alongside `SKILL.md` if the workflow cites them; gaps here are gaps in the test surface |
| Template | `*-skeleton.md`, `REPORT_TEMPLATE.md` | Verify the agent produces output matching the template when instructed |
| Workflow doc | `WORKFLOW.md`, `agent-build-plan-notes.md` | Include in the test surface if cited from `SKILL.md` |
| Checklist | `CHECKLIST.md`, `reference-checklist.md` | Include in the test surface; each item is a potential failure mode |
| Script | `scripts/*.py`, `scripts/*.sh` | Note whether agent-executed or human-executed; test execute path if agent-executed |
| README | `README.md` | Human-only; not part of the test surface |

## Workflow

1. Confirm the target path, skill type, and pressure scenarios. List all files in the package directory (including `scripts/`). Classify each by type using the Package member types table. Determine the full test surface: which files must be attached for the with-skill run.
2. If anything is missing (path, skill type, or at least one pressure scenario), ask once with one consolidated question.
3. Run a baseline scenario in a fresh session without the skill attached.
4. Record exact agent choices and rationalizations verbatim.
5. Run the same scenario with the skill attached.
6. Verify behaviour differs.
7. If the skill is discipline-enforcing, run combined-pressure variants.
8. Record any loopholes or rationalizations the skill did not address.

## Output format

Use `reference-report-skeleton.md` for the report structure.

## Additional resources

- [reference-report-skeleton.md](reference-report-skeleton.md)
- [reference-examples.md](reference-examples.md)
