"""v11 supplements: trial misread entries, posture ledger, shot-size rule, live-action module, extended lint."""
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


class SupplementDocumentTests(unittest.TestCase):
    def test_misread_rewrites_live_in_owning_modules(self) -> None:
        grammar = read("knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md")
        self.assertIn("- 人数写死：正向数清", grammar)
        self.assertIn("会被读成第一人称", grammar)
        self.assertIn("前后差两三帧", grammar)
        action = read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md")
        for phrase in ("静止状态写成持续过程", "非攻击姿势不写完成态", "不用他/她", "红色液体"):
            self.assertIn(phrase, action)
        self.assertIn("| 人数越来越多 |", read("knowledge/08_MODEL_QC_REPAIR.md"))

    def test_shot_card_has_posture_ledger_and_roster(self) -> None:
        card = read("knowledge/02J_SHOT_CARD.md")
        self.assertIn("## 逐人起止体态", card)
        self.assertIn("站位只写在拍到它的那一镜", card)
        self.assertIn("机位角度变化超过30°", card)

    def test_core_card_supplements(self) -> None:
        core = read("knowledge/00_CORE_CARD.md")
        for rule in ("| R12 |", "| R13 |", "| R14 |"):
            self.assertIn(rule, core)
        self.assertIn("增补级别", core)
        self.assertIn("先给几个方案", core)
        self.assertLessEqual(len(core), 15000)

    def test_supplements_do_not_replace_existing_guidance(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        self.assertIn("复杂复合运镜优先调用 `@视频`", camera)
        self.assertIn("运镜方向的读不反证据（补充，不替换方向词", camera)
        self.assertIn("### 光影物理补充", camera)
        self.assertIn("one continuous shot, no hard cut", read("knowledge/06_TIMELINE_EDITING_SOUND.md"))
        self.assertIn("单镜到底的声音补充", read("knowledge/06_TIMELINE_EDITING_SOUND.md"))
        self.assertIn("### 偏心构图的占位补充", read("knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md"))
        self.assertIn("## 可观测物理证据（补充）", read("knowledge/05D_ACTION_SCENE_PHYSICS.md"))

    def test_live_action_module_is_routed_and_optional(self) -> None:
        module = read("knowledge/04A_LIVE_ACTION_TEXTURE.md")
        self.assertIn("priority: optional", module)
        self.assertIn("04A_LIVE_ACTION_TEXTURE.md", read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md"))
        self.assertIn("04A_LIVE_ACTION_TEXTURE.md", read("knowledge/README.md"))

    def test_fast_preflight_stays_bounded(self) -> None:
        self.assertLessEqual(len(read("knowledge/08_FAST_PREFLIGHT.md")), 8000)


class ExtendedLintTests(unittest.TestCase):
    def test_standard_example_is_clean(self) -> None:
        self.assertEqual(warnings_for(read("examples/seedance_25_standard.md")), [])

    def test_pronoun_in_multi_character_cut(self) -> None:
        text = example_with("林岚向前递出半臂", "她向前递出半臂")
        self.assertTrue(any(w.startswith("lint M22") for w in warnings_for(text)))

    def test_array_growth_and_pov_and_sensitive_words(self) -> None:
        text = example_with("门外低弱车声", "门外低弱车声")
        text = text.replace("林岚把钥匙平放进周远掌心", "门外的人越来越多，两只手从画面下边伸上来，林岚把钥匙平放进周远掌心", 1)
        text = text.replace("钥匙尺寸、齿形和圆环一致。", "钥匙尺寸、齿形和圆环一致，地上有一滩血。", 1)
        found = " | ".join(warnings_for(text))
        for code in ("lint M18", "lint M17", "lint M19"):
            self.assertIn(code, found)

    def test_restriction_conflict(self) -> None:
        text = example_with("钥匙尺寸、齿形和圆环一致。", "钥匙尺寸、齿形和圆环一致；画面里没有半开的门。")
        self.assertTrue(any(w.startswith("lint M23") for w in warnings_for(text)))

    def test_negated_mention_in_timeline_is_not_a_conflict(self) -> None:
        text = example_with("钥匙尺寸、齿形和圆环一致。", "钥匙尺寸、齿形和圆环一致；没有慢动作。")
        text = text.replace("林岚把钥匙平放进周远掌心", "没有慢动作，林岚把钥匙平放进周远掌心", 1)
        self.assertFalse(any(w.startswith("lint M23") for w in warnings_for(text)))


if __name__ == "__main__":
    unittest.main()
