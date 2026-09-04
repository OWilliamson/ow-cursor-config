#!/usr/bin/env python3
"""A/M/R inventory assist for owcc-plan-review-execution.

Purpose: Parse plan Additions/Modifications/Removals vs git baseline; emit
claimed/unplanned/code_loc/bugbot_default JSON. Inventory assist only — does
not judge pass/fail. The agent completes judgment (Aims, todos, F-ids).

Dependencies: plan_lib via plan_lib_import (owcc-plan-validation-report scripts).

Agent: execute (RUN from SKILL §5.3.2 / VALIDATION). Not human-only.
"""

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

import plan_lib_import as pli  # noqa: E402

plan_lib = pli.import_plan_lib()

# Commands likely runnable in shell (not bare file paths) — optional field only.
CMD_PREFIX_RE = re.compile(
    r"^(?:python3?|bash|sh|npm|pnpm|yarn|make|cargo|go|pytest|git|curl|node|npx|"
    r"ruby|perl|php|dotnet|mvn|gradle|./)",
    re.IGNORECASE,
)
PIPE_OR_CHAIN_RE = re.compile(r"(?:&&|\|\||\|)")
BACKTICK_RE = re.compile(r"`([^`]+)`")

SECTION_RE = re.compile(
    r"^##\s+(Additions|Modifications|Removals)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")
ABBREV_RE = re.compile(
    r"\band\s+(\d+)\s+similar\b",
    re.IGNORECASE,
)
NONE_RE = re.compile(r"^None\.?\s*$", re.IGNORECASE)

# Name-status letters from git diff --name-status
GIT_ADD = frozenset({"A", "C", "R"})  # copy/rename treated as add-ish for claimed
GIT_MOD = frozenset({"M", "T"})
GIT_DEL = frozenset({"D"})

CODE_EXTENSIONS = frozenset(
    {
        ".py",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".go",
        ".rs",
        ".java",
        ".c",
        ".cpp",
        ".cc",
        ".cxx",
        ".h",
        ".hpp",
        ".cs",
        ".rb",
        ".php",
        ".sh",
        ".bash",
        ".zsh",
        ".ps1",
    }
)

# Unplanned noise — ignore these path tiers when listing unexpected diffs.
IGNORE_PATH_PREFIXES = (
    "node_modules/",
    ".git/",
    "__pycache__/",
    ".venv/",
    "venv/",
    "dist/",
    "build/",
    ".tox/",
    ".mypy_cache/",
    ".pytest_cache/",
    "archive/",
)
IGNORE_PATH_SUFFIXES = (
    ".lock",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Cargo.lock",
    "poetry.lock",
    ".pyc",
    ".pyo",
    ".DS_Store",
)
IGNORE_PATH_NAMES = frozenset(
    {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "Cargo.lock",
        "poetry.lock",
        "uv.lock",
    }
)

BUGBOT_LOC_MAX = 5000
# Git empty tree — baseline when HEAD is a root commit (no HEAD~1).
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d6927dc6ad6df0"


