#!/usr/bin/env python3
"""Structural validation for plan close (objective checks, not sizing advice)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_VR_SCRIPTS = (
    Path.home() / ".cursor" / "skills" / "owcc-plan-validation-report" / "scripts"
)
if not _VR_SCRIPTS.is_dir():
    _hub = _SCRIPT_DIR.parent.parent / "owcc-plan-validation-report" / "scripts"
    if _hub.is_dir():
        _VR_SCRIPTS = _hub
if str(_VR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_VR_SCRIPTS))

import plan_lib  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate plan structure for close (statuses, gates, verify pairs).",
    )
    parser.add_argument("plan", nargs="?", help="Path to plan file")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable issue list",
    )
    args = parser.parse_args()

    if not args.plan:
        parser.print_help()
        return 0

    try:
        plan = plan_lib.read_plan(args.plan)
        issues = plan_lib.validate_structure(plan)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2

    errors = [i for i in issues if i.severity == "error"]
    warns = [i for i in issues if i.severity == "warn"]

    if args.json:
        print(
            json.dumps(
                {
                    "plan": str(plan.path),
                    "ok": not errors,
                    "errors": [{"code": i.code, "message": i.message} for i in errors],
                    "warnings": [{"code": i.code, "message": i.message} for i in warns],
                },
                indent=2,
            )
        )
    else:
        print(f"Plan: {plan.path}")
        print(f"Todos: {len(plan.todos)}")
        if not issues:
            print("OK — no structural issues found.")
        else:
            if errors:
                print(f"\nErrors ({len(errors)}):")
                for i in errors:
                    print(f"  [{i.code}] {i.message}")
            if warns:
                print(f"\nWarnings ({len(warns)}):")
                for i in warns:
                    print(f"  [{i.code}] {i.message}")
            print(f"\nResult: {'FAIL' if errors else 'PASS with warnings'}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
