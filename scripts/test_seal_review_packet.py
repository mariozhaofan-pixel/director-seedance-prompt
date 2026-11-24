#!/usr/bin/env python3
"""Deterministic tests for the sealed cold-review packet and round gate.

Most cases call seal_review_packet.main() in-process; SealCliSmokeTests keeps real subprocess runs.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import seal_review_packet as seal
import validate_combat_prompt


SCRIPT_DIR = Path(__file__).resolve().parent
TOOL = SCRIPT_DIR / "seal_review_packet.py"
VALIDATOR = SCRIPT_DIR / "validate_combat_prompt.py"


def make_prompt(*, style: str = "固定测试风格", extra_timeline: str = "", sound: str = "") -> str:
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
        f"{sound}同步环境声、动作声与清晰对白。\n"
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


class SealTestCase(unittest.TestCase):
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

    def run_tool(self, *args: str) -> SimpleNamespace:
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            returncode = seal.main(list(args))
        return SimpleNamespace(returncode=returncode, stdout=stdout.getvalue(), stderr=stderr.getvalue())

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

    def seal_args(
        self,
        candidate: Path,
        output: Path,
        *,
        contract: Path | None = None,
        template: Path | None = None,
        extra: tuple[str, ...] = (),
    ) -> list[str]:
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
            *extra,
        ]
        if contract is not None:
            args.extend(["--contract", str(contract)])
        return args

    def seal(self, candidate: Path, output: Path, **options) -> SimpleNamespace:
        return self.run_tool(*self.seal_args(candidate, output, **options))

    def start(
        self,
        packet: Path,
        reviewer: str,
    ) -> SimpleNamespace:
        return self.run_tool(
            "start",
            "--state",
            str(self.state),
            "--snapshot",
            str(packet),
            "--reviewer",
            reviewer,
        )

    def finish_args(
        self,
        packet: Path,
        reviewer: str,
        verdict: str,
        *,
        structural_change: str | None = None,
    ) -> list[str]:
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
        return args

    def finish(self, packet: Path, reviewer: str, verdict: str, **options) -> SimpleNamespace:
        return self.run_tool(*self.finish_args(packet, reviewer, verdict, **options))

    def write_contract(self, data: dict) -> Path:
        contract = self.root / "contract.json"
        contract.write_bytes(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        return contract


class SealReviewPacketTests(SealTestCase):
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

    def test_mechanical_failure_does_not_publish(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        packet = self.root / "packet.md"
        result = self.seal(candidate, packet, extra=("--mode", "onetake"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("mechanical preflight failed; no packet was published", result.stderr)
        self.assertIn("ERROR:", result.stderr)
        self.assertFalse(packet.exists())
        self.assertEqual(list(self.root.glob(".packet.md.*")), [])

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
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            returncode = validate_combat_prompt.main([
                "--version", "2.5", "--duration", "4", "--mode", "cut",
                "--project-rules", str(project_rules), "--candidate", str(candidate),
            ])

        self.assertNotEqual(returncode, 0)
        self.assertIn("exactly one", stderr.getvalue())

    def test_template_pollution_fails_without_publishing(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        pollutants = {
            "candidate section": "# 规则\n\n## 候选提示词\n旧候选",
            "multiple candidates": "# 规则\n\n## 多候选区\n候选A与候选B",
            "tool wrapper": "Output:\n# 规则",
            "old report": "# 规则\n\nVERDICT: REPAIR\nBLOCKING_FINDINGS:\n- 旧报告",
            "prior conclusion": "# 规则\n\n首轮审阅指出CUT 2空间轴线错误，期待修复。",
            "stale segment": "# 规则\n\n  ### 第 3 段｜旧候选｜4秒",
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

    def test_story_text_about_a_previous_round_is_not_a_review_leak(self) -> None:
        candidate = self.write_candidate(
            "candidate.md", make_prompt(extra_timeline="角色乙躲开上一轮攻势，发现出口。")
        )
        result = self.seal(candidate, self.root / "packet.md")
        self.assertEqual(result.returncode, 0, result.stderr)

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
        contract = self.write_contract(contract_data)
        passing_packet = self.root / "contract-pass.md"

        passing = self.seal(candidate, passing_packet, contract=contract)

        self.assertEqual(passing.returncode, 0, passing.stderr)
        self.assertIn(
            "CONTRACT_APPLIED=True",
            passing_packet.read_bytes().decode("utf-8"),
        )

        contract_data["expected_cut_count"] = 3
        contract = self.write_contract(contract_data)
        failing_packet = self.root / "contract-fail.md"
        failing = self.seal(candidate, failing_packet, contract=contract)

        self.assertNotEqual(failing.returncode, 0)
        self.assertIn("expected_cut_count", failing.stderr)
        self.assertFalse(failing_packet.exists())

    def test_contract_cut_count_reads_only_the_timeline(self) -> None:
        candidate = self.write_candidate(
            "candidate.md", make_prompt(sound="CUT 1：风声。\nCUT 2：脚步声。\nCUT 3：门响。\n")
        )
        contract = self.write_contract({"expected_cut_count": 2})
        result = self.seal(candidate, self.root / "packet.md", contract=contract)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_contract_rejects_non_finite_numbers(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        for raw in ('{"crowd_ratios": {"前景": 1e999}}', '{"crowd_ratios": {"前景": NaN}}'):
            with self.subTest(raw=raw):
                contract = self.root / "contract.json"
                contract.write_bytes(raw.encode("utf-8"))
                result = self.seal(candidate, self.root / "packet.md", contract=contract)
                self.assertEqual(result.returncode, 1)
                self.assertIn("finite", result.stderr)

    def test_dialogue_windows_use_the_shared_speech_estimate(self) -> None:
        line = "我……【抬起手】你……？"
        candidate = self.write_candidate(
            "candidate.md", make_prompt(extra_timeline=f"角色乙：{line}")
        )
        # Two spoken characters fit 0.5s; the action mark is not spoken (the old count saw five characters).
        fits = self.seal(candidate, self.root / "fits.md",
                         contract=self.write_contract({"dialogue_windows": [{"text": line, "seconds": 0.5}]}))
        self.assertEqual(fits.returncode, 0, fits.stderr)
        too_long = self.seal(candidate, self.root / "too-long.md",
                             contract=self.write_contract({"dialogue_windows": [{"text": line, "seconds": 0.3}]}))
        self.assertEqual(too_long.returncode, 1)
        self.assertIn("dialogue_windows[0] needs about 2 spoken zh units", too_long.stderr)

    def test_project_lint_and_speech_lang_are_forwarded(self) -> None:
        candidate = self.write_candidate(
            "candidate.md",
            make_prompt(extra_timeline="角色乙低声说：“我们现在就从后门出去然后一直往前跑不要回头。”"),
        )
        lint = self.root / "lint.json"
        lint.write_bytes(json.dumps({"rules": [
            {"id": "key-word", "pattern": "钥匙", "message": "project rule hit"}]}).encode("utf-8"))
        packet = self.root / "packet.md"
        result = self.seal(candidate, packet,
                           extra=("--project-lint", str(lint), "--speech-lang", "zh"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(packet.is_file())
        self.assertIn("WARNING: project lint key-word: project rule hit", result.stderr)
        self.assertIn("WARNING: lint M37 dialogue may not fit CUT 2", result.stderr)

        broken = self.root / "broken-lint.json"
        broken.write_bytes(b'{"rules": [{"pattern": "("}]}')
        failed = self.seal(candidate, self.root / "packet-2.md", extra=("--project-lint", str(broken)))
        self.assertEqual(failed.returncode, 1)
        self.assertFalse((self.root / "packet-2.md").exists())


class StateLockTests(SealTestCase):
    def lock_path(self) -> Path:
        return self.state.with_name(self.state.name + ".lock")

    def write_lock(self, pid: int, *, age: float = 0.0) -> Path:
        lock = self.lock_path()
        lock.write_bytes(f"pid={pid}\nhost={seal.socket.gethostname()}\n".encode("utf-8"))
        if age:
            stamp = time.time() - age
            os.utime(lock, (stamp, stamp))
        return lock

    def test_live_lock_blocks_a_second_operation(self) -> None:
        lock = self.write_lock(os.getpid())
        candidate = self.write_candidate("candidate.md", make_prompt())
        result = self.seal(candidate, self.root / "packet.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("review state is locked by another operation", result.stderr)
        self.assertIn(f"pid {os.getpid()}", result.stderr)
        self.assertTrue(lock.exists())

    def test_lock_of_an_ended_process_is_released(self) -> None:
        lock = self.write_lock(424242)
        candidate = self.write_candidate("candidate.md", make_prompt())
        with mock.patch.object(seal, "process_alive", return_value=False):
            result = self.seal(candidate, self.root / "packet.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("removed stale review-state lock", result.stderr)
        self.assertIn("process 424242 that created it is no longer running", result.stderr)
        self.assertFalse(lock.exists())

    def test_lock_older_than_the_limit_is_released_even_if_the_pid_is_alive(self) -> None:
        self.write_lock(os.getpid(), age=seal.STALE_LOCK_SECONDS + 60)
        candidate = self.write_candidate("candidate.md", make_prompt())
        result = self.seal(candidate, self.root / "packet.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("older than", result.stderr)

    def test_lock_replaced_after_the_staleness_check_is_kept(self) -> None:
        lock = self.write_lock(424242)
        real_read = seal.read_lock
        calls = []

        def racing_read(path: Path):
            calls.append(path)
            if len(calls) == 2:  # another process broke the lock and took it before us
                lock.write_bytes(f"pid={os.getpid()}\n".encode("utf-8"))
            return real_read(path)

        with mock.patch.object(seal, "process_alive", return_value=False), \
                mock.patch.object(seal, "read_lock", side_effect=racing_read):
            with self.assertRaises(seal.GateError):
                with seal.state_lock(self.state):
                    self.fail("lock must not be acquired")
        self.assertEqual(lock.read_bytes(), f"pid={os.getpid()}\n".encode("utf-8"))

    def test_concurrent_breaker_leaves_the_lock_alone(self) -> None:
        lock = self.write_lock(424242)
        breaker = lock.with_name(lock.name + ".break")
        breaker.write_bytes(b"")
        with mock.patch.object(seal, "process_alive", return_value=False):
            with self.assertRaises(seal.GateError):
                with seal.state_lock(self.state):
                    self.fail("lock must not be acquired")
        self.assertTrue(lock.exists())

    def test_process_alive(self) -> None:
        self.assertTrue(seal.process_alive(os.getpid()))
        self.assertFalse(seal.process_alive(0))
        child = subprocess.Popen([sys.executable, "-c", "pass"])
        child.wait()
        self.assertFalse(seal.process_alive(child.pid))


class SealCliSmokeTests(SealTestCase):
    """Real subprocess runs: the published packet passes the standalone combat validator, and the
    gate commands keep their exit codes and messages."""

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"}, check=False,
        )

    def test_standard_seal_passes_with_bom_and_crlf(self) -> None:
        candidate_text = make_prompt().replace("\n", "\r\n")
        candidate = self.write_candidate("candidate.md", candidate_text, bom=True)
        self.template.write_bytes(
            b"\xef\xbb\xbf"
            + "# 冷审规则\r\n\r\n只审阅密封包内的唯一候选全文。".encode("utf-8")
        )
        packet = self.root / "PROJECT_RULES.md"

        result = self.run_cli(*self.seal_args(candidate, packet))

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

    def test_start_and_finish_commands(self) -> None:
        candidate = self.write_candidate("candidate.md", make_prompt())
        packet = self.root / "round-1.md"
        self.assertEqual(self.seal(candidate, packet).returncode, 0)
        started = self.run_cli("start", "--state", str(self.state), "--snapshot", str(packet),
                               "--reviewer", "reviewer-a")
        finished = self.run_cli(*self.finish_args(packet, "reviewer-a", "PASS"))
        again = self.run_cli("start", "--state", str(self.state), "--snapshot", str(packet),
                             "--reviewer", "reviewer-b")
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertIn("PASS: review round 1 started", started.stdout)
        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertIn("STATE_STATUS=terminated", finished.stdout)
        self.assertEqual(again.returncode, 1)
        self.assertIn("ERROR: review state is terminated", again.stderr)


if __name__ == "__main__":
    unittest.main()
