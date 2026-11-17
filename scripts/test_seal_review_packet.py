#!/usr/bin/env python3
"""Deterministic tests for the sealed cold-review packet and round gate."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TOOL = SCRIPT_DIR / "seal_review_packet.py"
VALIDATOR = SCRIPT_DIR / "validate_combat_prompt.py"


def make_prompt(*, style: str = "固定测试风格", extra_timeline: str = "") -> str:
    return (
        "### 第1段｜密封冷审测试｜4秒\n"
        "【角色/场景/素材锁定】\n"
        "角色甲：地域语境中国；口音为通用普通话；音色为中低音、胸腔共鸣；"
        "说话习惯为语速偏慢、句尾下沉；生理状态为呼吸稳定。\n"
        "测试场景与钥匙道具锁定。\n"
        "【基础风格】\n"
        f"{style}。\n"
        "【运镜与时间轴】\n"
        "前提：两名成年演员在测试场景执行撤离任务。\n"
        "核心关系：角色甲完成交接，角色乙接替并撤离。\n"
        "导演意图：先看清钥匙归属变化，再看清角色乙完成撤离。\n"
        "演员指令：角色甲交出钥匙并确认接收；角色乙接住后转身撤离。\n"
        "对白规则：只允许角色甲说“我们立刻撤离。”，画内自然lip-sync。\n"
        "CUT 1（0-2秒）角色甲说：我们立刻撤离。钥匙已交给角色乙。\n"
        f"CUT 2（2-4秒）角色乙完成撤离。{extra_timeline}\n"
        "【声音设计】\n"
        "同步环境声、动作声与清晰对白。\n"
        "【画面限制】\n"
        "无字幕、无水印。"
    )


def make_report(verdict: str) -> str:
    blocking = "- 重建CUT拓扑。" if verdict == "REPAIR" else "- NONE"
    return (
        f"VERDICT: {verdict}\n"
        "BLOCKING_FINDINGS:\n"
        f"{blocking}\n"
        "OPTIONAL_FINDINGS:\n"
        "- 保持动作简洁。\n"
        "PROTECTED_FACTS:\n"
        "- 保留钥匙交接。"
    )


class SealReviewPacketCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.state = self.root / "review-state.json"
        self.template = self.root / "rules-template.md"
        self.template.write_bytes(
            "# 冷审规则\n\n只审阅密封包内的唯一候选全文。".encode("utf-8")
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_tool(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            check=False,
        )

    def write_candidate(
        self,
        name: str,
        text: str,
        *,
        bom: bool = False,
    ) -> Path:
        path = self.root / name
        payload = text.encode("utf-8")
        if bom:
            payload = b"\xef\xbb\xbf" + payload
        path.write_bytes(payload)
        return path

    def seal(
        self,
        candidate: Path,
        output: Path,
        *,
        contract: Path | None = None,
        template: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        args = [
            "seal",
            "--candidate",
            str(candidate),
            "--template",
            str(template or self.template),
            "--output",
            str(output),
            "--state",
            str(self.state),
            "--duration",
            "4",
            "--version",
            "2.5",
            "--mode",
            "cut",
        ]
        if contract is not None:
            args.extend(["--contract", str(contract)])
        return self.run_tool(*args)

    def start(
        self,
        packet: Path,
        reviewer: str,
    ) -> subprocess.CompletedProcess[str]:
        return self.run_tool(
            "start",
            "--state",
            str(self.state),
            "--snapshot",
            str(packet),
            "--reviewer",
            reviewer,
        )

    def finish(
        self,
        packet: Path,
        reviewer: str,
        verdict: str,
        *,
        structural_change: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        report = self.root / f"{reviewer}-{verdict}.txt"
        report.write_bytes(make_report(verdict).encode("utf-8"))
        args = [
            "finish",
            "--state",
            str(self.state),
            "--snapshot",
            str(packet),
            "--reviewer",
            reviewer,
            "--report",
            str(report),
        ]
        if structural_change is not None:
            args.extend(["--structural-change", structural_change])
        return self.run_tool(*args)

    def test_standard_seal_passes_with_bom_and_crlf(self) -> None:
        candidate_text = make_prompt().replace("\n", "\r\n")
        candidate = self.write_candidate("candidate.md", candidate_text, bom=True)
        self.template.write_bytes(
            b"\xef\xbb\xbf"
            + "# 冷审规则\r\n\r\n只审阅密封包内的唯一候选全文。".encode("utf-8")
        )
        packet = self.root / "PROJECT_RULES.md"

        result = self.seal(candidate, packet)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(packet.is_file())
        packet_text = packet.read_bytes().decode("utf-8")
        self.assertIn("EXACT_MATCH=True", packet_text)
        self.assertIn("MECHANICAL_PASS=True", packet_text)
        self.assertEqual(packet_text.count("## 候选提示词"), 1)
        self.assertIn(candidate_text, packet_text)
        self.assertNotIn("```", packet_text)
        validator = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--version",
                "2.5",
                "--duration",
                "4",
                "--mode",
                "cut",
                "--project-rules",
                str(packet),
                "--candidate",
                str(candidate),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
            check=False,
        )
        self.assertEqual(validator.returncode, 0, validator.stderr)
        self.assertEqual(validator.stdout.strip(), "PASS")

    def test_general_untimed_profile_is_forwarded_without_combat_requirements(self) -> None:
        candidate_text = make_prompt().replace(
            "CUT 1（0-2秒）角色甲说：我们立刻撤离。钥匙已交给角色乙。\n"
            "CUT 2（2-4秒）角色乙完成撤离。",
            "CUT 1\n角色甲说：我们立刻撤离。钥匙已交给角色乙，角色乙完成撤离。",
        )
        candidate = self.write_candidate("general-candidate.md", candidate_text)
        packet = self.root / "general-packet.md"
        result = self.run_tool(
            "seal", "--candidate", str(candidate), "--template", str(self.template),
            "--output", str(packet), "--state", str(self.state), "--duration", "4",
            "--profile", "general", "--timeline", "untimed",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        packet_text = packet.read_text(encoding="utf-8")
        self.assertIn("VALIDATOR_PROFILE=general", packet_text)
        self.assertIn("VALIDATOR_TIMELINE=untimed", packet_text)
        self.assertIn(candidate_text, packet_text)

    def test_seal_rejects_multiple_segment_envelopes(self) -> None:
        first = make_prompt()
        second = make_prompt().replace("### 第1段", "### 第2段", 1)
        candidate = self.write_candidate("multi-segment.md", first + "\n" + second)
        packet = self.root / "multi-segment-PROJECT_RULES.md"

        result = self.seal(candidate, packet)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one independent segment envelope; found 2", result.stderr)
        self.assertFalse(packet.exists())

    def test_path_only_project_rules_fails_existing_validator(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        project_rules = self.root / "PROJECT_RULES.md"
        project_rules.write_bytes(
            f"# 冷审规则\n\n候选路径：{candidate}".encode("utf-8")
        )

        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--version",
                "2.5",
                "--duration",
                "4",
                "--mode",
                "cut",
                "--project-rules",
                str(project_rules),
                "--candidate",
                str(candidate),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one", result.stderr)

    def test_template_pollution_fails_without_publishing(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        pollutants = {
            "candidate section": "# 规则\n\n## 候选提示词\n旧候选",
            "multiple candidates": "# 规则\n\n## 多候选区\n候选A与候选B",
            "tool wrapper": "Output:\n# 规则",
            "old report": "# 规则\n\nVERDICT: REPAIR\nBLOCKING_FINDINGS:\n- 旧报告",
            "prior conclusion": "# 规则\n\n首轮审阅指出CUT 2空间轴线错误，期待修复。",
        }
        for label, content in pollutants.items():
            with self.subTest(label=label):
                template = self.root / f"template-{len(label)}.md"
                template.write_bytes(content.encode("utf-8"))
                packet = self.root / f"packet-{len(label)}.md"
                result = self.seal(candidate, packet, template=template)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(packet.exists())
                self.assertIn("ERROR:", result.stderr)

    def test_same_snapshot_cannot_start_twice(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        packet = self.root / "round-1.md"
        self.assertEqual(self.seal(candidate, packet).returncode, 0)
        first = self.start(packet, "reviewer-a")

        duplicate = self.start(packet, "reviewer-b")

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("already active", duplicate.stderr)

    def test_first_round_pass_terminates_gate(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        packet = self.root / "round-1.md"
        self.assertEqual(self.seal(candidate, packet).returncode, 0)
        self.assertEqual(self.start(packet, "reviewer-a").returncode, 0)
        finished = self.finish(packet, "reviewer-a", "PASS")

        retry = self.start(packet, "reviewer-b")

        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn("terminated", retry.stderr)

    def test_nonstructural_repair_does_not_allow_second_round(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        packet = self.root / "round-1.md"
        self.assertEqual(self.seal(candidate, packet).returncode, 0)
        self.assertEqual(self.start(packet, "reviewer-a").returncode, 0)
        finished = self.finish(
            packet,
            "reviewer-a",
            "REPAIR",
            structural_change="false",
        )

        retry = self.start(packet, "reviewer-b")

        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn("terminated", retry.stderr)

    def test_structural_repair_allows_one_new_second_round_and_no_third(self) -> None:
        candidate_1 = self.write_candidate("candidate-1.md", make_prompt())
        packet_1 = self.root / "round-1.md"
        self.assertEqual(self.seal(candidate_1, packet_1).returncode, 0)
        self.assertEqual(self.start(packet_1, "reviewer-a").returncode, 0)
        first_finish = self.finish(
            packet_1,
            "reviewer-a",
            "REPAIR",
            structural_change="true",
        )
        self.assertEqual(first_finish.returncode, 0, first_finish.stderr)

        candidate_2 = self.write_candidate(
            "candidate-2.md",
            make_prompt(style="结构修复后的固定测试风格"),
        )
        packet_2 = self.root / "round-2.md"
        second_seal = self.seal(candidate_2, packet_2)
        second_start = self.start(packet_2, "reviewer-b")
        duplicate_start = self.start(packet_2, "reviewer-c")
        second_finish = self.finish(packet_2, "reviewer-b", "PASS")
        third_start = self.start(packet_2, "reviewer-c")

        self.assertEqual(second_seal.returncode, 0, second_seal.stderr)
        self.assertEqual(second_start.returncode, 0, second_start.stderr)
        self.assertNotEqual(duplicate_start.returncode, 0)
        self.assertIn("already active", duplicate_start.stderr)
        self.assertEqual(second_finish.returncode, 0, second_finish.stderr)
        self.assertNotEqual(third_start.returncode, 0)
        self.assertIn("terminated", third_start.stderr)

    def test_second_round_rejects_first_report_leak(self) -> None:
        candidate_1 = self.write_candidate("candidate-1.md", make_prompt())
        packet_1 = self.root / "round-1.md"
        self.assertEqual(self.seal(candidate_1, packet_1).returncode, 0)
        self.assertEqual(self.start(packet_1, "reviewer-a").returncode, 0)
        self.assertEqual(
            self.finish(
                packet_1,
                "reviewer-a",
                "REPAIR",
                structural_change="true",
            ).returncode,
            0,
        )
        candidate_2 = self.write_candidate(
            "candidate-2.md", make_prompt(style="第二轮固定测试风格")
        )
        packet_2 = self.root / "round-2.md"
        self.assertEqual(self.seal(candidate_2, packet_2).returncode, 0)
        packet_2.write_bytes(
            packet_2.read_bytes() + b"\n\n" + make_report("REPAIR").encode("utf-8")
        )

        result = self.start(packet_2, "reviewer-b")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("leaks first-round review report", result.stderr)

    def test_optional_contract_passes_and_failure_does_not_publish(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        contract_data = {
            "expected_cut_count": 2,
            "voice_profiles": {
                "角色甲": {
                    "region": {"required_terms": ["地域语境中国"]},
                    "accent": {"required_regex": ["口音为.*普通话"]},
                    "timbre": {"required_terms": ["中低音", "胸腔共鸣"]},
                    "speech_habits": {"required_terms": ["语速偏慢", "句尾下沉"]},
                    "physiology": {"required_regex": ["生理状态为呼吸稳定"]},
                }
            },
            "dialogue_windows": [{"text": "我们立刻撤离", "seconds": 2}],
            "crowd_ratios": {"前景": 40, "后景": 60},
            "required_state_tokens": ["钥匙已交给角色乙"],
            "forbidden_state_tokens": ["钥匙仍在角色甲手中"],
        }
        contract = self.root / "contract.json"
        contract.write_bytes(
            json.dumps(contract_data, ensure_ascii=False).encode("utf-8")
        )
        passing_packet = self.root / "contract-pass.md"

        passing = self.seal(candidate, passing_packet, contract=contract)

        self.assertEqual(passing.returncode, 0, passing.stderr)
        self.assertIn(
            "CONTRACT_APPLIED=True",
            passing_packet.read_bytes().decode("utf-8"),
        )

        contract_data["expected_cut_count"] = 3
        contract.write_bytes(
            json.dumps(contract_data, ensure_ascii=False).encode("utf-8")
        )
        failing_packet = self.root / "contract-fail.md"
        failing = self.seal(candidate, failing_packet, contract=contract)

        self.assertNotEqual(failing.returncode, 0)
        self.assertIn("expected_cut_count", failing.stderr)
        self.assertFalse(failing_packet.exists())


if __name__ == "__main__":
    unittest.main()
