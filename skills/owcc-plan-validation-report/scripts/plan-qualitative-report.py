#!/usr/bin/env python3
"""Pass 1 — qualitative hygiene report for plan files.

Checks empty content, UUID ids, operator chrome, Plan file edit rule, etc.
Does **not** re-run body outline / structure validation — use
`plan-validate-structure.py` for that (write-report and improve validate both
RUN structure separately so findings are not double-counted).

Does not recommend phasing or todo splits — use plan-chunk-report.py after
structural fixes.

Dependencies: Python 3.9+, PyYAML (same as plan_lib).

Agent: run during plan mutation or via plan-write-validation-report.py.
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


def build_report(plan_path: Path) -> dict:
    plan = plan_lib.read_plan(plan_path)
    metrics = plan_lib.compute_plan_metrics(plan)
    findings = plan_lib.qualitative_findings(plan)
    errors = [f for f in findings if f.severity == "error"]
    warns = [f for f in findings if f.severity == "warn"]
    return {
        "plan": str(plan.path),
        "metrics": metrics,
        "findings": findings,
        "error_count": len(errors),
        "warn_count": len(warns),
        "pair_count": metrics.pair_count,
        "missing_verify_count": metrics.missing_verify_count,
    }


def format_markdown(data: dict) -> str:
    m: plan_lib.PlanMetrics = data["metrics"]
    lines = [
        "## Qualitative report (pass 1)",
        "",
        "Qualitative hygiene only — **not** body-outline structure and **not** chunk sizing. "
        "RUN `plan-validate-structure.py` for structure; fix errors before `plan-chunk-report.py`.",
        "",
        f"**Summary:** {m.todo_count} todos, {m.pair_count} implement steps with verify coverage, "
        f"{data['missing_verify_count']} still need verify, "
        f"{data['error_count']} error(s), {data['warn_count']} warn(s).",
        "",
        f"- shape: {m.shape}",
        f"- phases: {m.phase_count or 1}",
        "",
    ]
    findings: list[plan_lib.QualitativeFinding] = data["findings"]
    if not findings:
        lines.append("_No qualitative findings._")
    else:
        lines.append("| Sev | Code | Todo | Message |")
        lines.append("|-----|------|------|---------|")
        for f in findings:
            tid = f.todo_id or "—"
            lines.append(f"| {f.severity} | {f.code} | {tid} | {f.message} |")
    lines.append("")
    lines.append(
        "_Do not add phases or extra todos solely to clear missing_verify — add verify "
        "siblings or phase/pack gates first._"
    )
    return "\n".join(lines)


def format_json(data: dict) -> str:
    findings = data["findings"]
    payload = {
        "plan": data["plan"],
        "error_count": data["error_count"],
        "warn_count": data["warn_count"],
        "pair_count": data["pair_count"],
        "missing_verify_count": data["missing_verify_count"],
        "findings": [
            {
                "severity": f.severity,
                "code": f.code,
                "message": f.message,
                "todo_id": f.todo_id,
            }
            for f in findings
        ],
    }
    return json.dumps(payload, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Qualitative structural report for a .plan.md")
    parser.add_argument("plan", help="Path to .plan.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        data = build_report(Path(args.plan))
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(format_json(data) if args.json else format_markdown(data))
    return 1 if data["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
