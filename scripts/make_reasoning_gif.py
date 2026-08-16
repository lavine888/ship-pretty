#!/usr/bin/env python3
"""Build an evidence-first reasoning GIF from the real landing-page renders."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


W, H = 1200, 820
BG = (247, 247, 244)
INK = (17, 20, 17)
MUTED = (91, 98, 92)
RULE = (205, 209, 203)
RED = (201, 54, 43)
GREEN = (29, 107, 76)
WHITE = (255, 255, 252)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def mono(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = Path("C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf")
    if path.is_file():
        return ImageFont.truetype(path, size)
    return font(size, bold)


def base(step: str, label: str, title: str, accent: tuple[int, int, int] = INK) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.text((56, 38), "SHIP PRETTY / VISUAL QA", fill=MUTED, font=mono(15, True))
    draw.text((W - 56, 38), step, fill=accent, font=mono(15, True), anchor="ra")
    draw.line((56, 76, W - 56, 76), fill=RULE, width=1)
    draw.text((56, 106), label, fill=accent, font=mono(16, True))
    draw.text((56, 136), title, fill=INK, font=font(42, True))
    return image, draw


def fit_screenshot(source: Image.Image, width: int, height: int) -> Image.Image:
    return ImageOps.contain(source.convert("RGB"), (width, height), method=Image.Resampling.LANCZOS)


def paste_screenshot(image: Image.Image, source: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x, y, width, height = box
    fitted = fit_screenshot(source, width, height)
    left = x + (width - fitted.width) // 2
    top = y + (height - fitted.height) // 2
    image.paste(fitted, (left, top))
    return left, top, fitted.width, fitted.height


def outline(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: tuple[int, int, int] = RED, width: int = 3) -> None:
    draw.rectangle(box, outline=color, width=width)


def step_bar(draw: ImageDraw.ImageDraw, active: int) -> None:
    labels = ["BEFORE", "JUDGE", "PATCH", "RE-RENDER", "GATE"]
    x = 56
    y = 768
    for index, label in enumerate(labels):
        color = INK if index == active else RULE
        draw.text((x, y), label, fill=color, font=mono(13, True))
        x += 125 if index == 0 else 132


def score(draw: ImageDraw.ImageDraw, x: int, y: int, value: str, status: str, color: tuple[int, int, int]) -> None:
    draw.text((x, y), value, fill=color, font=font(50, True))
    draw.text((x, y + 63), status, fill=color, font=mono(17, True))


def make_frames(before: Image.Image, after: Image.Image) -> list[Image.Image]:
    frames: list[Image.Image] = []

    # 1. State the evidence before adding any explanation.
    image, draw = base("01 / 05", "BEFORE", "The code runs. The frame doesn't hold.", RED)
    paste_screenshot(image, before, (56, 220, 1088, 516))
    draw.rectangle((56, 220, 1144, 736), outline=RED, width=3)
    score(draw, 970, 138, "43 / 100", "NOT READY", RED)
    draw.text((56, 742), "SAME LANDING-PAGE FIXTURE / DESKTOP 1440×1000", fill=MUTED, font=mono(13, True))
    step_bar(draw, 0)
    frames.append(image)

    # 2. Make the visible problems inspectable, rather than relying on code.
    image, draw = base("02 / 05", "BEFORE / VISIBLE PROBLEMS", "Three things the screenshot makes obvious.", RED)
    left, top, width, height = paste_screenshot(image, before, (56, 218, 780, 542))
    scale_x, scale_y = width / before.width, height / before.height
    source_boxes = [
        (190, 84, 1250, 548),
        (190, 582, 1250, 892),
        (260, 110, 1190, 520),
    ]
    labels = ["01  CENTERED HERO STACK", "02  THREE EQUAL CARDS", "03  EFFECTS CARRY NO MEANING"]
    for index, (source_box, label) in enumerate(zip(source_boxes, labels)):
        sx1, sy1, sx2, sy2 = source_box
        box = (left + int(sx1 * scale_x), top + int(sy1 * scale_y), left + int(sx2 * scale_x), top + int(sy2 * scale_y))
        outline(draw, box)
        py = 245 + index * 112
        draw.line((875, py + 13, box[2] + 8, box[1] + 18), fill=RED, width=2)
        draw.text((875, py), label, fill=RED, font=mono(14, True))
        draw.text((875, py + 27), ["one visual priority, no destination", "same weight, same shape, same job", "glow substitutes for specificity"][index], fill=MUTED, font=font(14))
    step_bar(draw, 0)
    frames.append(image)

    # 3. Give the judgement a name and a stopping condition.
    image, draw = base("03 / 05", "JUDGE", "Do not call this done yet.", RED)
    paste_screenshot(image, before, (56, 220, 570, 514))
    draw.rectangle((56, 220, 626, 734), outline=RULE, width=1)
    draw.text((690, 228), "VISUAL QUALITY GATE", fill=MUTED, font=mono(15, True))
    draw.text((690, 270), "43 / 100", fill=RED, font=font(68, True))
    draw.text((690, 348), "NOT READY", fill=RED, font=mono(20, True))
    issues = [
        "Hierarchy: 4 / 10",
        "Composition: 5 / 10",
        "Specificity: 3 / 10",
    ]
    for index, text in enumerate(issues):
        y = 432 + index * 60
        draw.line((690, y + 10, 738, y + 10), fill=RED, width=5)
        draw.text((758, y), text, fill=INK, font=font(18, True))
    draw.text((690, 644), "The agent needs a visible reason to keep iterating.", fill=MUTED, font=font(16))
    step_bar(draw, 1)
    frames.append(image)

    # 4. Show the patch as decisions, not as a magical transition.
    image, draw = base("04 / 05", "PATCH", "Fix the highest-leverage decisions first.", INK)
    patches = [
        ("01", "Make the message specific", "replace generic AI promise with a clear job"),
        ("02", "Remove repetitive chrome", "let hierarchy come from type and spacing"),
        ("03", "Recompose the frame", "give proof and action different visual jobs"),
    ]
    for index, (number, title, detail) in enumerate(patches):
        y = 236 + index * 143
        draw.text((74, y), number, fill=RED, font=mono(18, True))
        draw.line((142, y + 11, 1118, y + 11), fill=RULE, width=1)
        draw.text((74, y + 36), title, fill=INK, font=font(26, True))
        draw.text((74, y + 78), detail, fill=MUTED, font=font(17))
    draw.text((74, 680), "PATCH ONE TO THREE HIGH-IMPACT PROBLEMS → RENDER AGAIN", fill=INK, font=mono(15, True))
    step_bar(draw, 2)
    frames.append(image)

    # 5. Prove the patch with a new render and a green verdict.
    image, draw = base("05 / 05", "AFTER", "Now the page makes a decision.", GREEN)
    paste_screenshot(image, after, (56, 220, 1088, 516))
    draw.rectangle((56, 220, 1144, 736), outline=GREEN, width=3)
    score(draw, 970, 138, "84 / 100", "SHIP IT", GREEN)
    draw.text((56, 742), "SAME LANDING-PAGE FIXTURE / ONE VISUAL QA LOOP", fill=MUTED, font=mono(13, True))
    step_bar(draw, 4)
    frames.append(image)

    # 6. Land the concept as a compact, self-contained proof.
    image, draw = base("RESULT", "SAME FIXTURE / DIFFERENT VERDICT", "43 → 84. That is the product.", GREEN)
    paste_screenshot(image, before, (56, 232, 520, 360))
    paste_screenshot(image, after, (624, 232, 520, 360))
    draw.rectangle((56, 232, 576, 592), outline=RED, width=3)
    draw.rectangle((624, 232, 1144, 592), outline=GREEN, width=3)
    draw.text((56, 618), "WITHOUT SHIP PRETTY", fill=RED, font=mono(15, True))
    draw.text((56, 646), "43 / 100 · NOT READY", fill=RED, font=font(24, True))
    draw.text((624, 618), "WITH SHIP PRETTY", fill=GREEN, font=mono(15, True))
    draw.text((624, 646), "84 / 100 · SHIP IT", fill=GREEN, font=font(24, True))
    draw.text((56, 714), "RENDER → JUDGE → PATCH → RE-RENDER → GATE", fill=INK, font=mono(16, True))
    step_bar(draw, 4)
    frames.append(image)
    return frames


def main() -> int:
    asset_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets")
    before = Image.open(asset_root / "benchmarks/landing-page/before/desktop.png")
    after = Image.open(asset_root / "benchmarks/landing-page/after/desktop.png")
    frames = make_frames(before, after)
    palette_frames = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=256) for frame in frames]
    output = asset_root / "demo.gif"
    palette_frames[0].save(
        output,
        save_all=True,
        append_images=palette_frames[1:],
        duration=[1800, 2200, 2200, 2100, 2200, 3000],
        loop=0,
        disposal=2,
        optimize=False,
    )
    print(f"Reasoning GIF written: {output} ({len(frames)} frames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
