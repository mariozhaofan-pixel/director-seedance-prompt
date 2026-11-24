"""Helpers shared by the cover-performance scripts. Standard library only."""
from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import sys

# Model hard cap for one generated video segment, and so for one song-reference
# segment. Callers may lower it (shorter Tmax, user request); nothing may raise it.
MAX_SEGMENT_SECONDS = 30.0


def utf8_console():
    """Lyrics and paths can be in any language; a legacy console code page must not crash output."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ffmpeg_executable():
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise RuntimeError("ffmpeg required; use the cover-audio runtime or install ffmpeg") from exc
    return imageio_ffmpeg.get_ffmpeg_exe()
