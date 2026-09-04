# Examples

Sparse invoke samples for `/owcc-plan-build`. Policy: [DECISIONS.md](DECISIONS.md).

## Named todo

```text
/owcc-plan-build extract-timeline @.cursor/plans/my.plan.md
```

## Named phase (`isProject: true`)

```text
/owcc-plan-build "Phase 1 — API" @.cursor/plans/my.plan.md
```

Case-insensitive match on `phases[].name`.

## Whole plan — incomplete or complete

```text
/owcc-plan-build @.cursor/plans/my.plan.md
```

- Any todo `pending` / `in_progress` → incomplete.
- All `completed` / `cancelled` → complete (then RUN `plan-validate-close.py`).

## Native Build then reconcile

1. Flat: select one implement+verify pair → Build IN new agent.
2. Project: select all todos IN one phase → Build IN new agent.
3. Then `/owcc-plan-build` + `@plan.md` to reconcile layer A.
