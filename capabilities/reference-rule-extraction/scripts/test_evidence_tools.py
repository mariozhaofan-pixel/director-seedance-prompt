"""Tests for the reference-rule-extraction evidence tools (stdlib unittest).

Run from this directory:  python -B -m unittest discover -s . -p "test_*.py"
End-to-end cases skip cleanly when ffmpeg/ffprobe, numpy or Pillow are missing.
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import extract_subtitles_ocr as ocr  # noqa: E402
import prepare_video_evidence as pve  # noqa: E402
import transcribe_audio as asr  # noqa: E402
import validate_storyboard as vs  # noqa: E402

CAPABILITY = HERE.parent


def shot(number: int, heading_time: str = "", *, sound: list[str] | None = None,
         blocking_extra: list[str] | None = None, preamble: list[str] | None = None) -> str:
    sound = sound if sound is not None else [
        "  - `画内对白=` 无对白及其他语音",
        "  - `环境/拟音/音效=` 室内空调低鸣",
        "  - `音乐=` 无",
    ]
    lines = [f"### S{number:03d}{heading_time}", ""]
    lines += preamble or []
    lines += [
        "- **场景与人物：** 画面中央一张木桌。",
        "- **画面与构图：** 中景，平视。",
        "- **摄影机：** 固定机位。",
        "- **前后景、遮挡与遮罩：** 近层椅背遮住画面左下角。",
        "- **演员、道具运动与调度：**",
        "  - `IN=` 画面右侧人物半身。",
        *(blocking_extra or []),
        "  - `CHANGE=` 人物向画面中央移动。",
        "  - `OUT=` 人物停在画面中央。",
        "- **表演与微表情：** 嘴角收紧。",
        "- **特效与画面处理：** 无",
        "- **声音：**",
        *sound,
        "- **剪辑与节奏：** 尾词后硬切。",
        "",
    ]
    return "\n".join(lines)


def document(*shots: str) -> str:
    return "# 《样片》分镜脚本\n\n## 逐镜分镜\n\n" + "\n".join(shots)


def codes(report: dict, kind: str = "errors") -> list[str]:
    return [item["code"] for item in report[kind]]


class StoryboardValidatorTests(unittest.TestCase):
    def test_template_shot_passes(self) -> None:
        report = vs.validate_markdown(document(shot(1, "｜00:00:00.000–00:00:02.000｜2.000秒")))
        self.assertEqual(report["status"], "PASS", report["errors"])

    def test_sub_line_with_screen_position_and_colon_stays_in_sound(self) -> None:
        sound = ["  - `画内对白=` 画面右侧女人：“走吧。”",
                 "  - `环境/拟音/音效=` 风声", "  - `音乐=` 无"]
        report = vs.validate_markdown(document(shot(1, sound=sound)))
        self.assertEqual(report["status"], "PASS", report["errors"])

    def test_unindented_description_line_does_not_switch_field(self) -> None:
        extra = ["画面左侧女人：抬头看向画面右侧。"]
        report = vs.validate_markdown(document(shot(1, blocking_extra=extra)))
        self.assertNotIn("missing_blocking_states", codes(report))
        self.assertEqual(report["status"], "PASS", report["errors"])

    def test_speaker_named_analyst_is_not_a_prohibited_section(self) -> None:
        sound = ["  - `画内对白=` 人物对白", "分析师：“数据不对。”",
                 "  - `环境/拟音/音效=` 键盘声", "  - `音乐=` 无"]
        report = vs.validate_markdown(document(shot(1, sound=sound)))
        self.assertNotIn("prohibited_delivery_section", codes(report))
        self.assertEqual(report["status"], "PASS", report["errors"])

    def test_real_prohibited_sections_are_still_caught(self) -> None:
        text = document(shot(1)) + "\n- **证据：** 第 12 帧\n来源：网络\n## 分析总结\n"
        flagged = [item for item in vs.validate_markdown(text)["errors"]
                   if item["code"] == "prohibited_delivery_section"]
        self.assertEqual(len(flagged), 3)

    def test_plain_exact_field_name_still_counts_as_field(self) -> None:
        text = document(shot(1)).replace("- **剪辑与节奏：** 尾词后硬切。", "剪辑与节奏：尾词后硬切。")
        self.assertEqual(vs.validate_markdown(text)["status"], "PASS")

    def test_missing_bold_field_is_reported(self) -> None:
        text = document(shot(1)).replace("- **摄影机：** 固定机位。\n", "")
        self.assertIn("missing_required_field", codes(vs.validate_markdown(text)))

    def test_bossa_nova_is_not_a_voice_category(self) -> None:
        sound = ["  - `画内对白=` 无对白及其他语音", "  - `环境/拟音/音效=` 无",
                 "  - `音乐=` Bossa Nova 轻柔吉他"]
        self.assertEqual(vs.validate_markdown(document(shot(1, sound=sound)))["status"], "PASS")
        no_category = ["  - `环境/拟音/音效=` 无", "  - `音乐=` Bossa Nova 轻柔吉他"]
        self.assertIn("missing_dialogue_category",
                      codes(vs.validate_markdown(document(shot(1, sound=no_category)))))

    def test_voice_over_abbreviations_still_count(self) -> None:
        for token in ("V.O.", "O.S.", "（VO）"):
            with self.subTest(token=token):
                sound = [f"  - `画外音=` {token}：“我回来了。”", "  - `环境/拟音/音效=` 无", "  - `音乐=` 无"]
                self.assertEqual(vs.validate_markdown(document(shot(1, sound=sound)))["status"], "PASS")
        missing = ["  - `旁白=` V.O. 低声", "  - `环境/拟音/音效=` 无", "  - `音乐=` 无"]
        self.assertIn("missing_speech_content", codes(vs.validate_markdown(document(shot(1, sound=missing)))))

    def test_body_duration_ranges_are_not_shot_timecodes(self) -> None:
        extra = ["  - 0.5秒–1.5秒 手抬起；1.0s–2.0s 停住。"]
        text = document(shot(1, blocking_extra=extra), shot(2, blocking_extra=extra))
        report = vs.validate_markdown(text)
        self.assertEqual(report["timecodes"]["present_count"], 0)
        self.assertEqual(report["status"], "PASS", report["errors"])
        self.assertIn("timecode_checks_skipped", codes(report, "warnings"))

    def test_timecode_line_right_under_heading_still_counts(self) -> None:
        text = document(shot(1, preamble=["00:00:00.000–00:00:01.500", ""]),
                        shot(2, preamble=["00:00:01.500–00:00:03.000", ""]))
        report = vs.validate_markdown(text, require_timecodes=True)
        self.assertEqual(report["timecodes"]["present_count"], 2)
        self.assertEqual(report["status"], "PASS", report["errors"])

    def test_documented_strict_command_rejects_gaps_and_short_coverage(self) -> None:
        text = document(shot(1, "｜00:00:00.000–00:00:01.000"), shot(2, "｜00:00:01.500–00:00:02.000"))
        self.assertIn("timecode_gap", codes(vs.validate_markdown(text), "warnings"))
        strict = vs.validate_markdown(text, require_timecodes=True, strict_coverage=True,
                                      expected_start=0.0, expected_end=3.0)
        self.assertIn("timecode_gap", codes(strict))
        self.assertIn("coverage_end_mismatch", codes(strict))

    def test_docs_state_the_strict_command(self) -> None:
        protocol = (CAPABILITY / "VIDEO_EVIDENCE_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn('validate_storyboard.py "<最终分镜脚本.md>" --require-timecodes --strict-coverage '
                      "--expected-start <起点秒> --expected-end <终点秒>", protocol)
        contract = (CAPABILITY / "references/storyboard-contract.md").read_text(encoding="utf-8")
        self.assertIn("--require-timecodes --strict-coverage --expected-start", contract)

    def test_unheard_placeholder_counts_as_speech_content(self) -> None:
        sound = ["  - `画内对白=` [未听音]", "  - `环境/拟音/音效=` [未听音]", "  - `音乐=` [未听音]"]
        self.assertEqual(vs.validate_markdown(document(shot(1, sound=sound)))["status"], "PASS")


class PrepareHelperTests(unittest.TestCase):
    def test_full_range_parsing(self) -> None:
        self.assertEqual(pve.full_range("120-180"), ("frames", 120, 180))
        self.assertEqual(pve.full_range("4.0s-6.5s"), ("seconds", 4.0, 6.5))
        self.assertEqual(pve.full_range("4–6.5s"), ("seconds", 4.0, 6.5))
        for bad in ("180-120", "1.5-3", "6s-4s", "abc"):
            with self.subTest(value=bad), self.assertRaises(Exception):
                pve.full_range(bad)

    def test_ffmpeg_version_selects_passthrough_option(self) -> None:
        cases = {
            "ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright": "-vsync",
            "ffmpeg version 5.0.1 Copyright": "-vsync",
            "ffmpeg version n5.1.2 Copyright": "-fps_mode",
            "ffmpeg version 9.0.1-full_build-www.gyan.dev": "-fps_mode",
            "ffmpeg version N-112345-gabcdef Copyright": "-fps_mode",
        }
        for line, option in cases.items():
            with self.subTest(line=line):
                self.assertEqual(pve.passthrough_args(pve.parse_ffmpeg_version(line))[0], option)

    def test_frame_timestamp_and_duration_fields(self) -> None:
        self.assertEqual(pve.frame_pts({"best_effort_timestamp": 30, "pts": 20}), (30, "best_effort_timestamp"))
        self.assertEqual(pve.frame_pts({"pts": "20"}), (20, "pts"))
        self.assertEqual(pve.frame_pts({"pts": "N/A"}), (None, ""))
        self.assertEqual(pve.frame_duration_seconds({"duration_time": "0.04"}), 0.04)
        self.assertEqual(pve.frame_duration_seconds({"pkt_duration_time": "0.05"}), 0.05)
        self.assertIsNone(pve.frame_duration_seconds({"duration_time": "N/A"}))

    def test_repeated_pts_kept_backwards_rejected(self) -> None:
        stream = {"time_base": "1/10"}
        frames = [{"pts": p, "width": 4, "height": 2} for p in (10, 11, 11, 12, 13)]
        records = pve.select_frame_records({"frames": frames}, stream, 0.1, 0.3)
        self.assertEqual([r["source_frame_index"] for r in records], [1, 2, 3])
        self.assertEqual(records[0]["timestamp_s"], 0.1)
        with self.assertRaises(pve.EvidenceError):
            pve.select_frame_records({"frames": [{"pts": 5}, {"pts": 4}]}, stream, 0.0, None)

    def test_stream_selection_and_rotation(self) -> None:
        streams = [{"index": 0, "codec_type": "video", "disposition": {"attached_pic": 1}},
                   {"index": 1, "codec_type": "video", "disposition": {"attached_pic": 0},
                    "side_data_list": [{"rotation": -90}]},
                   {"index": 2, "codec_type": "audio"}]
        self.assertEqual([s["index"] for s in pve.select_video_streams(streams)], [1])
        chosen, cover_first = ocr._select_video_stream(streams)
        self.assertEqual(chosen["index"], 1)
        self.assertTrue(cover_first)
        self.assertEqual(pve.display_rotation(streams[1]), -90.0)
        self.assertEqual(ocr._display_rotation(streams[1]), -90.0)
        self.assertEqual(pve.display_rotation({"tags": {"rotate": "90"}}), 90.0)
        self.assertEqual(pve.right_angle(-90.0), 270)
        self.assertIsNone(pve.right_angle(45.0))
        self.assertEqual(pve.display_size(1920, 1080, -90.0), (1080, 1920))
        self.assertEqual(pve.display_size(1920, 1080, 180.0), (1920, 1080))
        self.assertEqual(pve.thumbnail_size(1920, 1080, 0.0, Fraction(1), 160), (160, 90))
        self.assertEqual(pve.thumbnail_size(1920, 1080, 90.0, Fraction(1), 160), (90, 160))
        self.assertEqual(pve.thumbnail_size(720, 576, 0.0, Fraction(16, 15), 160), (160, 120))

    def test_pts_alignment_and_showinfo(self) -> None:
        log = ("[Parsed_showinfo_1 @ 0x1] n:   0 pts: 144000 pts_time:1.6\n"
               "[Parsed_showinfo_1 @ 0x1] n:   1 pts: 153000 pts_time:1.7\n")
        shown = pve.parse_showinfo(log)
        self.assertEqual(shown, [(0, 144000), (1, 153000)])
        self.assertEqual(pve.pts_alignment(shown, [144000, 153000]), "exact")
        self.assertEqual(pve.pts_alignment([(0, 0), (1, 9000)], [144000, 153000]), "relative_offset")
        self.assertIsNone(pve.pts_alignment([(0, 0), (1, 9001)], [144000, 153000]))
        self.assertIsNone(pve.pts_alignment(shown[:1], [144000, 153000]))

    def test_ranges_and_runs(self) -> None:
        records = [{"source_frame_index": 10 + n, "timestamp_s": n * 0.1} for n in range(10)]
        self.assertEqual(pve.resolve_full_ranges([("frames", 12, 13), ("seconds", 0.5, 0.7)], records),
                         [2, 3, 5, 6])
        self.assertEqual(pve.contiguous_runs([6, 2, 3, 5]), [(2, 3), (5, 6)])
        with self.assertRaises(pve.EvidenceError):
            pve.resolve_full_ranges([("frames", 50, 60)], records)

    def test_subtitle_export_plan(self) -> None:
        self.assertEqual(pve.subtitle_export_plan("mov_text")[0], ".srt")
        self.assertEqual(pve.subtitle_export_plan("ass")[:2], (".ass", ["-c:s", "copy"]))
        self.assertEqual(pve.subtitle_export_plan("hdmv_pgs_subtitle")[0], ".mks")

    def test_parser_keeps_existing_flags(self) -> None:
        args = pve.build_parser().parse_args([
            "in.mp4", "out", "--start", "1", "--end", "2", "--cut-percentile", "95", "--min-cut-gap", "0.4",
            "--analysis-height", "720", "--resume-export", "--expected-video-sha256", "0" * 64])
        self.assertEqual((args.start, args.end, args.analysis_height), (1.0, 2.0, 720))
        self.assertFalse(args.export_full_frames)


class ScriptConsistencyTests(unittest.TestCase):
    def test_ocr_timeline_matches_evidence_pts_rule(self) -> None:
        timeline = ocr._timeline_from_frames([
            {"best_effort_timestamp_time": "0.0", "duration_time": "0.04"},
            {"best_effort_timestamp_time": "0.0", "pkt_duration_time": "0.05"},
            {"pts_time": "0.08"},
        ])
        self.assertEqual([t["duration"] for t in timeline], [0.04, 0.05, 0.0])
        with self.assertRaises(RuntimeError):
            ocr._timeline_from_frames([{"best_effort_timestamp_time": "1.0"}, {"best_effort_timestamp_time": "0.5"}])

    def test_ocr_refuses_existing_outputs_with_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "v.mp4"
            video.write_bytes(b"not a video")
            out = Path(tmp) / "ocr"
            out.mkdir()
            (out / "ocr_manifest.json").write_text("{}", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(ocr.main([str(video), str(out)]), 2)
            self.assertEqual((out / "ocr_manifest.json").read_text(encoding="utf-8"), "{}")

    def test_asr_refuses_existing_outputs_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audio = Path(tmp) / "a.wav"
            audio.write_bytes(b"RIFF")
            out = Path(tmp) / "asr"
            out.mkdir()
            (out / "transcript_raw.json").write_text("keep", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(asr.main([str(audio), str(out)]), 2)
            self.assertIn("--overwrite", stderr.getvalue())
            self.assertEqual((out / "transcript_raw.json").read_text(encoding="utf-8"), "keep")
            self.assertTrue(asr.build_parser().parse_args([str(audio), str(out), "--overwrite"]).overwrite)


def media_tools_available() -> bool:
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        return False
    try:
        import numpy  # noqa: F401
        import PIL  # noqa: F401
    except ImportError:
        return False
    return True


@unittest.skipUnless(media_tools_available(), "ffmpeg/ffprobe, numpy or Pillow not available")
class PrepareEndToEndTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.ts = cls.root / "clip.ts"  # MPEG-TS: container start_time is not 0
        cls.ffmpeg(["-f", "lavfi", "-i", "testsrc2=size=64x36:rate=10:duration=2",
                    "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=8000:duration=2",
                    "-c:v", "mpeg2video", "-c:a", "mp2", "-shortest", str(cls.ts)])

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    @staticmethod
    def ffmpeg(arguments: list[str]) -> bool:
        completed = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *arguments],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)
        return completed.returncode == 0

    def run_prepare(self, *arguments: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return pve.main(list(arguments))

    @staticmethod
    def rows(out: Path) -> list[dict]:
        with (out / "frame_index.csv").open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    @staticmethod
    def manifest(out: Path) -> dict:
        return json.loads((out / "analysis_manifest.json").read_text(encoding="utf-8"))

    def test_nonzero_start_time_full_coverage_and_range_append(self) -> None:
        out = self.root / "ts_full"
        self.assertEqual(self.run_prepare(str(self.ts), str(out)), 0)
        manifest = self.manifest(out)
        self.assertGreater(manifest["probe_summary"]["start_time_seconds"], 0)
        self.assertEqual(manifest["frame_sheets"]["pts_alignment"], "exact")
        rows = self.rows(out)
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(row["sheet_file"] and row["sheet_cell"] for row in rows))
        self.assertAlmostEqual(float(rows[0]["duration_s"]), 0.1, places=3)
        self.assertEqual(sum(s["frame_count"] for s in manifest["frame_sheets"]["sheets"]), 20)
        self.assertTrue(all((out / s["file"]).is_file() for s in manifest["frame_sheets"]["sheets"]))
        self.assertEqual(manifest["full_frame_export"]["status"], "not_requested")
        self.assertFalse((out / "frames").exists())
        self.assertEqual(manifest["audio"]["tracks"][0]["original_codec"], "pcm_f32le")
        # Follow-up: add full-size frames for a hard range to the same evidence directory.
        self.assertEqual(self.run_prepare(str(self.ts), str(out), "--full-range", "3-5"), 0)
        written = [row["source_frame_index"] for row in self.rows(out) if row["export_status"] == "written"]
        self.assertEqual(written, ["3", "4", "5"])
        self.assertTrue((out / "frames/full/frame_000000004.png").is_file())
        self.assertEqual(self.run_prepare(str(self.ts), str(out)), 2)  # never mixes a second run

    def test_start_end_selects_the_same_frames_in_both_passes(self) -> None:
        out = self.root / "ts_range"
        self.assertEqual(self.run_prepare(str(self.ts), str(out), "--start", "0.5", "--end", "1.5",
                                          "--full-range", "0.8s-1.0s"), 0)
        rows = self.rows(out)
        self.assertEqual([int(r["source_frame_index"]) for r in rows], list(range(5, 15)))
        self.assertTrue(all(0.5 <= float(r["timestamp_s"]) < 1.5 for r in rows))
        manifest = self.manifest(out)
        self.assertEqual(manifest["frame_sheets"]["pts_alignment"], "exact")
        self.assertEqual([r["source_frame_index"] for r in rows if r["export_status"] == "written"], ["8", "9"])

    def test_rotation_is_applied_to_sheets_and_frames(self) -> None:
        base, rotated = self.root / "base.mp4", self.root / "rot.mp4"
        if not (self.ffmpeg(["-f", "lavfi", "-i", "testsrc2=size=64x36:rate=10:duration=1",
                             "-c:v", "mpeg4", str(base)])
                and self.ffmpeg(["-display_rotation", "90", "-i", str(base), "-c", "copy", str(rotated)])):
            self.skipTest("this ffmpeg cannot write display rotation metadata")
        out = self.root / "rot_out"
        self.assertEqual(self.run_prepare(str(rotated), str(out), "--full-range", "0-0"), 0)
        manifest = self.manifest(out)
        summary = manifest["probe_summary"]
        self.assertEqual((summary["display_width"], summary["display_height"]), (36, 64))
        self.assertLess(manifest["frame_sheets"]["thumbnail_width"], manifest["frame_sheets"]["thumbnail_height"])
        from PIL import Image
        with Image.open(out / "frames/full/frame_000000000.png") as image:
            self.assertEqual(image.size, (36, 64))

    def test_embedded_subtitles_are_exported(self) -> None:
        srt, video = self.root / "s.srt", self.root / "sub.mp4"
        srt.write_bytes(b"1\n00:00:00,000 --> 00:00:00,500\nhello\n")
        if not self.ffmpeg(["-f", "lavfi", "-i", "testsrc2=size=64x36:rate=10:duration=1", "-i", str(srt),
                            "-map", "0", "-map", "1", "-c:v", "mpeg4", "-c:s", "mov_text", str(video)]):
            self.skipTest("this ffmpeg cannot write mov_text subtitles")
        out = self.root / "sub_out"
        self.assertEqual(self.run_prepare(str(video), str(out)), 0)
        manifest = self.manifest(out)
        self.assertEqual(manifest["probe_summary"]["subtitle_stream_count"], 1)
        self.assertEqual(manifest["subtitles"]["status"], "exported_all_tracks")
        self.assertIn("hello", (out / "subtitles/track_00.srt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
