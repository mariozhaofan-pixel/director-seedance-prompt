"""v18 supplements: phone vlog style pack, phone-held breathing, performance energy, open intent."""
from __future__ import annotations

import unittest
from pathlib import Path

from validate_prompt import lint_warnings, parse_sections

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V18PhoneVlogTests(unittest.TestCase):
    def test_router_lists_the_phone_vlog_pack(self) -> None:
        router = read("knowledge/styles/STYLE_ROUTER.md")
        self.assertIn("[Phone Vlog](phone-vlog/phone-vlog.md)", router)
        self.assertIn("不为比较而先读五个全文", router)
        self.assertIn("正剧里只有个别镜头是手机屏幕或手机视角时不换包", router)

    def test_pack_covers_the_four_shooting_relations(self) -> None:
        pack = read("knowledge/styles/phone-vlog/phone-vlog.md")
        for relation in ("| 自拍 |", "| 同伴手持拍 |", "| 镜面自拍 |", "| 放置机位 |"):
            self.assertIn(relation, pack)
        for rule in ("持机的那只手一直被占着", "景深保留环境", "本镜看不见", "不写拍摄者、摄影师、稳定器"):
            self.assertIn(rule, pack)
        self.assertIn("## 八、常见问题修复", pack)

    def test_pack_follows_the_house_prompt_conventions(self) -> None:
        pack = read("knowledge/styles/phone-vlog/phone-vlog.md")
        for column in ("【基础风格】", "【运镜与时间轴】", "【声音设计】"):
            self.assertIn(column, pack)
        self.assertIn("04 的画幅呼吸感照常开启", pack)

    def test_phone_held_breathing_is_an_04_rule(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        section = camera.split("### 自然呼吸感（默认开启）", 1)[1].split("\n## ", 1)[0]
        self.assertIn("**手机拍摄**", section)
        self.assertIn("styles/phone-vlog/phone-vlog.md", section)

    def test_selfie_framing_passes_the_crew_lint(self) -> None:
        text = ("【运镜与时间轴】\n前提：阿红右手举起的手机前置镜头视角，约一臂远、略高于眼睛；"
                "同伴在画外镜头后方，本镜看不见。\n")
        self.assertFalse(any(w.startswith("lint M32") for w in lint_warnings(text, parse_sections(text, []))))


class V18PerformanceTests(unittest.TestCase):
    def test_strategy_is_an_action_on_the_other_person(self) -> None:
        performance = read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md")
        self.assertIn("策略写成作用于对方的动作", performance)
        self.assertIn("这个办法要可能失败", performance)

    def test_energy_is_not_flattened_by_cinematic_restraint(self) -> None:
        performance = read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md")
        self.assertIn("### 人物活力与幅度（补充）", performance)
        self.assertIn("不是把所有人缩小的理由", performance)

    def test_vague_intent_keeps_open_endings(self) -> None:
        core = read("knowledge/00_CORE_CARD.md")
        self.assertIn("原话里有意的含混和开放结局保留", core)


if __name__ == "__main__":
    unittest.main()
