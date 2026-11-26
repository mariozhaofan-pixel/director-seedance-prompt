#!/usr/bin/env python3
"""Behavioral regressions for the shared general/combat validator."""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

from test_validate_combat_prompt import make_prompt
from validate_prompt import (dialogue_lines, lint_warnings, parse_args, parse_sections, speech_need,
                             validate_prompt)


GENERAL = Path(__file__).with_name("validate_prompt.py")
COMBAT = Path(__file__).with_name("validate_combat_prompt.py")


class SharedValidatorTests(unittest.TestCase):
    def check(self, candidate: str, duration: str = "15", **options):
        return validate_prompt(candidate, duration=Decimal(duration), **options)

    def assert_pass(self, result):
        self.assertEqual(result["verdict"], "PASS", result["errors"])

    def assert_fail(self, result, error):
        self.assertEqual(result["verdict"], "FAIL", result)
        self.assertIn(error, "\n".join(result["errors"]))

    def timed_prompt(self):
        return make_prompt("15", "CUT 1（0-7秒）起势。\nCUT 2（7-15秒）落定。")

    def test_prose_section_mentions_do_not_count_as_headings(self):
        candidate = self.timed_prompt().replace(
            "固定测试风格。", "固定测试风格。这里提及【声音设计】和【基础风格】。"
        )
        self.assert_pass(self.check(candidate, profile="combat"))

    def test_all_five_headers_must_be_standalone_lines(self):
        candidate = self.timed_prompt().replace("【基础风格】\n", "【基础风格】")
        self.assert_fail(self.check(candidate, profile="combat"), "standalone heading")

    def test_empty_contract_line_cannot_borrow_next_line(self):
        candidate = self.timed_prompt()
        for label in ("前提", "核心关系", "导演意图", "演员指令", "对白规则"):
            with self.subTest(label=label):
                lines = [label + "： \t" if line.startswith(label + "：") else line
                         for line in candidate.splitlines()]
                self.assert_fail(self.check("\n".join(lines), profile="combat"), "must be non-empty")

    def test_cut_numbers_must_be_unique_and_sequential(self):
        for number in ("1", "3", "0"):
            with self.subTest(number=number):
                candidate = self.timed_prompt().replace("CUT 2", "CUT " + number)
                self.assert_fail(self.check(candidate, profile="combat"), "unique and sequential")

    def test_sound_cues_cannot_replace_timeline_cuts(self):
        timeline = "CUT 1（0-7秒）起势。\nCUT 2（7-15秒）落定。\n"
        candidate = self.timed_prompt().replace(timeline, "").replace(
            "同步环境声与动作声。", timeline + "同步环境声与动作声。"
        )
        self.assert_fail(self.check(candidate, profile="combat"), "at least one CUT")

    def test_sound_cue_mentions_do_not_add_timeline_cuts(self):
        candidate = self.timed_prompt().replace("同步环境声与动作声。", "CUT 1：风声。\nCUT 2：脚步声。")
        self.assert_pass(self.check(candidate, profile="combat"))

    def test_combat_title_range_cannot_masquerade_as_upper_endpoint(self):
        candidate = self.timed_prompt().replace("自动化回归｜15秒", "自动化回归｜14–15秒")
        self.assert_fail(self.check(candidate, profile="combat"), "exact title duration")

    def test_general_title_ranges_check_both_bounds_and_expected_duration(self):
        for title, duration, valid in (("20–25", "22", True), ("20秒至25", "22", True),
                                       ("20–31", "22", False), ("25–20", "22", False),
                                       ("0–25", "22", False), ("20–25", "26", False),
                                       ("-15", "15", False), ("14--15", "15", False)):
            with self.subTest(title=title, duration=duration):
                result = self.check(make_prompt(title, "CUT 1\n自然地走到窗边。"), duration)
                self.assertEqual(result["verdict"], "PASS" if valid else "FAIL", result)

    def test_timed_general_requires_exact_title(self):
        candidate = self.timed_prompt().replace("自动化回归｜15秒", "自动化回归｜14-15秒")
        self.assert_fail(self.check(candidate, timeline="timed"), "exact title duration")

    def test_general_single_cut_without_beats(self):
        candidate = make_prompt("15", "CUT 1\n人物走到窗边并停下。")
        result = self.check(candidate)
        self.assert_pass(result)
        self.assertEqual(result["mode"], "onetake")
        self.assertEqual(result["timeline"], "untimed")
        self.assertIn("timeline_coverage_0_to_T", result["not_verified"])
        self.assertNotIn("timeline_coverage_0_to_T", result["checked"])

    def test_only_seedance_25_is_accepted(self):
        self.assertEqual(parse_args(["--duration", "20"]).version, "2.5")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parse_args(["--version", "2.0", "--duration", "15"])

    def test_timed_general_single_cut_does_not_require_beats(self):
        candidate = make_prompt("15", "CUT 1（0-15秒）人物自然地走到窗边并停下。")
        self.assert_pass(self.check(candidate, timeline="timed"))
        self.assert_fail(self.check(candidate, profile="combat", mode="onetake"), "no BEAT time ranges")

    def test_combat_allows_explicit_hidden_timestamps(self):
        candidate = make_prompt("15", "CUT 1\n前压和接触。\nCUT 2\n卸力和恢复。")
        self.assert_fail(self.check(candidate, profile="combat"), "valid time range")
        result = self.check(candidate, profile="combat", timeline="untimed")
        self.assert_pass(result)
        self.assertIn("timeline_gaps_and_overlaps", result["not_verified"])

    def test_display_policy_is_not_inferred_from_generated_text(self):
        self.assert_fail(self.check(self.timed_prompt()), "untimed CUT/BEAT")
        self.assert_pass(self.check(self.timed_prompt(), timeline="timed"))

    def test_decimal_and_sparse_frame_events_keep_existing_semantics(self):
        candidate = make_prompt("7.5", "CUT 1（0-7.5秒）保持完整动作。\nFrame 0：开始。\nFrame 180帧：结尾。")
        result = self.check(candidate, "7.5", timeline="timed", timestamp_policy="decimal-allowed")
        self.assert_pass(result)
        self.assertIn("timeline_coverage_0_to_T", result["checked"])
        self.assertIn("frame_event_bounds", result["checked"])
        for frame in ("181", "-1", "1.5"):
            with self.subTest(frame=frame):
                invalid = candidate.replace("Frame 180帧", "Frame " + frame + "帧")
                self.assert_fail(self.check(invalid, "7.5", timeline="timed"), "Frame")

    def test_character_limit_counts_actual_text_at_boundary(self):
        base = make_prompt("15", "CUT 1\n走向窗边。")
        for size in (9999, 10000, 10001):
            with self.subTest(size=size):
                candidate = base + "。" * (size - len(base))
                result = self.check(candidate)
                self.assertEqual(result["characters"], size)
                self.assertEqual(result["verdict"], "FAIL" if size > 10000 else "PASS")
        candidate = base + " " * (10001 - len(base))
        self.assert_fail(self.check(candidate), "10001 characters")

    def test_missing_duplicate_empty_and_reordered_sections_fail(self):
        base = self.timed_prompt()
        cases = (base.replace("【声音设计】", ""), base + "\n【声音设计】\n风声。",
                 base.replace("固定测试风格。", ""),
                 base.replace("【基础风格】", "TEMP").replace("【声音设计】", "【基础风格】").replace("TEMP", "【声音设计】"))
        for candidate in cases:
            with self.subTest(candidate=candidate):
                self.assertEqual(self.check(candidate, profile="combat")["verdict"], "FAIL")

    def test_api_rejects_non_finite_or_nonpositive_duration(self):
        for duration in ("NaN", "Infinity", "0", "-4"):
            with self.subTest(duration=duration):
                self.assert_fail(self.check(self.timed_prompt(), duration), "finite and positive")

    def test_beat_labels_can_restart_within_new_cuts_but_not_repeat_inside_one(self):
        candidate = make_prompt("15", "CUT 1\nBEAT A\n进入。\nBEAT B\n停顿。\nCUT 2\nBEAT A\n离开。")
        self.assert_pass(self.check(candidate))
        duplicate = candidate.replace("BEAT B", "BEAT A")
        self.assert_fail(self.check(duplicate), "BEAT labels must be unique")


