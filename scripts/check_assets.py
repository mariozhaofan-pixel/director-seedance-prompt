#!/usr/bin/env python3
"""Check reference files against a target platform's hard limits before upload.

Reads image dimensions from file headers (PNG, JPEG, GIF, WebP) without extra
dependencies; videos are checked for existence and, when ffprobe is available,
their aspect ratio. Limits live in knowledge/02L_PLATFORM_PROFILES.md.
"""

from __future__ import annotations

import argparse
import json
import shutil
import struct
import subprocess
import sys
from pathlib import Path

PLATFORMS = {
    "seedance-2.0": {"max_aspect": 2.5},
    "seedance-2.5": {"max_aspect": 2.5},
}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".webm", ".m4v"}


def image_size(data: bytes) -> tuple[int, int] | None:
    """Return (width, height) from an image header, or None if unrecognised."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP" and len(data) >= 30:
        chunk = data[12:16]
        if chunk == b"VP8X":
            w = 1 + int.from_bytes(data[24:27], "little")
            h = 1 + int.from_bytes(data[27:30], "little")
            return w, h
        if chunk == b"VP8L":
            bits = int.from_bytes(data[21:25], "little")
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if chunk == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            return w & 0x3FFF, h & 0x3FFF
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            length = int.from_bytes(data[i + 2:i + 4], "big")
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + length
    return None


def video_size(path: Path) -> tuple[int, int] | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    result = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
        capture_output=True, text=True, check=False,
    )
    try:
        w, h = result.stdout.strip().split("x")[:2]
        return int(w), int(h)
    except ValueError:
        return None


def check_file(path: Path, limits: dict) -> dict:
    item: dict[str, object] = {"path": str(path), "problems": []}
    if not path.is_file():
        item["problems"].append("missing file")
        return item
    suffix = path.suffix.lower()
    size = None
    if suffix in IMAGE_SUFFIXES:
        with path.open("rb") as handle:
            size = image_size(handle.read(65536))
        if size is None:
            item["problems"].append("unreadable image header")
    elif suffix in VIDEO_SUFFIXES:
        size = video_size(path)
        if size is None:
            item["note"] = "video dimensions not checked (ffprobe unavailable or unreadable)"
    else:
        item["problems"].append(f"unsupported file type {suffix or '(none)'}")
    if size:
        w, h = size
        ratio = max(w, h) / max(1, min(w, h))
        item.update({"width": w, "height": h, "aspect": round(ratio, 3)})
        if ratio > limits["max_aspect"] + 1e-9:
            item["problems"].append(
                f"aspect {ratio:.3f} exceeds platform limit {limits['max_aspect']}; crop before upload")
    return item


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="reference image/video files to check")
    parser.add_argument("--platform", choices=sorted(PLATFORMS), default="seedance-2.5")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    limits = PLATFORMS[args.platform]
    report = [check_file(Path(name), limits) for name in args.files]
    failed = [item for item in report if item["problems"]]
    if args.json:
        print(json.dumps({"platform": args.platform, "files": report,
                          "verdict": "FAIL" if failed else "PASS"}, ensure_ascii=False, indent=2))
    else:
        for item in report:
            status = "FAIL" if item["problems"] else "OK"
            dims = f" {item['width']}x{item['height']} ({item['aspect']})" if "width" in item else ""
            print(f"{status} {item['path']}{dims}")
            for problem in item["problems"]:
                print(f"  - {problem}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
