#!/usr/bin/env python3
"""
Internal documentation link checker for the `docs-audit` skill.

This script is conservative:
- It checks that Markdown targets exist within the scanned corpus.
- It checks anchor existence by best-effort slug/id matching.
- It records external HTTP(S) links as skipped external evidence.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple


MD_EXTS = {".md", ".markdown"}


def _validate_target_path(target_path: str) -> str:
    target_path = os.path.abspath(target_path)
    if not os.path.isdir(target_path):
        raise ValueError(f"target_path is not a directory: {target_path}")
    return target_path


def _generated_at() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _slugify_heading(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s


def _extract_headings_and_ids(md: str) -> Tuple[List[str], List[str]]:
    """
    Returns: (heading_slugs, explicit_ids)
    """
    heading_slugs: List[str] = []
    explicit_ids: List[str] = []

    in_code = False
    for line in md.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            heading_slugs.append(_slugify_heading(m.group(2)))

    # Explicit HTML ids/names (best-effort).
    for m in re.finditer(r'\b(?:id|name)\s*=\s*["\']([^"\']+)["\']', md):
        explicit_ids.append(m.group(1))

    return heading_slugs, explicit_ids


def _iter_markdown_files(root: str) -> List[str]:
    out: List[str] = []
    for cur, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", ".github"} and not d.startswith(".")]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in MD_EXTS:
                out.append(os.path.join(cur, fn))
    return sorted(out)


def _extract_markdown_links(md: str) -> List[Tuple[str, str]]:
    """
    Returns list of (label, url) for markdown links: [label](url).
    Excludes images: ![alt](url).
    """
    links: List[Tuple[str, str]] = []

    # Negative lookbehind for ! to exclude images.
    pattern = re.compile(r"(?<!\!)\[(?P<label>[^\]]+)\]\((?P<url>[^)]+)\)")
    for m in pattern.finditer(md):
        url = (m.group("url") or "").strip()
        label = (m.group("label") or "").strip()
        if not url:
            continue
        links.append((label, url))
    return links


def _split_url(url: str) -> Tuple[str, str]:
    # Split only on the first '#'
    if "#" in url:
        base, frag = url.split("#", 1)
        return base, frag
    return url, ""


def _resolve_target_file(
    from_path: str, target_root: str, base: str
) -> Optional[str]:
    """
    Returns resolved absolute path within target_root, or None if it cannot be resolved.
    """
    base = base.strip()
    if base == "" or base.startswith("#"):
        return from_path

    # Absolute URL roots are handled elsewhere.
    if base.startswith("http://") or base.startswith("https://"):
        return None

    if base.startswith("/"):
        rel = base.lstrip("/")
        cand = os.path.join(target_root, rel)
    else:
        cand = os.path.normpath(os.path.join(os.path.dirname(from_path), base))
    cand = os.path.abspath(cand)

    # Ensure target stays within the scanned corpus.
    if not cand.startswith(os.path.abspath(target_root) + os.sep) and cand != os.path.abspath(target_root):
        return None
    return cand


def _anchor_exists(target_md: str, fragment: str) -> bool:
    fragment = fragment.strip()
    if not fragment:
        return True
    fragment = fragment.lstrip("#")

    heading_slugs, explicit_ids = _extract_headings_and_ids(target_md)
    if fragment in heading_slugs or fragment in explicit_ids:
        return True

    # Also accept common rendered heading ids like GitHub style with prefix.
    # Best-effort: treat fragment as substring in id/name attributes.
    if re.search(r'\b(?:id|name)\s*=\s*["\']' + re.escape(fragment) + r'["\']', target_md):
        return True
    # As a last resort, check whether it appears in an anchor link.
    return ("#" + fragment) in target_md


def check_links(target_path: str) -> Dict[str, Any]:
    target_root = _validate_target_path(target_path)
    files = _iter_markdown_files(target_root)

    internal_links: List[Dict[str, Any]] = []
    missing_targets: List[Dict[str, Any]] = []
    missing_anchors: List[Dict[str, Any]] = []
    external_links: List[Dict[str, Any]] = []
    unreadable_files: List[Dict[str, str]] = []

    for from_path in files:
        try:
            md = open(from_path, "r", encoding="utf-8", errors="replace").read()
        except OSError as e:  # pragma: no cover
            unreadable_files.append({"file": from_path, "error": f"{type(e).__name__}: {e}"})
            continue

        links = _extract_markdown_links(md)
        for _label, raw_url in links:
            base, frag = _split_url(raw_url)
            raw_url_stripped = raw_url.strip()

            if raw_url_stripped.startswith("http://") or raw_url_stripped.startswith("https://"):
                external_links.append({"url": raw_url_stripped, "status": "external_not_checked"})
                continue

            resolved = _resolve_target_file(from_path, target_root, base)
            if resolved is None:
                internal_links.append(
                    {"from": from_path, "url": raw_url_stripped, "resolved": None, "status": "unresolved"}
                )
                continue

            if not os.path.exists(resolved):
                missing_target = {"from": from_path, "url": raw_url_stripped, "resolved_to": resolved}
                missing_targets.append(missing_target)
                internal_links.append(
                    {"from": from_path, "url": raw_url_stripped, "resolved": resolved, "status": "missing_target"}
                )
                continue

            # If there's a fragment, validate anchor best-effort.
            if frag.strip():
                try:
                    target_md = open(resolved, "r", encoding="utf-8", errors="replace").read()
                except OSError as e:  # pragma: no cover
                    unreadable_files.append({"file": resolved, "error": f"{type(e).__name__}: {e}"})
                    internal_links.append(
                        {"from": from_path, "url": raw_url_stripped, "resolved": resolved, "status": "unreadable_target"}
                    )
                    continue
                if not _anchor_exists(target_md, frag):
                    missing_anchors.append(
                        {
                            "from": from_path,
                            "url": raw_url_stripped,
                            "resolved_to": resolved,
                            "anchor": frag.strip().lstrip("#"),
                        }
                    )
                    internal_links.append(
                        {"from": from_path, "url": raw_url_stripped, "resolved": resolved, "status": "missing_anchor"}
                    )
                    continue

            internal_links.append(
                {
                    "from": from_path,
                    "url": raw_url_stripped,
                    "resolved": resolved,
                    "status": "ok",
                }
            )

    return {
        "target_path": target_root,
        "generated_at": _generated_at(),
        "files_scanned": len(files),
        "unreadable_files": unreadable_files,
        "internal_links": internal_links,
        "missing_targets": missing_targets,
        "missing_anchors": missing_anchors,
        "external_links": external_links,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target_path", help="Root documentation directory to check; emits read-only JSON evidence to stdout")
    args = ap.parse_args()

    try:
        payload = check_links(args.target_path)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

