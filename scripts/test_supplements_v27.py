"""v27 supplements: child and pet performance module, idle-frame checks, key-frame camera derivation and transition details."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\]\(([^)#\s]+\.md)")


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V27ChildPetModuleTests(unittest.TestCase):
    def test_module_is_routed(self) -> None:
        self.assertIn("knowledge/05H_CHILD_PET_PERFORMANCE.md", read("SKILL.md"))
        for source in (
            "knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md",
            "knowledge/README.md",
            "knowledge/08_FAST_PREFLIGHT.md",
            "knowledge/08_MODEL_QC_REPAIR.md",
        ):
            with self.subTest(source=source):
                targets = {Path(path).name for path in LINK_RE.findall(read(source))}
                self.assertIn("05H_CHILD_PET_PERFORMANCE.md", targets)

    def test_module_sections_and_links(self) -> None:
        module = read("knowledge/05H_CHILD_PET_PERFORMANCE.md")
        self.assertTrue(module.startswith("# 05H Child and Pet Performance"))
        for heading in ("## 一、取向：认真做事，不靠出糗", "## 二、能力边界", "## 三、可选表演机制",
                        "## 四、多角色同框", "## 五、镜头可读性", "## 六、结束前核对"):
            self.assertIn(heading, module)
        for target in LINK_RE.findall(module):
            with self.subTest(target=target):
                self.assertTrue((ROOT / "knowledge" / target).is_file(), target)

    def test_module_keeps_story_facts(self) -> None:
        module = read("knowledge/05H_CHILD_PET_PERFORMANCE.md")
        self.assertIn("照实设计这个状态", module)
        self.assertIn("一个姿势不直接等于一种情绪", module)


class V27CraftSupplementTests(unittest.TestCase):
    def test_idle_frame_rules(self) -> None:
        section = read("knowledge/06_TIMELINE_EDITING_SOUND.md").split("### 画面空转判定（补充）", 1)[1].split("\n## ", 1)[0]
        for phrase in ("不等于观众看见了", "单独都不算新的画面信息", "换一个信息承载者", "声音负载和画面负载分开估"):
            self.assertIn(phrase, section)
        self.assertIn("台词还在推进，画面停在同一状态", read("knowledge/08_MODEL_QC_REPAIR.md"))

    def test_space_and_form_checks(self) -> None:
        visual = read("knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md")
        for heading in ("### 关键画面反推机位（补充）", "### 运动归因、前景与升空俯拍（补充）"):
            self.assertIn(heading, visual)
        self.assertIn("### 形态相容（补充）", read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md"))
        self.assertIn("**暴露决定接触**", read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md"))

    def test_transition_details(self) -> None:
        section = read("knowledge/06B_TRANSITIONS_SOUND.md").split("### 转场物理细节（补充）", 1)[1].split("\n## ", 1)[0]
        for phrase in ("摄影机向右甩，背景向左掠过", "遮挡要完全不透明", "实体遮挡和后期蒙版是两回事"):
            self.assertIn(phrase, section)


if __name__ == "__main__":
    unittest.main()