def lint_prompt(lock: str = "角色A：成年女性。", style: str = "35mm。", timeline: str = "CUT 1\n测试。",
                sound: str = "无背景音乐。", limits: str = "无字幕、无水印。") -> str:
    return (f"### 第01段｜建议8秒｜测试\n【角色/场景/素材锁定】\n{lock}\n【基础风格】\n{style}\n"
            f"【运镜与时间轴】\n{timeline}\n【声音设计】\n{sound}\n【画面限制】\n{limits}")


def lint_ids(text: str) -> dict[str, str]:
    return {w.split()[1]: w for w in lint_warnings(text, parse_sections(text, [])) if w.startswith("lint M")}


class LintRuleTests(unittest.TestCase):
    """Each lint follows the document that states its rule."""

    def assert_lint(self, code: str, text: str, expected: bool) -> None:
        self.assertEqual(code in lint_ids(text), expected, lint_ids(text))

    def test_m1_scans_the_full_text_and_reads_english_next_to_chinese(self) -> None:
        # 00 翻译规则: full-text search; \b fails next to Chinese characters.
        for text in (lint_prompt(sound="风从北边吹来。"), lint_prompt(style="camera朝north看，35mm。"),
                     lint_prompt(timeline="CUT 1\n固定world-east座位，阿红转身。"),
                     lint_prompt(limits="无字幕，镜头不朝西边。")):
            with self.subTest(text=text):
                self.assert_lint("M1", text, True)

    def test_m1_allows_a_projection_in_the_same_clause_and_cultural_words(self) -> None:
        for text in (lint_prompt(timeline="CUT 1\n固定world-east座位在此反拍中投影到screen-left，camera看见人物三分之四正脸。"),
                     lint_prompt(style="东方美学，35mm。"), lint_prompt(lock="角色A：成年女性，南方口音。"),
                     lint_prompt(timeline="CUT 1\n角色A走向西装男人。")):
            with self.subTest(text=text):
                self.assert_lint("M1", text, False)

    def test_m2_allows_the_body_stillness_05f_directs(self) -> None:
        for timeline in ("CUT 1\n结构对的人被推时纹丝不动。", "CUT 1\n阿森回到窄侧身站架，完全静止，只有眼睛跟着他。"):
            with self.subTest(timeline=timeline):
                self.assert_lint("M2", lint_prompt(timeline=timeline), False)
        for timeline in ("CUT 1\n石门纹丝不动。", "CUT 1\n石手悬在头顶，只有手指在动。"):
            with self.subTest(timeline=timeline):
                self.assert_lint("M2", lint_prompt(timeline=timeline), True)

    def test_m4_covers_narration_and_inner_monologue_labels(self) -> None:
        for timeline in ("CUT 1\n老人弯腰捡稻穗，画外旁白说：“他没有意识到。”",
                         "CUT 1\n角色A（内心OS）画外音：“不会错。”"):
            with self.subTest(timeline=timeline):
                self.assert_lint("M4", lint_prompt(timeline=timeline), True)
        for timeline in ("CUT 1\n老人弯腰捡稻穗，嘴唇闭合。\n画外旁白说：“他没有意识到。”",
                         "CUT 1\n角色A嘴唇闭合，角色A：“（这个数值……不会错。）”",
                         "CUT 1\n车站广播的画外音：“列车进站。”",
                         "CUT 1\n无旁白，角色A自然 lip-sync 说：“好。”"):
            with self.subTest(timeline=timeline):
                self.assert_lint("M4", lint_prompt(timeline=timeline), False)

    def test_m19_flags_all_direct_blood_words_only(self) -> None:
        found = lint_ids(lint_prompt(timeline="CUT 1\n角色A额角渗血，嘴角吐血。"))
        self.assertIn("渗血", found.get("M19", ""))
        self.assertIn("吐血", found.get("M19", ""))
        self.assert_lint("M19", lint_prompt(lock="角色A：中英混血成年女性，手背血管清楚，眼里有血丝，脸上没有血色。"), False)

    def test_m22_reads_the_whole_cut_and_names_only_characters(self) -> None:
        lock = "林岚：32岁成年女性。\n周远：35岁成年男性。\n钥匙：银色钥匙。\n玄关：窄长玄关。"
        self.assert_lint("M22", lint_prompt(lock=lock, timeline="CUT 1\n林岚递出钥匙。\n周远接住，她收回手。"), True)
        self.assert_lint("M22", lint_prompt(lock=lock, timeline="CUT 1\n林岚在玄关递出钥匙，她收回手。"), False)

    def test_m24_follows_the_05_anchor(self) -> None:
        self.assert_lint("M24", lint_prompt(lock="角色A：成年女性，银色眼镜，紫色眼影。"), False)
        self.assert_lint("M24", lint_prompt(lock="角色A：成年女性，金色眼睛带明亮眼神光。"), True)
        self.assert_lint("M24", lint_prompt(lock="角色A：成年女性，金色眼睛，没有眼神光。"), False)

    def test_m32_reads_negative_lists_not_props(self) -> None:
        self.assert_lint("M32", lint_prompt(timeline="CUT 1\n角色A无声举起相机。"), False)
        self.assert_lint("M32", lint_prompt(limits="无字幕，无任何摄影机。"), True)

    def test_m34_needs_no_drive_side_for_a_motorcycle(self) -> None:
        # 05G 摩托车（补充）: the rider sits on the centreline; no 左舵/右舵.
        ride = "CUT 1\n骑手跨上车，驾驶者拧动油门，乘客上车坐稳。"
        for line in ("红色摩托车：街车，银色轮毂。", "白色踏板车：直坐骑姿。", "黑色机车：跑车，前趴骑姿。"):
            with self.subTest(line=line):
                self.assert_lint("M34", lint_prompt(lock=line, timeline=ride), False)
        self.assert_lint("M34", lint_prompt(lock="白色轿车：四门轿车。", timeline=ride), True)
        self.assert_lint("M34", lint_prompt(lock="红色摩托车：街车。\n白色轿车：四门轿车。", timeline=ride), True)


