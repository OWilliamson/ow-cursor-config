# Generic Cursor Tooling

This is a collection of Cursor and agent tooling you can use or adapt: rules, skills, hooks, and kit install scripts for your **global** Cursor profile.

## Install into your profile

Copy shipped **kits** into `~/.cursor/` (Linux/macOS). Each kit is a named set of rules, skills, and optionally hooks.

```bash
bash scripts/install-profile-kit.sh              # owcc-kit-starter (default)
bash scripts/install-profile-kit.sh --all        # every kit in this repo
bash scripts/install-profile-kit.sh --kit owcc-kit-author
bash scripts/prune-profile-kit.sh --kit owcc-kit-starter
```

Full reference: [scripts/profile-tooling.md](scripts/profile-tooling.md). Catalog: [catalog/bundle-manifest.yaml](catalog/bundle-manifest.yaml).

**Agent-assisted install:** open this repo as the Cursor workspace and use the project skills under [`.cursor/skills/`](.cursor/skills/). Those skills are **not** copied to your global profile.

**Identity:** personal `{handle}-user.mdc` is not shipped — use `/owcc-identity-create-rule` after installing skills to your profile.

## Layout

| Folder | Role |
|--------|------|
| [bundles/](bundles/) | Per-kit symlink trees (`owcc-kit-starter`, …) used by install/prune. |
| [catalog/](catalog/) | Kit catalog (`bundle-manifest.yaml` / `.json`). |
| [scripts/](scripts/) | `install-profile-kit.sh`, `prune-profile-kit.sh`, and helpers. |
| `.cursor/skills/` | **Project-only** install/prune skills (this workspace). See [AGENTS.md](AGENTS.md). |
| [commands/](commands/) | Slash commands — **none active**. See [commands/README.md](commands/README.md). |
| [rules/](rules/) | Cursor rules (`.mdc`). See [rules/README.md](rules/README.md). |
| [skills/](skills/) | Agent Skills (`owcc-*` packages). See [skills/README.md](skills/README.md). |
| [hooks.json](hooks.json) + [hooks/](hooks/) | Agent hook registration and implementations (e.g. `agent-retro-meter`). After install into `~/.cursor/`, paths in `hooks.json` are relative to that directory. See [hooks/README.md](hooks/README.md). |
| [subagents/](subagents/) | Placeholder for versioned subagent prompts or manifests. See [subagents/README.md](subagents/README.md). |
