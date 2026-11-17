"""v20 supplements: vehicle cinema module, content purpose, camera systems, vehicle lint."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

from validate_prompt import lint_warnings, parse_sections

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\]\(([^)#]+\.md)")


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def prompt(lock: str, timeline: str, style: str = "ARRI Alexa Mini LF，35mm。") -> str:
    return (
        "### 第01段｜建议8秒｜车辆测试\n"
        "【角色/场景/素材锁定】\n"
        f"{lock}\n"
        "【基础风格】\n"
        f"{style}\n"
        "【运镜与时间轴】\n"
        f"{timeline}\n"
        "【声音设计】\n"
        "无背景音乐；发动机低鸣与轮胎滚动声。\n"
        "【画面限制】\n"
        "无字幕、无水印、无乱码文字。"
    )


def lint(text: str) -> list[str]:
    return lint_warnings(text, parse_sections(text, []))


def ids(warnings: list[str]) -> set[str]:
    return {w.split()[1] for w in warnings if w.startswith("lint M")}


class V20VehicleModuleTests(unittest.TestCase):
    def test_module_is_routed(self) -> None:
        self.assertIn("knowledge/05G_VEHICLE_CINEMA.md", read("SKILL.md"))
        for source in (
            "knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md",
            "knowledge/05D_ACTION_SCENE_PHYSICS.md",
            "knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md",
            "knowledge/README.md",
            "knowledge/08_FAST_PREFLIGHT.md",
            "knowledge/08_MODEL_QC_REPAIR.md",
        ):
            with self.subTest(source=source):
                targets = {Path(path).name for path in LINK_RE.findall(read(source))}
                self.assertIn("05G_VEHICLE_CINEMA.md", targets)

    def test_module_sections(self) -> None:
        module = read("knowledge/05G_VEHICLE_CINEMA.md")
        self.assertTrue(module.startswith("# 05G Vehicle Cinema"))
        for heading in ("## 一、车辆身份锁", "## 二、车身左右：第三套左右", "## 三、机位：先定站位，再定运动",
                        "## 四、车拍运镜", "## 五、日常驾驶物理", "## 六、车漆、玻璃与反射",
                        "## 七、产品展示段（content_purpose=product）", "## 八、车辆常见问题与修法"):
            self.assertIn(heading, module)
        for rule in ("左舵或右舵", "同一句给出画面投影", "速度证据一致", "反射跟着视差走", "拍摄器材不进正文"):
            self.assertIn(rule, module)

    def test_module_links_resolve(self) -> None:
        base = ROOT / "knowledge"
        for target in LINK_RE.findall(read("knowledge/05G_VEHICLE_CINEMA.md")):
            with self.subTest(target=target):
                self.assertTrue((base / target).resolve().is_file(), target)

    def test_module_example_is_lint_clean(self) -> None:
        module = read("knowledge/05G_VEHICLE_CINEMA.md")
        good = module.split("\n合格：", 1)[1].split("```text\n", 1)[1].split("\n```", 1)[0]
        text = prompt("黑色跑车：低矮双门跑车，金属黑漆，五辐银色轮毂，左舵，驾驶座在车身左侧。", good)
        self.assertFalse(ids(lint(text)) & {"M1", "M30", "M32", "M34", "M35"}, lint(text))


class V20RoutingTests(unittest.TestCase):
    def test_content_purpose_is_resolved_with_supplement_level(self) -> None:
        core = read("knowledge/00_CORE_CARD.md")
        for token in ("`content_purpose`", "`product`", "`mixed`", "记入 Resolved Policy"):
            self.assertIn(token, core)

    def test_camera_systems_and_motion_gear(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        for body in ("ARRI Alexa 265", "ARRI Alexa Mini LF", "Panavision Millennium DXL2",
                     "Blackmagic URSA Cine 12K LF", "Canon EOS C400"):
            self.assertIn(f"| {body}", camera)
        self.assertIn("### 高速与稳定运动不按机身写（补充）", camera)
        self.assertIn("一段只选一套主摄影机系统", camera)

    def test_style_compiler_rows(self) -> None:
        genre = read("knowledge/07_STYLE_GENRE_FAMOUS_SCENE_COMPILER.md")
        self.assertIn("| Michael Mann 夜城疏离 |", genre)
        self.assertIn("| Refn 霓虹克制 |", genre)

    def test_asset_vehicle_views(self) -> None:
        assets = read("capabilities/asset-preproduction/ASSET_PREPRODUCTION.md")
        self.assertIn("### 车辆补充", assets)
        self.assertIn("左舵或右舵", assets)


class V20VehicleLintTests(unittest.TestCase):
    LOCK = "白色轿车：四门轿车，珍珠白漆，银色多辐轮毂。"

    def test_m34_missing_drive_side(self) -> None:
        text = prompt(self.LOCK, "CUT 1（0-8秒）：camera在车内副驾高度，驾驶者双手握方向盘看向前方道路，画左是车窗。")
        self.assertIn("M34", ids(lint(text)))

    def test_m34_clear_when_locked(self) -> None:
        text = prompt(self.LOCK + "左舵，驾驶座在车身左侧。",
                      "CUT 1（0-8秒）：camera在车内副驾高度，驾驶者双手握方向盘看向前方道路，画左是车窗。")
        self.assertNotIn("M34", ids(lint(text)))

    def test_m34_ignores_cars_without_cabin_action(self) -> None:
        text = prompt(self.LOCK, "CUT 1（0-8秒）：车头朝画右停在路边，camera在前3/4低机位极慢推近。")
        self.assertNotIn("M34", ids(lint(text)))

    def test_m35_side_without_projection(self) -> None:
        text = prompt(self.LOCK + "左舵。", "CUT 1（0-8秒）：camera在车身左侧低机位跟随，车辆加速驶离。")
        found = lint(text)
        self.assertIn("M35", ids(found))
        self.assertTrue(any("车身左侧" in w for w in found))

    def test_m35_clear_with_projection(self) -> None:
        text = prompt(self.LOCK + "左舵。", "CUT 1（0-8秒）：camera在驾驶侧前3/4，车头朝画左，驾驶侧车门正对镜头。")
        self.assertNotIn("M35", ids(lint(text)))

    def test_m32_catches_motion_gear_names(self) -> None:
        for word in ("DJI Ronin 4D", "云台", "摄影车", "gimbal"):
            with self.subTest(word=word):
                text = prompt(self.LOCK, "CUT 1（0-8秒）：车头朝画右，camera平稳横移。", style=f"{word}，35mm。")
                self.assertIn("M32", ids(lint(text)))

    def test_m32_allows_mountain_name(self) -> None:
        text = prompt("云台山：峡谷步道。", "CUT 1（0-8秒）：camera在步道画左低机位前推。")
        self.assertNotIn("M32", ids(lint(text)))


if __name__ == "__main__":
    unittest.main()
