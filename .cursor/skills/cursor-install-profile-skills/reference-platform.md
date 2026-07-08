# Platform routing (install skills)

## Repo root

1. `OW_CURSOR_CONFIG` if set.
2. Else three levels up from `.cursor/skills/cursor-install-profile-skills/`.
3. Else ask for checkout path.

## Profile directory

| OS | Default |
|----|---------|
| Linux / macOS / WSL | `$HOME/.cursor` |
| Windows | `%USERPROFILE%\.cursor` |

## Script selection

| Environment | Command |
|-------------|---------|
| Linux, macOS, WSL, Git Bash | `bash scripts/install-profile-skills.sh` |
| Windows PowerShell | `pwsh -File scripts/install-profile-skills.ps1` |

**Dry-run:** `--dry-run` or `-DryRun`.

## Python

Requires Python 3 on `PATH`.
