"""Bootstrap: ensure owcc-plan-validation-report scripts dir is on sys.path for plan_lib.

Purpose: Shared import helper for plan-amr-inventory.py.
Dependencies: sibling skill owcc-plan-validation-report (profile or hub path).
Agent: imported by inventory script — do not RUN standalone.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent


def ensure_plan_lib_path() -> Path:
    profile = (
        Path.home()
        / ".cursor"
        / "skills"
        / "owcc-plan-validation-report"
        / "scripts"
    )
    if profile.is_dir():
        scripts = profile
    else:
        hub = _SCRIPT_DIR.parent.parent / "owcc-plan-validation-report" / "scripts"
        scripts = hub if hub.is_dir() else _SCRIPT_DIR
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    return scripts


def import_plan_lib():
    ensure_plan_lib_path()
    import plan_lib  # noqa: WPS433

    return plan_lib
