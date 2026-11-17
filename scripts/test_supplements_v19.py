"""v19 supplements: martial styles module, dance density, anamorphic evidence, shared scene direction."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\]\(([^)#]+\.md)")


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V19MartialStylesTests(unittest.TestCase):
    def test_module_is_routed_from_05c_05_and_skill(self) -> None:
        for source in ("knowledge/05C_COMBAT_CHOREOGRAPHY.md", "knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md"):
            with self.subTest(source=source):
                targets = {Path(path).name for path in LINK_RE.findall(read(source))}
                self.assertIn("05F_MARTIAL_STYLES.md", targets)
        self.assertIn("截拳道/咏春加05F", read("SKILL.md"))

    def test_module_covers_both_styles(self) -> None:
        module = read("knowledge/05F_MARTIAL_STYLES.md")
        self.assertTrue(module.startswith("# 05F Martial Styles"))
        for heading in ("## 一、写法总则（两派通用）", "## 二、截拳道", "## 三、咏春", "## 四、人物与对手",
                        "## 五、摄影与节奏", "## 六、训练戏", "## 七、声音与风格锁", "## 九、常见问题修复"):
            self.assertIn(heading, module)
        for rule in ("招式名不进正文", "限制正面写", "反应，方向顺着来力", "站架首镜写全", "决胜交换用固定远景长镜头"):
            self.assertIn(rule, module)
        for template in ("P1 截击单次进攻", "P6 对刀", "搭桥破门", "静手截击"):
            self.assertIn(template, module)

    def test_style_locks_are_positive(self) -> None:
        module = read("knowledge/05F_MARTIAL_STYLES.md")
        locks = [line for line in module.splitlines() if line.startswith("- **截拳道风格锁**") or line.startswith("- **咏春风格锁**")]
        self.assertEqual(len(locks), 2)
        for lock in locks:
            body = lock.split("：", 1)[1]
            self.assertIn("每一脚都在腰带以下", body)
            self.assertNotRegex(body, r"不要|不能|没有|禁止")


class V19SupplementTests(unittest.TestCase):
    def test_dance_density_and_phrases(self) -> None:
        performance = read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md")
        section = performance.split("### 舞蹈与升格（补充）", 1)[1].split("\n## ", 1)[0]
        for phrase in ("**动作密度**", "**乐句接力**", "第一帧人物已经在跳的中途", "承重脚始终踩实", "**从视频还原**"):
            self.assertIn(phrase, section)

    def test_anamorphic_evidence_in_04(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        self.assertIn("### 变形宽银幕的画面证据（补充）", camera)
        self.assertIn("竖向拉长的椭圆", camera)
        self.assertIn("人脸不用 24mm", camera)

    def test_shared_scene_direction_and_eye_tasks(self) -> None:
        performance = read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md")
        self.assertIn("### 全场共同方向与眼神任务（补充）", performance)
        self.assertIn("眼神写成在做事", performance)
        # the existing muscle-action rule for emotion words stays in force
        self.assertIn("### 情绪词与可见动作（补充）", performance)

    def test_three_anchor_rule_and_repair_rows(self) -> None:
        self.assertIn("每个写三个锚点", read("knowledge/05C_COMBAT_CHOREOGRAPHY.md"))
        matrix = read("knowledge/08_MODEL_QC_REPAIR.md")
        for symptom in ("| 跳舞变成走路或跑步 |", "| 跳舞时脚底打滑 |", "| 舞蹈一顿一顿像摆拍 |",
                        "| 变形宽银幕没有椭圆焦外或拉丝 |", "| 少见招式被画成普通直拳或高踢 |"):
            self.assertIn(symptom, matrix)


if __name__ == "__main__":
    unittest.main()
