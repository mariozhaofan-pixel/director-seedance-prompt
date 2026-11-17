#!/usr/bin/env python3
"""Collect evidence from an accepted take before writing the next segment.

Outputs into --out: a contact sheet (1 frame per second), detected cut times,
an optional transcript, the suggested tail clip range, and an editable
`evidence.md` whose "actual end state" fields feed the shot card (knowledge/02J).
With --record-seconds, the appended staging record shot (knowledge/02C) is exported
whole as `staging_record.mp4`, the next segment's @视频1; --min-frames slows it uniformly
when it is shorter than the platform/project minimum.
Requires ffmpeg/ffprobe on PATH; transcription is optional (faster-whisper).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCENE_RE = re.compile(r"lavfi\.scd\.time=([0-9.]+)")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)


def probe(video: Path) -> dict:
    result = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                  "-show_entries", "stream=nb_read_frames,r_frame_rate,width,height:format=duration",
                  "-of", "json", str(video)])
    data = json.loads(result.stdout or "{}")
    stream = (data.get("streams") or [{}])[0]
    num, _, den = str(stream.get("r_frame_rate", "24/1")).partition("/")
    fps = float(num) / float(den or 1) if num else 24.0
    return {
        "duration": float(data.get("format", {}).get("duration", 0) or 0),
        "frames": int(stream.get("nb_read_frames", 0) or 0),
        "fps": round(fps, 3), "width": stream.get("width"), "height": stream.get("height"),
    }


def detect_cuts(video: Path, threshold: float) -> list[float]:
    result = run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf",
                  f"scdet=threshold={threshold},metadata=print", "-an", "-f", "null", "-"])
    return [round(float(t), 3) for t in SCENE_RE.findall(result.stderr)]


def contact_sheet(video: Path, out: Path, columns: int, rows: int) -> Path:
    target = out / "contact_sheet.png"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-vf",
         f"fps=1,scale=480:-1,tile={columns}x{rows}", "-frames:v", "1", str(target)])
    return target


def transcribe(video: Path) -> list[dict] | None:
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError:
        return None
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(video), language="zh")
    return [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segments]


def total_frames(info: dict) -> tuple[float, int]:
    fps = info["fps"] or 24.0
    return fps, info["frames"] or int(round(info["duration"] * fps))


def tail_range(info: dict, tail_frames: int, record_seconds: float = 0.0,
               record_start: int | None = None) -> dict:
    """Tail clip range; with a staging record shot appended, the tail ends where that shot begins."""
    fps, frames = total_frames(info)
    end = record_start if record_start is not None else max(0, frames - int(round(record_seconds * fps)))
    start = max(0, end - tail_frames)
    return {"start_frame": start, "end_frame": end,
            "start_seconds": round(start / fps, 3), "end_seconds": round(end / fps, 3)}


def record_range(info: dict, cuts: list[float], record_seconds: float, tolerance: float = 1.0) -> dict:
    """The appended staging record shot (02C): from its actual cut to the last frame.

    Generated record shots often run shorter than planned, so the last detected cut inside the
    final record_seconds + tolerance wins; the planned length is only a fallback.
    """
    fps, frames = total_frames(info)
    planned = max(0, frames - int(round(record_seconds * fps)))
    earliest = frames - int(round((record_seconds + tolerance) * fps))
    near_end = [int(round(t * fps)) for t in cuts if earliest <= int(round(t * fps)) < frames]
    start, source = (near_end[-1], "cut") if near_end else (planned, "planned")
    return {"start_frame": start, "end_frame": frames, "frames": frames - start,
            "start_seconds": round(start / fps, 3), "end_seconds": round(frames / fps, 3), "source": source}


def atempo_chain(speed: float) -> list[float]:
    """Split an audio speed factor into ffmpeg atempo steps that each stay within 0.5–2.0."""
    steps = []
    while speed < 0.5:
        steps.append(0.5)
        speed /= 0.5
    while speed > 2.0:
        steps.append(2.0)
        speed /= 2.0
    return [*steps, speed]


def record_clip_plan(record: dict, min_frames: int) -> dict:
    """Whole record shot as video; uniformly slowed (never padded with other frames) when too short."""
    target = max(record["frames"], min_frames)
    return {"frames": target, "slow_factor": round(target / record["frames"], 6) if record["frames"] else 1.0}


def has_audio(video: Path) -> bool:
    result = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=index",
                  "-of", "csv=p=0", str(video)])
    return bool(result.stdout.strip())


def record_clip(video: Path, out: Path, record: dict, plan: dict, fps: float) -> Path:
    target = out / "staging_record.mp4"
    factor = plan["slow_factor"]
    # Spread first..last source frame over first..last output frame so the cfr output has exactly
    # plan["frames"] frames; each source frame is held uniformly longer. One clone of the last frame
    # only gives that frame a duration at EOF and is cut off again by -frames:v.
    spread = (plan["frames"] - 1) / (record["frames"] - 1) if record["frames"] > 1 else 1.0
    vf = (f"trim=start_frame={record['start_frame']}:end_frame={record['end_frame']},"
          f"tpad=stop_mode=clone:stop=1,setpts=(PTS-STARTPTS)*{spread:.9f},fps={fps:g}")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-vf", vf,
           "-r", f"{fps:g}", "-frames:v", str(plan["frames"]), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16"]
    if has_audio(video):
        af = [f"atrim=start={record['start_frame'] / fps:.6f}:end={record['end_frame'] / fps:.6f}",
              "asetpts=PTS-STARTPTS"]
        if factor != 1.0:
            af += [f"atempo={step:.6f}" for step in atempo_chain(1 / factor)]
        # No -shortest: it drops the final video frame; the trimmed audio already matches the clip length.
        cmd += ["-af", ",".join(af), "-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    run([*cmd, str(target)])
    return target


def render_markdown(video: Path, info: dict, cuts: list[float], tail: dict,
                    transcript: list[dict] | None, record: dict | None = None, plan: dict | None = None) -> str:
    shots = [0.0, *cuts, info["duration"]]
    shot_lines = [f"| {i + 1} | {shots[i]:.2f}–{shots[i + 1]:.2f} |" for i in range(len(shots) - 1)]
    talk = "\n".join(f"- {t['start']:.2f}–{t['end']:.2f}秒：{t['text']}" for t in transcript) if transcript \
        else "- （未转写；需要时安装 faster-whisper 或人工听写）"
    overlap = ""
    if transcript and any(t["start"] < tail["end_seconds"] and t["end"] > tail["start_seconds"] for t in transcript):
        overlap = "\n- 注意：尾段里有台词。若下一段开场动作不同，改截前一镜并让声音在台词前淡出（02C）。"
    tail_label = "建议尾段（不开站位记录镜时用）" if record else "建议尾段"
    if record and plan:
        found = "按切点" if record["source"] == "cut" else "未找到切点，按计划时长"
        slowed = (f"，已整镜匀速放慢 ×{plan['slow_factor']:g} 补到 {plan['frames']} 帧"
                  if plan["frames"] > record["frames"] else "")
        overlap += (f"\n- 站位记录镜：第 {record['start_frame']}–{record['end_frame']} 帧"
                    f"（{record['start_seconds']}–{record['end_seconds']} 秒，实际 {record['frames']} 帧，{found}）"
                    f"→ staging_record.mp4{slowed}。下一段整镜作 @视频1（视频，不截帧），不另挂剧情尾段；"
                    "CUT 1 写记录镜画面，之后 direct cut 到新机位（02C）。")
    return f"""# 取证｜{video.name}

