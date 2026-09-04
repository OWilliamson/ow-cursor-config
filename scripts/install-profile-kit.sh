#!/usr/bin/env bash
# Install owcc-* profile kits from ow-cursor-config publish tree (consumer mode).
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
    --all)
      EXTRA+=(--all)
      shift
      ;;
    --kit)
      EXTRA+=(--kit "$2")
      shift 2
      ;;
    -h | --help)
      echo "Usage: $0 [--dry-run] [--all | --kit NAME ...]"
      echo "  Default kit: owcc-kit-starter"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

exec python3 "$SCRIPT_DIR/lib/profile_kits_lib.py" install-kit \
  --repo "$REPO_ROOT" \
  --profile "$CURSOR_PROFILE" \
  "${EXTRA[@]}"
