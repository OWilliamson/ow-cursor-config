#!/usr/bin/env python3
"""Profile kit manifest, symlink sync, catalog export, and install/prune."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

MANIFEST_NAME = ".ow-cursor-config-manifest.json"
PROFILE_KITS_MANIFEST = "profile-kits-manifest.yaml"
HOOKS_FRAGMENT_NAME = "hooks.json.fragment.yaml"
DEFAULT_KIT = "owcc-kit-starter"
KINDS = ("rules", "skills", "hooks")


def _require_yaml() -> Any:
    if yaml is None:
        raise SystemExit("PyYAML required (pip install pyyaml)")
    return yaml


def hub_root_from_env(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    env = os.environ.get("HUB_ROOT")
    if env:
        return Path(env).resolve()
    return Path.cwd().resolve()


def consumer_root_from_env(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    env = os.environ.get("OW_CURSOR_CONFIG")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent.parent


def detect_mode(hub_root: Path | None, consumer_root: Path | None) -> tuple[str, Path]:
    if hub_root is not None and (hub_root / PROFILE_KITS_MANIFEST).is_file():
        return "hub", hub_root
    root = consumer_root or consumer_root_from_env(None)
    if (root / "catalog" / "bundle-manifest.json").is_file():
        return "consumer", root
    if (root / "public" / "catalog" / "bundle-manifest.json").is_file():
        return "consumer", root / "public"
    raise SystemExit(
        "Cannot detect hub or consumer root. Set HUB_ROOT or OW_CURSOR_CONFIG, "
        "or pass --hub-root / --repo."
    )


def load_profile_kits_manifest(hub: Path) -> dict[str, Any]:
    path = hub / PROFILE_KITS_MANIFEST
    if not path.is_file():
        raise SystemExit(f"Missing {path}")
    y = _require_yaml()
    data = y.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "bundles" not in data:
        raise SystemExit(f"Invalid profile kits manifest: {path}")
    return data


def member_list(kit: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    raw = kit.get(kind, []) or []
    out: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, str):
            out.append({"name": item, "source": "public"})
        elif isinstance(item, dict):
            out.append(dict(item))
    return out


def canonical_target(hub: Path, kind: str, member: dict[str, Any]) -> Path:
    source = member.get("source", "public")
    name = member["name"]
    if source == "public":
        base = hub / "public" / kind
    elif source == "private":
        base = hub / "private" / kind
    elif source == "project-specific":
        bundle = member.get("bundle")
        if not bundle:
            raise SystemExit(f"project-specific member {name} missing bundle:")
        base = hub / "project-specific" / bundle / kind
    else:
        raise SystemExit(f"Unknown source {source!r} for {name}")
    if kind == "rules":
        return base / name
    return base / name


def public_canonical_target(hub: Path, kind: str, name: str) -> Path:
    return hub / "public" / kind / name


def iter_kit_members(kit_def: dict[str, Any], public_only: bool = False) -> list[tuple[str, dict[str, Any]]]:
    items: list[tuple[str, dict[str, Any]]] = []
    for kind in KINDS:
        for member in member_list(kit_def, kind):
            if public_only and member.get("source", "public") != "public":
                continue
            items.append((kind, member))
    return items


def kit_has_public_members(kit_def: dict[str, Any]) -> bool:
    return bool(iter_kit_members(kit_def, public_only=True)) or bool(kit_def.get("hooks_json"))


def write_hooks_fragment(path: Path, hooks_json: dict[str, Any] | None, dry_run: bool) -> None:
    if not hooks_json:
        if path.is_file() and not dry_run:
            path.unlink()
        return
    y = _require_yaml()
    text = y.dump(hooks_json, default_flow_style=False, sort_keys=False)
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_symlink(link: Path, target: Path, *, allow_copy_fallback: bool, dry_run: bool) -> None:
    if not target.exists():
        raise SystemExit(f"Canonical target missing: {target}")
    if dry_run:
        return
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink() or link.exists():
        if link.is_symlink() and link.resolve() == target.resolve():
            return
        if link.is_dir() and not link.is_symlink():
            shutil.rmtree(link)
        else:
            link.unlink()
    rel = os.path.relpath(target, link.parent)
    try:
        if target.is_dir():
            os.symlink(rel, link, target_is_directory=os.name == "nt")
        else:
            os.symlink(rel, link)
    except OSError as exc:
        if not allow_copy_fallback:
            raise SystemExit(f"symlink failed {link} -> {target}: {exc}") from exc
        if target.is_dir():
            shutil.copytree(target, link, dirs_exist_ok=True)
        else:
            shutil.copy2(target, link)


def sync_bundle_tree(
    hub: Path,
    kit_id: str,
    kit_def: dict[str, Any],
    *,
    bundle_root: Path,
    public_only: bool,
    prune_stale: bool,
    allow_copy_fallback: bool,
    dry_run: bool,
    errors: list[str],
) -> set[Path]:
    """Create symlinks under bundle_root/kit_id. Returns expected link paths."""
    expected: set[Path] = set()
    kit_dir = bundle_root / kit_id

    for kind, member in iter_kit_members(kit_def, public_only=public_only):
        if public_only and member.get("source") != "public":
            continue
        try:
            if public_only:
                target = public_canonical_target(hub, kind, member["name"])
            else:
                target = canonical_target(hub, kind, member)
        except SystemExit as exc:
            errors.append(f"{kit_id}: {exc}")
            continue
        if not target.exists():
            errors.append(f"{kit_id}: missing target {target}")
            continue
        link = kit_dir / kind / member["name"]
        expected.add(link)
        make_symlink(link, target, allow_copy_fallback=allow_copy_fallback, dry_run=dry_run)

    frag = kit_dir / HOOKS_FRAGMENT_NAME
    hooks_json = kit_def.get("hooks_json")
    if hooks_json and (not public_only or kit_has_public_members(kit_def)):
        expected.add(frag)
        write_hooks_fragment(frag, hooks_json, dry_run)
    elif prune_stale and frag.exists() and not dry_run:
        frag.unlink()

    if prune_stale and kit_dir.exists() and not dry_run:
        for path in kit_dir.rglob("*"):
            if path == frag:
                continue
            if path.is_symlink() and path not in expected:
                path.unlink()
        for kind in KINDS:
            kind_dir = kit_dir / kind
            if kind_dir.is_dir() and not any(kind_dir.iterdir()):
                kind_dir.rmdir()

    return expected


def cmd_sync(args: argparse.Namespace) -> int:
    hub = hub_root_from_env(args.hub_root)
    data = load_profile_kits_manifest(hub)
    bundles = data["bundles"]
    errors: list[str] = []

    for kit_id, kit_def in bundles.items():
        sync_bundle_tree(
            hub,
            kit_id,
            kit_def,
            bundle_root=hub / "bundles",
            public_only=False,
            prune_stale=args.prune_stale,
            allow_copy_fallback=args.allow_copy_fallback,
            dry_run=args.dry_run,
            errors=errors,
        )
        if kit_has_public_members(kit_def):
            sync_bundle_tree(
                hub,
                kit_id,
                kit_def,
                bundle_root=hub / "public" / "bundles",
                public_only=True,
                prune_stale=args.prune_stale,
                allow_copy_fallback=args.allow_copy_fallback,
                dry_run=args.dry_run,
                errors=errors,
            )
        elif args.prune_stale:
            pub_kit = hub / "public" / "bundles" / kit_id
            if pub_kit.exists() and not args.dry_run:
                shutil.rmtree(pub_kit)

    if errors:
        for line in errors:
            print(f"WARNING: {line}", file=sys.stderr)
        if args.strict:
            raise SystemExit(f"sync-profile-kit-bundles: {len(errors)} error(s)")

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Synced {len(bundles)} kit(s) under {hub / 'bundles'}")
    print(f"{prefix}Public bundle tree under {hub / 'public' / 'bundles'}")
    return 0


def export_public_catalog(hub: Path) -> dict[str, Any]:
    data = load_profile_kits_manifest(hub)
    out_bundles: dict[str, Any] = {}
    for kit_id, kit_def in data["bundles"].items():
        if not kit_has_public_members(kit_def):
            continue
        entry: dict[str, Any] = {"description": kit_def.get("description", "")}
        for kind in KINDS:
            members = [
                m["name"]
                for m in member_list(kit_def, kind)
                if m.get("source", "public") == "public"
            ]
            if members:
                entry[kind] = members
        if kit_def.get("hooks_json"):
            entry["hooks_json"] = kit_def["hooks_json"]
        out_bundles[kit_id] = entry
    return {
        "version": 2,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "default_kit": DEFAULT_KIT,
        "bundles": out_bundles,
    }


def write_catalog_files(hub: Path, catalog: dict[str, Any], dry_run: bool) -> None:
    catalog_dir = hub / "public" / "catalog"
    json_path = catalog_dir / "bundle-manifest.json"
    yaml_path = catalog_dir / "bundle-manifest.yaml"
    if dry_run:
        print(f"[dry-run] Would write {json_path}")
        return
    catalog_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Generated from profile-kits-manifest.yaml — do not edit",
        "# Regenerate: python3 scripts/export-profile-kits-catalog.py",
        f"version: {catalog['version']}",
        f"default_kit: {catalog['default_kit']}",
        "bundles:",
    ]
    for kit_id, kit_def in catalog["bundles"].items():
        lines.append(f"  {kit_id}:")
        lines.append(f'    description: "{kit_def.get("description", "")}"')
        for kind in KINDS:
            if kind in kit_def:
                lines.append(f"    {kind}:")
                for name in kit_def[kind]:
                    lines.append(f"      - {name}")
    yaml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {json_path.relative_to(hub)}")
    print(f"Wrote {yaml_path.relative_to(hub)}")


def cmd_export(args: argparse.Namespace) -> int:
    hub = hub_root_from_env(args.hub_root)
    if not args.skip_sync:
        sync_args = argparse.Namespace(
            hub_root=hub,
            prune_stale=True,
            allow_copy_fallback=args.allow_copy_fallback,
            dry_run=False,
            strict=True,
        )
        cmd_sync(sync_args)
    catalog = export_public_catalog(hub)
    write_catalog_files(hub, catalog, args.dry_run)
    return 0


def bundle_root_for_mode(mode: str, root: Path) -> Path:
    if mode == "hub":
        return root / "bundles"
    return root / "bundles"


def resolve_consumer_root(repo: Path) -> Path:
    if (repo / "catalog" / "bundle-manifest.json").is_file():
        return repo
    if (repo / "bundles").is_dir():
        return repo
    raise SystemExit(f"Not a consumer ow-cursor-config tree: {repo}")


def load_catalog(repo: Path) -> dict[str, Any]:
    path = repo / "catalog" / "bundle-manifest.json"
    if not path.is_file():
        raise SystemExit(f"Missing catalog: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile_manifest(profile: Path) -> dict[str, Any]:
    path = profile / MANIFEST_NAME
    if not path.is_file():
        return {
            "version": 2,
            "mode": "",
            "repo_hint": "",
            "installed_kits": [],
            "kit_members": {},
            "updated_at": "",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_profile_manifest(profile: Path, manifest: dict[str, Any]) -> Path:
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
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return "updated" if existed else "installed"


def merge_hooks_json(profile_hooks: Path, fragment: dict[str, Any], dry_run: bool) -> str:
    existing: dict[str, Any] = {"version": 1, "hooks": {}}
    if profile_hooks.is_file():
        existing = json.loads(profile_hooks.read_text(encoding="utf-8"))
    merged_hooks: dict[str, list[dict[str, Any]]] = dict(existing.get("hooks", {}))
    for event, entries in fragment.get("hooks", {}).items():
        by_cmd = {e.get("command"): e for e in merged_hooks.get(event, [])}
        for entry in entries:
            cmd = entry.get("command")
            if cmd:
                by_cmd[cmd] = entry
        merged_hooks[event] = list(by_cmd.values())
    out = {"version": fragment.get("version", 1), "hooks": merged_hooks}
    formatted = json.dumps(out, indent=2) + "\n"
    if profile_hooks.is_file() and profile_hooks.read_text(encoding="utf-8") == formatted:
        return "unchanged"
    if dry_run:
        return "would_update" if profile_hooks.exists() else "would_install"
    profile_hooks.parent.mkdir(parents=True, exist_ok=True)
    existed = profile_hooks.exists()
    profile_hooks.write_text(formatted, encoding="utf-8")
    return "updated" if existed else "installed"


def install_kit_from_bundle(
    kit_id: str,
    bundle_dir: Path,
    profile: Path,
    dry_run: bool,
) -> dict[str, Any]:
    """Install one kit by walking bundle_dir symlinks. Returns member snapshot."""
    snapshot: dict[str, Any] = {"rules": [], "skills": [], "hooks": []}
    if not bundle_dir.is_dir():
        raise SystemExit(f"Bundle directory missing: {bundle_dir}")

    for kind in KINDS:
        kind_dir = bundle_dir / kind
        if not kind_dir.is_dir():
            continue
        for entry in sorted(kind_dir.iterdir()):
            if entry.name.startswith("."):
                continue
            if not entry.exists():
                continue
            resolved = entry.resolve() if entry.is_symlink() else entry
            name = entry.name
            if kind == "rules":
                dst = profile / "rules" / name
                result = copy_file(resolved, dst, dry_run)
                snapshot["rules"].append({"name": name, "result": result})
            elif kind == "skills":
                dst = profile / "skills" / name
                result = copy_tree(resolved, dst, dry_run)
                snapshot["skills"].append({"name": name, "result": result})
            elif kind == "hooks":
                dst = profile / "hooks" / name
                result = copy_tree(resolved, dst, dry_run)
                snapshot["hooks"].append({"name": name, "result": result})

    frag = bundle_dir / HOOKS_FRAGMENT_NAME
    if frag.is_file():
        y = _require_yaml()
        fragment = y.safe_load(frag.read_text(encoding="utf-8"))
        merge_hooks_json(profile / "hooks.json", fragment, dry_run)

    return snapshot


def list_kit_ids(mode: str, root: Path, hub: Path | None) -> list[str]:
    if mode == "hub" and hub is not None:
        data = load_profile_kits_manifest(hub)
        return sorted(data["bundles"].keys())
    catalog = load_catalog(resolve_consumer_root(root))
    return sorted(catalog.get("bundles", {}).keys())


def cmd_list_kits(args: argparse.Namespace) -> int:
    hub = hub_root_from_env(args.hub_root) if args.hub_root or (Path.cwd() / PROFILE_KITS_MANIFEST).is_file() else None
    if hub and (hub / PROFILE_KITS_MANIFEST).is_file():
        mode = "hub"
        data = load_profile_kits_manifest(hub)
        for kit_id in sorted(data["bundles"]):
            desc = data["bundles"][kit_id].get("description", "")
            pub = kit_has_public_members(data["bundles"][kit_id])
            print(f"{kit_id}: {desc} [{'shippable' if pub else 'hub-only'}]")
        return 0
    repo = resolve_consumer_root(consumer_root_from_env(args.repo))
    catalog = load_catalog(repo)
    for kit_id, kit_def in sorted(catalog.get("bundles", {}).items()):
        print(f"{kit_id}: {kit_def.get('description', '')}")
    return 0


def cmd_install_kit(args: argparse.Namespace) -> int:
    profile = args.profile or (Path.home() / ".cursor")
    hub = hub_root_from_env(args.hub_root) if args.hub_root else None
    if hub is None and (Path.cwd() / PROFILE_KITS_MANIFEST).is_file():
        hub = Path.cwd().resolve()

    if hub and (hub / PROFILE_KITS_MANIFEST).is_file():
        mode = "hub"
        root = hub
        data = load_profile_kits_manifest(hub)
        all_kits = sorted(data["bundles"].keys())
    else:
        mode = "consumer"
        root = resolve_consumer_root(consumer_root_from_env(args.repo))
        catalog = load_catalog(root)
        all_kits = sorted(catalog.get("bundles", {}).keys())

    kits: list[str] = []
    if args.all:
        kits = all_kits
    elif args.kit:
        kits = args.kit
    else:
        kits = [DEFAULT_KIT]

    pm = load_profile_manifest(profile)
    pm["version"] = 2
    pm["mode"] = mode
    pm["repo_hint"] = str(root)
    if "installed_kits" not in pm:
        pm["installed_kits"] = []
    if "kit_members" not in pm:
        pm["kit_members"] = {}

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Install kit(s) -> {profile} ({mode} mode)")

    for kit_id in kits:
        bundle_dir = bundle_root_for_mode(mode, root) / kit_id
        if mode == "consumer" and not bundle_dir.is_dir():
            print(f"  {kit_id}: skipped (not in published catalog)")
            continue
        if mode == "hub" and not bundle_dir.is_dir():
            print(f"  {kit_id}: run sync-profile-kit-bundles.py first", file=sys.stderr)
            continue
        print(f"=== {kit_id} ===")
        snapshot = install_kit_from_bundle(kit_id, bundle_dir, profile, args.dry_run)
        pm["kit_members"][kit_id] = snapshot
        if kit_id not in pm["installed_kits"]:
            pm["installed_kits"].append(kit_id)

    if not args.dry_run:
        path = save_profile_manifest(profile, pm)
        print(f"Manifest: {path}")
    return 0


def members_from_snapshot(snapshot: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {"rules": set(), "skills": set(), "hooks": set()}
    for kind in KINDS:
        for item in snapshot.get(kind, []):
            out[kind].add(item["name"])
    return out


def cmd_prune_kit(args: argparse.Namespace) -> int:
    profile = args.profile or (Path.home() / ".cursor")
    pm = load_profile_manifest(profile)
    installed: list[str] = pm.get("installed_kits", [])
    if not installed:
        raise SystemExit(f"No installed kits in {profile / MANIFEST_NAME}")

    to_prune = [args.kit] if args.kit else installed
    if args.kit and args.kit not in installed:
        raise SystemExit(f"Kit not installed: {args.kit}")

    # Union of members from kits we're keeping
    keep_kits = [k for k in installed if k not in to_prune]
    keep_union: dict[str, set[str]] = {"rules": set(), "skills": set(), "hooks": set()}
    for k in keep_kits:
        snap = pm.get("kit_members", {}).get(k, {})
        for kind, names in members_from_snapshot(snap).items():
            keep_union[kind] |= names

    remove_union: dict[str, set[str]] = {"rules": set(), "skills": set(), "hooks": set()}
    for k in to_prune:
        snap = pm.get("kit_members", {}).get(k, {})
        for kind, names in members_from_snapshot(snap).items():
            remove_union[kind] |= names

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Prune kit(s) {to_prune} from {profile}")

    for kind in KINDS:
        for name in sorted(remove_union[kind] - keep_union[kind]):
            target = profile / kind / name
            if not target.exists():
                print(f"  {kind}/{name}: already_absent")
                continue
            if args.dry_run:
                print(f"  {kind}/{name}: would_remove")
                continue
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            print(f"  {kind}/{name}: removed")

    if not args.dry_run:
        for k in to_prune:
            if k in pm["installed_kits"]:
                pm["installed_kits"].remove(k)
            pm.get("kit_members", {}).pop(k, None)
        save_profile_manifest(profile, pm)
    return 0


def cmd_install_legacy_all(args: argparse.Namespace) -> int:
    print("DEPRECATED: use install-profile-kit.sh --all", file=sys.stderr)
    args.all = True
    args.kit = None
    return cmd_install_kit(args)


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile kit tooling")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sync = sub.add_parser("sync", help="Sync bundle symlink trees from manifest")
    p_sync.add_argument("--hub-root", type=Path, default=None)
    p_sync.add_argument("--prune-stale", action="store_true", default=True)
    p_sync.add_argument("--no-prune-stale", action="store_false", dest="prune_stale")
    p_sync.add_argument("--allow-copy-fallback", action="store_true")
    p_sync.add_argument("--strict", action="store_true", default=True)
    p_sync.add_argument("--no-strict", action="store_false", dest="strict")
    p_sync.add_argument("--dry-run", action="store_true")

    p_export = sub.add_parser("export", help="Sync bundles and export public catalog")
    p_export.add_argument("--hub-root", type=Path, default=None)
    p_export.add_argument("--skip-sync", action="store_true")
    p_export.add_argument("--allow-copy-fallback", action="store_true")
    p_export.add_argument("--dry-run", action="store_true")

    p_list = sub.add_parser("list-kits", help="List available kits")
    p_list.add_argument("--hub-root", type=Path, default=None)
    p_list.add_argument("--repo", type=Path, default=None)

    p_install = sub.add_parser("install-kit", help="Install profile kit(s)")
    p_install.add_argument("--hub-root", type=Path, default=None)
    p_install.add_argument("--repo", type=Path, default=None)
    p_install.add_argument("--profile", type=Path, default=None)
    p_install.add_argument("--kit", action="append", default=None)
    p_install.add_argument("--all", action="store_true")
    p_install.add_argument("--dry-run", action="store_true")

    p_prune = sub.add_parser("prune-kit", help="Prune installed kit(s)")
    p_prune.add_argument("--profile", type=Path, default=None)
    p_prune.add_argument("--kit", type=str, default=None)
    p_prune.add_argument("--dry-run", action="store_true")

    p_legacy = sub.add_parser("install-all-legacy", help="Deprecated flat install")

    args = parser.parse_args()
    if args.command == "sync":
        return cmd_sync(args)
    if args.command == "export":
        return cmd_export(args)
    if args.command == "list-kits":
        return cmd_list_kits(args)
    if args.command == "install-kit":
        return cmd_install_kit(args)
    if args.command == "prune-kit":
        return cmd_prune_kit(args)
    return cmd_install_legacy_all(args)


if __name__ == "__main__":
    sys.exit(main())
