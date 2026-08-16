#!/usr/bin/env python3
"""Turn captured benchmark screenshots into README and release assets."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def copy_capture(capture_root: Path, asset_root: Path, source_name: str, target_name: str) -> None:
    for viewport in ("desktop", "mobile"):
        source = capture_root / source_name / f"{viewport}.png"
        target = asset_root / target_name / f"{viewport}.png"
        if not source.is_file():
            raise FileNotFoundError(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def make_gif(asset_root: Path) -> None:
    before = Image.open(asset_root / "benchmarks/landing-page/before/desktop.png").convert("RGB")
    after = Image.open(asset_root / "benchmarks/landing-page/after/desktop.png").convert("RGB")
    size = (960, 667)
    frames = [image.resize(size, Image.Resampling.LANCZOS) for image in (before, after)]
    frames[0].save(asset_root / "demo.gif", save_all=True, append_images=[frames[1]], duration=[2200, 2800], loop=0, optimize=True)


def make_social_preview(asset_root: Path) -> None:
    canvas = Image.new("RGB", (1200, 630), "#f4f1e9")
    draw = ImageDraw.Draw(canvas)
    dark = "#15221f"
    orange = "#ed6a42"
    draw.rectangle((0, 0, 26, 630), fill=orange)
    draw.text((86, 98), "SHIP PRETTY", fill="#17634b", font=font(24, bold=True))
    draw.text((86, 155), "AI can generate.", fill=dark, font=font(62, bold=True))
    draw.text((86, 224), "Ship Pretty decides.", fill=dark, font=font(62, bold=True))
    draw.text((88, 340), "Render → Judge → Patch → Re-render", fill="#66736d", font=font(24))
    draw.text((88, 392), "The visual quality gate for AI-built interfaces.", fill="#66736d", font=font(22))

    screenshot = Image.open(asset_root / "benchmarks/landing-page/after/desktop.png").convert("RGB")
    screenshot.thumbnail((480, 420), Image.Resampling.LANCZOS)
    x = 650
    y = 108
    canvas.paste(screenshot, (x, y))
    draw.rectangle((x + screenshot.width, y + screenshot.height, 1180, 528), fill="#f7d6c8")
    canvas.save(asset_root / "social-preview.png", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_root", type=Path, help="Directory containing capture_screenshots.mjs outputs")
    parser.add_argument("asset_root", type=Path, nargs="?", default=Path("assets"))
    args = parser.parse_args()

    capture_root = args.capture_root.resolve()
    asset_root = args.asset_root.resolve()
    copy_capture(capture_root, asset_root, "landing-page-before", "benchmarks/landing-page/before")
    copy_capture(capture_root, asset_root, "landing-page-after", "benchmarks/landing-page/after")
    copy_capture(capture_root, asset_root, "dashboard-after", "benchmarks/dashboard/after")
    copy_capture(capture_root, asset_root, "mobile-after", "benchmarks/mobile/after")
    make_gif(asset_root)
    make_social_preview(asset_root)
    print(f"Release assets written to {asset_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
