"""v12 supplements: eye colour, off-screen naming, emotion cues, rhythm aids, delivery table, combat variants."""
from __future__ import annotations

import unittest
from pathlib import Path

from validate_prompt import lint_warnings, parse_sections

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def example_with(old: str, new: str) -> str:
    text = read("examples/seedance_25_standard.md")
    assert old in text, old
    return text.replace(old, new, 1)


def warnings_for(text: str) -> list[str]:
    return lint_warnings(text, parse_sections(text, []))


class V12DocumentTests(unittest.TestCase):
    def test_misread_entries(self) -> None:
        action = read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md")
        self.assertIn("- 眼睛颜色（补充）：", action)
        self.assertIn("### 情绪词与可见动作（补充）", action)
        self.assertIn("- 画外角色不点名：", read("knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md"))
        self.assertIn("| 眼睛发光 |", read("knowledge/08_MODEL_QC_REPAIR.md"))

    def test_performance_supplements_keep_existing_tables(self) -> None:
        body = read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md")
        self.assertIn("| 麻木 | 表情平、动作机械 | locked-off frame |", body)
        self.assertIn("### 情绪词与可见动作（补充）", body)
        self.assertIn("### 全身动力学写法模板（补充）", body)
        self.assertIn("眼睛颜色（补充", body)

    def test_rhythm_supplement(self) -> None:
        timeline = read("knowledge/06_TIMELINE_EDITING_SOUND.md")
        self.assertIn("没有理由的切镜会降低 Seedance 稳定性。", timeline)
        self.assertIn("### 切点、张力曲线与节拍速查（补充）", timeline)
        for beat in ("| 铺垫 |", "| 升级 |", "| 转折 |", "| 爆发 |", "| 收尾 |"):
            self.assertIn(beat, timeline)

    def test_delivery_table_and_combat_variants(self) -> None:
        self.assertIn("镜头｜画面内容｜作用", read("knowledge/02A_PROJECT_WORKFLOW.md"))
        combat = read("knowledge/05C_COMBAT_CHOREOGRAPHY.md")
        self.assertIn("#### 递进反馈链与失衡构图（补充，可选）", combat)
        self.assertIn("#### 非对称尺度摄影", combat)


class EyeColourLintTests(unittest.TestCase):
    def test_eye_colour_without_anchor_warns(self) -> None:
        text = example_with("齐肩黑发", "齐肩黑发，一双紫色眼睛")
        self.assertTrue(any(w.startswith("lint M24") for w in warnings_for(text)))

    def test_eye_colour_with_anchor_is_clean(self) -> None:
        text = example_with("齐肩黑发", "齐肩黑发，紫色眼睛有黑瞳仁、不发光")
        self.assertFalse(any(w.startswith("lint M24") for w in warnings_for(text)))

    def test_standard_example_still_clean(self) -> None:
        self.assertEqual(warnings_for(read("examples/seedance_25_standard.md")), [])


if __name__ == "__main__":
    unittest.main()
