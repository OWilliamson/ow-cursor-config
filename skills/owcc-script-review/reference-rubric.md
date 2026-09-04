# Script review — full rubric

Work through each section when reviewing; report under the same headings as in the main skill.

## 1. Potential errors and issues

- Logic bugs, off-by-one errors, wrong assumptions
- Edge cases and boundary conditions
- Invalid inputs or states that could break execution
- Security-sensitive issues: injection, secrets in code or logs, unsafe use of external input

## 2. Good practice in code

- Naming, style, and readability
- Consistency with language and project conventions
- Clear intent and minimal magic numbers/strings

## 3. Redundant code

- Duplicated logic that should be shared
- Dead code or unused variables/functions
- Overlapping or unnecessary steps

## 4. Functions that can be merged

- Small, closely related functions that do one conceptual thing together
- Call sites that always use the same sequence of functions

## 5. Functions that are doing too much and can be split

- Functions with multiple responsibilities
- Long functions or deep nesting that would be clearer as smaller units
- Single-responsibility violations

## 6. Script/code structure and overall flow

- Is the entry point and control flow clear?
- Does the order of operations make sense?
- Are dependencies and data flow easy to follow?

## 7. Running efficiency

- Unnecessary work, repeated work, or expensive operations in hot paths
- I/O, subprocesses, or network calls that could be reduced or batched
- Algorithms or data structures that could be more efficient

## 8. Code efficiency (brevity and clarity)

- Are we using too many lines for simple tasks?
- Can logic be expressed more clearly and concisely without obscuring intent?
- Avoid both unnecessary verbosity and harmful cleverness

## 9. Useful notes and helptext

- Docstrings, comments, and usage notes where they add value
- Help text (e.g. `--help`) that is accurate and helpful
- README or inline docs if the script is shared or non-obvious

## 10. Error handling and exception catching

- Try/except (or equivalent) used at every appropriate opportunity
- Failures are caught, reported clearly, and exit codes or exceptions are meaningful
- No silent swallowing of errors unless intentional and documented

## 11. Useful debug information

- Logging or debug output that would help diagnose failures
- Sensitive data not exposed in logs
- Enough context (e.g. inputs, step) to trace issues

## 12. Final sanity check

- Is every change we have **suggested in this review** a good idea?
- Do suggested fixes actually improve correctness, clarity, or maintainability?
- No unnecessary or speculative changes

## Monitoring scripts (Opsview)

When the code under review is a monitoring/check script (e.g. Nagios-compatible), also consider: is it framed for Opsview where appropriate? If there are Nagios-only references and the script is not OP5-specific, offer Opsview-oriented wording or updates.
