# Platform routing (install rules)

Resolve paths before running scripts.

## Repo root

1. `OW_CURSOR_CONFIG` if set.
2. Else three levels up from this skill directory (`skills/cursor-install-profile-rules/` → repo root).
3. Else ask the user for the `ow-cursor-config` checkout path.

Repo root must contain `rules/`, `catalog/bundle-manifest.json`, and `scripts/`.

## Profile directory

| OS | Default |
|----|---------|
| Linux / macOS / WSL | `$HOME/.cursor` |
| Windows | `%USERPROFILE%\.cursor` |

Override with `CURSOR_PROFILE` when Cursor uses a non-default profile path.

## Script selection

| Environment | Command |
|-------------|---------|
| Linux, macOS, WSL, Git Bash | `bash scripts/install-profile-rules.sh` |
| Windows PowerShell | `pwsh -File scripts/install-profile-rules.ps1` |

Run from repo root, or pass absolute paths via env vars (wrappers default repo to parent of `scripts/`).

**Dry-run:** append `--dry-run` (bash) or `-DryRun` (PowerShell).

**Detection:** if `$env:OS -eq 'Windows_NT'` and the user is not in WSL, use PowerShell. Otherwise use bash. If unclear, ask once.

## Python

Wrappers call `python3` / `python` on `scripts/lib/profile-tooling.py`. Python 3 must be on `PATH`.
