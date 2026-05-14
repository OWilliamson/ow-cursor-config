# Cursor Build operator notes

These notes are user/operator advice, not mandatory plan rules.
Keep this file for operator behavior; keep plan files focused on executable work.

## What Cursor documents

- Plan Mode researches the codebase, asks clarifying questions, creates an editable Markdown plan, then waits for approval before Build.
- Cursor recommends editing plans directly, saving useful plans to the workspace, and restarting from a refined plan if execution goes off course.
- Planning is most useful for complex, multi-file, ambiguous, or architectural work; simple changes may not need a plan.

## Practical caveats

- Build agents can treat the plan body as read-only context and skip marking todos complete. An explicit sequential-execution directive in the plan body (not only in operator prompts) significantly reduces this; see [reference-patterns.md](reference-patterns.md).
- Larger Build runs may stop before the whole plan is complete.
- Internal todos and saved plan files may not always stay in sync during or after Build.
- Re-clicking Build on an unchanged partially completed plan can confuse execution or repeat old work.
- Some users report model-selection surprises when moving from Plan to Build. If the execution model matters, verify the selected Agent model before Build, or save the plan and start a new Agent run with `@plan`.

## User-side habits that help

1. Prefer Build-sized phase plans over one large master plan.
2. Save important plans into the workspace before Build so they can be referenced later.
3. Treat the workspace plan/progress file as authoritative for resumable work; treat Cursor internal todos as a useful mirror, not the only source of truth.
4. If Build stops early, update or split the plan before continuing. Avoid pressing Build again on a stale plan.
5. If implementation goes in the wrong direction, revert, refine the plan, and rerun from the improved plan instead of steering a confused thread for many turns.
6. Use a review pass before Build for high-risk plans: run `/plan-check-cursor`, ask a stronger reasoning model to critique the plan, or manually edit the plan.
7. Put exact validation commands and stop-if gates in the plan so the agent can iterate against real signals.
8. Keep attachments thin: attach the plan and canonical files only; let Agent search for the rest.

## Suggested operator prompt after a partial Build

```text
Continue from the saved plan. First inspect the plan and current diff, then identify completed and pending todos. Resume from the first pending todo only. Do not redo completed work unless the diff shows it is incomplete. Run the validation gates named in the plan before reporting done.
```

## Suggested operator prompt before Build when model choice matters

```text
Use the currently selected Agent model to execute this saved plan. Treat the workspace plan file as the source of truth. If anything conflicts with Cursor internal todos, follow the workspace plan and ask before changing scope.
```
