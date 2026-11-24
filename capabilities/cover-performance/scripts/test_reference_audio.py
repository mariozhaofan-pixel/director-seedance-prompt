import io
import json
import math
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
from unittest import mock
from types import SimpleNamespace
import wave

import fit_reference_audio
from fit_reference_audio import allocate_budget, duration, fit_rate, map_lyrics, render, run


def write_tone(path, seconds):
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(44100)
        w.writeframes(b''.join(struct.pack('<h',round(10000*math.sin(2*math.pi*440*i/44100))) for i in range(round(seconds*44100))))
    return path


def legacy_wave_open(f, mode=None, _open=wave.open):
    """Python < 3.12 wave rejects WAVE_FORMAT_EXTENSIBLE (65534); emulate that on any Python."""
    if mode in (None, 'r', 'rb'):
        with open(f, 'rb') as handle:
            header = handle.read(64)
        at = header.find(b'fmt ')
        tag = int.from_bytes(header[at+8:at+10], 'little')
        if tag != 1:
            raise wave.Error(f'unknown format: {tag}')
    return _open(f, mode)


class BudgetTests(unittest.TestCase):
    def test_default_and_observed_short_voice(self):
        self.assertEqual(allocate_budget()['song_limit_seconds'],26)
        self.assertEqual(allocate_budget(voice_durations=[3.996708])['song_limit_seconds'],26)

    def test_long_voice_and_all_other_uploads(self):
        self.assertEqual(allocate_budget(voice_durations=[6],other_durations=[2,3])['song_limit_seconds'],19)
        self.assertEqual(allocate_budget(voice_durations=[4,4])['song_limit_seconds'],22)

    def test_text_voice_and_shorter_video(self):
        self.assertEqual(allocate_budget(reserve=0)['song_limit_seconds'],30)
        self.assertEqual(allocate_budget(max_song=15)['song_limit_seconds'],15)

    def test_invalid_and_exhausted_budget(self):
        for kwargs in ({'total':float('nan')},{'reserve':-1},{'max_song':float('inf')},{'voice_durations':[31]}):
            with self.assertRaises(ValueError): allocate_budget(**kwargs)

    def test_segment_cap_can_be_lowered_not_raised(self):
        self.assertEqual(allocate_budget(max_song=12)['song_limit_seconds'],12)
        # A larger entry budget is recorded, but one song segment stays within the 30 s cap.
        self.assertEqual(allocate_budget(total=40)['song_limit_seconds'],30)
        with self.assertRaises(ValueError): allocate_budget(max_song=30.5)

    def test_speed_never_drops_content_silently(self):
        self.assertAlmostEqual(fit_rate(28.62,26),1.1007692307692307)
        self.assertEqual(fit_rate(25,26),1)
        with self.assertRaises(ValueError): fit_rate(30,26)
        with self.assertRaises(ValueError): fit_rate(28.62,26,1)

    def test_mapping_offset_and_partial_phrase(self):
        data={'phrases':[{'id':'L1','text':'test fixture','start':2,'end':6,'words':[{'word':'test','start':2,'end':3}]}]}
        mapped=map_lyrics(data,2,6,2)['phrases'][0]
        self.assertEqual((mapped['start'],mapped['end']),(0,2))
        self.assertEqual(mapped['words'][0]['end'],.5)
        self.assertEqual(mapped['evidence'],'transformed ASR candidate')
        self.assertIsNone(map_lyrics(data,3,5,1)['phrases'][0]['text'])

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg required')
    def test_render_duration_budget_pitch_and_immutable_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            source=write_tone(root/'song.wav',2.2); voice=write_tone(root/'voice.wav',.4)
            original=source.read_bytes()
            args=SimpleNamespace(audio=source,start=0,end=2.2,reference_audio_budget=2.4,
                voice_reserve_seconds=.4,voice_reference=[voice],other_reference_audio=[],max_seconds=30,
                max_speed=1.12,companion=source,lyrics=None,output=root/'out')
            result=run(args)
            self.assertAlmostEqual(duration(root/'out/song-reference.wav'),2,places=6)
            self.assertLessEqual(result['actual_uploaded_total_seconds'],2.4+1e-6)
            self.assertEqual(source.read_bytes(),original)
            self.assertNotIn('instrumental-backup.wav',result['upload_set'])
            with wave.open(str(root/'out/song-reference.wav'),'rb') as w:
                b=w.readframes(w.getnframes())
            values=[int.from_bytes(b[i:i+3],'little',signed=True) for i in range(0,len(b),6)][4410:66150]
            cycles=sum(a<=0<b for a,b in zip(values,values[1:]))
            estimated=cycles/(len(values)/44100)
            self.assertLess(abs(estimated-440),2)  # Tempo must not turn 440Hz into 484Hz.

    @unittest.skipUnless(shutil.which('ffmpeg'),'ffmpeg required')
    def test_render_keeps_24_bit_without_extensible_wave_support(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            source=write_tone(root/'song.wav',1.2)
            frames=math.floor(1.2/1.1*44100+1e-7)
            with mock.patch('wave.open',legacy_wave_open):
                result=render(source,root/'out.wav',0,1.2,1.1,frames)
                with wave.open(str(root/'out.wav'),'rb') as w:
                    self.assertEqual((w.getsampwidth(),w.getnchannels(),w.getnframes()),(3,2,result['frames']))


class CommandLineTests(unittest.TestCase):
    argv=['fit_reference_audio.py','song.wav','--output','out']

    def test_prints_any_language_on_a_legacy_console(self):
        out,err=io.BytesIO(),io.BytesIO()
        stdout,stderr=io.TextIOWrapper(out,encoding='ascii'),io.TextIOWrapper(err,encoding='ascii')
        with mock.patch.object(fit_reference_audio,'run',return_value={'lyrics':'사랑해 风经过窗前'}), \
             mock.patch.object(sys,'argv',self.argv), mock.patch.object(sys,'stdout',stdout), mock.patch.object(sys,'stderr',stderr):
            fit_reference_audio.main()
            stdout.flush()
        self.assertIn('사랑해 风经过窗前',out.getvalue().decode('utf-8'))

    def test_unreadable_wave_is_a_clean_error(self):
        stderr=io.StringIO()
        with mock.patch.object(fit_reference_audio,'run',side_effect=wave.Error('unknown format: 65534')), \
             mock.patch.object(sys,'argv',self.argv), mock.patch.object(sys,'stdout',io.StringIO()), mock.patch.object(sys,'stderr',stderr):
            with self.assertRaises(SystemExit) as exit_:
                fit_reference_audio.main()
        self.assertEqual(exit_.exception.code,1)
        self.assertIn('unknown format: 65534',stderr.getvalue())


if __name__=='__main__': unittest.main()
