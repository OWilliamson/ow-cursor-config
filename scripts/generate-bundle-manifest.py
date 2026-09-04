#!/usr/bin/env python3
"""The kit catalog ships in catalog/. Do not regenerate from a consumer checkout."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "generate-bundle-manifest.py is retired.\n"
        "The kit catalog is catalog/bundle-manifest.json (and .yaml).\n"
        "Do not regenerate it from this checkout.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
