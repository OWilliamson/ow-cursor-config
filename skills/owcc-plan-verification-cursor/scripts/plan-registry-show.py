#!/usr/bin/env python3
"""Read-only Cursor plan registry inspection (layer C)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import plan_registry_lib as prl  # noqa: E402


def build_json_summary(plan_path: Path, composer_id: str | None) -> dict:
    summary = prl.show_summary(plan_path, composer_id)
    entry = summary.get("registry_entry") or {}
    built_by = entry.get("builtBy") if isinstance(entry.get("builtBy"), dict) else {}
    registry_todo_ids: set[str] = set()
    for ids in built_by.values():
        if isinstance(ids, list):
            registry_todo_ids.update(str(i) for i in ids)
    plan = prl.plan_lib.read_plan(plan_path)
    plan_todo_ids = {t.id for t in plan.todos}
    return {
        "plan": summary["plan_path"],
        "registered": summary["registered"],
        "plan_id": summary.get("plan_id"),
        "all_complete": summary.get("all_complete"),
        "todo_status_counts": summary.get("todo_status_counts"),
        "builtBy": built_by,
        "registry_todo_ids": sorted(registry_todo_ids),
        "plan_todo_ids": sorted(plan_todo_ids),
        "builtBy_covers_all_todos": plan_todo_ids <= registry_todo_ids if built_by else False,
        "builtBy_nonempty": bool(built_by),
        "resolved_composer_id": summary.get("resolved_composer_id"),
        "resolve_error": summary.get("resolve_error"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Show Cursor composer.planRegistry row for a plan (read-only)",
    )
    parser.add_argument("plan", type=Path, help="Path to .plan.md")
    parser.add_argument("--composer", metavar="UUID", help="Force composer id")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        if args.json:
            print(json.dumps(build_json_summary(args.plan, args.composer), indent=2))
            return 0
        summary = prl.show_summary(args.plan, args.composer)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"plan: {summary['plan_path']}")
    print(f"registry id: {summary['plan_id'] or '(none)'}")
    print(f"registered: {summary['registered']}")
    print(f"todos: {summary['todo_status_counts']}")
    print(f"all complete: {summary['all_complete']}")
    entry = summary.get("registry_entry")
    if entry:
        print(f"builtBy: {json.dumps(entry.get('builtBy'), indent=2)}")
    else:
        print("(no registry row)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
