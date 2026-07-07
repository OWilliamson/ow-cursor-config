#!/usr/bin/env python3
"""Regenerate catalog/bundle-manifest.yaml and .json from rules/ and skills/ trees."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def collect_rules(rules_dir: Path) -> list[str]:
    if not rules_dir.is_dir():
        return []
    return sorted(p.name for p in rules_dir.glob("*.mdc") if p.is_file())


def collect_skills(skills_dir: Path) -> list[str]:
    if not skills_dir.is_dir():
        return []
    names: list[str] = []
    for p in sorted(skills_dir.iterdir()):
        if p.is_dir() and (p / "SKILL.md").is_file():
            names.append(p.name)
    return names


def write_yaml(path: Path, data: dict) -> None:
  lines = [
      "# Shipped rules and skills for profile install/prune.",
      "# Regenerate: python3 scripts/generate-bundle-manifest.py",
      f"version: {data['version']}",
      "rules:",
  ]
  for name in data["rules"]:
      lines.append(f"  - {name}")
  lines.append("skills:")
  for name in data["skills"]:
      lines.append(f"  - {name}")
  path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    root = repo_root()
    catalog_dir = root / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rules": collect_rules(root / "rules"),
        "skills": collect_skills(root / "skills"),
    }

    yaml_path = catalog_dir / "bundle-manifest.yaml"
    json_path = catalog_dir / "bundle-manifest.json"
    write_yaml(yaml_path, data)
    json_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {yaml_path.relative_to(root)} ({len(data['rules'])} rules, {len(data['skills'])} skills)")
    print(f"Wrote {json_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
