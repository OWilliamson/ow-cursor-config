---
name: script-review
description: >-
  Performs a structured review of scripts and small tooling code (shell, Python CLIs, checks, CI glue)
  covering errors, best practices, redundancy, function design, structure, efficiency, documentation,
  error handling, debug info, and a final sanity check. Use when the user asks for a script review,
  check plugin review, or review checklist in this style.
disable-model-invocation: true
---

# Script and tooling code review

## When to use

- User asks for a script review, check plugin review, or code review in this style.
- Target is a shell script, Python CLI, CI glue, or small tooling module.

## Required inputs

- **Target**: file path(s) or pasted script content to review.

## Definition of done

- All 12 rubric sections from [reference-rubric.md](reference-rubric.md) addressed in order.
- Each finding includes file/line reference and a concrete suggestion.
- Sections with nothing to report state so briefly.

## Non-goals

- Do not modify the target script.
- Do not perform a security audit beyond the rubric's scope.

When the user asks for a review of a script or small tooling module, use the **12-section rubric** in [reference-rubric.md](reference-rubric.md). Work through it in order and report findings under the same numbered headings.

## Output format

For each section:

- State what was checked.
- List specific findings (file/line or function name when helpful).
- Give concrete, actionable suggestions where applicable.
- Where useful, label findings as **Critical** / **Suggestion** / **Nice to have** (Critical: must fix; Suggestion: should consider; Nice to have: optional).

Keep the review focused: only mention items that are relevant; if a section has nothing to report, say so briefly (e.g. “No issues found” or “N/A for this script”).

**Example (one section):**

### 3. Redundant code

- **Finding:** Lines 45–52 and 78–85 both parse the same CSV format.
- **Suggestion:** Extract a `parse_csv_config()` function and call it from both places.
- *(If using severity: Suggestion)*
