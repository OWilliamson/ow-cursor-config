# Profile install and prune tooling

Scripts and **project skills** for copying **rules** and **skills** from this repository into the Cursor user profile (`~/.cursor/` on Linux/macOS; `%USERPROFILE%\.cursor` on Windows).

**Out of scope:** hooks, `hooks.json`, commands, subagents, and any “install everything” one-shot.

## Layout

| Path | Role |
|------|------|
| [`catalog/bundle-manifest.yaml`](../catalog/bundle-manifest.yaml) | Human-readable list of shipped rule and skill names |
| [`catalog/bundle-manifest.json`](../catalog/bundle-manifest.json) | Machine-readable catalog (scripts read this) |
| [`scripts/generate-bundle-manifest.py`](generate-bundle-manifest.py) | Regenerate catalog from `rules/` and `skills/` trees |
| [`scripts/lib/profile-tooling.py`](lib/profile-tooling.py) | Shared install/prune implementation (Python 3 stdlib) |
| `scripts/install-profile-*.sh` / `.ps1` | Platform wrappers |
| `scripts/prune-profile-*.sh` / `.ps1` | Platform wrappers |
| [`.cursor/skills/`](../.cursor/skills/) | **Project-only** install/prune agent skills (not copied to profile) |

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `OW_CURSOR_CONFIG` | Parent of `scripts/` | Repo root containing `rules/`, `skills/`, `catalog/` |
| `CURSOR_PROFILE` | `$HOME/.cursor` or `%USERPROFILE%\.cursor` | Cursor user profile directory |

On WSL vs native Windows, set `CURSOR_PROFILE` explicitly if Cursor uses a different profile path.

## Prerequisites

- **Python 3** on `PATH` (`python3` on Linux/macOS; `python` on Windows PowerShell wrappers).
- Linux/macOS: `chmod +x scripts/*.sh` optional (scripts are invoked via `bash` or `exec python3`).

## Catalog

Regenerate after adding or removing rules/skills:

```bash
python3 scripts/generate-bundle-manifest.py
```

Hub maintainers run this in `cursor-config-generic/public/` before publish.

## Install

Copies shipped items into the profile. Updates only names in the catalog. Does **not** delete extra profile rules or skills. Writes/updates `$CURSOR_PROFILE/.ow-cursor-config-manifest.json` for safe prune.

### Linux / macOS / WSL

```bash
bash scripts/install-profile-rules.sh
bash scripts/install-profile-skills.sh
bash scripts/install-profile-rules.sh --dry-run
```

### Windows (PowerShell)

```powershell
pwsh -File scripts/install-profile-rules.ps1
pwsh -File scripts/install-profile-skills.ps1
pwsh -File scripts/install-profile-skills.ps1 -DryRun
```

If execution policy blocks scripts: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Prune

Removes profile rules or skills that were **previously installed from this bundle** (recorded in the manifest) but are **no longer** in `catalog/bundle-manifest.json`. User-authored rules/skills never listed in the manifest are untouched.

Run install at least once before prune.

```bash
bash scripts/prune-profile-rules.sh --dry-run
bash scripts/prune-profile-skills.sh --dry-run
bash scripts/prune-profile-rules.sh
```

```powershell
pwsh -File scripts/prune-profile-rules.ps1 -DryRun
pwsh -File scripts/prune-profile-skills.ps1
```

## Project skills (this workspace only)

Open **ow-cursor-config** as the Cursor workspace. Skills under `.cursor/skills/` are **not** installed to `~/.cursor/skills/`:

| Skill | Use when |
|-------|----------|
| `@cursor-install-profile-rules` | Install or update shipped rules via script |
| `@cursor-install-profile-skills` | Install or update shipped skills via script |
| `@cursor-prune-profile-tooling` | Prune retired rules or skills (input: `rules` or `skills`) |

See [AGENTS.md](../AGENTS.md).

**Identity rules** (`{handle}-user.mdc`) are not shipped in `rules/` — use `@cursor-create-identity-rule` from the profile after installing skills.
