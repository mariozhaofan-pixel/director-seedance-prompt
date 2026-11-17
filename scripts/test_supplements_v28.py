"""v28 supplements: the folk fantasy realism style pack and its routing."""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = "knowledge/styles/folk-fantasy-realism/folk-fantasy-realism.md"
LINK_RE = re.compile(r"\]\(([^)#\s]+\.md)")
SOURCE_NAME = "\u540d\u5f52\u540d"  # the source file's name, kept out of every tracked file


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V28FolkFantasyPackTests(unittest.TestCase):
    def test_pack_is_routed(self) -> None:
        router = read("knowledge/styles/STYLE_ROUTER.md")
        self.assertIn("[Folk Fantasy Realism](folk-fantasy-realism/folk-fantasy-realism.md)", router)
        self.assertIn("选写实民俗奇幻", router)
        self.assertIn("styles/folk-fantasy-realism/folk-fantasy-realism.md", read("knowledge/README.md"))
        self.assertIn("六类", read("README.md"))

    def test_pack_structure_matches_the_library(self) -> None:
        pack = read(PACK)
        self.assertTrue(pack.startswith("# Folk Fantasy Realism"))
        for heading in ("## 挂载与作用域", "## 一、整体视觉目标", "## 二、构图机制 →【运镜与时间轴】",
                        "## 三、运动机制 →【运镜与时间轴】", "## 四、镜组与时间分配 →【运镜与时间轴】",
                        "## 五、人物情绪与表演 →【运镜与时间轴】", "## 六、音频与声画接力 →【声音设计】和【运镜与时间轴】",
                        "## 七、编译约束"):
            self.assertIn(heading, pack)
        for prefix, count in (("L", 13), ("C", 18), ("M", 18), ("P", 13), ("S", 9)):
            with self.subTest(prefix=prefix):
                self.assertIn(f"| {prefix}{count} ", pack)
        for target in LINK_RE.findall(pack):
            with self.subTest(target=target):
                self.assertTrue((ROOT / PACK).parent.joinpath(target).resolve().is_file(), target)

    def test_pack_follows_current_rules(self) -> None:
        pack = read(PACK)
        self.assertIn("用于 Seedance 提示词", pack)
        self.assertIn("各行定义按 [06]", pack)
        for stale in ("Seedance 2.5 提示词", "遮挡藏切", "允许藏切", "灰蓝瞳色", "白皙肤色", "肩扛摄像机", "摄影师跟随", "不磨皮、不美颜滤镜"):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, pack)
        limits = pack.split("| 【画面限制】 |", 1)[1].split("\n", 1)[0]
        self.assertIn("正向句", limits)

    def test_source_name_stays_out_of_tracked_files(self) -> None:
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if tracked.returncode != 0:
            self.skipTest("not a git checkout")
        for name in tracked.stdout.splitlines():
            path = ROOT / name
            if path.suffix in {".md", ".json", ".in", ".py", ".yml", ".yaml"} and path.is_file():
                with self.subTest(path=name):
                    self.assertNotIn(SOURCE_NAME, path.read_text(encoding="utf-8-sig", errors="ignore"))


if __name__ == "__main__":
    unittest.main()