class SpeechCapacityTests(unittest.TestCase):
    def test_dialogue_forms_from_06(self) -> None:
        self.assertEqual(dialogue_lines("CUT 1\n角色A：【贴近】“（这个数值……不会错。）”"), ["（这个数值……不会错。）"])
        self.assertEqual(dialogue_lines("CUT 1\n角色A：我……【抬起手】你……？"), ["我……【抬起手】你……？"])
        self.assertEqual(dialogue_lines("CUT 1\n角色A受到惊吓：*我操！*"), ["*我操！*"])
        self.assertEqual(dialogue_lines("CUT 1\n前提：角色A在门口。\n角色B：“好。”角色A：我……【抬起手】你……？"),
                         ["好。", "我……【抬起手】你……？"])
        self.assertEqual(dialogue_lines("CUT 1\n角色A：成年女性，站在门口。"), [])

    def test_action_marks_are_not_spoken(self) -> None:
        self.assertEqual(speech_need("我……【抬起手】你……？", "zh")[0], 2)
        self.assertEqual(speech_need("“我……【抬起手】你……？”", "zh")[0], 2)
        self.assertEqual(speech_need("OK，走", "zh")[0], 3)

    def test_marked_lines_count_against_the_cut(self) -> None:
        long_line = "我们现在就从后门出去然后一直往前跑不要回头"
        for line in (f"角色A：【贴近】“（{long_line}。）”", f"角色A：{long_line}【抬起手】快走！"):
            with self.subTest(line=line):
                text = make_prompt("4", f"CUT 1（0-2秒）{line}\nCUT 2（2-4秒）测试。")
                report = validate_prompt(text, duration=Decimal("4"), timeline="timed", speech_lang="zh")
                self.assertTrue(any(w.startswith("lint M37 dialogue may not fit CUT 1") for w in report["warnings"]),
                                report["warnings"])
                self.assertEqual(report["verdict"], "PASS", report["errors"])


