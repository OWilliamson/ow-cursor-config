#!/usr/bin/env python3
"""Verify paths exist relative to --repo (files or directories).

Reads newline-separated paths from --from-stdin or --from-file. Lines starting
with # and empty lines are ignored. Prints missing paths to stderr; exits 1
if any missing.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _read_paths(args: argparse.Namespace) -> list[str]:
    lines: list[str] = []
    if args.from_stdin:
        lines.extend(sys.stdin.read().splitlines())
    elif args.from_file:
        p = Path(args.from_file)
        lines.extend(p.read_text(encoding="utf-8", errors="replace").splitlines())
    out: list[str] = []
    for raw in lines:
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="Repository root")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--from-stdin", action="store_true", help="Read paths from stdin")
    g.add_argument("--from-file", help="Read paths from a file (newline-separated)")
    ap.add_argument("--quiet", action="store_true", help="Only print missing paths")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"error: --repo is not a directory: {repo}", file=sys.stderr)
        return 2

    paths = _read_paths(args)
    if not paths:
        print("error: no paths to check", file=sys.stderr)
        return 2

    missing: list[str] = []
    for rel in paths:
        cand = repo / rel
        if cand.is_file() or cand.is_dir():
            if not args.quiet:
                print(f"OK {rel}")
        else:
            missing.append(rel)

    if missing:
        print("Missing paths:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
