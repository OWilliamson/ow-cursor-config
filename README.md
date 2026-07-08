# Generic Cursor tooling

This is a collection of cursor and agent tooling which can be used or adapted to suit your project and can be used in your **global** Cursor profile: rules, slash commands, skills, hooks, and subagent notes.

## Install into your profile (rules and skills)

Use **scripts** to copy shipped **rules** and **skills** into `~/.cursor/` (Linux/macOS) or `%USERPROFILE%\.cursor` (Windows). Hooks, commands, and subagents are not covered.

| | Rules | Skills | Prune retired |
|--|-------|--------|----------------|
| Linux / macOS | `bash scripts/install-profile-rules.sh` | `bash scripts/install-profile-skills.sh` | `bash scripts/prune-profile-rules.sh` / `prune-profile-skills.sh` |
| Windows | `pwsh -File scripts/install-profile-rules.ps1` | `pwsh -File scripts/install-profile-skills.ps1` | `pwsh -File scripts/prune-profile-*.ps1` |

**Agent-assisted install:** open this repo as the Cursor workspace and use project skills `@cursor-install-profile-rules`, `@cursor-install-profile-skills`, or `@cursor-prune-profile-tooling` — see [AGENTS.md](AGENTS.md). Those skills live in `.cursor/skills/` and are **not** installed to your global profile.

**Identity:** personal `{handle}-user.mdc` is not shipped — use `@cursor-create-identity-rule` after installing skills to your profile.

Full reference: [scripts/profile-tooling.md](scripts/profile-tooling.md).

## Layout


| Folder | Role |
|--------|------|
| [catalog/](catalog/) | Shipped rule/skill name list for install and prune (`bundle-manifest.yaml`). |
| [scripts/](scripts/) | Cross-platform install/prune wrappers (bash + PowerShell; Python 3 helper). |
| `.cursor/skills/` | **Project-only** install/prune skills (this workspace; not shipped to profile). See [AGENTS.md](AGENTS.md). |
| [commands/](commands/) | Slash commands — **none active** (retired 2026-06-12). See [commands/README.md](commands/README.md). |
| [rules/](rules/) | Cursor rules (`.mdc`). See [rules/README.md](rules/README.md). |
| [skills/](skills/) | Agent Skills (`repo-*`, `script-*`, `cursor-*` packages). See [skills/README.md](skills/README.md). |
| [hooks.json](hooks.json) + [hooks/](hooks/) | Agent hook registration and implementations (e.g. `agent-retro-meter`). After install into `~/.cursor/`, paths in `hooks.json` are relative to that directory. See [hooks/README.md](hooks/README.md). |
| [subagents/](subagents/) | Placeholder for versioned subagent prompts or manifests. See [subagents/README.md](subagents/README.md). |

