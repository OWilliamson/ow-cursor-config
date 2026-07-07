#!/usr/bin/env bash
# Install shipped rules from this repo into the Cursor user profile.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${OW_CURSOR_CONFIG:-$(cd "$SCRIPT_DIR/.." && pwd)}"
CURSOR_PROFILE="${CURSOR_PROFILE:-$HOME/.cursor}"
EXTRA=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      EXTRA+=(--dry-run)
      shift
      ;;
    -h | --help)
      echo "Usage: $0 [--dry-run]"
      echo "  OW_CURSOR_CONFIG  Repo root (default: parent of scripts/)"
      echo "  CURSOR_PROFILE    Profile dir (default: \$HOME/.cursor)"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

exec python3 "$SCRIPT_DIR/lib/profile-tooling.py" install-rules \
  --repo "$REPO_ROOT" \
  --profile "$CURSOR_PROFILE" \
  "${EXTRA[@]}"
