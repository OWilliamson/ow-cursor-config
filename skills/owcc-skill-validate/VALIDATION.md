# Validation rubric

Completion checks for `/owcc-skill-validate`. This file is **not** a second CS-* copy.

**Norms source of truth:** [../owcc-skill-improve/VALIDATION.md](../owcc-skill-improve/VALIDATION.md)

On failure of **this skill’s process**, re-READ SKILL.md §5, resolve, re-check. On CS-* findings against the **target**: report AND stop — do **not** mutate the target and do **not** enter `/owcc-skill-improve` §5.

## Scripted validation

None bundled. RUN mechanical commands from improve VALIDATION.md against the target directory.

## Local overrides

1. **Failure handling:** Report findings; do NOT RETURN TO improve §5 to fix; do NOT WRITE/MODIFY/DELETE/ARCHIVE the target.
2. **Shape policy:** Always enforce new shape as Critical ([DECISIONS §2](DECISIONS.md#2-shape-policy)).
3. **Agent questions:** RUN improve questions for structure, CS-*, META References, WORKFLOW sync. SKIP fidelity-gate / improve-RESPONSE-ready / self-improve dual-target ([DECISIONS §3](DECISIONS.md#3-agent-question-filter)).
4. **Peer links:** This skill’s SKILL.md may cite `../owcc-skill-improve/VALIDATION.md`; that path MUST appear under META References → Reference To (`CS-PKG-REFS-EXIST` peer allowlist).

## Agent questions (this package / run)

- [ ] Target path unambiguous?
- [ ] Inventory complete?
- [ ] Improve VALIDATION.md READ and applied to target?
- [ ] Shape norms Critical-enforced (no legacy waiver)?
- [ ] Improve-only questions skipped per filter?
- [ ] Chat OUTPUT ready per [RESPONSE.md](RESPONSE.md)?
- [ ] Target untouched (no mutation)?

## Interrogation agent

None by default. IF operator requests, THEN read-only subagent: inventory + Critical CS-* only.