class SharedValidatorCliTests(unittest.TestCase):
    def run_cli(self, tool: Path, candidate: str, *args: str):
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        return subprocess.run([sys.executable, str(tool), "--duration", "15", *args],
                              input=candidate, capture_output=True, text=True,
                              encoding="utf-8", env=env, check=False)

    def test_json_reports_unverified_untimed_coverage(self):
        result = self.run_cli(GENERAL, make_prompt("15", "CUT 1\n缓慢转身。"), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "PASS")
        self.assertIn("timeline_coverage_0_to_T", report["not_verified"])
        self.assertIn("semantic_quality", report["not_verified"])
        self.assertEqual(result.stderr, "")

    def test_old_cli_and_explicit_combat_profile_are_equivalent(self):
        candidate = make_prompt("15", "CUT 1（0-7秒）进入。\nCUT 2（7-15秒）恢复。")
        old = self.run_cli(COMBAT, candidate)
        new = self.run_cli(GENERAL, candidate, "--profile", "combat")
        self.assertEqual((old.returncode, old.stdout, old.stderr), (new.returncode, new.stdout, new.stderr))
        self.assertEqual(old.stdout.strip(), "PASS")

    def test_json_failure_is_parseable_and_nonzero(self):
        result = self.run_cli(GENERAL, "缺少结构", "--json")
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["verdict"], "FAIL")
        self.assertTrue(report["errors"])

    def test_bom_crlf_input_file_remains_supported(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.md"
            path.write_bytes(b"\xef\xbb\xbf" + make_prompt("15", "CUT 1\n缓慢转身。").replace("\n", "\r\n").encode("utf-8"))
            result = self.run_cli(GENERAL, "", str(path), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
