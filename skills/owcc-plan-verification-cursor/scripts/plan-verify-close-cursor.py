#!/usr/bin/env python3
"""Cursor-native closeout check for build agents: file completion + registry + close markers."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import plan_registry_lib as prl  # noqa: E402

PLAN_BUILD_COMPLETE_RE = re.compile(
    r"\*\*Plan\s+build:\*\*\s*complete\b",
    re.IGNORECASE,
)


def _plan_lib_scripts_dir() -> Path:
    profile = Path.home() / ".cursor" / "skills" / "owcc-plan-validation-report" / "scripts"
    if profile.is_dir():
        return profile
    hub = _SCRIPT_DIR.parent.parent / "owcc-plan-validation-report" / "scripts"
    return hub if hub.is_dir() else profile


def _plan_build_scripts_dir() -> Path:
    profile = Path.home() / ".cursor" / "skills" / "owcc-plan-build" / "scripts"
    if profile.is_dir():
        return profile
    hub = _SCRIPT_DIR.parent.parent / "owcc-plan-build" / "scripts"
    return hub if hub.is_dir() else profile


def _run_json_script(script_path: Path, plan_path: Path) -> dict | None:
    if not script_path.is_file():
        return None
    proc = subprocess.run(
        [sys.executable, str(script_path), str(plan_path), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 2 or not proc.stdout.strip():
        return {"error": proc.stderr.strip() or "script failed"}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"error": "invalid json from script"}


def verify_handover(plan_path: Path, composer_id: str | None = None) -> dict:
    plan_path = prl.normalize_plan_path(plan_path)
    failures: list[dict] = []
    checks: list[dict] = []

    incomplete = prl.incomplete_todo_ids(plan_path)
    file_ok = not incomplete
    checks.append({"id": "file_todos", "status": "pass" if file_ok else "fail"})
    if incomplete:
        failures.append(
            {
                "check": "file_todos",
                "code": "incomplete_todos",
                "message": f"YAML todos not completed/cancelled: {', '.join(incomplete)}",
                "todo_ids": incomplete,
            }
        )

    plan = prl.plan_lib.read_plan(plan_path)
    has_close_line = bool(PLAN_BUILD_COMPLETE_RE.search(plan.body))
    checks.append({"id": "plan_build_complete_line", "status": "pass" if has_close_line else "fail"})
    if not has_close_line:
        failures.append(
            {
                "check": "file_body",
                "code": "missing_plan_build_complete",
                "message": "Execution contract missing '**Plan build:** complete — YYYY-MM-DD'",
            }
        )

    close_script = _plan_build_scripts_dir() / "plan-validate-close.py"
    close_data = _run_json_script(close_script, plan_path)
    if close_data is None:
        checks.append({"id": "structure", "status": "skip"})
    elif close_data.get("error"):
        checks.append({"id": "structure", "status": "fail"})
        failures.append(
            {
                "check": "structure",
                "code": "validate_close_error",
                "message": close_data["error"],
            }
        )
    elif not close_data.get("ok", False):
        checks.append({"id": "structure", "status": "fail"})
        for err in close_data.get("errors", []):
            failures.append(
                {
                    "check": "structure",
                    "code": err.get("code", "structure_error"),
                    "message": err.get("message", ""),
                }
            )
    else:
        checks.append({"id": "structure", "status": "pass"})

    registry_summary: dict | None = None
    try:
        registry_summary = prl.show_summary(plan_path, composer_id)
    except Exception as exc:  # noqa: BLE001
        checks.append({"id": "registry", "status": "fail"})
        failures.append(
            {
                "check": "registry",
                "code": "registry_read_failed",
                "message": str(exc),
            }
        )
    else:
        registered = bool(registry_summary.get("registered"))
        entry = registry_summary.get("registry_entry") or {}
        built_by = entry.get("builtBy") if isinstance(entry.get("builtBy"), dict) else {}
        plan_todo_ids = {t.id for t in plan.todos}
        registry_todo_ids: set[str] = set()
        for ids in built_by.values():
            if isinstance(ids, list):
                registry_todo_ids.update(str(i) for i in ids)

        registry_ok = (
            registered
            and bool(built_by)
            and plan_todo_ids <= registry_todo_ids
            and registry_summary.get("all_complete")
        )
        checks.append({"id": "registry", "status": "pass" if registry_ok else "fail"})

        if not registered:
            failures.append(
                {
                    "check": "registry",
                    "code": "not_registered",
                    "message": "Plan has no composer.planRegistry row",
                }
            )
        elif not built_by:
            failures.append(
                {
                    "check": "registry",
                    "code": "empty_builtBy",
                    "message": "Registry builtBy is empty — Plan UI Build attribution missing",
                }
            )
        else:
            missing = sorted(plan_todo_ids - registry_todo_ids)
            if missing:
                failures.append(
                    {
                        "check": "registry",
                        "code": "builtBy_missing_todos",
                        "message": f"builtBy does not list all plan todo ids; missing: {', '.join(missing)}",
                        "todo_ids": missing,
                    }
                )
        if registered and not registry_summary.get("all_complete"):
            failures.append(
                {
                    "check": "registry",
                    "code": "registry_incomplete",
                    "message": "Registry summary reports plan not all complete",
                }
            )

    result = "pass" if not failures else "fail"
    return {
        "schema": 1,
        "plan": str(plan_path),
        "result": result,
        "checks": checks,
        "failures": failures,
        "registry": {
            "registered": registry_summary.get("registered") if registry_summary else False,
            "builtBy": (registry_summary.get("registry_entry") or {}).get("builtBy")
            if registry_summary
            else None,
            "resolved_composer_id": registry_summary.get("resolved_composer_id")
            if registry_summary
            else None,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Closeout verify for build agents (file + registry + Plan build complete)",
    )
    parser.add_argument("plan", type=Path, help="Path to .plan.md")
    parser.add_argument("--composer", metavar="UUID", help="Force composer id for registry")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        data = verify_handover(args.plan, args.composer)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Plan: {data['plan']}")
        print(f"Result: {data['result']}")
        for item in data["failures"]:
            print(f"  [{item['check']}] {item['code']}: {item['message']}")
    return 0 if data["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
