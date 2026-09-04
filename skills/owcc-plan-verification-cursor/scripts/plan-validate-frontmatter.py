#!/usr/bin/env python3
"""
Validate .plan.md YAML frontmatter after cursor-native plan edits.

Purpose: Fail when todos have empty content, root+phase duplication (isProject),
body references missing todo ids, or operator-only content in the plan body.

Dependencies: Python 3.9+ stdlib only.

Who runs: Agent after cursor-native plan file writes.

Exit codes: 0 = pass, 1 = fail (errors on stderr).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

UUID_ID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.I,
)
FIRST_ACTION = re.compile(
    r"\*\*First action:\*\*\s*`([^`]+)`",
    re.I,
)
FINAL_VALIDATION = re.compile(
    r"\*\*Final validation:\*\*\s*`([^`]+)`",
    re.I,
)
FORBIDDEN_BODY_LABELS = (
    "Execution route:",
    "Plan shape:",
    "Native chunks:",
    "Plan-change-composer role:",
    "Plan-build role:",
    "Plan-registry role:",
)


def _split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[3:end], text[end + 4 :]


def _parse_todo_blocks(yaml: str) -> list[dict[str, str]]:
    """Extract todo dicts with id, content, status from YAML-ish frontmatter."""
    todos: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in yaml.splitlines():
        if re.match(r"^\s*-\s+id:\s*", line):
            if current:
                todos.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif current is not None:
            m = re.match(r"^\s+content:\s*(.*)$", line)
            if m:
                val = m.group(1).strip()
                if (val.startswith('"') and val.endswith('"')) or (
                    val.startswith("'") and val.endswith("'")
                ):
                    val = val[1:-1]
                current["content"] = val
            m = re.match(r"^\s+status:\s*(\S+)", line)
            if m:
                current["status"] = m.group(1).strip()
    if current:
        todos.append(current)
    return todos


def _section_block(yaml: str, key: str) -> str:
    """Return YAML substring for top-level key until next top-level key."""
    pattern = re.compile(rf"^{re.escape(key)}:\s*$", re.M)
    m = pattern.search(yaml)
    if not m:
        return ""
    start = m.end()
    rest = yaml[start:]
    end_m = re.search(r"^[a-zA-Z][a-zA-Z0-9_-]*:\s", rest, re.M)
    block = rest[: end_m.start()] if end_m else rest
    return block


def _root_todos(yaml: str) -> list[dict[str, str]]:
    block = _section_block(yaml, "todos")
    if not block.strip():
        return []
    if re.match(r"^\s*\[\s*\]\s*$", block.strip()):
        return []
    return _parse_todo_blocks("todos:\n" + block)


def _phase_todos(yaml: str) -> list[dict[str, str]]:
    phases_block = _section_block(yaml, "phases")
    if not phases_block:
        return []
    return _parse_todo_blocks(phases_block)


def _is_project(yaml: str) -> bool:
    m = re.search(r"^isProject:\s*true\s*$", yaml, re.M | re.I)
    return bool(m)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)
    if not fm:
        errors.append("missing YAML frontmatter (--- delimiters)")
        return errors

    root = _root_todos(fm)
    phase = _phase_todos(fm)
    is_project = _is_project(fm)

    all_todos = root + phase
    if not all_todos:
        errors.append("no todos found in frontmatter (root or phases)")

    for t in all_todos:
        tid = t.get("id", "")
        content = t.get("content", "").strip()
        if not tid:
            errors.append("todo entry missing id")
            continue
        if not content:
            errors.append(f"todo {tid!r} has empty content")
        if UUID_ID.match(tid):
            errors.append(
                f"todo id {tid!r} looks like a Plan UI UUID — use stable kebab-case ids "
                f"(e.g. outlet-timing-impl); re-write frontmatter, do not let UI own ids"
            )

    if is_project:
        if root:
            errors.append(
                "isProject: true but root todos is not empty — set `todos: []` and put "
                "all work only under phases[].todos"
            )
        if not phase:
            errors.append("isProject: true but phases have no todos")
    elif phase and root:
        errors.append(
            "flat plan has both root todos and phases[].todos — pick one shape"
        )

    root_ids = {t["id"] for t in root if t.get("id")}
    phase_ids = {t["id"] for t in phase if t.get("id")}
    dup = root_ids & phase_ids
    if dup:
        errors.append(f"duplicate todo ids at root and in phases: {sorted(dup)}")

    ids_in_yaml = root_ids | phase_ids
    for m in (FIRST_ACTION, FINAL_VALIDATION):
        for ref in m.findall(body):
            if ref not in ids_in_yaml:
                errors.append(
                    f"body references todo {ref!r} but that id is not in frontmatter"
                )

    for label in FORBIDDEN_BODY_LABELS:
        if re.search(rf"\*\*{re.escape(label)}\*\*", body, re.I):
            errors.append(
                f"body contains operator-only '**{label}**' — remove from plan body"
            )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: plan-validate-frontmatter.py /absolute/path/to/plan.plan.md",
            file=sys.stderr,
        )
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2
    errors = validate(path)
    if errors:
        print(f"FAIL {path}", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
