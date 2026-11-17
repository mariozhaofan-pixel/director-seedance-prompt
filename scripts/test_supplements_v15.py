"""v15: trial entries apply directly and audit fixes."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V15DocumentTests(unittest.TestCase):
    def test_trial_entries_apply_directly(self) -> None:
        self.assertIn("新的写法问题直接写进 `项目规则.md`", read("knowledge/02K_PROJECT_SLOT.md"))
        self.assertIn("运镜方向词保留，再补一句读不反的证据", read("knowledge/00_CORE_CARD.md"))

    def test_audit_fixes(self) -> None:
        self.assertIn("十四条硬规则", read("knowledge/00_CORE_CARD.md"))
        self.assertIn("匿名类型群像（补充）", read("knowledge/02A_PROJECT_WORKFLOW.md"))
        self.assertIn("`状态事件链.md`", read("knowledge/02K_PROJECT_SLOT.md"))
        self.assertIn("按场景图里实际看到的写", read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md"))
        self.assertIn("动作所需实体", read("knowledge/08_FAST_PREFLIGHT.md"))
        self.assertIn("04A", read("SKILL.md"))

    def test_platform_profiles_stay_model_level(self) -> None:
        self.assertNotIn("PixVerse", read("knowledge/02L_PLATFORM_PROFILES.md"))


if __name__ == "__main__":
    unittest.main()
