#!/usr/bin/env python3
"""Write .cursor/plans/reports/<plan-name>.validation.json — owcc-plan-validation-report only."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import plan_lib  # noqa: E402


def _run_json_script(script: str, plan_path: Path, extra: list[str] | None = None) -> dict:
    cmd = [sys.executable, str(_SCRIPT_DIR / script), str(plan_path), "--json"]
    if extra:
        cmd.extend(extra)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode == 2:
        raise RuntimeError(proc.stderr.strip() or f"{script} failed")
    if not proc.stdout.strip():
        raise RuntimeError(f"{script} produced no output")
    return json.loads(proc.stdout)


def build_report(plan_path: Path, sizing: str) -> dict:
    qualitative = _run_json_script("plan-qualitative-report.py", plan_path)
    chunk = _run_json_script("plan-chunk-report.py", plan_path)
    structure = _run_json_script("plan-validate-structure.py", plan_path)

    checks: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []

    qual_status = "pass" if qualitative.get("error_count", 0) == 0 else "fail"
    checks.append({"id": "qualitative", "status": qual_status})
    if qual_status == "fail":
        for f in qualitative.get("findings", []):
            if f.get("severity") == "error":
                failures.append(
                    {
                        "check": "qualitative",
                        "code": f.get("code", ""),
                        "message": f.get("message", ""),
                    }
                )

    struct_status = structure.get("result", "fail")
    checks.append({"id": "structure", "status": struct_status})
    if struct_status == "fail":
        for f in structure.get("failures", []):
            failures.append(
                {
                    "check": "structure",
                    "code": f.get("code", ""),
                    "message": f.get("message", ""),
                }
            )

    checks.append({"id": "chunk", "status": "pass"})
    chunk_advisory: list[dict] = []
    if chunk.get("split_actions"):
        chunk_advisory = chunk["split_actions"]
    if chunk.get("merge_phases_suggested"):
        chunk_advisory.append(
            {"action": "merge_phases", "note": "advisory — does not fail validation"}
        )

    result = "pass" if not failures else "fail"
    plan = plan_lib.read_plan(plan_path)
    ws = plan_lib.resolve_workspace_root(plan, None)
    out_path = plan_lib.validation_report_path(plan_path, ws)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema": 1,
        "plan": str(plan.path.resolve()),
        "issued_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skill": "owcc-plan-validation-report",
        "sizing": sizing,
        "result": result,
        "checks": checks,
        "failures": failures,
        "chunk_advisory": chunk_advisory,
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write validation report JSON for owcc-plan-build gate",
    )
    parser.add_argument("plan", help="Absolute path to plan file")
    parser.add_argument(
        "--sizing",
        choices=("lean", "full", "auto"),
        default="lean",
    )
    args = parser.parse_args()
    try:
        payload = build_report(Path(args.plan).resolve(), args.sizing)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2
    out = plan_lib.validation_report_path(args.plan)
    print(str(out))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
