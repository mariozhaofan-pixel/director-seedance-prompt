"""v21 fixes: vehicle nose-to-side geometry, gear detection next to Chinese, M35 scope, product breathing."""
from __future__ import annotations

import unittest
from pathlib import Path

from validate_prompt import CREW_RE, lint_warnings, parse_sections

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def prompt(lock: str, timeline: str) -> str:
    return (
        "### 第01段｜建议8秒｜车辆测试\n"
        "【角色/场景/素材锁定】\n"
        f"{lock}\n"
        "【基础风格】\n"
        "ARRI Alexa Mini LF，35mm。\n"
        "【运镜与时间轴】\n"
        f"{timeline}\n"
        "【声音设计】\n"
        "无背景音乐；发动机低鸣。\n"
        "【画面限制】\n"
        "无字幕、无水印、无乱码文字。"
    )


def ids(text: str) -> set[str]:
    return {w.split()[1] for w in lint_warnings(text, parse_sections(text, [])) if w.startswith("lint M")}


LEFT = "黑色跑车：低矮双门跑车，金属黑漆，左舵，驾驶座在车身左侧。"
RIGHT = "黑色跑车：低矮双门跑车，金属黑漆，右舵，驾驶座在车身右侧。"


class V21NoseSideGeometryTests(unittest.TestCase):
    def test_left_drive_driver_side_needs_nose_screen_left(self) -> None:
        bad = prompt(LEFT, "CUT 1（0-8秒）：车头始终朝画右；camera在驾驶侧约5米同速横移，全程拍到车身侧面。")
        self.assertIn("M36", ids(bad))
        good = prompt(LEFT, "CUT 1（0-8秒）：车头始终朝画左；camera在驾驶侧约5米同速横移，全程拍到车身侧面。")
        self.assertNotIn("M36", ids(good))

    def test_right_drive_mirrors(self) -> None:
        self.assertNotIn("M36", ids(prompt(RIGHT, "CUT 1（0-8秒）：车头朝画右，camera在驾驶侧前3/4，驾驶侧车门正对镜头。")))
        self.assertIn("M36", ids(prompt(RIGHT, "CUT 1（0-8秒）：车头朝画左，camera在驾驶侧前3/4，驾驶侧车门正对镜头。")))

    def test_passenger_side_and_named_sides(self) -> None:
        self.assertNotIn("M36", ids(prompt(LEFT, "CUT 1（0-8秒）：车头朝画右，camera在副驾侧约3米。")))
        self.assertIn("M36", ids(prompt(LEFT, "CUT 1（0-8秒）：车头朝画左，camera在副驾侧约3米。")))
        # named vehicle sides need no drive-side lock
        unlocked = "白色轿车：四门轿车，珍珠白漆。"
        self.assertIn("M36", ids(prompt(unlocked, "CUT 1（0-8秒）：车头朝画右，车身左侧正对镜头。")))
        self.assertNotIn("M36", ids(prompt(unlocked, "CUT 1（0-8秒）：车头朝画左，车身左侧正对镜头。")))

    def test_skips_interior_turning_and_multiple_cars(self) -> None:
        self.assertNotIn("M36", ids(prompt(LEFT, "CUT 1（0-8秒）：camera在车内副驾高度朝驾驶侧拍，车头朝画右。")))
        turning = "CUT 1（0-8秒）：车头朝画右驶来，camera在驾驶侧；车转弯后车头朝画左。"
        self.assertNotIn("M36", ids(prompt(LEFT, turning)))
        two_cars = LEFT + "\n白色轿车：四门轿车，珍珠白漆，右舵。"
        self.assertNotIn("M36", ids(prompt(two_cars, "CUT 1（0-8秒）：车头朝画右，camera在驾驶侧约5米。")))

    def test_module_example_and_table_are_consistent(self) -> None:
        module = read("knowledge/05G_VEHICLE_CINEMA.md")
        self.assertIn("车头朝哪边，就看到车身哪一侧", module)
        self.assertNotIn("车头始终朝画右，背景", module)
        good = module.split("\n合格：", 1)[1].split("```text\n", 1)[1].split("\n```", 1)[0]
        self.assertFalse(ids(prompt(LEFT, good)) & {"M34", "M35", "M36"})
        table = module.split("## 四、车拍运镜", 1)[1].split("\n- 平行跟拍", 1)[0]
        rows = [line for line in table.splitlines() if line.startswith("| ") and "---" not in line and "稳定写法" not in line]
        self.assertEqual(len(rows), 8)
        for row in rows:
            sentence = row.strip("|").split("|")[2].strip()
            with self.subTest(sentence=sentence):
                self.assertFalse(ids(prompt(LEFT, f"CUT 1（0-8秒）：{sentence}。")) & {"M35", "M36"})


