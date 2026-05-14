#!/usr/bin/env python3
"""
Mechanical documentation scan for the `docs-audit` skill.

This script is intentionally conservative: it extracts evidence and potential issues
so the model can score against `CHECKLIST.md` without inventing facts.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple


try:
    import yaml  # type: ignore

    _HAVE_YAML = True
except Exception:  # pragma: no cover
    yaml = None  # type: ignore
    _HAVE_YAML = False


MD_EXTS = {".md", ".markdown"}
GENERIC_FILENAME_TOKENS = {
    "about",
    "advanced",
    "config",
    "configuration",
    "details",
    "doc",
    "docs",
    "documentation",
    "general",
    "guide",
    "info",
    "intro",
    "introduction",
    "misc",
    "notes",
    "overview",
    "readme",
    "reference",
    "setup",
    "summary",
    "topic",
}

NAMING_PATTERNS = {
    "lowercase-with-hyphens": re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.(?:md|markdown)$"),
    "lowercase-with-underscores": re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.(?:md|markdown)$"),
    "title-case": re.compile(r"^[A-Z][A-Za-z0-9]+(?:[ -][A-Z][A-Za-z0-9]+)*\.(?:md|markdown)$"),
}

CRITICAL_KEYWORDS = [
    "required",
    "warning",
    "prerequisite",
    "api key",
    "breaking change",
    "must",
    "mandatory",
]


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _validate_target_path(target_path: str) -> str:
    target_path = os.path.abspath(target_path)
    if not os.path.isdir(target_path):
        raise ValueError(f"target_path is not a directory: {target_path}")
    return target_path


def _generated_at() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _relpath(path: str, root: str) -> str:
    return os.path.relpath(path, root)


def _iso_date_or_none(s: Any) -> Optional[str]:
    if not isinstance(s, str):
        return None
    s = s.strip()
    if not s:
        return None
    # Expect YYYY-MM-DD
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    return None


def _parse_front_matter(md: str) -> Tuple[bool, Dict[str, Any], List[str]]:
    """
    Parses YAML front matter delimited by leading '---' blocks.
    Returns: (has_front_matter, parsed_obj, issues)
    """

    issues: List[str] = []
    if not md.startswith("---"):
        return False, {}, issues

    # Find the closing delimiter on its own line.
    lines = md.splitlines()
    if not lines or not lines[0].strip().startswith("---"):
        return False, {}, issues

    end_idx = None
    for i in range(1, min(len(lines), 2000)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        issues.append("front_matter_delimiter_not_closed")
        return True, {}, issues

    raw = "\n".join(lines[1:end_idx]).strip()
    if not raw:
        issues.append("front_matter_empty")
        return True, {}, issues

    if _HAVE_YAML:
        try:
            obj = yaml.safe_load(raw)  # type: ignore[no-untyped-call]
            if obj is None:
                obj = {}
            if not isinstance(obj, dict):
                issues.append("front_matter_not_a_mapping")
                return True, {}, issues
            return True, obj, issues
        except Exception as e:  # pragma: no cover
            issues.append(f"front_matter_yaml_parse_error:{type(e).__name__}")
            return True, {}, issues

    # Fallback conservative parsing without PyYAML.
    obj_fallback: Dict[str, Any] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        # Very small set of array heuristics.
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if inner:
                parts = [p.strip().strip("'").strip('"') for p in inner.split(",")]
                obj_fallback[key] = [p for p in parts if p]
            else:
                obj_fallback[key] = []
        else:
            # Strip quotes but keep as string.
            obj_fallback[key] = value.strip("'").strip('"')

    issues.append("front_matter_parsed_without_yaml_library")
    return True, obj_fallback, issues


def _first_h1(md: str) -> Optional[str]:
    in_code = False
    for line in md.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^#\s+", line):
            return line.strip().lstrip("#").strip()
    return None


def _extract_headings(md: str) -> List[Tuple[int, str]]:
    """
    Returns list of (level, heading_text).
    Excludes fenced code blocks.
    """
    headings: List[Tuple[int, str]] = []
    in_code = False
    for line in md.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2).strip()
        headings.append((level, text))
    return headings


def _dominant_naming(files: List[str]) -> Tuple[str, Dict[str, int], List[Dict[str, str]]]:
    """
    Determine dominant filename style among markdown files.
    Returns: (dominant_style, counts, deviations)
    """

    counts: Dict[str, int] = {k: 0 for k in NAMING_PATTERNS.keys()}
    deviations: List[Dict[str, str]] = []

    for path in files:
        name = os.path.basename(path)
        matched = False
        for style, rx in NAMING_PATTERNS.items():
            if rx.match(name):
                counts[style] += 1
                matched = True
                break
        if not matched:
            deviations.append({"file": name, "reason": "unmatched_naming_pattern"})
        # Space/special char signals
        if " " in name:
            deviations.append({"file": name, "reason": "contains_spaces"})
        if re.search(r"[^A-Za-z0-9._-]", name):
            deviations.append({"file": name, "reason": "contains_special_characters"})

        # Basic date stamp heuristic: if YYYY-MM-DD appears, ensure it's valid.
        # If other formats appear, we flag separately.
        if re.search(r"\d{4}[-_]\d{2}[-_]\d{2}", name):
            if re.search(r"\d{4}_\d{2}_\d{2}", name):
                deviations.append({"file": name, "reason": "date_stamp_underscore_format"})
            if re.search(r"\d{4}[-]\d{2}[-]\d{2}", name) is None:
                deviations.append({"file": name, "reason": "unknown_date_stamp_format"})

    dominant = max(counts.items(), key=lambda kv: kv[1])[0] if files else "unknown"
    return dominant, counts, deviations


def _detected_naming_style(name: str) -> str:
    for style, rx in NAMING_PATTERNS.items():
        if rx.match(name):
            return style
    return "unmatched"


def _filename_signals(name: str) -> Dict[str, Any]:
    stem, ext = os.path.splitext(name)
    return {
        "contains_spaces": " " in name,
        "contains_uppercase": any(c.isupper() for c in name),
        "contains_underscores": "_" in stem,
        "contains_hyphens": "-" in stem,
        "contains_special_characters": bool(re.search(r"[^A-Za-z0-9._-]", name)),
        "date_stamp_yyyy_mm_dd": bool(re.search(r"\d{4}_\d{2}_\d{2}", name)),
        "date_stamp_yyyy_mm_dd_hyphen": bool(re.search(r"\d{4}-\d{2}-\d{2}", name)),
        "extension": ext.lower(),
    }


def _filename_tokens(stem: str) -> List[str]:
    return [tok.lower() for tok in re.split(r"[^A-Za-z0-9]+", stem) if tok]


def _semantic_name_signals(stem: str) -> Dict[str, Any]:
    tokens = _filename_tokens(stem)
    generic_tokens = [tok for tok in tokens if tok in GENERIC_FILENAME_TOKENS]
    non_generic_tokens = [tok for tok in tokens if tok not in GENERIC_FILENAME_TOKENS and not tok.isdigit()]
    return {
        "tokens": tokens,
        "generic_tokens": generic_tokens,
        "non_generic_tokens": non_generic_tokens,
        "only_generic_tokens": bool(tokens) and not non_generic_tokens,
        "token_count": len(tokens),
        "non_generic_token_count": len(non_generic_tokens),
    }


def _document_inventory(files: List[str], target_path: str) -> List[Dict[str, Any]]:
    inventory = []
    for path in sorted(files):
        name = os.path.basename(path)
        inventory.append(
            {
                "file": path,
                "relative_path": _relpath(path, target_path),
                "directory": _relpath(os.path.dirname(path), target_path),
                "filename": name,
                "stem": os.path.splitext(name)[0],
                "extension": os.path.splitext(name)[1].lower(),
                "detected_naming_style": _detected_naming_style(name),
                "naming_signals": _filename_signals(name),
                "semantic_name_signals": _semantic_name_signals(os.path.splitext(name)[0]),
            }
        )
    return inventory


def _summarize_document_names(inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    token_to_files: Dict[str, List[str]] = {}
    stem_to_files: Dict[str, List[str]] = {}
    only_generic = []
    short_names = []

    for item in inventory:
        relative_path = item["relative_path"]
        stem = item["stem"].lower()
        stem_to_files.setdefault(stem, []).append(relative_path)
        signals = item.get("semantic_name_signals", {})
        tokens = signals.get("tokens", [])
        for token in tokens:
            token_to_files.setdefault(token, []).append(relative_path)
        if signals.get("only_generic_tokens"):
            only_generic.append(relative_path)
        if signals.get("non_generic_token_count", 0) <= 1 and item["filename"].lower() != "readme.md":
            short_names.append(relative_path)

    repeated_generic_tokens = {
        token: files
        for token, files in sorted(token_to_files.items())
        if token in GENERIC_FILENAME_TOKENS and len(files) > 1
    }
    duplicate_stems = {stem: files for stem, files in sorted(stem_to_files.items()) if len(files) > 1}

    return {
        "only_generic_names": only_generic,
        "low_specificity_names": short_names,
        "repeated_generic_tokens": repeated_generic_tokens,
        "duplicate_stems": duplicate_stems,
        "token_to_files": {token: files for token, files in sorted(token_to_files.items())},
    }


def _natural_sort_key(s: str) -> List[Any]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", s)]


def _directory_sort_order(files: List[str]) -> Dict[str, Any]:
    names = [os.path.basename(p) for p in files]
    lexical = sorted(names)
    natural = sorted(names, key=_natural_sort_key)
    return {
        "filenames": lexical,
        "natural_sort_order": natural,
        "lexical_differs_from_natural": lexical != natural,
    }


def _parse_readme_index(readme_path: str) -> Dict[str, Any]:
    """
    Parse a best-effort Markdown table from a README.md.
    Looks for column headers that contain:
    - 'index' / 'no'
    - 'document' / 'name' / 'file'
    - 'description' / 'short'
    """
    md = _read_text(readme_path)
    lines = md.splitlines()

    # Find header row.
    header_idx = None
    header_cols: List[str] = []
    for i in range(0, len(lines) - 1):
        line = lines[i].strip()
        if not (line.startswith("|") and "|" in line[1:]):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        header_l = " ".join(cols).lower()
        if ("index" in header_l or "no" in header_l) and ("doc" in header_l or "name" in header_l or "file" in header_l) and (
            "desc" in header_l or "short" in header_l
        ):
            header_idx = i
            header_cols = cols
            break

    if header_idx is None:
        return {
            "status": "unparseable_or_missing_index_table",
            "index_entries": [],
        }

    def _find_col(predicates: List[str]) -> Optional[int]:
        for idx, col in enumerate(header_cols):
            cl = col.lower()
            if any(p in cl for p in predicates):
                return idx
        return None

    idx_col = _find_col(["index", "no", "number"])
    name_col = _find_col(["document", "name", "file", "doc"])
    desc_col = _find_col(["description", "desc", "short"])

    if idx_col is None or name_col is None or desc_col is None:
        return {
            "status": "unparseable_index_table_columns",
            "index_entries": [],
        }

    # Separator row is often next; parse subsequent rows that look like tables.
    index_entries: List[Dict[str, str]] = []
    for j in range(header_idx + 2, len(lines)):
        line = lines[j].strip()
        if not (line.startswith("|") and "|" in line[1:]):
            # stop at first non-table after header
            break
        cols = [c.strip() for c in line.strip("|").split("|")]
        if max(idx_col, name_col, desc_col) >= len(cols):
            continue
        index_entries.append(
            {
                "index": cols[idx_col],
                "document_name": cols[name_col],
                "description": cols[desc_col],
            }
        )

    return {
        "status": "parsed",
        "index_entries": index_entries,
        "columns": {
            "index_col": idx_col,
            "name_col": name_col,
            "description_col": desc_col,
        },
    }


def _normalize_index_name(raw: str) -> str:
    raw = raw.strip().strip("`")
    link = re.search(r"\[[^\]]+\]\(([^)#]+)", raw)
    if link:
        raw = link.group(1)
    raw = raw.split("#", 1)[0].strip()
    return os.path.basename(raw)


def _extract_abs_internal_urls(md: str) -> List[str]:
    # Conservative: only record absolute URLs that look like they point to markdown paths in a repo.
    urls = re.findall(r"https?://[^\s)\"']+", md)
    internalish = []
    for u in urls:
        if any(x in u for x in ["/blob/", "/tree/"]) and (u.lower().endswith(".md") or "/docs/" in u.lower()):
            internalish.append(u)
    return sorted(set(internalish))


def _style_evidence(md: str) -> Dict[str, Any]:
    list_markers: Dict[str, int] = {}
    code_fence_language_tags: List[str] = []
    blank_line_issues: List[Dict[str, Any]] = []
    heading_case_counts: Dict[str, int] = {}
    in_code_fence = False
    lines = md.splitlines()

    for idx, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code_fence:
                if idx + 1 < len(lines) and lines[idx + 1].strip():
                    blank_line_issues.append({"line": idx + 1, "issue": "missing_blank_line_after_code_fence"})
                in_code_fence = False
                continue

            tag = stripped[3:].strip()
            code_fence_language_tags.append(tag if tag else "unspecified")
            if idx > 0 and lines[idx - 1].strip():
                blank_line_issues.append({"line": idx + 1, "issue": "missing_blank_line_before_code_fence"})
            in_code_fence = True
            continue

        if in_code_fence:
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            text = heading.group(2).strip()
            words = [w for w in re.split(r"\s+", text) if w]
            if text.isupper():
                heading_case = "upper"
            elif words and sum(1 for w in words if w[:1].isupper()) >= max(1, len(words) - 1):
                heading_case = "title"
            elif text[:1].isupper():
                heading_case = "sentence"
            else:
                heading_case = "lower_or_other"
            heading_case_counts[heading_case] = heading_case_counts.get(heading_case, 0) + 1

        unordered = re.match(r"^\s*([-*+])\s+", line)
        ordered = re.match(r"^\s*(\d+)([.)])\s+", line)
        marker = None
        if unordered:
            marker = unordered.group(1)
        elif ordered:
            marker = f"number{ordered.group(2)}"

        if marker:
            list_markers[marker] = list_markers.get(marker, 0) + 1
            prev_is_list = idx > 0 and bool(re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", lines[idx - 1]))
            if idx > 0 and lines[idx - 1].strip() and not prev_is_list:
                blank_line_issues.append({"line": idx + 1, "issue": "missing_blank_line_before_list"})

    return {
        "code_fence_language_tags": sorted(set(code_fence_language_tags)),
        "list_marker_counts": list_markers,
        "heading_case_counts": heading_case_counts,
        "blank_line_issues": blank_line_issues[:100],
    }


def _summarize_style(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    code_tags_by_file = {}
    list_markers_by_file = {}
    admonition_variants_by_file = {}
    heading_sequences_by_file = {}
    heading_case_by_file = {}
    style_candidate_issues = []

    for item in files:
        path = item["file"]
        style = item.get("style_profile", {})
        code_tags_by_file[path] = style.get("code_fence_language_tags", [])
        list_markers_by_file[path] = style.get("list_marker_counts", {})
        admonition_variants_by_file[path] = style.get("admonition_variants_counts", {})
        heading_sequences_by_file[path] = item.get("heading_structure", {}).get("heading_levels", [])
        heading_case_by_file[path] = style.get("heading_case_counts", {})

        if len(style.get("list_marker_counts", {})) > 1:
            style_candidate_issues.append({"file": path, "issue": "mixed_list_marker_styles"})
        if len(style.get("code_fence_language_tags", [])) > 1:
            style_candidate_issues.append({"file": path, "issue": "mixed_code_fence_language_tags"})
        if style.get("blank_line_issues"):
            style_candidate_issues.append({"file": path, "issue": "markdown_blank_line_inconsistencies"})

    return {
        "code_fence_language_tags_by_file": code_tags_by_file,
        "list_markers_by_file": list_markers_by_file,
        "admonition_variants_by_file": admonition_variants_by_file,
        "heading_sequences_by_file": heading_sequences_by_file,
        "heading_case_by_file": heading_case_by_file,
        "candidate_issues": style_candidate_issues,
    }


def scan_docs(target_path: str) -> Dict[str, Any]:
    target_path = _validate_target_path(target_path)
    # Inventory
    all_markdown_files: List[str] = []
    dirs_with_md: Dict[str, List[str]] = {}
    unreadable_files: List[Dict[str, str]] = []

    for root, dirnames, filenames in os.walk(target_path):
        # Skip VCS dirs and hidden dirs.
        dirnames[:] = [d for d in dirnames if d not in {".git", ".github"} and not d.startswith(".")]
        md_files = [
            os.path.join(root, fn)
            for fn in filenames
            if os.path.splitext(fn)[1].lower() in MD_EXTS
        ]
        if md_files:
            dirs_with_md[root] = md_files
            all_markdown_files.extend(md_files)

    naming_dominant, naming_counts, naming_deviations = _dominant_naming(all_markdown_files)

    directory_indexing: List[Dict[str, Any]] = []

    for dpath, md_files in sorted(dirs_with_md.items()):
        dir_issue: Dict[str, Any] = {
            "directory": dpath,
            "sort_order": _directory_sort_order(md_files),
        }
        readme = os.path.join(dpath, "README.md")
        if not os.path.exists(readme):
            dir_issue["readme_status"] = "missing"
            directory_indexing.append(dir_issue)
            continue

        dir_issue["readme_status"] = "present"
        try:
            parsed = _parse_readme_index(readme)
        except OSError as e:
            dir_issue["readme_index_parse"] = "unreadable"
            dir_issue["read_error"] = f"{type(e).__name__}: {e}"
            unreadable_files.append({"file": readme, "error": dir_issue["read_error"]})
            directory_indexing.append(dir_issue)
            continue
        dir_issue["readme_index_parse"] = parsed.get("status")

        index_entries: List[Dict[str, str]] = parsed.get("index_entries", []) or []
        dir_issue["readme_index_entries_count"] = len(index_entries)

        entry_names = [_normalize_index_name(e.get("document_name", "")) for e in index_entries if e.get("document_name")]
        # Build a set of acceptable file name representations.
        md_basenames = {os.path.basename(p) for p in md_files}
        md_noext = {os.path.splitext(os.path.basename(p))[0] for p in md_files}
        entry_refs = {n for n in entry_names if n}
        entry_refs_noext = {os.path.splitext(n)[0] for n in entry_refs}

        missing_from_index: List[str] = []
        for p in md_files:
            name = os.path.basename(p)
            if name == "README.md":
                continue
            base = os.path.splitext(name)[0]
            if name not in entry_refs and base not in entry_refs_noext:
                missing_from_index.append(p)

        stale_entries: List[str] = []
        for n in entry_names:
            # n might include extension or not.
            if n not in md_basenames and n not in md_noext:
                stale_entries.append(n)

        dir_issue["missing_markdown_files_in_readme_index"] = missing_from_index
        dir_issue["stale_index_entries"] = stale_entries
        directory_indexing.append(dir_issue)

    file_results: List[Dict[str, Any]] = []

    for mpath in sorted(all_markdown_files):
        try:
            md = _read_text(mpath)
        except OSError as e:
            unreadable_files.append({"file": mpath, "error": f"{type(e).__name__}: {e}"})
            continue

        has_fm, fm_obj, fm_issues = _parse_front_matter(md)
        # Required fields presence.
        required_fields = ["title", "description", "version", "audience", "tags", "created", "last_updated"]
        missing_fields = []
        type_issues: List[str] = []
        if has_fm:
            for k in required_fields:
                if k not in fm_obj:
                    missing_fields.append(k)

            if "version" in fm_obj and not isinstance(fm_obj.get("version"), str):
                type_issues.append("version_not_string")
            if "tags" in fm_obj and not isinstance(fm_obj.get("tags"), list):
                type_issues.append("tags_not_list")
            if _iso_date_or_none(fm_obj.get("created")) is None and "created" in fm_obj:
                type_issues.append("created_not_iso_YYYY-MM-DD")
            if _iso_date_or_none(fm_obj.get("last_updated")) is None and "last_updated" in fm_obj:
                type_issues.append("last_updated_not_iso_YYYY-MM-DD")

        # Compare title to first H1
        title_mismatch = False
        md_h1 = _first_h1(md)
        if has_fm and "title" in fm_obj and md_h1:
            if str(fm_obj.get("title", "")).strip() != md_h1.strip():
                title_mismatch = True

        # Heading structure
        headings = _extract_headings(md)
        has_h1 = any(level == 1 for level, _ in headings)
        heading_levels = [level for level, _ in headings]
        skips: List[Dict[str, Any]] = []
        prev_level = None
        for level, text in headings:
            if prev_level is None:
                prev_level = level
                continue
            if level - prev_level > 1:
                skips.append({"from": prev_level, "to": level, "heading": text})
            prev_level = level

        style_evidence = _style_evidence(md)

        # Admonition syntaxes presence
        admonition_variants = {
            "admonition__bangbangbang": len(re.findall(r"^\s*!!!\s+", md, flags=re.M)),
            "admonition__blockquote_bold": len(re.findall(r"^\s*>\s*\*\*.+?\*\*", md, flags=re.M)),
        }

        # Hidden blocks: <details>
        details_blocks = []
        for m in re.finditer(r"<details\b[^>]*>(.*?)</details>", md, flags=re.I | re.S):
            details_blocks.append(m.group(1))

        details_keyword_hits: List[str] = []
        for block in details_blocks:
            lower = block.lower()
            for kw in CRITICAL_KEYWORDS:
                if kw in lower:
                    details_keyword_hits.append(kw)
        details_keyword_hits = sorted(set(details_keyword_hits))

        # Critical keyword placement
        lower_full = md.lower()
        first_keyword_pos = None
        first_keyword = None
        for kw in CRITICAL_KEYWORDS:
            idx = lower_full.find(kw)
            if idx != -1 and (first_keyword_pos is None or idx < first_keyword_pos):
                first_keyword_pos = idx
                first_keyword = kw

        first_code_block_pos = None
        idx_code = lower_full.find("```")
        if idx_code != -1:
            first_code_block_pos = idx_code

        doc_len = max(len(md), 1)
        last20_start = int(doc_len * 0.8)
        critical_after_last20 = bool(first_keyword_pos is not None and first_keyword_pos >= last20_start)
        code_after_last20 = bool(first_code_block_pos is not None and first_code_block_pos >= last20_start)

        # Images alt text
        missing_alt_images = []
        for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", md):
            alt = (m.group(1) or "").strip()
            if alt == "":
                missing_alt_images.append(m.group(2))

        # Absolute internalish URLs
        absolute_internal_urls = _extract_abs_internal_urls(md)

        file_results.append(
            {
                "file": mpath,
                "is_markdown": True,
                "front_matter": {
                    "present": has_fm,
                    "parsed_without_yaml_library": (has_fm and not _HAVE_YAML),
                    "missing_required_fields": missing_fields if has_fm else [],
                    "type_issues": type_issues if has_fm else [],
                    "title_mismatch_with_first_h1": title_mismatch,
                    "front_matter_parse_issues": fm_issues if has_fm else [],
                },
                "heading_structure": {
                    "has_h1": has_h1,
                    "h1_count": sum(1 for level, _ in headings if level == 1),
                    "heading_levels": heading_levels,
                    "heading_texts": [text for _, text in headings],
                    "skips": skips,
                },
                "style_profile": {
                    "code_fence_language_tags": style_evidence["code_fence_language_tags"],
                    "list_marker_counts": style_evidence["list_marker_counts"],
                    "blank_line_issues": style_evidence["blank_line_issues"],
                    "admonition_variants_counts": admonition_variants,
                },
                "hidden_blocks": {
                    "details_blocks_count": len(details_blocks),
                    "critical_keywords_inside_details_blocks": details_keyword_hits,
                },
                "critical_placement": {
                    "first_critical_keyword": first_keyword,
                    "critical_keywords_after_last_20_percent": critical_after_last20,
                    "first_code_block_after_last_20_percent": code_after_last20,
                },
                "images": {
                    "missing_alt_images": missing_alt_images[:50],
                },
                "absolute_internal_urls": absolute_internal_urls[:200],
            }
        )

    document_inventory = _document_inventory(all_markdown_files, target_path)

    result: Dict[str, Any] = {
        "target_path": target_path,
        "generated_at": _generated_at(),
        "files_scanned": len(file_results),
        "directories_scanned": len(dirs_with_md),
        "unreadable_files": unreadable_files,
        "naming": {
            "dominant_style": naming_dominant,
            "counts": naming_counts,
            "deviations": naming_deviations[:2000],
            "semantic_review": _summarize_document_names(document_inventory),
        },
        "document_inventory": document_inventory,
        "style_consistency_evidence": _summarize_style(file_results),
        "directory_indexing": directory_indexing,
        "files": file_results,
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target_path", help="Root docs directory to scan; emits read-only JSON evidence to stdout")
    args = ap.parse_args()

    try:
        payload = scan_docs(args.target_path)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

