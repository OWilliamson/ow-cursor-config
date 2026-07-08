# AGENTS — ow-cursor-config

Published bundle of Cursor **rules** and **skills** for install into a user profile. This repo is the consumer-facing checkout — not the hub maintenance repo (`cursor-config-generic`).

## Layout

| Path | Role |
|------|------|
| `rules/` | Shipped `.mdc` rules — install to `~/.cursor/rules/` |
| `skills/` | Shipped agent skills — install to `~/.cursor/skills/` |
| `scripts/` | Cross-platform install/prune wrappers (bash + PowerShell) |
| `catalog/` | Bundle manifest (`bundle-manifest.json`) for install/prune |
| `.cursor/skills/` | **Project-only** skills for install/prune workflows — **not** shipped to profile |

## Profile install

Use **scripts** from this repo, or open this workspace and invoke **project skills**:

| Goal | Script | Project skill (this repo only) |
|------|--------|--------------------------------|
| Install/update rules | `scripts/install-profile-rules.sh` / `.ps1` | `@cursor-install-profile-rules` |
| Install/update skills | `scripts/install-profile-skills.sh` / `.ps1` | `@cursor-install-profile-skills` |
| Prune retired bundle items | `scripts/prune-profile-*.sh` / `.ps1` | `@cursor-prune-profile-tooling` |

Install/prune skills live under `.cursor/skills/` — they do **not** sync to `~/.cursor/skills/`.

Full reference: [scripts/profile-tooling.md](scripts/profile-tooling.md).

## Hub publish

Content under `rules/`, `skills/`, `scripts/`, `catalog/`, `hooks/`, etc. is mirrored from `cursor-config-generic/public/` via `/owcursor-repo-update`. **`.cursor/` is maintained in this repo only** — publish does not overwrite it.
