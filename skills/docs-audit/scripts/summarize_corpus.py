#!/usr/bin/env python3
"""
Conservative corpus summarizer for the `docs-audit` skill.

Goal: extract compact evidence/facts to help the agent complete checks faster.
This script is NOT a replacement for judgment-heavy rubric scoring.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from collections import Counter
from typing import Any, Dict, List, Set


MD_EXTS = {".md", ".markdown"}


CODE_FENCE_RE = re.compile(r"^```.*$")


PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bComing\s+soon\b", re.IGNORECASE),
    re.compile(r"\bto\s+be\s+written\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
]

SECTION_HINTS = [
    "prerequisites",
    "installation",
    "configuration",
    "usage",
    "examples",
    "troubleshooting",
    "reference",
    "overview",
]


ENDPOINT_RE = re.compile(
    r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[-A-Za-z0-9_./{}]+)", re.IGNORECASE
)

# Captures `GET /path` style in text, and /path mentions inside backticks.
INLINE_BACKTICK_PATH_RE = re.compile(r"`(/[-A-Za-z0-9_./{}]+)`")


TIMEOUT_RE = re.compile(r"\btimeout\b[^0-9]*([0-9]+)\s*(ms|s)\b", re.IGNORECASE)


CLI_COMMAND_LINE_RE = re.compile(r"^\s*(\$|>|\+)\s+(?P<cmd>.+?)\s*$")

BACKTICK_TOKEN_RE = re.compile(r"`([A-Za-z0-9_.-]+)`")

# Environment variables (conservative).
ENV_VAR_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")


def _validate_target_path(target_path: str) -> str:
    target_path = os.path.abspath(target_path)
    if not os.path.isdir(target_path):
        raise ValueError(f"target_path is not a directory: {target_path}")
    return target_path


def _generated_at() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _iter_markdown_files(root: str) -> List[str]:
    out: List[str] = []
    root = os.path.abspath(root)
    for cur, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", ".github"} and not d.startswith(".")]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in MD_EXTS:
                out.append(os.path.join(cur, fn))
    return sorted(out)


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _extract_code_fences(md: str) -> List[str]:
    fences: List[str] = []
    lines = md.splitlines()
    in_code = False
    buff: List[str] = []
    for line in lines:
        if CODE_FENCE_RE.match(line.strip()):
            if in_code:
                fences.append("\n".join(buff))
                buff = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            buff.append(line)
    if buff:
        # Unclosed fence; ignore.
        pass
    return fences


def _extract_cli_from_block(block: str) -> Set[str]:
    cmds: Set[str] = set()
    for line in block.splitlines():
        m = CLI_COMMAND_LINE_RE.match(line)
        if m:
            cmd = m.group("cmd").strip()
            if cmd:
                cmds.add(cmd)
        # Also look for common command starters inside code.
        stripped = line.strip()
        if re.match(r"^(curl|python|pip|npm|yarn|pnpm|git|docker|kubectl|psql)\b", stripped):
            cmds.add(stripped)
    return cmds


def _extract_endpoints(md: str, code_fences: List[str]) -> Set[str]:
    endpoints: Set[str] = set()
    # In code fences and plain text.
    for fence in code_fences:
        for m in ENDPOINT_RE.finditer(fence):
            endpoints.add(f"{m.group(1).upper()} {m.group(2)}")

    for m in ENDPOINT_RE.finditer(md):
        endpoints.add(f"{m.group(1).upper()} {m.group(2)}")

    # Also gather backticked /paths (useful for completeness check).
    for m in INLINE_BACKTICK_PATH_RE.finditer(md):
        endpoints.add(m.group(1))
    return endpoints


def _extract_timeouts(md: str) -> List[str]:
    hits: List[str] = []
    for m in TIMEOUT_RE.finditer(md):
        hits.append(f"{m.group(1)}{m.group(2).lower()}")
    return hits


def _extract_placeholders(md: str) -> List[str]:
    hits: List[str] = []
    for pat in PLACEHOLDER_PATTERNS:
        if pat.search(md):
            hits.append(pat.pattern)
    return sorted(set(hits))


def _extract_versions(md: str) -> List[str]:
    versions: Set[str] = set()
    # Match dotted semantic-like versions (e.g., 6.14.1, 7.0.0).
    for m in re.finditer(r"\b\d+\.\d+(?:\.\d+)?\b", md):
        v = m.group(0)
        # Avoid common year patterns.
        if v.startswith(("20", "19")) and len(v) <= 5:
            continue
        versions.add(v)
    return sorted(versions)


def _extract_env_vars(md: str) -> List[str]:
    hits: Set[str] = set()
    for m in ENV_VAR_RE.finditer(md):
        hits.add(m.group(0))
    return sorted(hits)


def _extract_headings(md: str) -> List[str]:
    headings: List[str] = []
    in_code = False
    for line in md.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.append(match.group(1).strip())
    return headings


def _section_shape(headings: List[str]) -> Dict[str, Any]:
    lower_headings = [h.lower() for h in headings]
    present_hints = [hint for hint in SECTION_HINTS if any(hint in h for h in lower_headings)]
    return {
        "headings": headings[:100],
        "section_hints_present": present_hints,
        "has_examples_section": "examples" in present_hints,
        "has_troubleshooting_section": "troubleshooting" in present_hints,
        "has_prerequisites_section": "prerequisites" in present_hints,
    }


def _workflow_evidence(md: str, commands: Set[str], endpoints: Set[str]) -> Dict[str, Any]:
    numbered_steps = len(re.findall(r"^\s*\d+[.)]\s+", md, flags=re.M))
    return {
        "numbered_step_count": numbered_steps,
        "has_numbered_steps": numbered_steps > 0,
        "has_code_fence": "```" in md,
        "commands_found_count": len(commands),
        "endpoints_found_count": len(endpoints),
    }


def _extract_config_like_tokens(md: str) -> List[str]:
    # Backticked tokens that look like config keys.
    keys: Set[str] = set()
    for tok in BACKTICK_TOKEN_RE.findall(md):
        if "." in tok or "_" in tok or "-" in tok:
            if any(x in tok.lower() for x in ["auth", "config", "env", "token", "key", "timeout", "url", "endpoint"]):
                keys.add(tok)
    return sorted(keys)


def summarize_corpus(target_path: str) -> Dict[str, Any]:
    target_path = _validate_target_path(target_path)
    files = _iter_markdown_files(target_path)

    per_file: List[Dict[str, Any]] = []
    unreadable_files: List[Dict[str, str]] = []
    all_endpoints: Set[str] = set()
    all_timeouts: List[str] = []
    all_versions: Set[str] = set()
    all_env_vars: Set[str] = set()
    all_placeholder_hits: Set[str] = set()
    all_commands: Set[str] = set()
    all_backticked_config_keys: Set[str] = set()

    for fp in files:
        try:
            md = _read_text(fp)
        except OSError as e:
            unreadable_files.append({"file": fp, "error": f"{type(e).__name__}: {e}"})
            continue

        code_fences = _extract_code_fences(md)
        endpoints = _extract_endpoints(md, code_fences)
        timeouts = _extract_timeouts(md)
        versions = set(_extract_versions(md))
        env_vars = set(_extract_env_vars(md))
        placeholders = _extract_placeholders(md)

        commands: Set[str] = set()
        for fence in code_fences:
            commands |= _extract_cli_from_block(fence)

        # Include inline `$ ...`-style outside fences too.
        for line in md.splitlines():
            m = CLI_COMMAND_LINE_RE.match(line)
            if m:
                commands.add(m.group("cmd").strip())

        config_keys = set(_extract_config_like_tokens(md))
        headings = _extract_headings(md)
        section_shape = _section_shape(headings)
        workflow_evidence = _workflow_evidence(md, commands, endpoints)

        all_endpoints |= endpoints
        all_timeouts.extend(timeouts)
        all_versions |= versions
        all_env_vars |= env_vars
        all_placeholder_hits |= set(placeholders)
        all_commands |= commands
        all_backticked_config_keys |= config_keys

        per_file.append(
            {
                "file": fp,
                "endpoints_found": sorted(endpoints)[:200],
                "timeout_values_found": timeouts[:50],
                "versions_found": sorted(versions),
                "env_vars_found": sorted(env_vars),
                "placeholder_hints": placeholders,
                "commands_found": sorted(commands)[:200],
                "config_key_candidates": sorted(config_keys)[:200],
                "section_shape": section_shape,
                "workflow_evidence": workflow_evidence,
            }
        )

    timeout_counts = Counter(all_timeouts)
    repeated_timeout_values = [k for k, v in timeout_counts.items() if v >= 2]

    # Conflict heuristic: if multiple timeout values exist at all.
    timeout_values_sorted = sorted(timeout_counts.keys())
    timeout_conflict = len(timeout_values_sorted) >= 2

    return {
        "target_path": target_path,
        "generated_at": _generated_at(),
        "files_scanned": len(per_file),
        "unreadable_files": unreadable_files,
        "summary": {
            "endpoints_found_count": len(all_endpoints),
            "endpoints_found": sorted(all_endpoints)[:500],
            "commands_found_count": len(all_commands),
            "commands_found": sorted(all_commands)[:500],
            "env_vars_found": sorted(all_env_vars)[:500],
            "config_key_candidates": sorted(all_backticked_config_keys)[:500],
            "versions_found": sorted(all_versions)[:500],
            "placeholder_hints": sorted(all_placeholder_hits),
            "timeout_values_counts": dict(timeout_counts),
            "timeout_conflict_heuristic": timeout_conflict,
            "repeated_timeout_values": sorted(repeated_timeout_values),
        },
        "per_file": per_file,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target_path", help="Root docs directory to summarize; emits read-only JSON evidence to stdout")
    args = ap.parse_args()

    try:
        payload = summarize_corpus(args.target_path)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

