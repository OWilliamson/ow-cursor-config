#!/usr/bin/env python3
"""Audit plan text for cursor-native closeout verification injection gaps.

Reads the plan file only — does not check live todo status or registry state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
_VR_SCRIPTS = Path.home() / ".cursor" / "skills" / "owcc-plan-validation-report" / "scripts"
if not _VR_SCRIPTS.is_dir():
    _hub = _SCRIPT_DIR.parent.parent / "owcc-plan-validation-report" / "scripts"
    if _hub.is_dir():
        _VR_SCRIPTS = _hub
if str(_VR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_VR_SCRIPTS))

import plan_lib  # noqa: E402

VERIFY_SCRIPT_MARKER = "plan-verify-close-cursor.py"
REGISTRY_SHOW_MARKER = "plan-registry-show.py"
CLOSEOUT_ID_RE = re.compile(
    r"(?:cursor-native-close-verify|completion-audit|closeout-verify|cursor-handover-verify|phase-\d+-close-verify|-close-verify$)",
    re.IGNORECASE,
)
PLAN_BUILD_CONTENT_RE = re.compile(
    r"\*\*Plan\s+build:\*\*.*\bcomplete\b",
    re.IGNORECASE | re.DOTALL,
)
BODY_CLOSEOUT_HEADING_RE = re.compile(r"^##\s+Cursor-native closeout\b", re.MULTILINE | re.IGNORECASE)
BODY_EXEC_CLOSEOUT_RE = re.compile(
    r"(?:closeout|builtBy|plan-verify-close-cursor)",
    re.IGNORECASE,
)


def _content_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _has_registry_language(text: str) -> bool:
    low = text.lower()
    return (
        "builtby" in low
        or "built-by" in low
        or "registry" in low
        or REGISTRY_SHOW_MARKER in low
    )


def _is_closeout_candidate(todo_id: str, content: str, is_last_in_scope: bool) -> bool:
    if CLOSEOUT_ID_RE.search(todo_id):
        return True
    if not is_last_in_scope:
        return False
    low = content.lower()
    return "closeout" in low or ("verify" in low and ("close" in low or "handover" in low))


def _audit_closeout_content(
    gaps: list[dict[str, Any]],
    todo_id: str,
    content: str,
    scope: str,
) -> None:
    if VERIFY_SCRIPT_MARKER not in content:
        gaps.append(
            {
                "code": "missing_verify_script_path",
                "scope": scope,
                "todo_id": todo_id,
                "message": f"Closeout todo `{todo_id}` lacks `{VERIFY_SCRIPT_MARKER}` in content",
            }
        )
    if not _has_registry_language(content):
        gaps.append(
            {
                "code": "missing_registry_language",
                "scope": scope,
                "todo_id": todo_id,
                "message": f"Closeout todo `{todo_id}` lacks registry / builtBy check language",
            }
        )
    if not PLAN_BUILD_CONTENT_RE.search(content):
        gaps.append(
            {
                "code": "missing_plan_build_complete_language",
                "scope": scope,
                "todo_id": todo_id,
                "message": f"Closeout todo `{todo_id}` lacks **Plan build:** complete requirement",
            }
        )


def audit_plan(plan_path: Path) -> dict[str, Any]:
    plan_path = plan_path.expanduser().resolve()
    plan = plan_lib.read_plan(plan_path)
    gaps: list[dict[str, Any]] = []

    if plan.is_project:
        phases = plan.meta.get("phases") or []
        if not phases:
            gaps.append(
                {
                    "code": "missing_phases",
                    "scope": "project",
                    "message": "isProject plan has no phases[] array",
                }
            )
        for phase in phases:
            if not isinstance(phase, dict):
                continue
            phase_name = str(phase.get("name") or "unnamed-phase")
            todos = phase.get("todos") or []
            scope = f"phase:{phase_name}"
            if not todos:
                gaps.append(
                    {
                        "code": "missing_closeout_todo",
                        "scope": scope,
                        "message": f"Phase `{phase_name}` has no todos — need closeout verify as last todo",
                    }
                )
                continue
            last = todos[-1]
            if not isinstance(last, dict):
                gaps.append(
                    {
                        "code": "missing_closeout_todo",
                        "scope": scope,
                        "message": f"Phase `{phase_name}` last todo is not a mapping",
                    }
                )
                continue
            tid = str(last.get("id") or "")
            content = _content_str(last.get("content"))
            if not _is_closeout_candidate(tid, content, is_last_in_scope=True):
                gaps.append(
                    {
                        "code": "missing_closeout_todo",
                        "scope": scope,
                        "todo_id": tid or None,
                        "message": (
                            f"Phase `{phase_name}` last todo `{tid}` is not a closeout verify todo"
                        ),
                    }
                )
            else:
                _audit_closeout_content(gaps, tid, content, scope)
    else:
        root_todos = plan.meta.get("todos") or []
        scope = "flat"
        if not root_todos:
            gaps.append(
                {
                    "code": "missing_closeout_todo",
                    "scope": scope,
                    "message": "Flat plan has no todos — need final closeout verify todo",
                }
            )
        else:
            last = root_todos[-1]
            if not isinstance(last, dict):
                gaps.append(
                    {
                        "code": "missing_closeout_todo",
                        "scope": scope,
                        "message": "Flat plan last todo is not a mapping",
                    }
                )
            else:
                tid = str(last.get("id") or "")
                content = _content_str(last.get("content"))
                if not _is_closeout_candidate(tid, content, is_last_in_scope=True):
                    gaps.append(
                        {
                            "code": "missing_closeout_todo",
                            "scope": scope,
                            "todo_id": tid or None,
                            "message": (
                                f"Flat plan last todo `{tid}` is not a closeout verify todo "
                                "(expected cursor-native-close-verify or completion-audit with closeout language)"
                            ),
                        }
                    )
                else:
                    _audit_closeout_content(gaps, tid, content, scope)

    has_body_closeout = bool(
        BODY_CLOSEOUT_HEADING_RE.search(plan.body)
        or (
            "## Execution contract" in plan.body
            and BODY_EXEC_CLOSEOUT_RE.search(plan.body)
        )
    )
    if not has_body_closeout:
        gaps.append(
            {
                "code": "missing_body_closeout_addendum",
                "scope": "body",
                "message": (
                    "Plan body lacks ## Cursor-native closeout section or execution-contract closeout language"
                ),
            }
        )

    ok = not gaps
    return {
        "schema": 1,
        "plan": str(plan_path),
        "is_project": plan.is_project,
        "ok": ok,
        "gaps": gaps,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit plan text for cursor-native closeout verification gaps",
    )
    parser.add_argument("plan", type=Path, help="Path to .plan.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON on stdout")
    args = parser.parse_args()
    try:
        data = audit_plan(args.plan)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Plan: {data['plan']}")
        print(f"OK: {data['ok']}")
        for gap in data["gaps"]:
            print(f"  [{gap['code']}] {gap.get('scope', '')}: {gap['message']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
