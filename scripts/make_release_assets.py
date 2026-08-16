#!/usr/bin/env python3
"""Turn captured benchmark screenshots into README and release assets."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageOps


def copy_capture(capture_root: Path, asset_root: Path, source_name: str, target_name: str) -> None:
    for viewport in ("desktop", "mobile"):
        source = capture_root / source_name / f"{viewport}.png"
        target = asset_root / target_name / f"{viewport}.png"
        if not source.is_file():
            raise FileNotFoundError(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def make_social_preview(asset_root: Path) -> None:
    hero = Image.open(asset_root / "ship-pretty-hero.png").convert("RGB")
    preview = ImageOps.fit(hero, (1200, 630), method=Image.Resampling.LANCZOS, centering=(0.5, 0.45))
    preview.save(asset_root / "social-preview.png", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_root", type=Path, help="Directory containing capture_screenshots.mjs outputs")
    parser.add_argument("asset_root", type=Path, nargs="?", default=Path("assets"))
    args = parser.parse_args()

    capture_root = args.capture_root.resolve()
    asset_root = args.asset_root.resolve()
    copy_capture(capture_root, asset_root, "landing-page-before", "benchmarks/landing-page/before")
    copy_capture(capture_root, asset_root, "landing-page-after", "benchmarks/landing-page/after")
    copy_capture(capture_root, asset_root, "dashboard-before", "benchmarks/dashboard/before")
    copy_capture(capture_root, asset_root, "dashboard-after", "benchmarks/dashboard/after")
    copy_capture(capture_root, asset_root, "mobile-before", "benchmarks/mobile/before")
    copy_capture(capture_root, asset_root, "mobile-after", "benchmarks/mobile/after")
    make_social_preview(asset_root)
    print(f"Release assets written to {asset_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
