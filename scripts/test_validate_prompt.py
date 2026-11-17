#!/usr/bin/env python3
"""Behavioral regressions for the shared general/combat validator."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

from test_validate_combat_prompt import make_prompt
from validate_prompt import validate_prompt


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

    def test_general_single_cut_without_beats_in_both_versions(self):
        for version in ("2.0", "2.5"):
            with self.subTest(version=version):
                candidate = make_prompt("15", "CUT 1\n人物走到窗边并停下。")
                result = self.check(candidate, version=version)
                self.assert_pass(result)
                self.assertEqual(result["mode"], "onetake")
                self.assertEqual(result["timeline"], "untimed")
                self.assertIn("timeline_coverage_0_to_T", result["not_verified"])
                self.assertNotIn("timeline_coverage_0_to_T", result["checked"])

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
        self.assert_fail(self.check(self.timed_prompt(), version="2.0", timeline="timed"), "does not support")

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

    def test_beat_labels_can_restart_within_new_cuts_but_not_repeat_inside_one(self):
        candidate = make_prompt("15", "CUT 1\nBEAT A\n进入。\nBEAT B\n停顿。\nCUT 2\nBEAT A\n离开。")
        self.assert_pass(self.check(candidate))
        duplicate = candidate.replace("BEAT B", "BEAT A")
        self.assert_fail(self.check(duplicate), "BEAT labels must be unique")


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
