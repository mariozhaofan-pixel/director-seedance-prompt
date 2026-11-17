"""Core card, shot card, project slot, advisory lint and evidence/asset helpers."""
from __future__ import annotations

import json
import struct
import tempfile
import unittest
import zlib
from decimal import Decimal
from pathlib import Path

import check_assets
import take_evidence
from validate_prompt import lint_warnings, load_project_lint, parse_sections, validate_prompt

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def example_with(old: str, new: str) -> str:
    text = read("examples/seedance_25_standard.md")
    assert old in text, old
    return text.replace(old, new, 1)


def warnings_for(text: str, rules: list[dict] | None = None) -> list[str]:
    return lint_warnings(text, parse_sections(text, []), rules)


class ExecutionLayerRoutingTests(unittest.TestCase):
    def test_entry_routes_new_execution_files(self) -> None:
        skill = read("SKILL.md")
        for path in ("knowledge/00_CORE_CARD.md", "knowledge/02J_SHOT_CARD.md", "knowledge/02K_PROJECT_SLOT.md",
                     "knowledge/02L_PLATFORM_PROFILES.md"):
            with self.subTest(path=path):
                self.assertIn(path, skill)
                self.assertTrue((ROOT / path).is_file())

    def test_core_card_is_small_and_lists_hard_rules(self) -> None:
        card = read("knowledge/00_CORE_CARD.md")
        self.assertLessEqual(len(card), 15000)
        for rule in (f"R{n}" for n in range(1, 12)):
            self.assertIn(f"| {rule} |", card)

    def test_fast_preflight_opens_with_grouped_checks(self) -> None:
        fast = read("knowledge/08_FAST_PREFLIGHT.md")
        head = fast.split("## Fast Preflight Card", 1)[0]
        for group in ("**A 衔接**", "**B 空间**", "**C 人和物**", "**D 动作**", "**E 戏**", "**F 技术**"):
            self.assertIn(group, head)

    def test_symptom_lookup_lives_in_the_repair_matrix(self) -> None:
        self.assertFalse((ROOT / "knowledge/09_MODEL_MISREAD_PATTERNS.md").exists())
        matrix = read("knowledge/08_MODEL_QC_REPAIR.md").split("## 故障修复矩阵", 1)[1]
        for symptom in ("| 方向反了、镜头乱 |", "| 群演反应莫名其妙 |", "| 台词烧成字幕 |"):
            self.assertIn(symptom, matrix)

    def test_new_runtime_files_stay_local_only(self) -> None:
        for path in ("knowledge/00_CORE_CARD.md", "knowledge/02J_SHOT_CARD.md", "knowledge/02K_PROJECT_SLOT.md",
                     "knowledge/02L_PLATFORM_PROFILES.md",
                     "scripts/check_assets.py", "scripts/take_evidence.py"):
            with self.subTest(path=path):
                # Built from code points so this test file itself passes the local-edition route audit.
                cloud_words = "|".join("".join(chr(c) for c in word) for word in ((0x98DE, 0x4E66), (0x591A, 0x7EF4, 0x8868), (0x4E91, 0x8868), (0x4E91, 0x7AEF)))
                self.assertNotRegex(read(path), cloud_words + "|fei" + "shu")


