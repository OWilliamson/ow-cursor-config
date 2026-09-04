"""Bootstrap: ensure owcc-plan-validation-report scripts dir is on sys.path for plan_lib."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent


def ensure_plan_lib_path() -> Path:
    if str(_SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPT_DIR))
    return _SCRIPT_DIR


def import_plan_lib():
    ensure_plan_lib_path()
    import plan_lib  # noqa: WPS433

    return plan_lib


def resolve_validation_report_scripts_dir(from_script: Path | None = None) -> Path:
    """Profile path after reconcile, else hub sibling skill layout for dev."""
    profile = (
        Path.home()
        / ".cursor"
        / "skills"
        / "owcc-plan-validation-report"
        / "scripts"
    )
    if profile.is_dir():
        return profile
    if from_script is not None:
        hub = from_script.resolve().parent.parent.parent / "owcc-plan-validation-report" / "scripts"
        if hub.is_dir():
            return hub
    return _SCRIPT_DIR
