# Skill package

Contract for the structured skill package this skill produces when improving a target. After improve, only the roles below are allowed. Legacy `reference-*.md` and old unnumbered spines are migrate targets, not final roles.

| Role | Required | Purpose | SKILL may link? |
|------|----------|---------|-----------------|
| `SKILL.md` | Yes | Master definition + workflow (§1–7) | n/a |
| `DECISIONS.md` | IF branching / judgment / decision matrices help | Enumerated decision tables | Yes |
| `RESPONSE.md` | Yes | Chat/session completion template + contract | Yes (§7) |
| `OUTPUTS.md` | IF file/package/structured artifact output | File template(s) + section contracts | Yes |
| `VALIDATION.md` | Yes | Completion rubric | Yes (§6) |
| `META.md` | Yes | Maintainer meta | **No** |
| `EXAMPLES.md` | No | Sparse worked examples | Yes, sparingly |
| `WORKFLOW.yaml` | Yes | Machine-structured workflow (§5.3 mirror) | Only from §6 |
| `scripts/` | IF present | Agent- or human-run helpers | Yes when executed |

---

# SKILL.md

## Template

```markdown
---
name: <kebab-case-name>
description: >-
  <Trigger-only: what and when. Use when …>
disable-model-invocation: true
---

# 1. <Skill display name>

<Aim: one short paragraph.>

## 2. When to use

- …

## 3. Inputs

| Signal | How to act |
|--------|------------|
| … | … |

## 4. Scope

**In scope:** …
**Out of scope:** …

## 5. Workflow

### 5.1. Workflow Operators

These operator words mark specific operations in the workflow. When used as operators, they must be capitalised. When used for ordinary meaning (not as an operator), they must be lower case.

| Operator | Meaning | Example |
|----------|---------|---------|
| IF | … | … |
| … | … | … |

### 5.2. Workflow Rules

- …

### 5.3. Workflow Steps

#### 5.3.1. <Step title>

1. …
**Outcome:** …
```

## Sections

### Frontmatter

#### Use

Always.

#### Empty Allowance

No.

### `# 1. <Skill display name>`

#### Use

Always. Heading is the skill display name.

#### Empty Allowance

No.

### `## 2. When to use`

#### Use

Always.

#### Empty Allowance

No.

### `## 3. Inputs`

#### Use

Always.

#### Empty Allowance

No.

### `## 4. Scope`

#### Use

Always.

#### Empty Allowance

No.

### `## 5. Workflow`

#### Use

Always. Body only under 5.1, 5.2, and 5.3.

#### Empty Allowance

No.

### `### 5.1. Workflow Operators`

#### Use

Always.

#### Empty Allowance

No.

### `### 5.2. Workflow Rules`

#### Use

Always.

#### Empty Allowance

No.

### `### 5.3. Workflow Steps`

#### Use

Always.

#### Empty Allowance

No.

### `## 6. Validation`

#### Use

Always.

#### Empty Allowance

No.

### `## 7. Completion`

#### Use

Always.

#### Empty Allowance

No.

## Section Contract

### Content

- Frontmatter: `name` matches folder; trigger-only `description`; `disable-model-invocation` set intentionally.
- §1: aim only — not workflow summary.
- §2: operator invoke situations.
- §3: table of message signals → how to act.
- §4: in-scope areas/actions and out-of-scope (absorb former non-goals).
- §5.1: operator word table (Operator | Meaning | Example); capitalise only when used as operators.
- §5.2: rules for all steps (order, Outcome check, stay in §4, READ linked docs, apply §5.1).
- §5.3: multilevel enumerated steps (`5.3.1.`, `5.3.1.1.`, …); §5.1 operators; **Outcome:** per step; DECIDE links to DECISIONS when branching.
- §6: final validation actions (scripted / agent questions / interrogation); on failure RETURN TO §5.
- §7: where/how to OUTPUT results; point to RESPONSE.md.

### Authoring

- Define operators in §5.1; capitalise them only when used as operators in step bodies; lower case for ordinary meaning.
- Keep SKILL procedural; deep policy in sibling files one hop away (DECISIONS may point to OUTPUTS/VALIDATION).
- Do NOT link META.md from SKILL.md.
- Do NOT summarize workflow steps in `description`.

---

# DECISIONS.md

## Template

```markdown
# Improve-run decisions

Enumerated decisions IN **[SKILL.md](SKILL.md)** workflow order.

## Index

| # | Decision | Workflow step |
|---|----------|---------------|
| 1 | [Title](#1-title) | 5.3.x … |

## 1. Title

**Workflow:** 5.3.x

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **A** | … | … | … |
```

## Sections

### Index

#### Use

When DECISIONS.md EXISTS.

#### Empty Allowance

No.

### Numbered decision sections

#### Use

One section per judgment call the workflow can hit.

#### Empty Allowance

No empty decision sections; omit unused decisions.

## Section Contract

### Content

- Tables with columns: Option | Description | Choose when | Apply to.
- Decisions ordered by first appearance IN §5.3.
- Each section states **Workflow:** step id.

### Authoring

- Prefer DECIDE links from SKILL over inlining matrices.
- Do NOT duplicate SECTIONS/OUTPUTS contracts here — only branching.

---

# RESPONSE.md

## Template

```markdown
# Completion response

## Template

\`\`\`markdown
## Skill improve — complete

**Target:** <path>
**Scope:** <full | siblings-only | SKILL-only>

### Capabilities and usage
- What the rewritten skill does now:
- When to use it:
- Required inputs:
- Out of scope:

### Package inventory
| File | Role | Action taken | Rationale |
|------|------|--------------|-----------|
| SKILL.md | Entry | | |

### Edit summary
- File:
- What changed:
- Why:

### Before/after pair(s)
### Residual risks
- …
\`\`\`

## Sections
…

## Section Contract
…
```

