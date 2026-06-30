# Generic Cursor tooling

This is a collection of cursor and agent tooling which can be used or adapted to suit your project and can be used in your **global** Cursor profile: rules, slash commands, skills, hooks, and subagent notes.

## Layout


| Folder | Role |
|--------|------|
| [commands/](commands/) | Slash commands — **none active** (retired 2026-06-12). See [commands/README.md](commands/README.md). |
| [rules/](rules/) | Cursor rules (`.mdc`). See [rules/README.md](rules/README.md). |
| [skills/](skills/) | Agent Skills (`repo-*`, `plan-*`, `docs-*`, `script-*`, `cursor-*` packages). See [skills/README.md](skills/README.md). |
| [hooks.json](hooks.json) + [hooks/](hooks/) | Agent hook registration and implementations (e.g. `agent-retro-meter`). After install into `~/.cursor/`, paths in `hooks.json` are relative to that directory. See [hooks/README.md](hooks/README.md). |
| [subagents/](subagents/) | Placeholder for versioned subagent prompts or manifests. See [subagents/README.md](subagents/README.md). |


