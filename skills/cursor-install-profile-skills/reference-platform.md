# Platform routing (install skills)

## Repo root

1. `OW_CURSOR_CONFIG` if set.
2. Else three levels up from `skills/cursor-install-profile-skills/`.
3. Else ask for the `ow-cursor-config` checkout path.

## Profile directory

| OS | Default |
|----|---------|
| Linux / macOS / WSL | `$HOME/.cursor` |
| Windows | `%USERPROFILE%\.cursor` |

Override with `CURSOR_PROFILE` when needed.

## Script selection

| Environment | Command |
|-------------|---------|
| Linux, macOS, WSL, Git Bash | `bash scripts/install-profile-skills.sh` |
| Windows PowerShell | `pwsh -File scripts/install-profile-skills.ps1` |

**Dry-run:** `--dry-run` or `-DryRun`.

**Detection:** `$env:OS -eq 'Windows_NT'` without WSL → PowerShell; else bash.

## Python

Requires Python 3 on `PATH` (`scripts/lib/profile-tooling.py`).
