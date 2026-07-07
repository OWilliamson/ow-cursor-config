#!/usr/bin/env python3
"""Shared helpers for profile install/prune scripts (bash and PowerShell invoke this)."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_NAME = ".ow-cursor-config-manifest.json"
CATALOG_JSON = "catalog/bundle-manifest.json"


def repo_root_from_script() -> Path:
    # scripts/lib/profile-tooling.py -> repo root (ow-cursor-config or hub public/)
    return Path(__file__).resolve().parent.parent.parent


def default_profile() -> Path:
    return Path.home() / ".cursor"


def load_catalog(repo: Path) -> dict:
    path = repo / CATALOG_JSON
    if not path.is_file():
        raise SystemExit(f"Missing catalog: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest(profile: Path) -> dict:
    path = profile / MANIFEST_NAME
    if not path.is_file():
        return {
            "version": 1,
            "repo_hint": "",
            "rules": [],
            "skills": [],
            "updated_at": "",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(profile: Path, manifest: dict) -> Path:
    profile.mkdir(parents=True, exist_ok=True)
    path = profile / MANIFEST_NAME
    manifest["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def copy_file(src: Path, dst: Path, dry_run: bool) -> str:
    if dst.is_file() and dst.read_bytes() == src.read_bytes():
        return "unchanged"
    if dry_run:
        return "would_update" if dst.exists() else "would_install"
    dst.parent.mkdir(parents=True, exist_ok=True)
    existed = dst.exists()
    shutil.copy2(src, dst)
    return "updated" if existed else "installed"


def _iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        files.append(path)
    return files


def trees_match(src: Path, dst: Path) -> bool:
    if not dst.is_dir():
        return False
    src_files = {p.relative_to(src) for p in _iter_files(src)}
    dst_files = {p.relative_to(dst) for p in _iter_files(dst)}
    if src_files != dst_files:
        return False
    for rel in src_files:
        if (src / rel).read_bytes() != (dst / rel).read_bytes():
            return False
    return True


def copy_tree(src: Path, dst: Path, dry_run: bool) -> str:
    if trees_match(src, dst):
        return "unchanged"
    existed = dst.exists()
    if dry_run:
        return "would_update" if existed else "would_install"
    if existed:
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return "updated" if existed else "installed"


def _bump(counts: dict[str, int], result: str) -> None:
    mapping = {
        "installed": "installed",
        "updated": "updated",
        "unchanged": "unchanged",
        "would_install": "installed",
        "would_update": "updated",
    }
    counts[mapping[result]] += 1


def cmd_install(kind: str, repo: Path, profile: Path, dry_run: bool) -> int:
    catalog = load_catalog(repo)
    names: list[str] = catalog[kind]
    manifest = load_manifest(profile)
    manifest["repo_hint"] = str(repo.resolve())

    counts = {"installed": 0, "updated": 0, "unchanged": 0}
    actions: list[str] = []

    if kind == "rules":
        for name in names:
            src = repo / "rules" / name
            if not src.is_file():
                raise SystemExit(f"Catalog rule missing on disk: {src}")
            dst = profile / "rules" / name
            result = copy_file(src, dst, dry_run)
            _bump(counts, result)
            actions.append(f"  {name}: {result}")
        manifest["rules"] = names
    else:
        for name in names:
            src = repo / "skills" / name
            if not src.is_dir():
                raise SystemExit(f"Catalog skill missing on disk: {src}")
            dst = profile / "skills" / name
            result = copy_tree(src, dst, dry_run)
            _bump(counts, result)
            actions.append(f"  {name}: {result}")
        manifest["skills"] = names

    manifest_path = None
    if not dry_run:
        manifest_path = save_manifest(profile, manifest)

    prefix = "[dry-run] " if dry_run else ""
    print(f"{prefix}Install {kind} -> {profile}")
    print("\n".join(actions))
    print(
        f"Summary: installed={counts['installed']} updated={counts['updated']} "
        f"unchanged={counts['unchanged']}"
    )
    if manifest_path:
        print(f"Manifest: {manifest_path}")
    return 0


def cmd_prune(kind: str, repo: Path, profile: Path, dry_run: bool) -> int:
    catalog = load_catalog(repo)
    manifest = load_manifest(profile)
    current: set[str] = set(catalog[kind])
    previous: set[str] = set(manifest.get(kind, []))

    manifest_path = profile / MANIFEST_NAME
    if not previous:
        raise SystemExit(
            f"No {kind} recorded in {manifest_path}. Run install-profile-{kind} first."
        )

    to_remove = sorted(previous - current)
    actions: list[str] = []
    removed = 0

    for name in to_remove:
        target = profile / ("rules" if kind == "rules" else "skills") / name
        if not target.exists():
            actions.append(f"  {name}: already_absent")
            continue
        if dry_run:
            actions.append(f"  {name}: would_remove")
            removed += 1
            continue
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        actions.append(f"  {name}: removed")
        removed += 1

    if not dry_run:
        manifest[kind] = sorted(current)
        manifest["repo_hint"] = str(repo.resolve())
        save_manifest(profile, manifest)

    prefix = "[dry-run] " if dry_run else ""
    print(f"{prefix}Prune {kind} from {profile}")
    if not actions:
        print("  (nothing to remove)")
    else:
        print("\n".join(actions))
    print(f"Removed count: {removed}")
    if not dry_run and removed:
        print(f"Manifest: {manifest_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile tooling helper")
    parser.add_argument(
        "command",
        choices=["install-rules", "install-skills", "prune-rules", "prune-skills"],
    )
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--profile", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = args.repo or repo_root_from_script()
    profile = args.profile or default_profile()

    if args.command == "install-rules":
        return cmd_install("rules", repo, profile, args.dry_run)
    if args.command == "install-skills":
        return cmd_install("skills", repo, profile, args.dry_run)
    if args.command == "prune-rules":
        return cmd_prune("rules", repo, profile, args.dry_run)
    return cmd_prune("skills", repo, profile, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
