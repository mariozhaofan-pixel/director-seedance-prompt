#!/usr/bin/env python3
"""Regression tests for validate_combat_prompt.py."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_combat_prompt.py")

SEGMENT_CONTRACT = (
    "前提：两名成年演员在可控场地完成已编排表演。\n"
    "核心关系：角色A持续施压，角色B通过移动化解并改变节奏。\n"
    "导演意图：先建立力量差，再让观众读到关系反转。\n"
    "演员指令：角色A以前压和短停升级压迫；角色B以侧移和呼吸变化寻找空档。\n"
    "对白规则：本段只允许既定原句；台词、说话动作和听者反应写入对应CUT。"
)


def make_prompt(
    duration: str,
    timeline: str,
    *,
    segment_contract: str | None = SEGMENT_CONTRACT,
) -> str:
    contract = f"{segment_contract}\n" if segment_contract is not None else ""
    return (
        f"### 第1段｜自动化回归｜{duration}秒\n"
        "【角色/场景/素材锁定】\n"
        "测试角色与测试场景锁定。\n"
        "【基础风格】\n"
        "固定测试风格。\n"
        "【运镜与时间轴】\n"
        f"{contract}"
        f"{timeline}\n"
        "【声音设计】\n"
        "同步环境声与动作声。\n"
        "【画面限制】\n"
        "无字幕、无水印。"
    )


class ValidatorCliTests(unittest.TestCase):
    def run_validator(
        self,
        candidate: str,
        *,
        duration: str,
        extra_args: tuple[str, ...] = (),
        project_rules: str | None = None,
        candidate_bom: bool = False,
        project_rules_bom: bool = False,
        version: str = "2.5",
        mode: str = "cut",
        include_positional_input: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            candidate_path = temp_path / "candidate.md"
            candidate_bytes = candidate.encode("utf-8")
            if candidate_bom:
                candidate_bytes = b"\xef\xbb\xbf" + candidate_bytes
            candidate_path.write_bytes(candidate_bytes)

            command = [
                sys.executable,
                str(VALIDATOR),
                "--version",
                version,
                "--duration",
                duration,
                "--mode",
                mode,
                *extra_args,
            ]
            if project_rules is None:
                command.append(str(candidate_path))
            else:
                project_rules_path = temp_path / "PROJECT_RULES.md"
                project_rules_bytes = project_rules.encode("utf-8")
                if project_rules_bom:
                    project_rules_bytes = b"\xef\xbb\xbf" + project_rules_bytes
                project_rules_path.write_bytes(project_rules_bytes)
                command.extend(
                    [
                        "--project-rules",
                        str(project_rules_path),
                        "--candidate",
                        str(candidate_path),
                    ]
                )
                if include_positional_input:
                    command.append(str(candidate_path))

            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
                check=False,
            )

    @staticmethod
    def make_project_rules(candidate: str, *, prefix: str = "") -> str:
        return (
            f"{prefix}# PROJECT_RULES.md\n\n"
            "## 审阅边界\n"
            "仅依据本文件。\n\n"
            "## 候选提示词\n"
            f"{candidate}\n\n"
            "## 审阅输出格式\n"
            "VERDICT: PASS | REPAIR"
        )

    def test_default_integer_timeline_passes(self) -> None:
        candidate = make_prompt(
            "15",
            "CUT 1（0-5秒）测试。\nCUT 2（5-10秒）测试。\nCUT 3（10-15秒）测试。",
        )

        result = self.run_validator(candidate, duration="15")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "PASS")
        self.assertNotIn("WARNING:", result.stderr)

    def test_version_duration_limits_accept_upper_bound_and_decimals(self) -> None:
        for version, duration in (
            ("2.0", "15"),
            ("2.0", "14.999"),
            ("2.5", "30"),
            ("2.5", "29.999"),
        ):
            with self.subTest(version=version, duration=duration):
                timeline = (
                    "CUT 1\n测试。\nCUT 2\n测试。"
                    if version == "2.0"
                    else f"CUT 1（0-5秒）测试。\nCUT 2（5-{duration}秒）测试。"
                )
                result = self.run_validator(
                    make_prompt(duration, timeline),
                    duration=duration,
                    version=version,
                    extra_args=("--timestamp-policy", "decimal-allowed"),
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), "PASS")

    def test_version_duration_limits_reject_excess(self) -> None:
        for version, duration, limit in (
            ("2.0", "16", "15"),
            ("2.0", "15.001", "15"),
            ("2.5", "31", "30"),
            ("2.5", "30.001", "30"),
        ):
            with self.subTest(version=version, duration=duration):
                timeline = (
                    "CUT 1\n测试。\nCUT 2\n测试。"
                    if version == "2.0"
                    else f"CUT 1（0-5秒）测试。\nCUT 2（5-{duration}秒）测试。"
                )
                result = self.run_validator(
                    make_prompt(duration, timeline),
                    duration=duration,
                    version=version,
                    extra_args=("--timestamp-policy", "decimal-allowed"),
                )
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(f"exceeds Seedance {version} limit of {limit} seconds", result.stderr)
                self.assertNotIn("PASS", result.stdout)

    def test_seedance_20_title_tolerance_cannot_bypass_duration_limit(self) -> None:
        candidate = make_prompt("15.001", "CUT 1\n测试。\nCUT 2\n测试。")

        result = self.run_validator(candidate, duration="15", version="2.0")

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("title duration 15.001 exceeds Seedance 2.0 limit of 15 seconds", result.stderr)

    def test_seedance_25_every_cut_requires_a_valid_time_range(self) -> None:
        for mode in ("cut", "auto"):
            for middle_cut in ("CUT 2\n测试。", "CUT 2（5-?秒）测试。"):
                with self.subTest(mode=mode, middle_cut=middle_cut):
                    candidate = make_prompt(
                        "15",
                        f"CUT 1（0-5秒）测试。\n{middle_cut}\nCUT 3（5-15秒）测试。",
                    )
                    result = self.run_validator(candidate, duration="15", mode=mode)

                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn("requires a valid time range for every CUT", result.stderr)
                    self.assertNotIn("PASS", result.stdout)

    def test_seedance_25_onetake_every_beat_requires_a_valid_time_range(self) -> None:
        for mode in ("onetake", "auto"):
            for middle_beat in ("BEAT B\n测试。", "BEAT B（5-?秒）测试。"):
                with self.subTest(mode=mode, middle_beat=middle_beat):
                    candidate = make_prompt(
                        "15",
                        "CUT 1（0-15秒）测试。\n"
                        f"BEAT A（0-5秒）测试。\n{middle_beat}\nBEAT C（5-15秒）测试。",
                    )
                    result = self.run_validator(candidate, duration="15", mode=mode)

                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn("requires a valid time range for every BEAT", result.stderr)
                    self.assertNotIn("PASS", result.stdout)

    def test_seedance_25_onetake_rejects_extra_untimed_cut(self) -> None:
        candidate = make_prompt(
            "15",
            "CUT 1（0-15秒）测试。\nBEAT A（0-5秒）测试。\n"
            "CUT 2\n测试。\nBEAT B（5-15秒）测试。",
        )

        result = self.run_validator(candidate, duration="15", mode="onetake")

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("requires a valid time range for every CUT", result.stderr)

    def test_seedance_25_segment_contract_is_required_and_ordered(self) -> None:
        timeline = "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。"
        missing = self.run_validator(
            make_prompt("4", timeline, segment_contract=None),
            duration="4",
        )
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("timeline contract label 前提 occurs 0 times", missing.stderr)

        out_of_order = SEGMENT_CONTRACT.replace(
            "前提：两名成年演员在可控场地完成已编排表演。\n核心关系：角色A持续施压，角色B通过移动化解并改变节奏。",
            "核心关系：角色A持续施压，角色B通过移动化解并改变节奏。\n前提：两名成年演员在可控场地完成已编排表演。",
        )
        misordered = self.run_validator(
            make_prompt("4", timeline, segment_contract=out_of_order),
            duration="4",
        )
        self.assertNotEqual(misordered.returncode, 0)
        self.assertIn("timeline contract labels must be ordered", misordered.stderr)

    def test_seedance_25_segment_contract_must_precede_first_cut(self) -> None:
        candidate = make_prompt(
            "4",
            "CUT 1（0-2秒）测试。\n" + SEGMENT_CONTRACT + "\nCUT 2（2-4秒）测试。",
            segment_contract=None,
        )

        result = self.run_validator(candidate, duration="4")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must appear before the first CUT", result.stderr)

    def test_seedance_25_director_intent_rejects_source_workflow_metadata(self) -> None:
        contaminated_contract = SEGMENT_CONTRACT.replace(
            "导演意图：先建立力量差，再让观众读到关系反转。",
            "导演意图：按照用户要求复刻原片镜序，让Seedance模型理解。",
        )
        candidate = make_prompt(
            "4",
            "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。",
            segment_contract=contaminated_contract,
        )

        result = self.run_validator(candidate, duration="4")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compiler-authored dramatic interpretation", result.stderr)

    def test_multiple_segment_envelopes_fail(self) -> None:
        first = make_prompt("4", "CUT 1（0-4秒）测试。")
        second = make_prompt("4", "CUT 1（0-4秒）测试。").replace(
            "### 第1段", "### 第2段", 1
        )

        result = self.run_validator(first + "\n" + second, duration="4")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one independent segment envelope; found 2", result.stderr)

    def test_decimal_allowed_accepts_fractional_ranges(self) -> None:
        candidate = make_prompt(
            "15",
            "CUT 1（0-1.2秒）测试。\n"
            "CUT 2（1.2-4秒）测试。\n"
            "CUT 3（4-7.5秒）测试。\n"
            "CUT 4（7.5-15秒）测试。",
        )

        result = self.run_validator(
            candidate,
            duration="15",
            extra_args=("--timestamp-policy", "decimal-allowed"),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("WARNING:", result.stderr)

    def test_decimal_allowed_accepts_decimal_total_duration(self) -> None:
        candidate = make_prompt(
            "7.5",
            "CUT 1（0-1.2秒）测试。\nCUT 2（1.2-4秒）测试。\nCUT 3（4-7.5秒）测试。",
        )

        result = self.run_validator(
            candidate,
            duration="7.5",
            extra_args=("--timestamp-policy", "decimal-allowed"),
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_decimal_timeline_discontinuities_fail(self) -> None:
        cases = {
            "late start": "CUT 1（0.1-1.2秒）测试。\nCUT 2（1.2-7.5秒）测试。",
            "gap": "CUT 1（0-1.2秒）测试。\nCUT 2（1.3-4秒）测试。\nCUT 3（4-7.5秒）测试。",
            "overlap": "CUT 1（0-1.2秒）测试。\nCUT 2（1.1-4秒）测试。\nCUT 3（4-7.5秒）测试。",
            "reverse": "CUT 1（0-1.2秒）测试。\nCUT 2（1.2-1.1秒）测试。\nCUT 3（1.1-7.5秒）测试。",
            "out of order": "CUT 1（0-4秒）测试。\nCUT 2（4-5秒）测试。\nCUT 3（3-7.5秒）测试。",
            "wrong endpoint": "CUT 1（0-1.2秒）测试。\nCUT 2（1.2-4秒）测试。\nCUT 3（4-7.4秒）测试。",
        }
        for label, timeline in cases.items():
            with self.subTest(label=label):
                candidate = make_prompt("7.5", timeline)
                result = self.run_validator(
                    candidate,
                    duration="7.5",
                    extra_args=("--timestamp-policy", "decimal-allowed"),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("ERROR:", result.stderr)

    def test_decimal_onetake_checks_cut_and_beat_coverage(self) -> None:
        valid_timeline = (
            "CUT 1（0-7.5秒）测试。\n"
            "BEAT A（0-1.2秒）测试。\n"
            "BEAT B（1.2-4秒）测试。\n"
            "BEAT C（4-7.5秒）测试。"
        )
        valid = self.run_validator(
            make_prompt("7.5", valid_timeline),
            duration="7.5",
            extra_args=("--timestamp-policy", "decimal-allowed"),
            mode="auto",
        )
        self.assertEqual(valid.returncode, 0, valid.stderr)

        beat_gap = valid_timeline.replace("BEAT B（1.2-4秒）", "BEAT B（1.3-4秒）")
        invalid = self.run_validator(
            make_prompt("7.5", beat_gap),
            duration="7.5",
            extra_args=("--timestamp-policy", "decimal-allowed"),
            mode="onetake",
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("BEAT gap", invalid.stderr)

    def test_integer_preferred_allows_decimals_with_warning(self) -> None:
        candidate = make_prompt(
            "7.5",
            "CUT 1（0-1.2秒）测试。\nCUT 2（1.2-7.5秒）测试。",
        )

        result = self.run_validator(candidate, duration="7.5")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARNING:", result.stderr)
        self.assertEqual(result.stdout.strip(), "PASS")

    def test_integer_required_rejects_decimals(self) -> None:
        candidate = make_prompt(
            "15",
            "CUT 1（0-1.2秒）测试。\nCUT 2（1.2-15秒）测试。",
        )

        result = self.run_validator(
            candidate,
            duration="15",
            extra_args=("--timestamp-policy", "integer-required"),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("integer-required", result.stderr)

    def test_sparse_frame_events_pass_without_covering_segment(self) -> None:
        candidate = make_prompt(
            "15",
            "CUT 1（0-7.5秒）测试。Frame 0帧：起始接触。\n"
            "Frame 180帧：中间事件。\n"
            "CUT 2（7.5-15秒）测试。Frame 360帧：终点边界。",
        )

        result = self.run_validator(
            candidate,
            duration="15",
            extra_args=("--timestamp-policy", "decimal-allowed", "--fps", "24"),
        )

        self.assertEqual(result.returncode, 0, result.stderr)

        without_suffix = candidate.replace("Frame 180帧", "Frame 180")
        result_without_suffix = self.run_validator(
            without_suffix,
            duration="15",
            extra_args=("--timestamp-policy", "decimal-allowed", "--fps", "24"),
        )
        self.assertEqual(result_without_suffix.returncode, 0, result_without_suffix.stderr)

    def test_frame_events_must_be_nonnegative_and_within_boundary(self) -> None:
        for frame in ("-1", "361"):
            with self.subTest(frame=frame):
                candidate = make_prompt(
                    "15",
                    f"CUT 1（0-7秒）Frame {frame}帧：非法。\nCUT 2（7-15秒）测试。",
                )
                result = self.run_validator(candidate, duration="15")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Frame", result.stderr)

    def test_integer_required_rejects_frame_events(self) -> None:
        candidate = make_prompt(
            "15",
            "CUT 1（0-7秒）Frame 24：接触。\nCUT 2（7-15秒）测试。",
        )
        result = self.run_validator(
            candidate,
            duration="15",
            extra_args=("--timestamp-policy", "integer-required"),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("integer-required", result.stderr)

    def test_reference_handle_policy_is_project_specific(self) -> None:
        candidate = make_prompt(
            "4",
            "CUT 1（0-2秒）使用@角色图A。\nCUT 2（2-4秒）测试。",
        )
        default_result = self.run_validator(candidate, duration="4")
        self.assertEqual(default_result.returncode, 0, default_result.stderr)

        lock_only_result = self.run_validator(
            candidate,
            duration="4",
            extra_args=("--reference-handle-policy", "lock-only"),
        )
        self.assertNotEqual(lock_only_result.returncode, 0)
        self.assertIn("lock-only", lock_only_result.stderr)

        locked_once = candidate.replace(
            "测试角色与测试场景锁定。",
            "@角色图A：测试角色身份主参考。",
        ).replace("使用@角色图A。", "使用角色A。")
        valid_lock_only = self.run_validator(
            locked_once,
            duration="4",
            extra_args=("--reference-handle-policy", "lock-only"),
        )
        self.assertEqual(valid_lock_only.returncode, 0, valid_lock_only.stderr)

    def test_internal_production_metadata_is_forbidden(self) -> None:
        timeline = "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。"
        cases = (
            "画面参考输入仅使用下列两张头像与两张服装图；住宅派对、背景宾客、旧手机和全部环境均由文字生成。"
            "授权BGM母带仅在后期按声音设计所列时码挂接，不作为视频生成参考输入。",
            "本段独立冷启动，不依赖其他段落或未列出的素材。",
            "参考片仅作项目窗口内分析证据，不作为生成输入。",
            "生成参考输入仅限以上两张头像与三张服装图；手机、店铺和全部环境由文字建立。",
        )
        for metadata in cases:
            with self.subTest(metadata=metadata):
                candidate = make_prompt("4", timeline).replace(
                    "测试角色与测试场景锁定。",
                    metadata,
                )
                result = self.run_validator(candidate, duration="4")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "visible internal production/material-management metadata",
                    result.stderr,
                )

    def test_normal_asset_control_and_storyworld_lines_remain_allowed(self) -> None:
        timeline = "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。"
        cases = (
            "@图片1：女主身份参考，只控制脸部身份和五官比例；服装、场景与灯光按本段文字。",
            "无背景音乐；只保留对白、房间底噪和手机按键声。",
            "住宅派对客厅，暖灯下背景宾客分层交谈，旧式黑色按键手机在男主右手。",
        )
        for control_line in cases:
            with self.subTest(control_line=control_line):
                candidate = make_prompt("4", timeline).replace(
                    "测试角色与测试场景锁定。",
                    control_line,
                )
                result = self.run_validator(candidate, duration="4")
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_audit_package_exact_match_passes(self) -> None:
        candidate = make_prompt("4", "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。")
        project_rules = self.make_project_rules(candidate)

        result = self.run_validator(
            candidate,
            duration="4",
            project_rules=project_rules,
            candidate_bom=True,
            project_rules_bom=True,
            include_positional_input=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_audit_package_mismatch_fails(self) -> None:
        candidate = make_prompt("4", "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。")
        project_rules = self.make_project_rules(candidate.replace("固定测试风格", "漂移风格"))

        result = self.run_validator(candidate, duration="4", project_rules=project_rules)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("EXACT_MATCH", result.stderr)

    def test_audit_package_line_ending_mismatch_fails(self) -> None:
        candidate = make_prompt("4", "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。")
        embedded_crlf = candidate.replace("\n", "\r\n")
        project_rules = self.make_project_rules(embedded_crlf)

        result = self.run_validator(candidate, duration="4", project_rules=project_rules)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("EXACT_MATCH", result.stderr)

    def test_audit_package_stale_candidate_residue_fails(self) -> None:
        candidate = make_prompt("4", "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。")
        stale = "### 第99段｜旧候选｜4秒\n旧候选残留。\n\n"
        project_rules = self.make_project_rules(candidate, prefix=stale)

        result = self.run_validator(candidate, duration="4", project_rules=project_rules)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale candidate-like", result.stderr)

    def test_audit_package_tool_wrapper_fails(self) -> None:
        candidate = make_prompt("4", "CUT 1（0-2秒）测试。\nCUT 2（2-4秒）测试。")
        for wrapper in (
            "Exit code: 0\n",
            "Process exited with code 0\n",
            "Output:\n",
            "tool output\n",
            "tool_call:\n",
            "Command: python validator.py\n",
        ):
            with self.subTest(wrapper=wrapper.strip()):
                project_rules = self.make_project_rules(candidate, prefix=wrapper)
                result = self.run_validator(candidate, duration="4", project_rules=project_rules)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("tool wrapper", result.stderr)

    def test_one_line_segment_title_plus_five_sections_passes(self) -> None:
        candidate = make_prompt("6", "CUT 1（0-3秒）测试。\nCUT 2（3-6秒）测试。")

        result = self.run_validator(candidate, duration="6")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("unexpected visible section", result.stderr)

    def test_seedance_20_untimed_behavior_remains(self) -> None:
        untimed = make_prompt(
            "8",
            "CUT 1\n起势与接触。\nCUT 2\n受力与恢复。",
            segment_contract=None,
        )
        valid = self.run_validator(
            untimed,
            duration="8",
            version="2.0",
        )
        self.assertEqual(valid.returncode, 0, valid.stderr)

        for mode in ("onetake", "auto"):
            with self.subTest(mode=mode):
                onetake = make_prompt(
                    "8",
                    "CUT 1\nBEAT A\n起势与接触。\nBEAT B\n受力与恢复。",
                    segment_contract=None,
                )
                valid_onetake = self.run_validator(
                    onetake,
                    duration="8",
                    version="2.0",
                    mode=mode,
                )
                self.assertEqual(valid_onetake.returncode, 0, valid_onetake.stderr)

        timed = make_prompt(
            "8",
            "CUT 1（0-4秒）测试。\nCUT 2（4-8秒）测试。",
        )
        invalid = self.run_validator(
            timed,
            duration="8",
            version="2.0",
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("untimed CUT/BEAT", invalid.stderr)

        frame_timed = make_prompt(
            "8",
            "CUT 1\n起势。\nFrame 24：接触。\nCUT 2\n受力与恢复。",
        )
        frame_invalid = self.run_validator(
            frame_timed,
            duration="8",
            version="2.0",
        )
        self.assertNotEqual(frame_invalid.returncode, 0)
        self.assertIn("untimed CUT/BEAT", frame_invalid.stderr)


if __name__ == "__main__":
    unittest.main()
