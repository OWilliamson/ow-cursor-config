# Platform routing (prune)

## Repo root

1. `OW_CURSOR_CONFIG` if set.
2. Else three levels up from `skills/cursor-prune-profile-tooling/`.
3. Else ask for checkout path.

## Profile directory

| OS | Default |
|----|---------|
| Linux / macOS / WSL | `$HOME/.cursor` |
| Windows | `%USERPROFILE%\.cursor` |

Set `CURSOR_PROFILE` when non-default.

## Script selection

Replace `<kind>` with `rules` or `skills` from required user input.

| Environment | Command |
|-------------|---------|
| Linux, macOS, WSL, Git Bash | `bash scripts/prune-profile-<kind>.sh` |
| Windows PowerShell | `pwsh -File scripts/prune-profile-<kind>.ps1` |

**Dry-run:** `--dry-run` or `-DryRun`.

## Manifest

Prune reads `$CURSOR_PROFILE/.ow-cursor-config-manifest.json`. If the chosen kind has no recorded names, abort and direct the user to the matching install skill.

## Python

Requires Python 3 on `PATH`.

Operator reference: **[../../scripts/profile-tooling.md](../../scripts/profile-tooling.md)**.
