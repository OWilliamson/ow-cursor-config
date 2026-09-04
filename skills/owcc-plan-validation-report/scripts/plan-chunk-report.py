#!/usr/bin/env python3
"""Pass 2 — chunk / sizing report for plan files.

Prints a short brief for the agent: phase count, split hints, heavy todos, actions.

Dependencies: Python 3.9+, PyYAML.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import plan_lib  # noqa: E402


def format_report(data: plan_lib.ChunkReportData) -> str:
    lines: list[str] = []
    lines.extend(plan_lib.format_agent_brief_lines(data.agent_brief))
    lines.append("")
    lines.extend(plan_lib.format_split_summary_lines(data.split_suggestions))
    return "\n".join(lines)


def format_json(data: plan_lib.ChunkReportData) -> str:
    b = data.agent_brief
    return json.dumps(
        {
            "plan": data.plan_path,
            "recommended_phases": b.recommended_phases,
            "current_phases": b.current_phases,
            "plan_weight": b.plan_weight,
            "overweighted_phases": [
                {"name": n, "weight": w} for n, w in b.overweighted_phases
            ],
            "underweighted_phases": [
                {"name": n, "weight": w} for n, w in b.underweighted_phases
            ],
            "phases_may_require_splitting": b.phases_may_require_splitting,
            "todos_may_require_splitting": b.todos_may_require_splitting,
            "heavy_todos": [
                {"id": tid, "weight": w}
                for tid, w in b.individual_todo_weights
                if w >= plan_lib.TODO_WEIGHT_WATCH
            ],
            "merge_phases_suggested": b.merge_phases_suggested,
            "add_phases_suggested": b.add_phases_suggested,
            "split_actions": [
                {"action": s.action, "target": s.target, "why": s.why}
                for s in data.split_suggestions
            ],
        },
        indent=2,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Chunk/sizing report for a .plan.md")
    parser.add_argument("plan", help="Path to .plan.md")
    parser.add_argument(
        "--workspace",
        help="Workspace root for resolving referenced file paths (default: nearest .git parent)",
    )
    parser.add_argument(
        "--estimates",
        metavar="JSON",
        help="Optional todo id -> {files, edits, tool_uses} bands",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        plan = plan_lib.read_plan(Path(args.plan))
        estimates = plan_lib.load_estimates(Path(args.estimates) if args.estimates else None)
        ws = Path(args.workspace) if args.workspace else None
        data = plan_lib.build_chunk_report(plan, estimates, ws)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(format_json(data) if args.json else format_report(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
