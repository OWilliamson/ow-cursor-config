# Delegation reference

Subagent tool results are injected into the **main thread context**. Structured, path-first output keeps parent sessions usable across many delegations.

## When to delegate

| Task | Prefer | Not |
|------|--------|-----|
| Where is X defined / what calls Y / list uses of Z | `explore` (readonly) | Main thread grep loops |
| Same + architecture commentary for a human | Main thread or `generalPurpose` | Terse contract-only explore |
| Run commands, git status, build, test (readonly sandbox OK) | `shell` | Main thread if one command |
| Surgical edit, ≤2 files, path known | Main thread | Subagent without prior locate |
| New feature / 3+ files / cross-cutting refactor | Main thread (or plan skill first) | Single builder subagent |
| Review diff or branch for bugs | `bugbot` (readonly) | Inline skim without skill |
| Security review of local changes | `security-review` (readonly) | One-line nit format |
| Deep PR review with rationale + alternatives | Main thread + `script-review` / team standards | Compressed one-liners only |
| Answer already known from open context | Main thread | Any subagent |

**Rule of thumb:** delegate when the return payload would be long prose; keep inline when the edit or answer is small and path-known.

## Output contracts

Embed the chosen block in the Task **prompt** so the subagent returns predictable shape.

### explore (locate / map)

```text
Return format:
<topic>:
- path:line — `symbol` — short note
totals: <counts>.
Or: No match.

Rules: file-path first; line numbers; backtick symbols; no essay; no tool-call narration.
```

### shell (command output)

```text
Return format:
command: `<exact command>`
exit: <code>
stdout: <decisive lines only, or "empty">
stderr: <decisive lines only, or "empty">
Or: blocked — <reason>.
```

### generalPurpose (small bounded task)

```text
Return format:
done: <one sentence>
artifacts: path — <what changed or found>
verified: <re-read OK | not verified>
Or: blocked — <reason>.
```

### bugbot / security-review

Use the built-in subagent; ask for **findings list** not a rewrite. Parent summarizes for the user.

For security-review only — **Auto-Clarity:** allow full paragraphs for CVE-class or irreversible-risk items.

## Chaining patterns

### Locate → fix → verify (common)

1. `explore` → path:line list.
2. Main thread picks 1–2 sites and edits.
3. `bugbot` or `security-review` on the diff if risk warrants.

### Parallel scout (broad unknown)

Spawn 2–3 `explore` tasks in one message (defs vs callers vs tests). Aggregate in main thread.

### Single-shot edit (site known)

Skip explore. Edit inline or hand exact `path:line` to a bounded `generalPurpose` task.

## Anti-patterns

- Delegating an edit when the file path is unknown — locate first or main thread pays token tax passing context.
- Chaining explore → edit subagent for 5+ files — subagent returns `too-big`; use main thread or a plan.
- Expecting architecture opinions from bugbot — use main thread or `generalPurpose` with explicit ask.
- Pasting subagent terse output to customers without paraphrase — rewrite in normal prose.

## Hub cross-links

| Need | Skill / doc |
|------|-------------|
| Pick any hub tool | `@cursor-tooling-help` |
| Session friction retro | `@cursor-session-retro` |
| Ephemeral handoff note | `@chat-notation` (private) |
| Compress always-on context | `@cursor-compress-context` |

Versioned subagent notes: `subagents/README.md` in the publish tree (see `@cursor-delegate` skill package for hub path).
