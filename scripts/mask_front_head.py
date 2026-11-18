#!/usr/bin/env python3
"""Cover the head of the front full-body view on a character board with the background colour.

The board is generated normally, with a head on the front full body. This script then
paints that head out locally, so the only readable face on the board is the large portrait.
Default layout: portrait on the left, front and back full bodies side by side on the right;
the two rightmost full-body figures are taken as front and back. The original file is kept;
the result is written beside it.

Exit codes: 0 masked, 2 nothing safe to mask (the report says why), 3 Pillow missing.
Requires Pillow.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat
except ImportError:  # pragma: no cover - only without Pillow
    Image = None

THRESHOLD = 28        # largest channel difference that still counts as background
DIVIDER_FILL = 0.95   # a thin column this full of foreground, with background beside it, is a panel line


class BoardError(Exception):
    """The board cannot be masked safely; the message says what to pass instead."""


def parse_span(text: str, size: int) -> tuple[int, int]:
    """'0.52:0.74' (fractions) or '1330:1900' (pixels) -> pixel span."""
    a, b = (float(v) for v in text.split(":", 1))
    if max(a, b) <= 1.0:
        a, b = a * size, b * size
    lo, hi = sorted((int(round(a)), int(round(b))))
    if not 0 <= lo < hi <= size:
        raise ValueError(f"span {text} lies outside 0..{size}")
    return lo, hi


def parse_pos(text: str, size: int) -> int:
    value = float(text)
    if value <= 1.0:
        value *= size
    pos = int(round(value))
    if not 0 < pos < size:
        raise ValueError(f"position {text} lies outside 0..{size}")
    return pos


def background(img: "Image.Image", box: tuple[int, int, int, int]) -> tuple[int, int, int]:
    """Median colour of the region's top, left and right borders (median of the three)."""
    x0, y0, x1, y1 = box
    band_y = max(2, (y1 - y0) // 33)
    band_x = max(2, (x1 - x0) // 50)
    strips = (img.crop((x0, y0, x1, y0 + band_y)),
              img.crop((x0, y0, x0 + band_x, y1)),
              img.crop((x1 - band_x, y0, x1, y1)))
    medians = [ImageStat.Stat(strip).median for strip in strips]
    return tuple(sorted(m[c] for m in medians)[1] for c in range(3))


def foreground(img: "Image.Image", bg: tuple[int, int, int]) -> "Image.Image":
    diff = ImageChops.difference(img, Image.new("RGB", img.size, bg))
    r, g, b = diff.split()
    mask = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mask = mask.point(lambda v: 255 if v > THRESHOLD else 0)
    return mask.filter(ImageFilter.MedianFilter(3))


def column_fill(mask: "Image.Image") -> list[float]:
    return [v / 255 for v in mask.resize((mask.width, 1), Image.BOX).tobytes()]


def row_fill(mask: "Image.Image") -> list[float]:
    return [v / 255 for v in mask.resize((1, mask.height), Image.BOX).tobytes()]


def smooth(values: list[float], radius: int) -> list[float]:
    prefix = [0.0]
    for v in values:
        prefix.append(prefix[-1] + v)
    n = len(values)
    out = []
    for i in range(n):
        lo, hi = max(0, i - radius), min(n, i + radius + 1)
        out.append((prefix[hi] - prefix[lo]) / (hi - lo))
    return out


def remove_dividers(mask: "Image.Image", fill: list[float]) -> None:
    """Erase thin full-height lines with background on both sides (panel dividers)."""
    thin = max(3, len(fill) // 200)
    draw = ImageDraw.Draw(mask)
    x = 0
    while x < len(fill):
        if fill[x] < DIVIDER_FILL:
            x += 1
            continue
        end = x
        while end < len(fill) and fill[end] >= DIVIDER_FILL:
            end += 1
        beside = [fill[i] for i in (x - 6, x - 5, end + 4, end + 5) if 0 <= i < len(fill)]
        if end - x <= thin and beside and all(v < 0.5 for v in beside):
            for i in range(max(0, x - 3), min(len(fill), end + 3)):
                draw.line([(i, 0), (i, mask.height)], fill=0)
                fill[i] = 0.0
        x = end


def figure_runs(fill: list[float], merge_gap: int) -> list[list[int]]:
    """Runs of columns that hold some foreground, merged across small gaps."""
    runs: list[list[int]] = []
    for x, v in enumerate(fill):
        if v > 0.01:
            if runs and x - runs[-1][1] <= merge_gap:
                runs[-1][1] = x + 1
            else:
                runs.append([x, x + 1])
    return runs


def plateau(width: list[float], idx: int, lo: int, hi: int) -> int:
    """Middle row of the narrow band around idx (rows within 8% of its width)."""
    limit = width[idx] * 1.08 + 1
    a = idx
    while a - 1 >= lo and width[a - 1] <= limit:
        a -= 1
    b = idx
    while b + 1 < hi and width[b + 1] <= limit:
        b += 1
    return (a + b) // 2


def find_neck(width: list[float], top: int, fig: int) -> tuple[int, str]:
    head_w = max(width[top: top + int(0.09 * fig) + 1])
    lo = top + int(0.07 * fig)
    # Realistic proportions: the shoulders are clearly wider than the widest part of the head.
    shoulder = next((y for y in range(top + int(0.09 * fig), top + int(0.5 * fig))
                     if width[y] >= 1.3 * head_w), None)
    if shoulder is not None and shoulder - top >= 0.1 * fig:
        seg = width[lo:shoulder]
        idx = lo + seg.index(min(seg))
        cut = plateau(width, idx, lo, shoulder)
        head_max = max(width[top:idx + 1])
        if head_max >= 1.12 * width[idx]:
            return cut, "neck"
        # Hair hangs beside the neck, so no narrowing shows: stop just above the shoulder line.
        return shoulder - max(2, int(0.01 * fig)), "shoulder-line"
    # Stylised proportions: the head is as wide as the body, so take the narrowest
    # row that has a wider head above it and a wider body just below it.
    best = None
    reach = int(0.15 * fig)
    for y in range(top + int(0.06 * fig), top + int(0.45 * fig)):
        above = max(width[top:y])
        below = max(width[y:y + reach])
        if above >= 1.2 * width[y] and below >= 1.2 * width[y]:
            if best is None or width[y] < width[best]:
                best = y
    if best is not None:
        return plateau(width, best, top + int(0.06 * fig), top + int(0.45 * fig)), "narrowest"
    raise BoardError("no head found on the front view; nothing changed. "
                     "If it does have a head, pass --cut-y with the row to cover down to.")


def edge_colour(img: "Image.Image", x: int, y: int, step: int, bg: tuple[int, int, int]) -> tuple[int, ...]:
    """Median of a few pixels just outside the fill box on this row; bg if they are not background."""
    xs = [x + step * k for k in range(1, 7) if 0 <= x + step * k < img.width]
    if not xs:
        return bg
    px = [img.getpixel((xx, y)) for xx in xs]
    colour = tuple(sorted(p[c] for p in px)[len(px) // 2] for c in range(3))
    if max(abs(colour[c] - bg[c]) for c in range(3)) > THRESHOLD * 1.5:
        return bg
    return colour


def mask_front_head(img: "Image.Image", front: tuple[int, int] | None = None,
                    cut_y: int | None = None) -> tuple["Image.Image", dict]:
    img = img.convert("RGB")
    W, H = img.size
    bg = background(img, (W // 2, 0, W, H))
    mask = foreground(img, bg)
    # Column profile from the upper 80% only, so a drawn floor or shadow does not join the figures.
    upper = mask.crop((0, 0, W, int(H * 0.8)))
    fill = column_fill(upper)
    remove_dividers(mask, fill)

    if front is not None:
        left_limit, right_limit = front
        cols = [x for x in range(front[0], front[1]) if fill[x] > 0.01]
        if not cols:
            raise BoardError("--front span holds no figure")
        bx0, bx1 = cols[0], cols[-1] + 1
    else:
        figures = []
        for x0, x1 in figure_runs(fill, max(2, W // 400)):
            if not 0.03 * W <= x1 - x0 <= 0.3 * W:
                continue
            rows = [y for y, v in enumerate(row_fill(mask.crop((x0, 0, x1, H)))) if v > 0.02]
            if rows and rows[-1] - rows[0] >= 0.6 * H:
                figures.append((x0, x1))
        if len(figures) < 2:
            raise BoardError("could not find separate front and back full-body views; pass --front x0:x1")
        (bx0, bx1), back = figures[-2], figures[-1]
        prev_end = figures[-3][1] if len(figures) > 2 else 0
        left_limit = (prev_end + bx0) // 2
        right_limit = (bx1 + back[0]) // 2

    figure = mask.crop((bx0, 0, bx1, H))
    rows = smooth(row_fill(figure), max(2, H // 300))
    width = [v * (bx1 - bx0) for v in rows]
    on = [y for y, v in enumerate(width) if v > max(3, 0.02 * (bx1 - bx0))]
    if not on:
        raise BoardError("front view is empty")
    top, bottom = on[0], on[-1]
    fig = bottom - top
    if fig < 0.4 * H:
        raise BoardError("front view is not a full body; nothing changed")

    if cut_y is not None:
        cut, method = cut_y, "manual"
    else:
        cut, method = find_neck(width, top, fig)
    if cut <= top:
        raise BoardError("cut row lies above the front view; nothing changed")

    head = figure.crop((0, top, bx1 - bx0, cut)).getbbox()
    if head is None:
        raise BoardError("nothing to cover above the cut row")
    hx0, hx1 = bx0 + head[0], bx0 + head[2]
    pad_x = max(4, int(0.12 * (hx1 - hx0)))
    x0 = max(left_limit, hx0 - pad_x)
    x1 = min(right_limit, hx1 + pad_x)
    y0 = max(0, top - max(3, int(0.01 * fig)))
    y1 = cut

    patch = []
    span = max(1, x1 - x0 - 1)
    for y in range(y0, y1):
        left = edge_colour(img, x0, y, -1, bg)
        right = edge_colour(img, x1 - 1, y, 1, bg)
        for i in range(x1 - x0):
            t = i / span
            patch.append(tuple(int(round(left[c] + (right[c] - left[c]) * t)) for c in range(3)))
    block = Image.new("RGB", (x1 - x0, y1 - y0))
    block.putdata(patch)
    out = img.copy()
    out.paste(block, (x0, y0))
    report = {
        "front_view": [bx0, bx1],
        "figure_rows": [top, bottom],
        "cut_y": cut,
        "covered_box": [x0, y0, x1, y1],
        "method": method,
        "background": list(bg),
    }
    return out, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("board", help="character board image")
    parser.add_argument("-o", "--output", help="output path (default: <name>-front-masked.png beside the board)")
    parser.add_argument("--front", help="front view column, x0:x1 in pixels or fractions of the width")
    parser.add_argument("--cut-y", help="cover down to this row, in pixels or a fraction of the height")
    args = parser.parse_args(argv)
    if Image is None:
        print(json.dumps({"ok": False, "error": "Pillow is not installed (pip install pillow)"}, ensure_ascii=False))
        return 3
    src = Path(args.board)
    img = Image.open(src)
    try:
        front = parse_span(args.front, img.width) if args.front else None
        cut = parse_pos(args.cut_y, img.height) if args.cut_y else None
        out, report = mask_front_head(img, front, cut)
    except (BoardError, ValueError) as exc:
        print(json.dumps({"ok": False, "board": str(src), "error": str(exc)}, ensure_ascii=False))
        return 2
    dest = Path(args.output) if args.output else src.with_name(f"{src.stem}-front-masked.png")
    out.save(dest)
    print(json.dumps({"ok": True, "board": str(src), "output": str(dest), **report}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