def _find_git_root(start: Path) -> Path | None:
    current = start.resolve()
    for _ in range(32):
        if (current / ".git").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def _resolve_workspace(plan_path: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    git_root = _find_git_root(plan_path.parent)
    if git_root:
        return git_root
    if ".cursor" in plan_path.parts:
        idx = plan_path.parts.index(".cursor")
        if idx > 0:
            return Path(*plan_path.parts[:idx]).resolve()
    return plan_path.parent.resolve()


def _run_git(workspace: Path, *args: str, timeout: int = 30) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, "", str(exc)


def _resolve_baseline(workspace: Path, explicit: str | None) -> dict:
    """Return {rev, method, error} for git diff base."""
    if explicit:
        code, out, err = _run_git(workspace, "rev-parse", "--verify", explicit)
        if code != 0:
            return {
                "rev": None,
                "method": "explicit",
                "error": f"invalid --base {explicit!r}: {err.strip() or out.strip()}",
            }
        return {"rev": out.strip(), "method": "explicit", "error": None}

    git_root = _find_git_root(workspace)
    if not git_root:
        return {"rev": None, "method": "none", "error": "not a git repository"}

    last_mb_error: str | None = None
    for branch in ("main", "master"):
        code, _, _ = _run_git(workspace, "rev-parse", "--verify", f"refs/heads/{branch}")
        if code != 0:
            code, _, _ = _run_git(
                workspace, "rev-parse", "--verify", f"refs/remotes/origin/{branch}"
            )
            ref = f"origin/{branch}" if code == 0 else None
        else:
            ref = branch
        if not ref:
            continue
        code, out, err = _run_git(workspace, "merge-base", "HEAD", ref)
        if code == 0 and out.strip():
            return {
                "rev": out.strip(),
                "method": f"merge-base:{ref}",
                "error": None,
            }
        last_mb_error = err.strip() or f"merge-base failed for {ref}"
        # Try the other default branch before giving up.
        continue

    # HEAD+WT: parent of tip so last commit + working tree are in range.
    code, out, err = _run_git(workspace, "rev-parse", "--verify", "HEAD~1")
    if code == 0 and out.strip():
        return {"rev": out.strip(), "method": "HEAD+WT", "error": None}

    code, out, err = _run_git(workspace, "rev-parse", "HEAD")
    if code != 0:
        return {
            "rev": None,
            "method": "HEAD+WT",
            "error": last_mb_error or err.strip() or "cannot resolve HEAD",
        }
    # Root commit: diff empty tree → HEAD + WT includes the tip commit.
    return {"rev": EMPTY_TREE, "method": "HEAD+WT", "error": None}


def _looks_like_command(text: str) -> bool:
    s = text.strip()
    if not s or len(s) < 3:
        return False
    if s.startswith("http://") or s.startswith("https://"):
        return False
    if CMD_PREFIX_RE.match(s):
        return True
    if PIPE_OR_CHAIN_RE.search(s):
        return True
    if " " not in s and re.search(r"\.(?:py|sh)$", s, re.IGNORECASE):
        return False
    return " " in s and not re.fullmatch(
        r"[\w./-]+\.(?:py|sh|md|json|yaml|yml)", s, re.I
    )


def _extract_commands(content: str) -> list[str]:
    seen: set[str] = set()
    commands: list[str] = []
    for m in BACKTICK_RE.finditer(content):
        raw = m.group(1).strip()
        if _looks_like_command(raw) and raw not in seen:
            seen.add(raw)
            commands.append(raw)
    return commands


def _filter_todos(
    todos: list,
    todo_id: str | None,
    phase_name: str | None,
    is_project: bool,
) -> tuple[list, str | None]:
    if todo_id:
        matched = [t for t in todos if t.id == todo_id]
        if not matched:
            return [], f"todo id not found: {todo_id}"
        return matched, None
    if phase_name:
        if not is_project:
            return [], "phase scope not applicable (flat plan)"
        key = phase_name.casefold()
        matched = [
            t for t in todos if t.phase_name and t.phase_name.casefold() == key
        ]
        if not matched:
            return [], f"phase not found: {phase_name}"
        return matched, None
    return todos, None


def _section_body(plan_body: str, heading: str) -> str | None:
    matches = list(SECTION_RE.finditer(plan_body))
    for i, m in enumerate(matches):
        if m.group(1).casefold() != heading.casefold():
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(plan_body)
        # Prefer cut at next ## of any kind
        next_h2 = re.search(r"^##\s+", plan_body[start:], re.MULTILINE)
        if next_h2:
            end = start + next_h2.start()
        return plan_body[start:end]
    return None


def _strip_cell(cell: str) -> str:
    return cell.strip().strip("`").strip()


def _parse_path_table(section_text: str | None) -> tuple[list[dict], bool]:
    """Return (rows, inventory_incomplete). None. → empty."""
    if section_text is None:
        return [], False
    text = section_text.strip()
    if not text or NONE_RE.match(text.splitlines()[0].strip() if text else ""):
        # Entire section is None. or only None. before tables
        lines_nonempty = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if not lines_nonempty or (
            len(lines_nonempty) == 1 and NONE_RE.match(lines_nonempty[0])
        ):
            return [], False
        if lines_nonempty and NONE_RE.match(lines_nonempty[0]) and len(lines_nonempty) == 1:
            return [], False

    inventory_incomplete = bool(ABBREV_RE.search(text))
    rows: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not TABLE_ROW_RE.match(line):
            continue
        cells = [_strip_cell(c) for c in line.strip("|").split("|")]
        if not cells:
            continue
        path = cells[0]
        # Skip header / separator
        if path.casefold() in {"path", ""}:
            continue
        if set(path) <= {"-", ":", " "}:
            continue
        if NONE_RE.match(path):
            continue
        # Skip "and N similar" pseudo-rows
        if ABBREV_RE.search(path):
            inventory_incomplete = True
            continue
        rows.append(
            {
                "path": path,
                "detail": cells[1] if len(cells) > 1 else "",
                "reason": cells[2] if len(cells) > 2 else "",
            }
        )
    # Section that is only "None." after stripping tables
    if not rows:
        compact = re.sub(r"\s+", " ", text).strip()
        if NONE_RE.match(compact) or compact.casefold().startswith("none."):
            return [], inventory_incomplete
    return rows, inventory_incomplete


def _norm_repo_path(path: str, workspace: Path) -> str:
    raw = path.strip().strip("`").replace("\\", "/")
    if raw.startswith("./"):
        raw = raw[2:]
    try:
        p = Path(raw)
        if p.is_absolute():
            try:
                raw = str(p.resolve().relative_to(workspace.resolve())).replace("\\", "/")
            except ValueError:
                raw = p.name
    except OSError:
        pass
    return raw.lstrip("/")


def _should_ignore_unplanned(path: str) -> bool:
    norm = path.replace("\\", "/")
    name = Path(norm).name
    if name in IGNORE_PATH_NAMES:
        return True
    for pref in IGNORE_PATH_PREFIXES:
        if norm.startswith(pref) or f"/{pref}" in f"/{norm}":
            return True
    for suf in IGNORE_PATH_SUFFIXES:
        if norm.endswith(suf):
            return True
    return False


def _is_code_path(path: str) -> bool:
    return Path(path).suffix.lower() in CODE_EXTENSIONS


def _git_name_status(workspace: Path, baseline: str) -> list[tuple[str, str, str | None]]:
    """Return list of (status_letter, path, rename_from_or_None).

    Uses baseline→working-tree so tip commit and uncommitted edits are included.
    Untracked files appear as additions (A).
    """
    by_path: dict[str, tuple[str, str, str | None]] = {}
    code, out, _ = _run_git(
        workspace, "diff", "--name-status", "--find-renames", baseline
    )
    if code == 0:
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            status = parts[0][0].upper()
            if status in {"R", "C"} and len(parts) >= 3:
                old_p = parts[1].replace("\\", "/")
                new_p = parts[2].replace("\\", "/")
                by_path[new_p] = (status, new_p, old_p)
                # Old path was removed by rename — record for Removals claims.
                by_path.setdefault(old_p, ("D", old_p, None))
                continue
            path = parts[1].replace("\\", "/")
            by_path[path] = (status, path, None)

    # Untracked (not ignored) paths — treat as additions.
    code, out, _ = _run_git(
        workspace, "ls-files", "--others", "--exclude-standard", "-z"
    )
    if code == 0 and out:
        for raw in out.split("\0"):
            path = raw.replace("\\", "/").strip()
            if not path or path in by_path:
                continue
            by_path[path] = ("A", path, None)

    return list(by_path.values())


def _count_file_lines(workspace: Path, rel: str) -> int:
    path = workspace / rel
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def _git_numstat_code_loc(workspace: Path, baseline: str) -> int:
    """Code LOC since baseline: one baseline→WT numstat + untracked code line counts.

    Avoids merging multiple diffs per path (which under-counted when WT overwrote
    committed numstat). Untracked code files are included so bugbot_default can
    turn on for new-only work.
    """
    path_loc: dict[str, int] = {}
    code, out, _ = _run_git(workspace, "diff", "--numstat", baseline)
    if code == 0:
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            added_s, deleted_s, path = parts[0], parts[1], parts[2].replace("\\", "/")
            if " => " in path:
                path = path.split(" => ")[-1].strip("{}")
            if not _is_code_path(path):
                continue
            if added_s == "-" or deleted_s == "-":
                continue
            try:
                loc = int(added_s) + int(deleted_s)
            except ValueError:
                continue
            path_loc[path] = loc

    code, out, _ = _run_git(
        workspace, "ls-files", "--others", "--exclude-standard", "-z"
    )
    if code == 0 and out:
        for raw in out.split("\0"):
            path = raw.replace("\\", "/").strip()
            if not path or not _is_code_path(path) or path in path_loc:
                continue
            path_loc[path] = _count_file_lines(workspace, path)

    return sum(path_loc.values())


def _expected_change_type(table: str) -> str:
    return {"additions": "A", "modifications": "M", "removals": "D"}[table]


def _status_for_claimed(
    expected: str,
    git_status: str | None,
    path_exists: bool,
) -> str:
    """Scaffold only: present | missing | wrong_change_type."""
    if expected == "A":
        if git_status in GIT_ADD or (git_status is None and path_exists):
            # present as addition or already on disk without git add signal
            if git_status in GIT_DEL:
                return "wrong_change_type"
            if git_status in GIT_MOD:
                return "wrong_change_type"
            if git_status in GIT_ADD or path_exists:
                return "present"
            return "missing"
        if path_exists and git_status is None:
            return "present"
        return "missing"
    if expected == "M":
        if git_status in GIT_MOD or git_status in GIT_ADD:
            return "present" if git_status in GIT_MOD else "wrong_change_type"
        if git_status in GIT_DEL:
            return "wrong_change_type"
        if path_exists:
            # modified claimed but no diff — still "present" on disk; agent judges content
            return "present"
        return "missing"
    # expected D — rename-away (R) counts as removed from the old path.
    if git_status in GIT_DEL or git_status == "R":
        return "present"
    if git_status in GIT_MOD or git_status in {"A", "C"}:
        return "wrong_change_type"
    if not path_exists:
        return "present"  # already gone
    return "missing"  # still on disk, not deleted in diff


def _path_exists(workspace: Path, rel: str) -> bool:
    return (workspace / rel).exists()


def build_evidence(
    plan_path: Path,
    workspace: Path,
    todo_id: str | None = None,
    phase_name: str | None = None,
    base: str | None = None,
) -> dict:
    plan = plan_lib.read_plan(plan_path)
    todos, scope_error = _filter_todos(
        plan.todos, todo_id, phase_name, plan.is_project
    )

    baseline_info = _resolve_baseline(workspace, base)
    baseline_rev = baseline_info["rev"]

    additions, inc_a = _parse_path_table(_section_body(plan.body, "Additions"))
    modifications, inc_m = _parse_path_table(_section_body(plan.body, "Modifications"))
    removals, inc_r = _parse_path_table(_section_body(plan.body, "Removals"))
    inventory_incomplete = inc_a or inc_m or inc_r

    git_rows: list[tuple[str, str, str | None]] = []
    git_by_path: dict[str, str] = {}
    code_loc = 0
    git_error = baseline_info.get("error")

    if baseline_rev:
        git_rows = _git_name_status(workspace, baseline_rev)
        for status, path, old in git_rows:
            git_by_path[path] = status
            # Rename rows: new path keeps R/C; old path already recorded as D in
            # _git_name_status. Do not overwrite old path with R.
            if old and old not in git_by_path:
                git_by_path[old] = "D"
        code_loc = _git_numstat_code_loc(workspace, baseline_rev)
    elif not git_error:
        git_error = "no baseline revision"

    claimed: list[dict] = []
    claimed_paths: set[str] = set()

    def _add_claimed(table: str, row: dict) -> None:
        rel = _norm_repo_path(row["path"], workspace)
        claimed_paths.add(rel)
        expected = _expected_change_type(table)
        gstatus = git_by_path.get(rel)
        exists = _path_exists(workspace, rel)
        status = _status_for_claimed(expected, gstatus, exists)
        claimed.append(
            {
                "table": table,
                "path": rel,
                "raw_path": row["path"],
                "expected_change": expected,
                "git_status": gstatus,
                "path_exists": exists,
                "status": status,
                "detail": row.get("detail", ""),
                "reason": row.get("reason", ""),
            }
        )

    for row in additions:
        _add_claimed("additions", row)
    for row in modifications:
        _add_claimed("modifications", row)
    for row in removals:
        _add_claimed("removals", row)

    unplanned: list[dict] = []
    for status, path, old in git_rows:
        if path in claimed_paths or (old and old in claimed_paths):
            continue
        if _should_ignore_unplanned(path):
            continue
        # Also skip if claimed under old name for renames
        if old and old in claimed_paths:
            continue
        unplanned.append(
            {
                "path": path,
                "git_status": status,
                "rename_from": old,
            }
        )

    if code_loc <= 0:
        bugbot_default = "off"
    elif code_loc <= BUGBOT_LOC_MAX:
        bugbot_default = "on"
    else:
        bugbot_default = "off"

    todo_rows: list[dict] = []
    for t in todos:
        todo_rows.append(
            {
                "id": t.id,
                "status": t.status,
                "phase": t.phase_name,
                "content_preview": t.content[:200]
                + ("…" if len(t.content) > 200 else ""),
                "commands": _extract_commands(t.content),
            }
        )

    has_close_line = bool(
        re.search(r"\*\*Plan\s+build:\*\*\s*complete\b", plan.body, re.IGNORECASE)
    )

    return {
        "schema": 2,
        "plan": str(plan.path),
        "workspace": str(workspace),
        "is_project": plan.is_project,
        "baseline": {
            "rev": baseline_rev,
            "method": baseline_info["method"],
            "error": git_error,
        },
        "scope": {
            "todo_id": todo_id,
            "phase": phase_name,
            "todo_count": len(todo_rows),
            "error": scope_error,
        },
        "plan_build_complete_line": has_close_line,
        "inventory_incomplete": inventory_incomplete,
        "claimed": claimed,
        "unplanned": unplanned,
        "code_loc": code_loc,
        "bugbot_default": bugbot_default,
        "bugbot_loc_max": BUGBOT_LOC_MAX,
        "todos": todo_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A/M/R inventory assist for owcc-plan-review-execution.",
    )
    parser.add_argument("plan", type=Path, help="Path to plan file")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--todo", metavar="ID", help="Scope to one todo id")
    parser.add_argument("--phase", metavar="NAME", help="Scope to phase name")
    parser.add_argument(
        "--workspace",
        metavar="PATH",
        help="Workspace root for file resolution (default: git root or plan parent)",
    )
    parser.add_argument(
        "--base",
        metavar="REV",
        help="Git baseline revision (default: merge-base main/master, else HEAD)",
    )
    args = parser.parse_args()

    try:
        plan_path = args.plan.expanduser().resolve()
        workspace = _resolve_workspace(plan_path, args.workspace)
        data = build_evidence(
            plan_path, workspace, args.todo, args.phase, args.base
        )
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Plan: {data['plan']}")
        print(f"Workspace: {data['workspace']}")
        print(
            f"Baseline: {data['baseline']['method']} "
            f"{data['baseline']['rev'] or '—'} "
            f"{data['baseline']['error'] or ''}".rstrip()
        )
        if data["scope"]["error"]:
            print(f"Scope error: {data['scope']['error']}")
        print(f"Claimed: {len(data['claimed'])}  Unplanned: {len(data['unplanned'])}")
        print(f"code_loc: {data['code_loc']}  bugbot_default: {data['bugbot_default']}")
        if data["inventory_incomplete"]:
            print("inventory_incomplete: true")
        for row in data["claimed"]:
            print(f"  [{row['table']}] {row['path']}: {row['status']}")
        for row in data["unplanned"][:20]:
            print(f"  [unplanned] {row['git_status']} {row['path']}")
        if len(data["unplanned"]) > 20:
            print(f"  … {len(data['unplanned']) - 20} more unplanned")

    return 1 if data["scope"]["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
