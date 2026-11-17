"""v14 supplements: crowd binding, asset reverse check, state chain, review table, scene/prop notes, anchors, M30."""
from __future__ import annotations

import unittest
from pathlib import Path

from validate_prompt import lint_warnings, parse_sections

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V14DocumentTests(unittest.TestCase):
    def test_misread_entries(self) -> None:
        self.assertIn("五官随机生成不同的陌生人", read("knowledge/02B_CHARACTER_BOARD.md"))
        self.assertIn("空泛质量词不写", read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md"))
        self.assertIn("低噪点", read("capabilities/asset-preproduction/ASSET_PREPRODUCTION.md"))
        self.assertIn("| 满场群众同一张脸 |", read("knowledge/08_MODEL_QC_REPAIR.md"))

    def test_crowd_binding_and_capability(self) -> None:
        self.assertIn("五官随机生成不同的陌生人", read("knowledge/02B_CHARACTER_BOARD.md"))
        capability = read("capabilities/asset-preproduction/ASSET_PREPRODUCTION.md")
        for heading in ("### 匿名类型群像（补充）", "### 场景补充", "### 道具补充", "### 审片表（补充）",
                        "### 多人群演半身资产", "### 中性身份板"):
            self.assertIn(heading, capability)
        self.assertIn("左右翻转原图不是反打", capability)

    def test_workflow_and_card_supplements(self) -> None:
        workflow = read("knowledge/02A_PROJECT_WORKFLOW.md")
        self.assertIn("状态事件链（补充）", workflow)
        self.assertIn("资产反查（补充）", workflow)
        self.assertIn("动作所需实体", read("knowledge/02J_SHOT_CARD.md"))
        self.assertIn("辨认特征（补充）", read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md"))
        self.assertIn("用一句话交代新的起始状态", read("knowledge/00_CORE_CARD.md"))
        self.assertIn("按场景图里实际看到的写", read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md"))


class EmptyQualityLintTests(unittest.TestCase):
    def test_buzzwords_warn(self) -> None:
        text = read("examples/seedance_25_standard.md").replace("柔和成像定焦镜头组", "柔和成像定焦镜头组，8K大师级电影感", 1)
        found = lint_warnings(text, parse_sections(text, []))
        self.assertTrue(any(w.startswith("lint M30") for w in found))

    def test_standard_example_clean(self) -> None:
        text = read("examples/seedance_25_standard.md")
        self.assertEqual(lint_warnings(text, parse_sections(text, [])), [])


if __name__ == "__main__":
    unittest.main()
