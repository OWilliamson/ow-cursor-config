# Completion response

Chat/session output when `/owcc-plan-improve` finishes. Cited from SKILL.md §7.

## Template

```markdown
## Plan improve — complete

**Target:** <absolute path to plan>
**Scope:** full | todos-only | body-only
**Sizing:** lean | full (source: lean|full|auto→…)
**Class:** buildable-lean | buildable-full | orchestrator | doc-only

### Edits
- …

### Relocations
- <inventory item> → <section> (or “none”)

### Script findings
- chunk: …
- qualitative: pass|fail — …
- structure: pass|fail — …

### Blockers / fidelity
- … (or “none”)
```

## Sections

### Edits

#### Use

Always when the plan changed.

#### Empty Allowance

No IF any edit occurred — list material changes.

### Relocations

#### Use

When inventory items moved section ([DECISIONS §18](DECISIONS.md#18-fidelity-gate)).

#### Empty Allowance

Yes — write `none`.

### Script findings

#### Use

Always after §5.3.5 (or note skipped for empty new skeleton).

#### Empty Allowance

No — state pass/fail or “not run yet”.

### Blockers / fidelity

#### Use

Always.

#### Empty Allowance

No — write `none` explicitly IF empty.

## Section Contract

### Content

- Absolute plan path, edit scope, sizing mode (and auto source), plan class.
- Material edits and section relocations.
- Chunk / qualitative / structure results (JSON-derived; no report-file write).
- Remaining fidelity blockers.

### Authoring

- Concise operator chat; do NOT dump full script JSON unless debugging.
- Do NOT claim behavioural effectiveness without a fresh-session pressure test.
- Do NOT suggest unrelated skills IN the delta.
