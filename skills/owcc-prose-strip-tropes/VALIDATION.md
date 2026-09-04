# Validation rubric

Completion checks for `/owcc-prose-strip-tropes`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

None bundled in this package. Confirm [WORKFLOW.yaml](WORKFLOW.yaml) mirrors SKILL §5.3 when steps change.

## Agent questions

- [ ] Target unambiguous ([DECISIONS §1](DECISIONS.md#1-target))?
- [ ] Mode decided ([DECISIONS §2](DECISIONS.md#2-mode))?
- [ ] Preserve regions mapped and left intact ([DECISIONS §3](DECISIONS.md#3-preserve))?
- [ ] All check categories C1–C15 considered ([DECISIONS §4](DECISIONS.md#4-check-categories)), with overlay READ IF the workspace file exists?
- [ ] Findings use cluster scoring ([DECISIONS §5](DECISIONS.md#5-severity)) — isolated seeds are `note`, not `must-fix`?
- [ ] Rewrite limits honored — no telegram, no invented claims or soul, in-artefact facts only ([DECISIONS §6](DECISIONS.md#6-rewrite-limits))?
- [ ] IF mode IS rewrite, residue rescan (5.3.6) ran?
- [ ] Chat matches [RESPONSE.md](RESPONSE.md) AND does not accuse authorship?
- [ ] `WORKFLOW.yaml` present; `skill: owcc-prose-strip-tropes`; step ids cover SKILL §5.3?

## Interrogation agent

None by default. Optional second pass: read-only on rewritten text only, IF operator requests.

## Authoring norms (this package)

| Norm ID | Check | Severity default |
|---------|-------|------------------|
| `PDA-WORKFLOW-SYNC` | `WORKFLOW.yaml` present; mirrors SKILL §5.3; `skill` matches `name` | Critical |
| `PDA-PRESERVE` | Code, links, facts, templates, intentional vocabulary unchanged | Critical |
| `PDA-NO-TELEGRAM` | Rewrite does not strip articles/connectives for terseness | Critical |
| `PDA-NO-INVENT` | No new claims, examples, or “soul” the source lacked | Critical |
| `PDA-CATEGORIES` | All C1–C15 considered (explicit `none` IF clean) | Critical |
| `PDA-CLUSTER` | Isolated C13/punctuation hits are `note` unless high-precision or stacked | Critical |
| `PDA-MODE` | Audit does not MODIFY; rewrite applies must-fix/should-fix per limits | Critical |
| `PDA-RESCAN` | Rewrite mode ran 5.3.6 residue pass | Critical |
| `PDA-NO-AUTHORSHIP` | Findings do not claim the text was written by a model | Suggestion |
| `PDA-NO-SKILL-ROUTE` | Chat does not name other skills | Suggestion |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
