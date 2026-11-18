"""Tests for mask_front_head.py on synthetic character boards."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover - only without Pillow
    Image = None

if Image is not None:
    import mask_front_head as mfh

BG = (200, 200, 204)
SKIN = (215, 170, 140)
HAIR = (25, 22, 20)
JACKET = (50, 70, 50)
TROUSERS = (190, 175, 140)
SHOE = (250, 250, 250)


def figure(draw: "ImageDraw.ImageDraw", cx: int, head: bool, back: bool = False) -> None:
    """A standing figure 60..760 px tall; its neck runs from y=150 to y=185."""
    if head:
        draw.ellipse([cx - 38, 60, cx + 38, 155], fill=HAIR if back else SKIN)
        draw.ellipse([cx - 40, 55, cx + 40, 100], fill=HAIR)
        draw.rectangle([cx - 15, 150, cx + 15, 186], fill=HAIR if back else SKIN)
    else:
        draw.rectangle([cx - 15, 172, cx + 15, 186], fill=SKIN)
    draw.rectangle([cx - 85, 185, cx + 85, 450], fill=JACKET)
    draw.rectangle([cx - 100, 195, cx - 86, 430], fill=JACKET)
    draw.rectangle([cx + 86, 195, cx + 100, 430], fill=JACKET)
    draw.rectangle([cx - 60, 450, cx - 6, 735], fill=TROUSERS)
    draw.rectangle([cx + 6, 450, cx + 60, 735], fill=TROUSERS)
    draw.rectangle([cx - 66, 735, cx - 4, 760], fill=SHOE)
    draw.rectangle([cx + 4, 735, cx + 66, 760], fill=SHOE)


def board(front_head: bool = True, dividers: bool = False, floor: bool = False) -> "Image.Image":
    img = Image.new("RGB", (1400, 800), BG)
    draw = ImageDraw.Draw(img)
    draw.ellipse([180, 90, 520, 560], fill=SKIN)          # portrait face
    draw.ellipse([160, 60, 540, 300], fill=HAIR)           # portrait hair
    draw.rectangle([120, 600, 580, 800], fill=JACKET)      # portrait shoulders
    figure(draw, 880, front_head)
    figure(draw, 1180, True, back=True)
    if dividers:
        for x in (680, 1030):
            draw.line([(x, 0), (x, 800)], fill=(30, 30, 30), width=2)
    if floor:
        draw.rectangle([700, 740, 1400, 800], fill=(245, 245, 245))
    return img


def close(a: tuple[int, ...], b: tuple[int, ...], tol: int = 6) -> bool:
    return all(abs(x - y) <= tol for x, y in zip(a, b))


@unittest.skipIf(Image is None, "Pillow is not installed")
class MaskFrontHeadTests(unittest.TestCase):
    def check_masked(self, src: "Image.Image") -> dict:
        out, report = mfh.mask_front_head(src)
        self.assertTrue(close(out.getpixel((880, 110)), BG), "front face still visible")
        self.assertTrue(close(out.getpixel((880, 70)), BG), "front hair still visible")
        self.assertEqual(out.getpixel((880, 300)), JACKET)
        self.assertEqual(out.getpixel((1180, 110)), HAIR)     # back view keeps its head
        self.assertEqual(out.getpixel((350, 400)), SKIN)      # portrait untouched
        self.assertTrue(150 <= report["cut_y"] <= 190, report)
        return report

    def test_masks_front_head_only(self) -> None:
        report = self.check_masked(board())
        self.assertEqual(report["method"], "neck")

    def test_dividers_and_floor_do_not_join_views(self) -> None:
        self.check_masked(board(dividers=True, floor=True))

    def test_headless_front_is_left_alone(self) -> None:
        with self.assertRaises(mfh.BoardError):
            mfh.mask_front_head(board(front_head=False))

    def test_cli_writes_beside_board_and_keeps_original(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "hero.png"
            board().save(src)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mfh.main([str(src)])
            self.assertEqual(code, 0)
            result = json.loads(buf.getvalue())
            dest = Path(result["output"])
            self.assertEqual(dest.name, "hero-front-masked.png")
            self.assertTrue(close(Image.open(dest).convert("RGB").getpixel((880, 110)), BG))
            self.assertEqual(Image.open(src).convert("RGB").getpixel((880, 110)), SKIN)

    def test_cli_reports_instead_of_guessing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "plain.png"
            Image.new("RGB", (1400, 800), BG).save(src)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mfh.main([str(src)])
            self.assertEqual(code, 2)
            self.assertFalse(json.loads(buf.getvalue())["ok"])
            self.assertFalse((Path(tmp) / "plain-front-masked.png").exists())

    def test_manual_overrides(self) -> None:
        out, report = mfh.mask_front_head(board(), front=(700, 1030), cut_y=170)
        self.assertEqual(report["method"], "manual")
        self.assertTrue(close(out.getpixel((880, 110)), BG))
        self.assertEqual(out.getpixel((880, 180)), SKIN)        # below the manual cut stays


if __name__ == "__main__":
    unittest.main()
