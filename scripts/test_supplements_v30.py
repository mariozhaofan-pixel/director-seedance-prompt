"""v30 supplements: frontal large portrait and local masking of the front full-body head."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def board_section() -> str:
    text = read("capabilities/asset-preproduction/ASSET_PREPRODUCTION.md")
    return text.split("### 中性身份板", 1)[1].split("\n### ", 1)[0]


class V30CharacterBoardTests(unittest.TestCase):
    def test_portrait_is_frontal_and_tight(self) -> None:
        section = board_section()
        for phrase in ("左侧正面大头特写", "必须正面向镜头", "鼻梁落在这一格的竖向中线", "双眼直视镜头",
                       "头部约占这一格高度的三分之二", "不是半身像，也不是胸像"):
            self.assertIn(phrase, section)
        self.assertNotIn("轻微三分之四", section)

    def test_front_head_is_masked_after_generation(self) -> None:
        section = board_section()
        for phrase in ("正面全身照常画出头", "scripts/mask_front_head.py", "-front-masked.png", "原图保留",
                       "--front x0:x1", "--cut-y", "以背景色涂掉", "交付、登记和视频引用都用盖头后的文件",
                       "不运行盖头步骤"):
            self.assertIn(phrase, section)
        self.assertNotIn("不是画一个无头人体", section)
        self.assertTrue((ROOT / "scripts/mask_front_head.py").is_file())

    def test_interfaces_describe_the_same_board(self) -> None:
        self.assertIn("正面大头特写", read("knowledge/02B_CHARACTER_BOARD.md"))
        self.assertIn("scripts/mask_front_head.py", read("INSTALL.md"))
        if (ROOT / "scripts/build_editions.py").is_file():  # source checkout; packages render README from a template
            self.assertIn("盖掉正面全身的头部", read("README.md"))
        for name in ("README.md", "INSTALL.md", "knowledge/02B_CHARACTER_BOARD.md"):
            with self.subTest(name=name):
                self.assertNotIn("不含头部", read(name))


if __name__ == "__main__":
    unittest.main()
