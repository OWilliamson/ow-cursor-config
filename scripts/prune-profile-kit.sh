#!/usr/bin/env bash
# Prune owcc-* profile kits (consumer / publish tree).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURSOR_PROFILE="${CURSOR_PROFILE:-$HOME/.cursor}"
EXTRA=()
KIT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      EXTRA+=(--dry-run)
      shift
      ;;
    --kit)
      KIT="$2"
      shift 2
      ;;
    -h | --help)
      echo "Usage: $0 [--dry-run] [--kit NAME]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

ARGS=(prune-kit --profile "$CURSOR_PROFILE" "${EXTRA[@]}")
if [[ -n "$KIT" ]]; then
  ARGS+=(--kit "$KIT")
fi

exec python3 "$SCRIPT_DIR/lib/profile_kits_lib.py" "${ARGS[@]}"
