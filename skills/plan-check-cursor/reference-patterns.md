# Plan patterns reference

Concrete templates for the elements checked by `reference-checklist.md`.
Copy and adapt; do not paste verbatim.

## Sequential-execution directive

Add to the plan's execution contract or `overview` section. Without this, Build
agents may treat the todo list as read-only context and skip marking items complete.

```markdown
**Execution rule**: Execute one todo at a time. Mark it complete before starting
the next. Do not batch, skip, or reorder unless the plan explicitly marks steps
as parallel-safe. If interrupted, resume from the first incomplete todo; do not
redo completed work unless the diff shows it is wrong.
```

## Implement + verify pair

**Bad** — single todo with no verification (agent assumes success):

```markdown
- id: add-config
  content: Add configuration file and validate it loads correctly
```

**Good** — split into implement then verify:

```markdown
- id: add-config
  content: Write config/settings.yaml with the required fields

- id: verify-config
  content: Run `python -c "import config; config.load()"` and confirm no errors
```

## Completion audit (final todo)

Always the last todo. Prevents early "done" reports when earlier todos were skipped.

```markdown
- id: completion-audit
  content: >
    Confirm all N todos above are marked done. Run the validation commands in the
    definition of done. Do not report success until every todo is ticked and every
    validation passes.
```

## Stop-if gate

Insert immediately before any step the agent must not guess.

```markdown
**Stop-if**: If the licence is not MIT or Apache-2.0, stop and ask before proceeding.
Do not infer or assume a licence.
```

## Short example annotation on an ambiguous todo

**Without example** (ambiguous — which layer? which file?):

```markdown
- id: update-schema
  content: Relax the required field constraint on user.email
```

**With example** (unambiguous):

```markdown
- id: update-schema
  content: >
    Relax the `required` constraint on `user.email` in the schema file only.
    Example: change `required: [email]` → `required: []` in user.schema.json.
    Do not change the API validation layer.
```

## Parallel-safe annotation

Use when two todos can run in either order or concurrently.

```markdown
- id: scaffold-frontend
  content: Create src/components/ directory structure (parallel-safe with scaffold-backend)

- id: scaffold-backend
  content: Create src/api/ directory structure (parallel-safe with scaffold-frontend)
```
