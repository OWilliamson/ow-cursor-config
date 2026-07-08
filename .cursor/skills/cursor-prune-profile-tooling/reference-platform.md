# Platform routing (prune)

## Repo root

1. `OW_CURSOR_CONFIG` if set.
2. Else three levels up from `.cursor/skills/cursor-prune-profile-tooling/`.
3. Else ask for checkout path.

## Profile directory

| OS | Default |
|----|---------|
| Linux / macOS / WSL | `$HOME/.cursor` |
| Windows | `%USERPROFILE%\.cursor` |

## Script selection

Replace `<kind>` with `rules` or `skills`.

| Environment | Command |
|-------------|---------|
| Linux, macOS, WSL, Git Bash | `bash scripts/prune-profile-<kind>.sh` |
| Windows PowerShell | `pwsh -File scripts/prune-profile-<kind>.ps1` |

**Dry-run:** `--dry-run` or `-DryRun`.

Operator reference: **[../../../scripts/profile-tooling.md](../../../scripts/profile-tooling.md)**.
