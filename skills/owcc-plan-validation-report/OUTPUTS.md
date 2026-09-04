# Validation report artifact

Contract for the structured file this skill WRITEs. Chat line: [RESPONSE.md](RESPONSE.md).

## Path

```
<workspace>/.cursor/plans/reports/<plan-name>.validation.json
```

- `<workspace>` — plan workspace root (via `plan_lib.resolve_workspace_root`).
- `<plan-name>` — slugified frontmatter `name:` (fallback: plan file stem).

Created by `scripts/plan-write-validation-report.py` only. Do NOT hand-write or invent paths.

## Schema (`schema: 1`)

| Field | Type | Meaning |
|-------|------|---------|
| `schema` | number | Always `1` |
| `plan` | string | Absolute path to the validated plan |
| `issued_at` | string | UTC ISO-8601 timestamp when written |
| `skill` | string | `"owcc-plan-validation-report"` |
| `sizing` | string | `lean` \| `full` \| `auto` used for the run |
| `result` | string | `pass` \| `fail` |
| `checks` | array | `{ "id", "status" }` for `qualitative`, `structure`, `chunk` |
| `failures` | array | `{ "check", "code", "message" }` — empty when pass |
| `chunk_advisory` | array | Advisory split/merge notes; never fails alone |

## Pass rules (script)

- **Qualitative:** `error_count == 0` on hygiene findings only (empty content, UUID ids, chrome, edit-rule — **not** a second structure pass).
- **Structure:** `validate_structure` result `pass` (single structure pass via `plan-validate-structure.py`).
- **Chunk:** always recorded as `pass`; advisories only.

The write script RUNs qualitative, structure, and chunk **once each** — qualitative must not embed `validate_structure`.

## Interpretation checklist (operator / peer)

After the JSON exists, peers may use:

- Body Title H1 + §1–10 order — [owcc-plan-improve OUTPUTS.md](../owcc-plan-improve/OUTPUTS.md)
- Section profile — [owcc-plan-improve DECISIONS §10](../owcc-plan-improve/DECISIONS.md#10-section-profile-by-class)
- Fidelity / chrome strip — improve DECISIONS §18 / OUTPUTS Appendix E

This skill does NOT re-check those in chat; the write script encodes structural + qualitative gates.

## Non-outputs

- Do NOT WRITE plan file edits.
- Do NOT WRITE a six-section chat report.
- Do NOT WRITE `.validation.json` from `/owcc-plan-improve` (improve RUNs chunk/qual/structure with `--json` only).
