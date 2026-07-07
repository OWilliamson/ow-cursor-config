# Remove profile skills previously installed from this bundle but no longer shipped.
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = if ($env:OW_CURSOR_CONFIG) { $env:OW_CURSOR_CONFIG } else { Split-Path -Parent $ScriptDir }
$CursorProfile = if ($env:CURSOR_PROFILE) { $env:CURSOR_PROFILE } else { Join-Path $env:USERPROFILE ".cursor" }

$Args = @(
    (Join-Path $ScriptDir "lib\profile-tooling.py"),
    "prune-skills",
    "--repo", $RepoRoot,
    "--profile", $CursorProfile
)
if ($DryRun) { $Args += "--dry-run" }

& python @Args
exit $LASTEXITCODE