class AdvisoryLintTests(unittest.TestCase):
    def test_standard_example_has_no_lint_warnings(self) -> None:
        self.assertEqual(warnings_for(read("examples/seedance_25_standard.md")), [])

    def test_world_direction_words_are_flagged(self) -> None:
        text = example_with("camera仍在两人连线的壁灯一侧", "camera在玄关南边朝北看")
        found = warnings_for(text)
        self.assertTrue(any(w.startswith("lint M1") for w in found), found)

    def test_ordinary_word_dongxi_is_not_flagged(self) -> None:
        text = example_with("台面空净", "台面上没有东西")
        self.assertFalse(any(w.startswith("lint M1") for w in warnings_for(text)))

    def test_static_state_wording_is_flagged(self) -> None:
        text = example_with("钥匙圆环露出手指", "钥匙悬在两人之间")
        self.assertTrue(any(w.startswith("lint M2") for w in warnings_for(text)))

    def test_reference_paste_and_voiceover_and_subtitle_hygiene(self) -> None:
        text = example_with("35mm中广景；", "35mm中广景，构图与图片1一致；")
        text = text.replace("林岚把钥匙平放进周远掌心", "画外音：门外有人喊了一声，林岚把钥匙平放进周远掌心", 1)
        text = text.replace("无字幕、无水印、无乱码文字；", "无水印、无乱码文字；", 1)
        found = " | ".join(warnings_for(text))
        for code in ("lint M3", "lint M4", "lint M11"):
            self.assertIn(code, found)

    def test_lint_never_changes_verdict(self) -> None:
        text = example_with("camera仍在两人连线的壁灯一侧", "camera在玄关南边朝北看")
        report = validate_prompt(text, version="2.5", profile="general", timeline="timed", duration=Decimal("24"))
        self.assertEqual(report["verdict"], "PASS", report["errors"])
        self.assertIn("advisory_lint", report["checked"])
        self.assertTrue(report["warnings"])

    def test_project_lint_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lint.json"
            path.write_text(json.dumps({"rules": [
                {"id": "key-ring", "pattern": "钥匙", "message": "project rule hit", "scope": "timeline"}]}),
                encoding="utf-8")
            rules = load_project_lint(str(path))
            found = warnings_for(read("examples/seedance_25_standard.md"), rules)
            self.assertIn("project lint key-ring: project rule hit", found)
            path.write_text(json.dumps({"rules": [{"pattern": "(", "scope": "timeline"}]}), encoding="utf-8")
            with self.assertRaises(Exception):
                load_project_lint(str(path))


def png_bytes(width: int, height: int) -> bytes:
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    chunk = b"IHDR" + ihdr
    return b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + chunk + struct.pack(">I", zlib.crc32(chunk))


class AssetCheckTests(unittest.TestCase):
    def test_header_sizes(self) -> None:
        self.assertEqual(check_assets.image_size(png_bytes(1280, 500)), (1280, 500))
        self.assertEqual(check_assets.image_size(b"GIF89a" + struct.pack("<HH", 320, 200)), (320, 200))
        jpeg = b"\xff\xd8\xff\xe0\x00\x04ab\xff\xc0\x00\x11\x08" + struct.pack(">HH", 500, 1200) + b"\x03"
        self.assertEqual(check_assets.image_size(jpeg + b"\x00" * 16), (1200, 500))

    def test_aspect_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wide, ok = Path(tmp) / "wide.png", Path(tmp) / "ok.png"
            wide.write_bytes(png_bytes(1280, 500))
            ok.write_bytes(png_bytes(1200, 500))
            limits = check_assets.PLATFORMS["seedance-2.5"]
            self.assertTrue(check_assets.check_file(wide, limits)["problems"])
            self.assertEqual(check_assets.check_file(ok, limits)["problems"], [])
            self.assertEqual(check_assets.main([str(ok)]), 0)
            self.assertEqual(check_assets.main([str(wide)]), 1)


class EvidenceTests(unittest.TestCase):
    def test_tail_range_and_markdown(self) -> None:
        info = {"duration": 21.042, "frames": 505, "fps": 24.0, "width": 1280, "height": 720}
        tail = take_evidence.tail_range(info, 51)
        self.assertEqual((tail["start_frame"], tail["end_frame"]), (454, 505))
        text = take_evidence.render_markdown(Path("take.mp4"), info, [2.0, 6.04], tail,
                                             [{"start": 18.84, "end": 20.64, "text": "回来了"}])
        self.assertIn("第 454–505 帧", text)
        self.assertIn("尾段里有台词", text)
        self.assertIn("| 3 | 6.04–21.04 |", text)
        self.assertIn("实际结尾状态", text)


if __name__ == "__main__":
    unittest.main()
