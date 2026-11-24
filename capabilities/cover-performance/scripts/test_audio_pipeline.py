import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from types import SimpleNamespace

from audio_segments import plan_segments, segment_lyrics
from cover_common import sha256_file as digest
from fit_reference_audio import allocate_budget
import prepare_song
from prepare_song import reuse_audio, stages, write_json
import setup_audio_runtime


class SegmentationTests(unittest.TestCase):
    def assert_partition(self, segments, samples, rate, cap=30):
        self.assertEqual(segments[0]["start_sample"], 0)
        self.assertEqual(segments[-1]["end_sample"], samples)
        for i, part in enumerate(segments):
            self.assertGreater(part["duration"], 0)
            self.assertLessEqual(part["end_sample"] - part["start_sample"], int(rate * cap))
            if i:
                self.assertEqual(part["start_sample"], segments[i - 1]["end_sample"])

    def test_short_audio_stays_complete(self):
        result = plan_segments(12345, 1000, [], [], [], 30)
        self.assertEqual(len(result), 1)
        self.assert_partition(result, 12345, 1000)

    def test_hard_cap_for_long_held_vowel(self):
        phrases = [{"id": "L1", "start": 0, "end": 71.123, "text": "啊", "words": [{"word": "啊", "start": 0, "end": 71.123}]}]
        result = plan_segments(71123, 1000, phrases, [], [t for t in range(1, 71)])
        self.assert_partition(result, 71123, 1000)
        self.assertTrue(any(p["boundary_review"] for p in result))

    def test_prefers_real_pauses_over_equal_thirty_second_slices(self):
        result = plan_segments(70000, 1000, [], [[23, 24], [46, 47]], [t for t in range(70)])
        self.assert_partition(result, 70000, 1000)
        self.assertTrue(23 <= result[0]["end"] <= 24)
        self.assertTrue(46 <= result[1]["end"] <= 47)

    def test_short_tail_does_not_create_padding_or_lose_samples(self):
        for samples in (30001, 60001, 61573, 301234):
            with self.subTest(samples=samples):
                result = plan_segments(samples, 1000, [], [], [])
                self.assert_partition(result, samples, 1000)

    def test_smaller_model_cap(self):
        result = plan_segments(41123, 1000, [], [[13, 14], [27, 28]], [], 15)
        self.assert_partition(result, 41123, 1000, 15)

    def test_invalid_caps(self):
        for cap in (0, -1, 30.1):
            with self.assertRaises(ValueError):
                plan_segments(1000, 1000, [], [], [], cap)

    def test_repeated_text_preserves_occurrences(self):
        phrases = [{"id": "L1", "start": 1, "end": 3, "text": "又见晴天", "words": []},
                   {"id": "L2", "start": 8, "end": 10, "text": "又见晴天", "words": []}]
        items = segment_lyrics({"start": 0, "end": 12}, phrases)
        self.assertEqual([p["occurrence_id"] for p in items], ["L1", "L2"])
        self.assertEqual([p["text"] for p in items], ["又见晴天", "又见晴天"])

    def test_cross_boundary_syllable_is_continuation(self):
        phrases = [{"id": "L1", "start": 28, "end": 34, "text": "晴天", "words": [
            {"word": "晴", "start": 28, "end": 29}, {"word": "天", "start": 29, "end": 34}]}]
        left = segment_lyrics({"start": 0, "end": 30}, phrases)[0]
        right = segment_lyrics({"start": 30, "end": 40}, phrases)[0]
        self.assertEqual(left["text"], "晴天")
        self.assertEqual(right["text"], "天")
        self.assertTrue(right["continuation_from_previous"])
        self.assertTrue(right["crosses_word"])
        self.assertEqual(right["words"][0]["start"], 0)
        self.assertEqual(right["words"][0]["end"], 4)
        self.assertEqual(right["source_start"], 30)

    def test_missing_word_alignment_does_not_invent_fragment(self):
        phrases = [{"id": "L1", "start": 28, "end": 34, "text": "风经过窗前", "words": []}]
        item = segment_lyrics({"start": 30, "end": 40}, phrases)[0]
        self.assertIsNone(item["text"])
        self.assertEqual(item["full_phrase_context"], "风经过窗前")

    def test_no_input_mutation(self):
        phrases = [{"start": 2, "end": 5, "text": "测试", "words": []}]
        saved = copy.deepcopy(phrases)
        plan_segments(40000, 1000, phrases, [[6, 7]], [5])
        self.assertEqual(phrases, saved)


