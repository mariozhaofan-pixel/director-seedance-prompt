"""v17 supplements: benchmark line, default breathing, 200mm shallow focus, weather, dance, crew lint."""
from __future__ import annotations

import unittest
from decimal import Decimal
from pathlib import Path

from validate_prompt import lint_warnings, parse_sections, validate_prompt

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def example_with(old: str, new: str) -> str:
    text = read("examples/seedance_25_standard.md")
    assert old in text, old
    return text.replace(old, new, 1)


def warnings_for(text: str) -> list[str]:
    return lint_warnings(text, parse_sections(text, []))


class V17DocumentTests(unittest.TestCase):
    def test_benchmark_line_is_written_into_base_style(self) -> None:
        compiler = read("knowledge/07_STYLE_GENRE_FAMOUS_SCENE_COMPILER.md")
        self.assertIn("## 指定对标（补充）", compiler)
        self.assertIn("`【基础风格】` 首行写一行“对标：”", compiler)
        self.assertIn("证据分三层", compiler)
        self.assertIn("没有对标时不写这一行", compiler)
        skill = read("SKILL.md")
        self.assertIn("对标行（07）", skill)
        self.assertIn("片名对标走07", skill)
        self.assertIn("07 指定对标", read("knowledge/02E_MEDIA_EVIDENCE.md"))
        self.assertIn("对标行（作品或片段与本场借鉴的视听方法）属于风格控制", read("knowledge/08_FAST_PREFLIGHT.md"))

    def test_breathing_is_on_by_default_with_exceptions(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        section = camera.split("### 自然呼吸感（默认开启）", 1)[1].split("\n## ", 1)[0]
        for phrase in ("locked-off camera", "站位记录镜", "画幅呼吸感：关", "不写拍摄者或器材", "高度与俯仰分开写"):
            self.assertIn(phrase, section)
        self.assertIn("画幅呼吸感（开/关，默认开", read("knowledge/02K_PROJECT_SLOT.md"))
        self.assertIn("画幅默认带克制的自然呼吸感", read("knowledge/00_CORE_CARD.md"))
        self.assertIn("自然呼吸漂移", read("examples/seedance_25_standard.md"))

    def test_long_lens_shallow_focus_is_mandatory(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        self.assertIn("### 200mm 及以上：超大光圈、极浅景深（默认强制）", camera)
        self.assertIn("| 200mm | 12° |", camera)
        self.assertIn("对标和一般空间说明都不构成破例", camera)

    def test_over_shoulder_size_follows_the_narrative_subject_in_prompts(self) -> None:
        card = read("knowledge/02J_SHOT_CARD.md")
        self.assertIn("越肩镜按最近处的主体算景别", card)
        self.assertIn("越肩镜的景别按叙事主体描述", card)

    def test_weather_dance_speech_frames_vfx_and_sound(self) -> None:
        self.assertIn("### 天气接触与光源依据（补充）", read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md"))
        self.assertIn("剧情里真的淋雨、出汗时照写接触证据", read("knowledge/04A_LIVE_ACTION_TEXTURE.md"))
        self.assertIn("### 舞蹈与升格（补充）", read("knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md"))
        self.assertIn("英文对白按词数估", read("knowledge/06_TIMELINE_EDITING_SOUND.md"))
        references = read("knowledge/02_REFERENCE_ROUTER_AND_LOCKS.md")
        self.assertIn("last frame target", references)
        self.assertIn("文字改不了已经固定的首帧像素", references)
        self.assertIn("## 视效方向与受光（补充）", read("knowledge/05D_ACTION_SCENE_PHYSICS.md"))
        self.assertIn("### 声音卫生补充", read("knowledge/06B_TRANSITIONS_SOUND.md"))

    def test_dictionary_removed_and_terms_merged_into_04(self) -> None:
        self.assertFalse((ROOT / "knowledge/09_MODEL_MISREAD_PATTERNS.md").exists())
        for path in ("SKILL.md", "knowledge/00_CORE_CARD.md", "knowledge/08_FAST_PREFLIGHT.md",
                     "knowledge/02K_PROJECT_SLOT.md", "knowledge/README.md"):
            self.assertNotIn("09_MODEL_MISREAD_PATTERNS", read(path))
        self.assertNotIn("| `误判补充.md` |", read("knowledge/02K_PROJECT_SLOT.md"))
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        self.assertIn("| 横移 | `truck left/right` |", camera)
        self.assertIn("| 航拍 | `aerial viewpoint` |", camera)
        self.assertIn("拍摄者和器材不写进正文", camera)
        matrix = read("knowledge/08_MODEL_QC_REPAIR.md")
        for symptom in ("| 画面里出现摄影师、器材或其影子 |", "| 长焦镜头背景太清楚 |", "| 雨中特写人物是干的 |"):
            self.assertIn(symptom, matrix)


class V17LintTests(unittest.TestCase):
    def test_crew_in_timeline_warns(self) -> None:
        text = example_with("camera沿壁灯那侧墙边缓慢前移约二十厘米",
                            "摄影师扛着稳定器沿壁灯那侧墙边缓慢前移约二十厘米")
        found = [w for w in warnings_for(text) if w.startswith("lint M32")]
        self.assertEqual(len(found), 1)
        self.assertIn("摄影师", found[0])
        self.assertIn("稳定器", found[0])

    def test_negative_crew_list_warns(self) -> None:
        text = example_with("无字幕、无水印、无乱码文字；", "无字幕、无水印、无乱码文字，没有摄影机和摄影师入画；")
        self.assertTrue(any(w.startswith("lint M32") for w in warnings_for(text)))

    def test_long_lens_cut_without_shallow_focus_warns(self) -> None:
        text = example_with("75mm双人手部近景", "250mm双人手部近景")
        found = [w for w in warnings_for(text) if w.startswith("lint M33")]
        self.assertEqual(found, ["lint M33 CUT at 200mm or longer without 超大光圈、极浅景深 (background only as "
                                 "unreadable out-of-focus colour blocks): CUT 2"])
        text = example_with("75mm双人手部近景", "250mm双人手部近景，超大光圈、极浅景深")
        self.assertFalse(any(w.startswith("lint M33") for w in warnings_for(text)))

    def test_standard_example_stays_clean_and_valid(self) -> None:
        text = read("examples/seedance_25_standard.md")
        self.assertEqual(warnings_for(text), [])
        report = validate_prompt(text, version="2.5", profile="general", timeline="timed", duration=Decimal("24"))
        self.assertEqual(report["verdict"], "PASS", report["errors"])

    def test_benchmark_line_passes_the_envelope(self) -> None:
        text = example_with("【基础风格】\n", "【基础风格】\n对标：《某片》门口交接一段的克制双人调度；借它的低幅侧移与延迟反应，保留自然呼吸漂移；人物、服装、场景和布光仍按本片素材。\n")
        report = validate_prompt(text, version="2.5", profile="general", timeline="timed", duration=Decimal("24"))
        self.assertEqual(report["verdict"], "PASS", report["errors"])
        self.assertEqual(report["warnings"], [])


if __name__ == "__main__":
    unittest.main()
