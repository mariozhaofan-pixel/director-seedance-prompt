"""v23 supplements from an episode retro: scene image direction, continuation clips, speech, assets, capacity lint."""
from __future__ import annotations

import unittest
from decimal import Decimal
from pathlib import Path

from validate_prompt import parse_args, spoken_units, validate_prompt

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def prompt(seconds: int, cut: str) -> str:
    return (
        f"### 第01段｜建议{seconds}秒｜测试\n"
        "【角色/场景/素材锁定】\n角色A：成年女性。\n"
        "【基础风格】\n35mm。\n"
        f"【运镜与时间轴】\n{cut}\n"
        "【声音设计】\n无背景音乐。\n"
        "【画面限制】\n无字幕、无水印、无乱码文字。"
    )


def m37(text: str, seconds: int, lang: str | None, timeline: str = "timed") -> list[str]:
    report = validate_prompt(text, duration=Decimal(seconds), version="2.5", profile="general",
                             timeline=timeline, speech_lang=lang)
    return [w for w in report["warnings"] if w.startswith("lint M37")]


FIFTY_MORAE = "あいうえお" * 10


class V23RuleTextTests(unittest.TestCase):
    def test_scene_images_follow_the_shot_direction(self) -> None:
        self.assertIn("一段只挂与本段主要镜头朝向一致的那一张场景图", read("knowledge/02_REFERENCE_ROUTER_AND_LOCKS.md"))
        self.assertIn("挂的每张场景图朝向都和本段用它的镜头一致", read("knowledge/08_FAST_PREFLIGHT.md"))

    def test_continuation_clip_cases(self) -> None:
        continuation = read("knowledge/02C_CONTINUATION_REFERENCES.md")
        for phrase in ("衔接片段之后的第一个新镜头（补充）", "**切到另一空间**", "**机位要拉开**", "**接着上一镜重说或补演**",
                       "静态末尾帧仍按下文硬切"):
            self.assertIn(phrase, continuation)

    def test_speech_rules(self) -> None:
        timeline = read("knowledge/06_TIMELINE_EDITING_SOUND.md")
        self.assertIn("四个字（或四拍）以内的短台词", timeline)
        self.assertIn("日语对白按音拍估（补充）", timeline)
        for path in ("knowledge/01_CORE_EXECUTION_CONTRACT.md", "knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md",
                     "knowledge/08_MODEL_QC_REPAIR.md", "SKILL.md"):
            with self.subTest(path=path):
                self.assertIn("非中文", read(path))
        self.assertIn("没有字幕的人声反应", read("knowledge/02E_MEDIA_EVIDENCE.md"))

    def test_reference_audio_minimum(self) -> None:
        self.assertIn("单条参考音频至少 2 秒", read("knowledge/02L_PLATFORM_PROFILES.md"))
        self.assertIn("单条参考音频至少 2 秒", read("knowledge/02D_AUDIO_REFERENCES.md"))

    def test_repair_rows_stay_positive(self) -> None:
        matrix = read("knowledge/08_MODEL_QC_REPAIR.md")
        for symptom in ("| 小物件自己发光（徽章、首饰、纽扣） |", "| 摘除东西后凭空出现伤口或痕迹 |",
                        "| 可数的东西多出来（碗、杯、椅子） |"):
            self.assertIn(symptom, matrix)
        self.assertNotIn("画面限制补一句不发光", matrix)

    def test_asset_rules(self) -> None:
        assets = read("capabilities/asset-preproduction/ASSET_PREPRODUCTION.md")
        for phrase in ("灰底手势参考图", "“不要太多细节”时，默认指弱化细碎纹理", "**改编项目以原片帧为底图。**"):
            self.assertIn(phrase, assets)
        self.assertIn("以原片对应帧为底图", read("knowledge/02A_PROJECT_WORKFLOW.md"))
        self.assertIn("某个特征成为本镜主体时", read("knowledge/02B_CHARACTER_BOARD.md"))


class V23SpeechCapacityTests(unittest.TestCase):
    def test_mora_counting(self) -> None:
        self.assertEqual(spoken_units("きゃきゅきょ", "ja"), 3)
        self.assertEqual(spoken_units("がっこう", "ja"), 4)
        self.assertEqual(spoken_units("ラーメン", "ja"), 4)
        self.assertEqual(spoken_units("東京", "ja"), 4)
        self.assertEqual(spoken_units("我不是来替你决定的", "zh"), 9)

    def test_japanese_line_against_cut_length(self) -> None:
        short = prompt(6, f"CUT 1（0-6秒）：角色A看向窗外说：“{FIFTY_MORAE}”")
        self.assertEqual(len(m37(short, 6, "ja")), 1)
        long = prompt(8, f"CUT 1（0-8秒）：角色A看向窗外说：“{FIFTY_MORAE}”")
        self.assertEqual(m37(long, 8, "ja"), [])

    def test_untimed_segment_total(self) -> None:
        untimed = prompt(6, f"CUT 1：角色A看向窗外说：“{FIFTY_MORAE}”")
        found = m37(untimed, 6, "ja", timeline="untimed")
        self.assertEqual(len(found), 1)
        self.assertIn("the segment", found[0])

    def test_quotes_without_speech_are_ignored(self) -> None:
        sign = prompt(2, "CUT 1（0-2秒）：墙上的招牌写着“欢迎光临本店今天全场特价请进来看看吧”。")
        self.assertEqual(m37(sign, 2, "zh"), [])

    def test_opt_in_only(self) -> None:
        short = prompt(6, f"CUT 1（0-6秒）：角色A看向窗外说：“{FIFTY_MORAE}”")
        report = validate_prompt(short, duration=Decimal(6), version="2.5", profile="general", timeline="timed")
        self.assertNotIn("dialogue_capacity_estimate", report["checked"])
        self.assertFalse(any(w.startswith("lint M37") for w in report["warnings"]))
        self.assertEqual(parse_args(["--duration", "6", "--speech-lang", "ja"]).speech_lang, "ja")

    def test_standard_example_fits_in_chinese(self) -> None:
        example = read("examples/seedance_25_standard.md")
        self.assertEqual(m37(example, 24, "zh"), [])


if __name__ == "__main__":
    unittest.main()