class V21GearDetectionTests(unittest.TestCase):
    def test_english_gear_next_to_chinese_is_caught(self) -> None:
        for text in ("用gimbal跟拍", "DJI Ronin4D", "Ronin 4D，35mm", "Ronin跟拍", "Phantom Flex插镜"):
            with self.subTest(text=text):
                self.assertTrue(CREW_RE.search(text))

    def test_module_gear_list_is_caught(self) -> None:
        for text in ("拍摄车", "摄影车", "吸盘支架", "摇臂车", "稳定器", "云台", "无人机"):
            with self.subTest(text=text):
                self.assertTrue(CREW_RE.search(text))

    def test_non_gear_words_pass(self) -> None:
        for text in ("a ronin warrior", "浪人ronin", "云台山", "厨房墙上的吸盘挂钩", "phantom limb", "stabilized tracking"):
            with self.subTest(text=text):
                self.assertFalse(CREW_RE.search(text))


class V21VehicleScopeTests(unittest.TestCase):
    def test_m35_needs_a_vehicle_in_the_scene(self) -> None:
        classroom = prompt("教室：普通高中教室，前后两扇门。", "CUT 1（0-8秒）：阿红从教室右后门走进来。")
        self.assertNotIn("M35", ids(classroom))
        car = prompt(LEFT, "CUT 1（0-8秒）：阿红拉开右后门坐进去。")
        self.assertIn("M35", ids(car))

    def test_m35_ignores_other_things_called_che(self) -> None:
        for sentence in ("自行车左边站着阿红", "马车右侧挂着灯", "火车左侧的窗亮着", "停车左边是小卖部"):
            with self.subTest(sentence=sentence):
                self.assertNotIn("M35", ids(prompt(LEFT, f"CUT 1（0-8秒）：{sentence}。")))

    def test_m34_covers_more_car_words(self) -> None:
        for word in ("黑色MPV：七座商务车。", "网约车：白色四门车。", "绿色吉普：方正越野车身。"):
            with self.subTest(word=word):
                self.assertIn("M34", ids(prompt(word, "CUT 1（0-8秒）：司机双手握方向盘。")))


class V21CoordinationTests(unittest.TestCase):
    def test_product_detail_shots_are_a_breathing_exception(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        section = camera.split("### 自然呼吸感（默认开启）", 1)[1].split("\n## ", 1)[0]
        self.assertIn("`content_purpose=product` 的产品细节镜", section)
        self.assertIn("产品细节镜", read("knowledge/00_CORE_CARD.md").split("画幅默认带克制的自然呼吸感", 1)[1].split("\n", 1)[0])
        self.assertIn("站位记录镜、产品细节镜或项目层已关闭", read("knowledge/08_FAST_PREFLIGHT.md"))

    def test_module_facts(self) -> None:
        module = read("knowledge/05G_VEHICLE_CINEMA.md")
        self.assertIn("驱动轮先发力", module)
        self.assertNotIn("后轮先发力", module)
        self.assertNotIn("机位低于或侧对挡风玻璃", module)


if __name__ == "__main__":
    unittest.main()
