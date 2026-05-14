#!/usr/bin/env python3
"""Extract repo-relative paths from hub markdown (links + conservative backticks).

Reads one or more hub files under --repo, emits unique POSIX-style paths
relative to repo root (when resolvable). For dead-link checks, pipe into
check_paths.py.

No third-party dependencies.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
BT_RE = re.compile(r"`([^`\n]+)`")

# Heuristic: backtick token looks like a repo path (not a shell flag or prose).
BT_SUFFIXES = (
    ".md",
    ".mdc",
    ".mdx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".sh",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".sql",
    ".jrxml",
    ".xml",
    ".zip",
)


def _external(target: str) -> bool:
    t = target.strip()
    return t.startswith(("http://", "https://", "mailto:", "//", "data:"))


def _strip_anchor(target: str) -> str:
    if "#" in target and not target.startswith("#"):
        return target.split("#", 1)[0]
    return target


def _glob_or_placeholder(s: str) -> bool:
    """True if string is a glob, placeholder, or pattern — not a single repo path."""
    if any(ch in s for ch in "*?[]<>|"):
        return True
    if "**" in s:
        return True
    return False


def _plausible_backtick(token: str) -> bool:
    s = token.strip()
    if not s or len(s) > 512 or "\n" in s:
        return False
    if _external(s) or s.startswith("#"):
        return False
    if " " in s:
        return False
    if _glob_or_placeholder(s):
        return False
    if s.startswith((".", "/", "..")) or "/" in s:
        if any(s.endswith(ext) for ext in BT_SUFFIXES):
            return True
        # directory-like: foo/bar (no extension) — allow short segments
        if "/" in s and not s.endswith("/") and ".." not in s.split("/"):
            parts = s.split("/")
            if len(parts) <= 8 and all(p and len(p) <= 80 for p in parts):
                return True
    return False


def _resolve_link(target: str, hub: Path, repo: Path) -> Path | None:
    t = _strip_anchor(target.strip())
    if not t or _external(t):
        return None
    if _glob_or_placeholder(t):
        return None
    # Ignore same-document anchors only
    if t.startswith("#"):
        return None
    # Absolute path on disk is unusual in markdown; treat as non-portable skip
    if t.startswith("/") and not t.startswith("//"):
        p = Path(t)
        if p.is_absolute():
            try:
                return p.resolve().relative_to(repo.resolve())
            except ValueError:
                return None
    base = hub.parent
    cand = (base / t).resolve()
    try:
        return cand.relative_to(repo.resolve())
    except ValueError:
        return None


def _resolve_backtick(token: str, hub: Path, repo: Path) -> Path | None:
    s = token.strip()
    if not _plausible_backtick(s):
        return None
    # Backtick paths are usually repo-relative from root
    if s.startswith("./"):
        s = s[2:]
    if s.startswith("../"):
        cand = (hub.parent / s).resolve()
    else:
        cand = (repo / s).resolve()
    try:
        return cand.relative_to(repo.resolve())
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="Repository root")
    ap.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Hub files relative to repo root (e.g. AGENTS.md docs/README.md)",
    )
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"error: --repo is not a directory: {repo}", file=sys.stderr)
        return 2

    out: set[str] = set()
    for rel in args.files:
        hub = (repo / rel).resolve()
        if not hub.is_file():
            print(f"warning: hub file missing, skipping: {rel}", file=sys.stderr)
            continue
        text = hub.read_text(encoding="utf-8", errors="replace")

        for m in LINK_RE.finditer(text):
            target = m.group(2).strip()
            p = _resolve_link(target, hub, repo)
            if p is not None and not _glob_or_placeholder(p.as_posix()):
                out.add(p.as_posix())

        for m in BT_RE.finditer(text):
            p = _resolve_backtick(m.group(1), hub, repo)
            if p is not None and not _glob_or_placeholder(p.as_posix()):
                out.add(p.as_posix())

    for line in sorted(out):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
