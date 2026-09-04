#!/usr/bin/env python3
"""Print YAML frontmatter summary for Cursor rule files (*.mdc) (no PyYAML).

Default rules directory: `<repo>/.cursor/rules`. Override with --rules-dir.

Emits TSV: path<TAB>alwaysApply<TAB>description<TAB>globs
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    i = 1
    buf_key: str | None = None
    buf_val: list[str] = []
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            if buf_key is not None:
                data[buf_key] = "\n".join(buf_val).strip()
            key, _, rest = line.partition(":")
            buf_key = key.strip()
            buf_val = [rest.strip()]
        elif buf_key is not None and (line.startswith(" ") or line.startswith("\t")):
            buf_val.append(line.strip())
        i += 1
    if buf_key is not None:
        data[buf_key] = "\n".join(buf_val).strip()
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="Repository root")
    ap.add_argument(
        "--rules-dir",
        default=".cursor/rules",
        help="Rules directory relative to repo (default: .cursor/rules)",
    )
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    rules_dir = (repo / args.rules_dir).resolve()
    if not rules_dir.is_dir():
        print(f"warning: no .cursor/rules directory: {rules_dir}", file=sys.stderr)
        return 0

    paths = sorted(rules_dir.glob("*.mdc"))
    if not paths:
        print(f"warning: no .mdc files under {rules_dir}", file=sys.stderr)
        return 0

    print("path\talwaysApply\tdescription\tglobs")
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = _parse_frontmatter(text)
        desc = fm.get("description", "").replace("\t", " ").replace("\n", " ")
        globs = fm.get("globs", "").replace("\t", " ").replace("\n", " ")
        always = fm.get("alwaysApply", "").strip().lower()
        rel = path.relative_to(repo).as_posix()
        print(f"{rel}\t{always}\t{desc}\t{globs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