## Sections

### Chat response shape

#### Use

Always — §7 Completion OUTPUT.

#### Empty Allowance

No.

## Section Contract

### Content

- Target path and scope.
- Capabilities/usage after rewrite.
- Package inventory table (file, role, action, rationale).
- Edit summary and at least one before/after when substance moved.
- Residual risks (including validate-skill norms drift IF relevant).

### Authoring

- Operator-facing; concise; no second copy of VALIDATION findings dump unless blockers remain.

---

# OUTPUTS.md

## Template

```markdown
# <Primary output name>

## Template
\`\`\`…\`\`\`

## Sections
### <Section>
#### Use
#### Empty Allowance

## Section Contract
### Content
### Authoring

# <Second file type>   <!-- IF multiple outputs -->
…
```

## Sections

### Per output file (H1)

#### Use

IF the skill produces file/package/structured artifacts.

#### Empty Allowance

File absent IF skill IS chat-only AND NOT package-shaped; ELSE required for package-improving skills.

## Section Contract

### Content

- H1 = output file name or type.
- Template (H2) with codeblock shape.
- Sections (H2) with Use / Empty Allowance.
- Section Contract with Content + Authoring.

### Authoring

- One H1 per distinct output file type when multiple.
- Contracts must be actionable; no orphan prose.

---

# VALIDATION.md

## Template

```markdown
# Validation rubric

## Scripted validation
- …

## Agent questions
- [ ] …

## Interrogation agent
- …

## Authoring norms (CS-*)
| Norm ID | Check | Severity |
|---------|-------|----------|
```

## Sections

### Scripted validation

#### Use

IF scripts or mechanical commands exist.

#### Empty Allowance

Yes — write `None.` IF no bundled scripts.

### Agent questions

#### Use

Always.

#### Empty Allowance

No.

### Interrogation agent

#### Use

IF a subagent should audit results.

#### Empty Allowance

Yes — write `None.` or omit block.

### Authoring norms

#### Use

For skill-authoring skills; package-shape + CS-* checks.

#### Empty Allowance

No for this improve skill.

## Section Contract

### Content

- Pass/fail checks preferred over advice.
- Include package-shape: required siblings; META exempt from SKILL citation; no live `reference-*`.
- CS-* table with severities.
- On failure: RETURN TO §5.

### Authoring

- Binary where possible; mark speculative findings explicitly.

---

# META.md

## Template

```markdown
# Meta

- **Version:** …
- **Updated:** …
- **Maintainer:** …

## Directory tree
\`\`\`
skill-name/
  SKILL.md       # …
\`\`\`

## Update rules
- …

## Scripts
| Script | Workflow stage | Input type | Expected inputs | Output shape |
|--------|----------------|------------|-----------------|--------------|
| — | — | — | — | — |

## References

### Referenced From
| Skill | Relationship |
|-------|----------------|
| — | — |

### Reference To
| Skill / path | Relationship |
|--------------|----------------|
| — | — |
```

## Sections

### Identity

#### Use

Always.

#### Empty Allowance

No.

### Directory tree

#### Use

Always.

#### Empty Allowance

No.

### Update rules

#### Use

Always. MUST include: do NOT link META from SKILL.

#### Empty Allowance

No.

### Scripts table

#### Use

Always (row of em dash IF none).

#### Empty Allowance

No — table required even IF empty of scripts.

### References

#### Use

Always. Document peer skills that invoke or recommend this skill (**Referenced From**) and peer skills/paths this package cites outside itself (**Reference To**). Peer paths cited from SKILL.md MUST appear under Reference To (allowlist for `CS-PKG-REFS-EXIST`).

#### Empty Allowance

No — both tables required; use a single em-dash row IF none.

## Section Contract

### Content

- Version, update timestamp, maintainer.
- Tree with purpose comments per path.
- Update rules for maintainers.
- Scripts inventory table.
- References: Referenced From + Reference To tables (peer allowlist).

### Authoring

- Human/maintainer only. Never cited from SKILL.md (`CS-PKG-NO-ORPHANS` exemption).
- Keep Reference To IN sync when adding cross-package SKILL links; keep Referenced From IN sync when known consumers change.

---

# EXAMPLES.md

## Template

```markdown
# Examples

## Example 1: <title>
### Before
### After
```

## Sections

### Example blocks

#### Use

IF sparse worked examples help workflow judgment.

#### Empty Allowance

File may be absent; IF present, at least one example.

## Section Contract

### Content

- Before/after or concrete invoke examples only.
- Must match current §1–7 + role norms (no superseded spines).

### Authoring

- Use carefully and cleanly; prune stale examples; link from SKILL only when a step needs them.

---

# WORKFLOW.yaml

## Template

```yaml
skill: <name>
steps:
  - id: "5.3.1"
    title: …
    actions: []
    outcome: …
    decisions: []
```

## Sections

### Root document

#### Use

Always. Machine mirror of SKILL §5.3 for subagents/scripts; cite from §6 only IF a validation step needs it (do NOT cite from §5).

#### Empty Allowance

No — file required; `steps` must be non-empty and cover every top-level §5.3 step id.

## Section Contract

### Content

- `skill:` matches frontmatter `name`.
- Structured mirror of §5.3 only — no prose policy.
- Each top-level §5.3 step has a matching `id`, `title`, `outcome`; optional `actions` / `decisions` arrays.

### Authoring

- Always CREATE/KEEP when improving a target. Keep IN sync with SKILL §5.3; SKILL remains the human source of truth.
