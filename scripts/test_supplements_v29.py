"""v29 supplements: 2D hand-drawn animation branch, destruction scale versus visual emphasis, material response, key-hit composition and realistic skin."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def section(text: str, heading: str) -> str:
    return text.split(heading, 1)[1].split("\n## ", 1)[0].split("\n### ", 1)[0]


class V29AnimationBranchTests(unittest.TestCase):
    def test_2d_branch_replaces_camera_language(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        branch = section(camera, "### 二维手绘动画的基础风格（补充）")
        for phrase in ("不用摄影机语言", "一拍二", "保持帧", "背景画层向后滚动", "画出来的"):
            self.assertIn(phrase, branch)
        self.assertIn("二维手绘动画不写摄影机", camera)
        self.assertIn("二维手绘动画（见上文", camera)
        self.assertIn("二维手绘段是否改写媒介", read("knowledge/08_MODEL_QC_REPAIR.md"))


class V29CombatMaterialTests(unittest.TestCase):
    def test_scale_and_emphasis_are_separate(self) -> None:
        combat = read("knowledge/05C_COMBAT_CHOREOGRAPHY.md")
        scale = combat.split("#### 破坏规模与视觉强调（补充）", 1)[1].split("需要表现可见体积或层次时", 1)[0]
        for phrase in ("先提高视觉强调", "闪避成功写躲开的路线", "破坏一旦发生就留下"):
            self.assertIn(phrase, scale)

    def test_material_table_and_afterimage(self) -> None:
        combat = read("knowledge/05C_COMBAT_CHOREOGRAPHY.md")
        for row in ("| 普通钢铁 |", "| 木材 |", "| 陶瓷 |", "| 湿泥 |", "| 能量护盾 |", "| 电气设备 |"):
            self.assertIn(row, combat)
        self.assertIn("**残影**", combat)
        self.assertNotIn("- 石材/玻璃/木材：裂纹", combat)

    def test_key_hit_composition(self) -> None:
        combat = read("knowledge/05C_COMBAT_CHOREOGRAPHY.md")
        key = combat.split("#### 关键一击的画面组织（补充）", 1)[1].split("### 战斗一镜到底摄影接力", 1)[0]
        for name in ("| 爆心 |", "| 切线 |", "| 对冲 |", "| 压境 |", "| 崩解 |"):
            self.assertIn(name, key)
        self.assertIn("只放一个瞬间", key)


class V29SkinTests(unittest.TestCase):
    def test_skin_section_and_routes(self) -> None:
        texture = read("knowledge/04A_LIVE_ACTION_TEXTURE.md")
        skin = section(texture, "## 三、写实人物肤质与眼睛")
        for phrase in ("不默认美白", "纹理跟景别走", "眼神光的位置、形状和数量对应现场光源", "写实 CG 人物", "| 玻璃珠眼睛 |"):
            self.assertIn(phrase, skin)
        self.assertIn("## 四、克制表演", texture)
        self.assertIn("写实人物肤质", read("SKILL.md"))
        self.assertIn("04A_LIVE_ACTION_TEXTURE.md", read("capabilities/asset-preproduction/ASSET_PREPRODUCTION.md"))
        self.assertIn("脸像塑料、蜡像", read("knowledge/08_MODEL_QC_REPAIR.md"))


if __name__ == "__main__":
    unittest.main()
