# Profile install and prune tooling

Install **owcc-*** profile kits into `~/.cursor/` from this repository.

## Layout

| Path | Role |
|------|------|
| [`bundles/`](../bundles/) | Symlink tree per kit (`owcc-kit-starter`, …) |
| [`catalog/bundle-manifest.json`](../catalog/bundle-manifest.json) | Generated kit catalog |
| [`scripts/install-profile-kit.sh`](install-profile-kit.sh) | Install kit(s) |
| [`scripts/prune-profile-kit.sh`](prune-profile-kit.sh) | Prune installed kit(s) |
| [`scripts/lib/profile_kits_lib.py`](lib/profile_kits_lib.py) | Implementation |

## Kits

| Kit | Contents (summary) |
|-----|-------------------|
| `owcc-kit-starter` | Core rules + delegate, tooling-help, identity skill (**default**) |
| `owcc-kit-author` | Validate/improve rules and skills, compress, workflow review |
| `owcc-kit-plan` | Plan improve, triage, verification, validation report, build, review |
| `owcc-kit-repo` | owcc-repo-cleanup, owcc-repo-convention-change |
| `owcc-kit-dev` | owcc-script-review |
| `owcc-kit-itrs` | ITRS rules + owcc-customer-explanation |
| `owcc-kit-session` | owcc-session-retro + agent-retro-meter hook |

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `OW_CURSOR_CONFIG` | Parent of `scripts/` | This repository root |
| `CURSOR_PROFILE` | `$HOME/.cursor` | Cursor profile directory |

## Install

```bash
bash scripts/install-profile-kit.sh              # owcc-kit-starter
bash scripts/install-profile-kit.sh --all        # every kit in this repo
bash scripts/install-profile-kit.sh --kit owcc-kit-author
bash scripts/install-profile-kit.sh --dry-run
```

Writes `~/.cursor/.ow-cursor-config-manifest.json` (v2) with `installed_kits`.

## Prune

```bash
bash scripts/prune-profile-kit.sh --dry-run
bash scripts/prune-profile-kit.sh --kit owcc-kit-starter
```

Removes members only if not required by another installed kit.

## Retired wrappers

`install-profile-rules.sh`, `install-profile-skills.sh`, `prune-profile-rules.sh`, and `prune-profile-skills.sh` (and `.ps1` twins) are retired. Use `install-profile-kit.sh` / `prune-profile-kit.sh`.

## Agent-assisted install

Project skills in this repo's `.cursor/skills/` (not copied to `~/.cursor/skills/`):

- `cursor-install-profile-kit` — invoke `install-profile-kit.sh`
- `cursor-prune-profile-kit` — invoke `prune-profile-kit.sh`
