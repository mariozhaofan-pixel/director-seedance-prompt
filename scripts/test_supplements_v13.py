"""v13 supplements: staging record shot, off-screen compromise, relation framing, POV wording."""
from __future__ import annotations

import unittest
from pathlib import Path

import take_evidence
from validate_prompt import lint_warnings, parse_sections

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V13DocumentTests(unittest.TestCase):
    def test_staging_record_mode_is_optional_and_documented(self) -> None:
        continuation = read("knowledge/02C_CONTINUATION_REFERENCES.md")
        self.assertIn("### 站位记录镜（可选模式）", continuation)
        self.assertIn("默认关", continuation)
        self.assertIn("站位记录镜", read("knowledge/02K_PROJECT_SLOT.md"))
        self.assertIn("站位记录镜整镜视频", read("knowledge/00_CORE_CARD.md"))

    def test_record_shot_is_attached_as_video_not_a_frame(self) -> None:
        continuation = read("knowledge/02C_CONTINUATION_REFERENCES.md")
        section = continuation.split("### 站位记录镜（可选模式）", 1)[1].split("\n## ", 1)[0]
        self.assertIn("整镜截出作 `@视频1`", section)
        self.assertIn("不截帧当 `@图片`", section)
        self.assertIn("不另挂记录镜之前的剧情尾段", section)
        self.assertIn("整镜匀速放慢补齐", section)
        self.assertNotIn("记录镜中的一帧", section)
        self.assertIn("站位记录镜整镜视频作 `@视频1`", continuation.split("### 站位记录镜", 1)[0])
        for path in ("knowledge/00_CORE_CARD.md", "knowledge/02J_SHOT_CARD.md"):
            self.assertNotIn("站位记录帧", read(path))

    def test_misread_entries_and_compromise(self) -> None:
        grammar = read("knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md")
        self.assertIn("某某在画外左侧，本镜看不见", grammar)
        self.assertIn("写明两人并肩同侧", grammar)
        self.assertIn("### 主观镜头写法（补充）", grammar)

    def test_visual_grammar_supplements(self) -> None:
        grammar = read("knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md")
        self.assertIn("### 关系构图口令（补充）", grammar)
        self.assertIn("### 主观镜头写法（补充", grammar)
        self.assertIn("视线点与机位相容（补充）", grammar)
        self.assertIn("- eyeline match：", grammar)


class V13ToolTests(unittest.TestCase):
    def test_tail_range_skips_record_shot(self) -> None:
        info = {"duration": 23.0, "frames": 552, "fps": 24.0, "width": 1280, "height": 720}
        tail = take_evidence.tail_range(info, 51, record_seconds=2)
        self.assertEqual((tail["start_frame"], tail["end_frame"]), (453, 504))
        tail = take_evidence.tail_range(info, 51, record_start=507)
        self.assertEqual((tail["start_frame"], tail["end_frame"]), (456, 507))

    def test_record_range_follows_the_actual_cut(self) -> None:
        info = {"duration": 23.0, "frames": 552, "fps": 24.0, "width": 1280, "height": 720}
        # Generated record shot ran 45 frames instead of the planned 48.
        record = take_evidence.record_range(info, [9.5, 18.04, 21.125], record_seconds=2)
        self.assertEqual((record["start_frame"], record["end_frame"], record["frames"]), (507, 552, 45))
        self.assertEqual(record["source"], "cut")
        # An earlier cut outside the window is ignored; the planned length is the fallback.
        record = take_evidence.record_range(info, [9.5, 18.04], record_seconds=2)
        self.assertEqual((record["start_frame"], record["frames"], record["source"]), (504, 48, "planned"))

    def test_short_record_shot_is_slowed_whole(self) -> None:
        record = {"start_frame": 507, "end_frame": 552, "frames": 45}
        plan = take_evidence.record_clip_plan(record, 51)
        self.assertEqual(plan["frames"], 51)
        self.assertAlmostEqual(plan["slow_factor"], 51 / 45, places=5)
        self.assertEqual(take_evidence.record_clip_plan(record, 0), {"frames": 45, "slow_factor": 1.0})
        for speed in (45 / 51, 0.3, 3.0):
            steps = take_evidence.atempo_chain(speed)
            self.assertTrue(all(0.5 <= s <= 2.0 for s in steps))
            product = 1.0
            for s in steps:
                product *= s
            self.assertAlmostEqual(product, speed, places=9)

    def test_evidence_markdown_routes_record_shot_as_video(self) -> None:
        info = {"duration": 23.0, "frames": 552, "fps": 24.0, "width": 1280, "height": 720}
        record = take_evidence.record_range(info, [21.125], record_seconds=2)
        plan = take_evidence.record_clip_plan(record, 51)
        tail = take_evidence.tail_range(info, 51, record_start=record["start_frame"])
        text = take_evidence.render_markdown(Path("01.mp4"), info, [21.125], tail, None, record, plan)
        self.assertIn("staging_record.mp4", text)
        self.assertIn("整镜作 @视频1（视频，不截帧）", text)
        self.assertIn("补到 51 帧", text)
        self.assertNotIn("staging_record.png", text)
        self.assertNotIn("@图片", text)

    def test_pov_eye_mask_lint(self) -> None:
        text = read("examples/seedance_25_standard.md").replace(
            "35mm中广景；", "35mm中广景，从眼睛里看出去；", 1)
        found = lint_warnings(text, parse_sections(text, []))
        self.assertTrue(any(w.startswith("lint M28") for w in found))


if __name__ == "__main__":
    unittest.main()
