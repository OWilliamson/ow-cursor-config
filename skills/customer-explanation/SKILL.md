---
name: customer-explanation
description: >-
  Drafts concise, accurate customer-facing text for a technical product user,
  from internal context the user will relay. Use when the user invokes
  @customer-explanation or asks for a customer explanation, client reply,
  external summary, capability description, or how-to without internal links or
  gap-focused language.
disable-model-invocation: true
---

# Customer-facing explanation

Explicit-only. Invoke with `@customer-explanation` or `/customer-explanation`.

## When to use

- The user needs paste-ready text for a **customer engineer or product user**.
- The user will relay the message (email, ticket, chat) — no greeting or sign-off unless requested.
- Typical tasks: **answer a question**, **describe a capability**, or **give a how-to** for a specific process.
- Internal investigation may already exist in the thread; this skill produces the **external** deliverable only.

## When not to use

- Internal engineering notes, Jira comments, or runbooks — write those without this skill.
- Full session handoff → `@chat-notation`.

## Assumptions (do not ask)

- **Audience:** customer engineer or product user — technically literate, not an ITRS insider.
- **Channel:** text the user will paste or adapt. No greeting or sign-off unless requested.
- **Length:** concise by default — accurate, not a mini manual. Honour overrides in the same message (`shorter`, `bullets only`, etc.).

## Required inputs

Ask **once** only if the thread lacks both topic and question:

- What question, capability, or process should this address?

Otherwise use thread context. Do not ask for audience, channel, or length.

## Definition of done

- **Customer-ready text** is returned — paste-ready, no internal metadata mixed in.
- Text is capability-led, accurate, and within scope of verified facts.
- Public doc links follow [reference-public-docs.md](reference-public-docs.md).
- If facts were uncertain, a **single brief line to the user** follows the draft (not inside customer text).
- No secrets, customer-identifying data, Jira keys, or internal URLs in the customer text.

## Non-goals

- Do not expose internal research, sources, or rationale in the customer text.
- Do not include roadmap, apologies, blame, or gap theatre (`known limitation`, ticket refs).
- Do not link Confluence, Jira, Slack, GitHub, or `knowledge.opsview.com`.
- Do not invent public doc URLs — omit links when no suitable page exists.
- When this skill is invoked, customer-facing output overrides engineering-first stance for the **deliverable only**; internal-first rules still apply during fact-finding.

## Workflow

### 1. Gather facts

Use thread context and internal sources if needed. Do not paste this research into the final answer.

### 2. Find public documentation

Follow [reference-public-docs.md](reference-public-docs.md): locate pages on `docs.itrsgroup.com`, pick section anchors, rewrite to `/current/` unless a version was specified, track pages for deduplication. Verify URLs resolve before linking.

### 3. Classify mode

Infer from the request — do not ask:

| Mode | Cues |
|------|------|
| **Answer** | why / can we / does it / customer question quoted |
| **Capability** | what does X do / explain feature / overview |
| **How-to** | how do I / steps / procedure / configuration |

Default to **Answer** when ambiguous.

### 4. Draft

Apply constraints below and the mode template. Weave each distinct doc page link **once** (first mention or a single closing reference — see reference).

### 5. Self-check

- [ ] Accurate to verified facts
- [ ] No internal URLs, ticket keys, repo paths, codenames, or team names
- [ ] Capability-led; limits are factual boundaries, not deficiencies
- [ ] Concise; no roadmap or blame
- [ ] Public doc rules passed ([reference-public-docs.md](reference-public-docs.md) checklist)
- [ ] Links are markdown `[text](url)` — never backticks or code blocks

## Constraints

**Include:** what the product does or how to do the task; clear unsupported behaviour when the customer might assume otherwise.

**Exclude:** internal links, engineering rationale, "we plan to", workarounds unless the customer must use one to succeed.

## Mode templates

### Answer

```markdown
[1–2 sentence direct answer]

[Optional: 2–4 bullets of supporting detail]

[Optional: **Scope** — one short line if something is not supported]
```

### Capability

```markdown
**[Feature name]** — [one-line purpose]

- [What it enables]
- [Typical use]

**Not available:** [only if the customer might reasonably expect it]
```

### How-to

```markdown
**[Task]**

**Before you start:** [only prerequisites that block success]

1. …
2. …

**Confirm:** [how to verify it worked — one line]
```

## Rewrite patterns

| Avoid | Prefer |
|-------|--------|
| Known limitation; tracked in PROJ-123 | This release does not support X. |
| We're hoping to fix… | Omit roadmap |
| Internal service Y handles… | The product … |
| Long gap analysis | One boundary line under **Scope** or **Not available** |

## Excuse → reality

| Excuse | Reality |
|--------|---------|
| "Customer should know it's a gap." | State factual boundaries only; no ticket refs or internal framing. |
| "I'll link Confluence for detail." | Public `docs.itrsgroup.com` only, or no link. |
| "Backticks make the URL stand out." | Markdown links only — backticks break clickability in many channels. |
| "I'll link the page top — close enough." | Use the section anchor when one exists. |
| "I'll repeat the doc link each step." | One link per distinct page, ever. |

## Output

Return **only the customer-ready text** unless the user asked for draft plus notes.

If facts were uncertain, add one line **after** the draft for the user (e.g. "Confirm X on Y before sending.") — never inside the customer block.

## Additional resources

- [reference-public-docs.md](reference-public-docs.md) — link rules, version URLs, deduplication, product entry points
- [examples.md](examples.md) — before/after samples per mode
