# Platform routing (install rules)

## Repo root

1. `OW_CURSOR_CONFIG` if set.
2. Else three levels up from `.cursor/skills/cursor-install-profile-rules/` (repo root).
3. Else ask for the ow-cursor-config checkout path.

Must contain `rules/`, `catalog/bundle-manifest.json`, and `scripts/`.

## Profile directory

| OS | Default |
|----|---------|
| Linux / macOS / WSL | `$HOME/.cursor` |
| Windows | `%USERPROFILE%\.cursor` |

Override with `CURSOR_PROFILE` when needed.

## Script selection

| Environment | Command (from repo root) |
|-------------|--------------------------|
| Linux, macOS, WSL, Git Bash | `bash scripts/install-profile-rules.sh` |
| Windows PowerShell | `pwsh -File scripts/install-profile-rules.ps1` |

**Dry-run:** `--dry-run` or `-DryRun`.

**Detection:** `$env:OS -eq 'Windows_NT'` without WSL → PowerShell; else bash.

## Python

Wrappers require Python 3 on `PATH`.