- 时长 {info['duration']:.2f} 秒，{info['frames']} 帧，{info['fps']} fps，{info['width']}x{info['height']}
- 联系表：contact_sheet.png（每秒一格）
- {tail_label}：第 {tail['start_frame']}–{tail['end_frame']} 帧（{tail['start_seconds']}–{tail['end_seconds']} 秒）{overlap}

## 镜头切点

| 镜头 | 区间（秒） |
| --- | --- |
{chr(10).join(shot_lines)}

## 台词时间

{talk}

## 实际结尾状态（看联系表后填写，进入编译卡“衔接”栏）

- 最后一镜景别与机位：
- 画面里有谁、各在画面哪里、朝哪：
- 手里拿着什么、道具在哪：
- 台词说到哪一句、哪一秒：
- 用户会不会用这一镜（被否掉的尾镜不当衔接）：
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scene-threshold", type=float, default=6.0)
    parser.add_argument("--tail-frames", type=int, default=51)
    parser.add_argument("--grid", default="5x5", help="contact sheet columns x rows")
    parser.add_argument("--transcribe", action="store_true", help="transcribe speech if faster-whisper is installed")
    parser.add_argument("--record-seconds", type=float, default=0.0,
                        help="planned length of an appended staging record shot (02C); exports it whole as video")
    parser.add_argument("--min-frames", type=int, default=0,
                        help="shortest reference video the platform/project accepts; a shorter record shot is slowed to it")
    args = parser.parse_args(argv)
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            print(f"ERROR: {tool} not found on PATH; extract frames manually and record that the tool was unavailable",
                  file=sys.stderr)
            return 2
    if not args.video.is_file():
        print(f"ERROR: missing video {args.video}", file=sys.stderr)
        return 2
    columns, _, rows = args.grid.partition("x")
    args.out.mkdir(parents=True, exist_ok=True)
    info = probe(args.video)
    cuts = detect_cuts(args.video, args.scene_threshold)
    contact_sheet(args.video, args.out, int(columns), int(rows or columns))
    transcript = transcribe(args.video) if args.transcribe else None
    record = record_range(info, cuts, args.record_seconds) if args.record_seconds else None
    plan = record_clip_plan(record, args.min_frames) if record else None
    tail = tail_range(info, args.tail_frames, record_start=record["start_frame"] if record else None)
    if record:
        record_clip(args.video, args.out, record, plan, total_frames(info)[0])
    (args.out / "evidence.json").write_text(json.dumps(
        {"video": str(args.video), "info": info, "cuts": cuts, "tail": tail, "record": record,
         "record_clip": plan, "transcript": transcript},
        ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "evidence.md").write_text(
        render_markdown(args.video, info, cuts, tail, transcript, record, plan), encoding="utf-8")
    print(str(args.out / "evidence.md"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
