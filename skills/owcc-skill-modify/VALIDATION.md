# Validation rubric

Completion checks for `/owcc-skill-modify`. On failure, RETURN TO SKILL.md §5, resolve, THEN re-run this rubric.

## Scripted validation

None. (This package has no `scripts/`. Mechanical checks below are agent-run commands.)

### Mechanical commands (agent-run)

- Confirm target has `META.md` AND `WORKFLOW.yaml` before any modify (hard-stop runs exempt from post-edit checks).
- Confirm orientation READ order: META.md then WORKFLOW.yaml before other target files.
- Compare frontmatter `name` to folder basename (this package AND target IF edited).
- After any edit run: confirm `WORKFLOW.yaml` step ids cover target SKILL §5.3 AND `skill:` matches `name`.
- Inventory target files vs target META directory tree after edits; confirm **Updated** touched when META changed.
- Confirm no new SKILL.md link to META.md was introduced.
- Confirm no live `reference-*.md` was added.

Word-count suggestion for **this** package’s SKILL.md (authoring hygiene):

```bash
python3 -c "import re,sys; t=open('SKILL.md').read(); print(len(re.sub(r'^---\n.*?\n---\n','',t,1,re.DOTALL).split()))"
```

## Agent questions

- [ ] Target path unambiguous; no unauthorized rename?
- [ ] META.md THEN WORKFLOW.yaml READ before other target files; IF either absent, zero edits AND improve recommended?
- [ ] Change plan listed loci **before** any MODIFY?
- [ ] Only planned primary loci changed before sync?
- [ ] Alignment sweep mode matches change class ([DECISIONS §5](DECISIONS.md#5-alignment-sweep))?
- [ ] IF non-aim edits: package still fits current §1 AND §4?
- [ ] IF aim/scope edits: workflow, siblings, description, VALIDATION, RESPONSE aligned?
- [ ] After other edits: maintainer sync RUN ([DECISIONS §7](DECISIONS.md#7-maintainer-sync)) — WORKFLOW mirrors §5.3 AND META tree/References/Updated correct?
- [ ] Chat OUTPUT matches [RESPONSE.md](RESPONSE.md) (complete OR hard-stop)?
- [ ] This package still has §1–7 spine AND required siblings when self-checked?

## Interrogation agent

None by default. IF operator requests a subagent audit, THEN scope it to: plan-vs-diff, META gate, AND alignment sweep only.

## Authoring norms (CS-*)

This skill does **not** own the CS-* table. For full package-shape audits of a target, prefer `/owcc-skill-validate` (reads improve VALIDATION). Modify runs still enforce the checks below as Critical for this workflow:

| Norm ID | Check | Severity |
|---------|-------|----------|
| `CS-NAME-FOLDER` | Target `name` matches folder (IF frontmatter touched) | Critical |
| `CS-DESC-WORKFLOW-SUMMARY` | description stays trigger-only IF description edited | Critical |
| `CS-DESC-BODY-ALIGN` | description matches body IF either changed | Critical |
| `CS-PKG-REFS-EXIST` | SKILL links resolve IN package OR META Reference To | Critical |
| `CS-PKG-WORKFLOW-SYNC` | WORKFLOW.yaml mirrors §5.3 after edit runs (maintainer sync) | Critical |
| `CS-PKG-SKILL-SPINE` | Do not destroy §1–7 numbering | Critical |
| `CS-PKG-NO-META-LINK` | SKILL.md must not link META.md | Critical |
| `MOD-META-FIRST` | META THEN WORKFLOW READ before other target files; either absent ⇒ no edits | Critical |
| `MOD-PLAN-BEFORE-EDIT` | Change plan exists before first MODIFY | Critical |
| `MOD-ALIGN-SWEEP` | Alignment sweep RUN for the change class | Critical |
| `MOD-MAINTAINER-SYNC` | After other edits, META.md AND WORKFLOW.yaml updated or verified no-op | Critical |

### Reporting rules

- Severity: Critical, Suggestion, or Nice to have.
- Mark unconfirmed findings speculative.
- Cap detailed findings; list remaining IDs IF many.
- Hard-stop runs: pass WHEN zero edits AND stop template used — do not fail for skipping post-edit alignment.