class StageTests(unittest.TestCase):
    def prepared_fixture(self, base):
        donor, target = base / "donor", base / "target"
        donor.mkdir(); target.mkdir()
        config = {"pipeline_version": "1.1.0", "separator_model": "fixture", "audio_separator_version": "test"}
        manifest = {"input_sha256": "same-source", "config": config, "stages": {}}
        for stage, names in {"normalize": ["source.wav", "audio-info.json"],
                             "separate": ["vocals.wav", "instrumental.wav", "separation.json"]}.items():
            rows = []
            for name in names:
                (donor/name).write_text(name, encoding="utf-8")
                rows.append({"path": name, "sha256": digest(donor/name)})
            manifest["stages"][stage] = {"outputs": rows}
        write_json(donor/"manifest.json", manifest)
        return donor, target, {"input_sha256": "same-source", "config": config.copy(), "stages": {}}

    def test_reuse_stems_is_verified_and_copy_is_independent(self):
        with tempfile.TemporaryDirectory() as temp:
            donor, target, manifest = self.prepared_fixture(Path(temp))
            reuse_audio(donor, target, manifest)
            self.assertEqual(set(manifest["stages"]), {"normalize", "separate"})
            self.assertEqual((donor/"vocals.wav").read_bytes(), (target/"vocals.wav").read_bytes())
            (target/"vocals.wav").write_bytes(b"changed")
            self.assertEqual((donor/"vocals.wav").read_bytes(), b"vocals.wav")

    def test_reuse_rejects_other_source_or_separator(self):
        with tempfile.TemporaryDirectory() as temp:
            donor, target, manifest = self.prepared_fixture(Path(temp))
            manifest["input_sha256"] = "different-source"
            with self.assertRaises(ValueError):
                reuse_audio(donor, target, manifest)
            manifest["input_sha256"] = "same-source"
            manifest["config"]["separator_model"] = "different-model"
            with self.assertRaises(ValueError):
                reuse_audio(donor, target, manifest)
            self.assertFalse(list(target.iterdir()))

    def test_reuse_checks_all_hashes_before_copying(self):
        with tempfile.TemporaryDirectory() as temp:
            donor, target, manifest = self.prepared_fixture(Path(temp))
            (donor/"vocals.wav").write_bytes(b"corrupt")
            with self.assertRaises(ValueError):
                reuse_audio(donor, target, manifest)
            self.assertFalse(list(target.iterdir()))

    def test_malformed_manifest_does_not_leave_processing_lock(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "input.wav"
            source.write_bytes(b"test input")
            args = SimpleNamespace(audio=source, output=base / "out", max_seconds=30, threads=1,
                separator_model="fixture", asr_model="small", language="en", reference_audio_budget=30,
                voice_reserve_seconds=4, voice_reference=[], other_reference_audio=[], reuse_prepared=None)
            with mock.patch.object(prepare_song, "ensure_runtime"), mock.patch.object(prepare_song.importlib.metadata, "version", return_value="test"), mock.patch.object(prepare_song, "normalize", side_effect=RuntimeError("expected fixture failure")):
                with self.assertRaises(RuntimeError):
                    prepare_song.run(args)
                root = next(args.output.iterdir())
                (root / "manifest.json").write_text("invalid json", encoding="utf-8")
                with self.assertRaises(json.JSONDecodeError):
                    prepare_song.run(args)
                self.assertFalse((root / ".processing.lock").exists())

    def test_cache_reuse_and_corruption_invalidates_downstream(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = {"stages": {}}
            calls = []
            def action():
                calls.append(1)
                (root / "source.wav").write_bytes(b"audio fixture")
                return [root / "source.wav"]
            execute = stages(manifest, root)
            execute("normalize", action)
            execute("normalize", action)
            self.assertEqual(len(calls), 1)
            manifest["stages"]["separate"] = {"outputs": []}
            (root / "source.wav").write_bytes(b"corrupt")
            execute("normalize", action)
            self.assertEqual(len(calls), 2)
            self.assertNotIn("separate", manifest["stages"])

    def test_atomic_json_is_readable(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "nested/state.json"
            write_json(target, {"歌词": "风经过窗前"})
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"歌词": "风经过窗前"})
            self.assertFalse(target.with_suffix(".json.tmp").exists())

    def test_separation_is_keyed_only_by_source_and_separator(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "input.wav"
            source.write_bytes(b"test input")
            calls = {"normalize": 0, "separate": 0, "transcribe": 0}

            def normalize(src, root):
                calls["normalize"] += 1
                for name in ("source.wav", "audio-info.json"):
                    (root / name).write_text(name, encoding="utf-8")
                return [root / "source.wav", root / "audio-info.json"]

            def separate(root, args):
                calls["separate"] += 1
                names = ("vocals.wav", "instrumental.wav", "separation.json")
                for name in names:
                    (root / name).write_text(f"{name}{calls['separate']}", encoding="utf-8")
                return [root / name for name in names]

            def transcribe(stems, work, args):
                calls["transcribe"] += 1
                (work / "lyrics.json").write_text(args.asr_model, encoding="utf-8")
                return [work / "lyrics.json"]

            def analyze(stems, work):
                (work / "rhythm.json").write_text("{}", encoding="utf-8")
                return [work / "rhythm.json"]

            def export_segments(stems, work, budget):
                (work / "compiler-input.json").write_text(json.dumps(budget), encoding="utf-8")
                return [work / "compiler-input.json"]

            def probe_budget(total, reserve, voices, others, max_song):
                result = allocate_budget(total, reserve, [], [], max_song)
                result["attachments"] = [str(path) for path in voices]
                return result

            def args(**changes):
                values = dict(audio=source, output=base / "out", max_seconds=30, threads=1,
                              separator_model="fixture", asr_model="small", language="auto",
                              reference_audio_budget=30, voice_reserve_seconds=4, voice_reference=[],
                              other_reference_audio=[], reuse_prepared=None)
                return SimpleNamespace(**{**values, **changes})

            with mock.patch.multiple(prepare_song, ensure_runtime=mock.DEFAULT, event=mock.DEFAULT,
                                     normalize=normalize, separate=separate, transcribe=transcribe,
                                     analyze=analyze, export_segments=export_segments, probe_budget=probe_budget), \
                 mock.patch.object(prepare_song.importlib.metadata, "version", return_value="test"):
                runs = [prepare_song.run(args()), prepare_song.run(args(asr_model="large-v3-turbo")),
                        prepare_song.run(args(language="ko")), prepare_song.run(args(max_seconds=15)),
                        prepare_song.run(args(voice_reference=[base / "voice.wav"]))]
                self.assertEqual(prepare_song.run(args()), runs[0])
                self.assertEqual((calls["normalize"], calls["separate"], calls["transcribe"]), (1, 1, 5))
                self.assertEqual(len({run.parent for run in runs}), 1)
                self.assertEqual(len(set(runs)), 5)
                self.assertEqual((runs[0] / "lyrics.json").read_text(encoding="utf-8"), "small")
                # Rebuilt stems make the downstream results of a run stale.
                (runs[0].parent / "vocals.wav").write_bytes(b"corrupt")
                prepare_song.run(args())
                self.assertEqual((calls["normalize"], calls["separate"], calls["transcribe"]), (1, 2, 6))
                prepare_song.run(args(separator_model="other-model"))
                self.assertEqual(len([p for p in (base / "out").iterdir() if p.is_dir()]), 2)

    def test_raised_segment_cap_fails_before_runtime_setup(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "input.wav"
            source.write_bytes(b"test input")
            args = SimpleNamespace(audio=source, output=Path(temp) / "out", max_seconds=31, threads=1)
            with mock.patch.object(prepare_song, "ensure_runtime") as ensure:
                with self.assertRaises(ValueError):
                    prepare_song.run(args)
            ensure.assert_not_called()


class RuntimeTests(unittest.TestCase):
    def ensure(self, ready, no_install):
        with mock.patch.object(prepare_song.importlib.util, "find_spec", return_value=None), \
             mock.patch.object(setup_audio_runtime, "check", return_value=ready), \
             mock.patch.object(setup_audio_runtime, "install") as install, \
             mock.patch.object(setup_audio_runtime, "runtime_python", return_value=Path("isolated/python")), \
             mock.patch.object(prepare_song.subprocess, "call", return_value=0) as call, \
             mock.patch.object(prepare_song, "event"):
            with self.assertRaises(SystemExit) as exit_:
                prepare_song.ensure_runtime(SimpleNamespace(no_install=no_install))
        return install, call, exit_.exception.code

    def test_no_install_uses_a_ready_runtime(self):
        install, call, code = self.ensure(ready=True, no_install=True)
        install.assert_not_called()
        self.assertEqual(code, 0)
        self.assertEqual(call.call_args.args[0][0], str(Path("isolated/python").resolve()))

    def test_no_install_fails_only_when_runtime_is_missing(self):
        with mock.patch.object(prepare_song.importlib.util, "find_spec", return_value=None), \
             mock.patch.object(setup_audio_runtime, "check", return_value=False), \
             mock.patch.object(setup_audio_runtime, "install") as install:
            with self.assertRaisesRegex(RuntimeError, "--no-install"):
                prepare_song.ensure_runtime(SimpleNamespace(no_install=True))
        install.assert_not_called()

    def test_missing_runtime_is_installed_without_the_flag(self):
        install, call, code = self.ensure(ready=False, no_install=False)
        install.assert_called_once_with()
        self.assertEqual((call.call_count, code), (1, 0))


if __name__ == "__main__":
    unittest.main()
