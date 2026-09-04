#!/usr/bin/env python3
"""Pre-build structural validation — JSON stdout for plan mutation and report writer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import plan_lib  # noqa: E402


def run(plan_path: Path) -> dict:
    plan = plan_lib.read_plan(plan_path)
    issues = plan_lib.validate_structure(plan)
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warn"]
    return {
        "plan": str(plan.path),
        "result": "pass" if not errors else "fail",
        "failures": [
            {"code": i.code, "message": i.message, "severity": i.severity}
            for i in errors
        ],
        "warnings": [
            {"code": i.code, "message": i.message, "severity": i.severity}
            for i in warnings
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-build structural validation for plan files",
    )
    parser.add_argument("plan", help="Path to plan file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        data = run(Path(args.plan))
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Plan: {data['plan']}")
        print(f"Result: {data['result']}")
        for item in data["failures"]:
            print(f"  [error] {item['code']}: {item['message']}")
        for item in data["warnings"]:
            print(f"  [warn] {item['code']}: {item['message']}")
    return 0 if data["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
