#!/usr/bin/env python3
"""Refresh package-manifest.json hashes and the knowledge index character counts.

Run from anywhere: python -B maintenance/refresh_manifest.py [--edition 2026-11-25-v33] [--check]

- Updates bytes/sha256 for every file already listed in package-manifest.json.
- Updates the character counts in maintenance/10_KNOWLEDGE_INDEX.md.
- Reports tracked files that ship but are not listed, and listed files that no longer exist.
- With --check, changes nothing and exits 1 when anything is stale (for tests and CI).
Writes with LF line endings and UTF-8, as the repository expects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "package-manifest.json"
INDEX = ROOT / "maintenance" / "10_KNOWLEDGE_INDEX.md"
INDEX_ROW = re.compile(r"(\| \[[^\]]+\]\(([^)]+)\) \| )(\d+) \|")
# Tracked files that never ship (build-only or maintenance); everything else that is tracked should be listed.
NOT_SHIPPED_PREFIXES = ("maintenance/", ".github/", "companion-skills/", "private/")
NOT_SHIPPED_FILES = {"scripts/build_editions.py", "scripts/test_build_editions.py", "package-manifest.json", ".gitignore"}


def digest(path: Path) -> tuple[int, str]:
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def tracked_files() -> list[str] | None:
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "-c", "core.quotepath=off", "ls-files"],
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [line for line in out.splitlines() if line]


def refreshed_index(text: str) -> str:
    def count(match: re.Match) -> str:
        target = (INDEX.parent / match.group(2)).resolve()
        return f"{match.group(1)}{len(target.read_bytes().decode('utf-8'))} |"
    return INDEX_ROW.sub(count, text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--edition", help="also set the manifest edition, e.g. 2026-11-25-v33")
    parser.add_argument("--check", action="store_true", help="report staleness without writing")
    args = parser.parse_args(argv)

    manifest = json.loads(MANIFEST.read_bytes().decode("utf-8"))
    stale, missing = [], []
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            missing.append(entry["path"])
            continue
        size, sha = digest(path)
        if entry.get("bytes") != size or entry.get("sha256") != sha:
            stale.append(entry["path"])
            entry["bytes"], entry["sha256"] = size, sha
    if args.edition:
        manifest["edition"] = args.edition

    index_text = INDEX.read_bytes().decode("utf-8")
    new_index = refreshed_index(index_text)
    index_stale = new_index != index_text

    listed = {entry["path"] for entry in manifest["files"]}
    unlisted = []
    tracked = tracked_files()
    if tracked is not None:
        unlisted = sorted(name for name in tracked
                          if name not in listed and name not in NOT_SHIPPED_FILES and (ROOT / name).is_file()
                          and not name.startswith(NOT_SHIPPED_PREFIXES) and not name.startswith("."))

    report = {"stale_hashes": stale, "missing_files": missing, "unlisted_tracked_files": unlisted,
              "index_counts_stale": index_stale}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.check:
        return 1 if (stale or missing or unlisted or index_stale) else 0
    if index_stale:
        INDEX.write_bytes(new_index.encode("utf-8"))
        # The index is itself listed in the manifest; hash it after rewriting.
        for entry in manifest["files"]:
            if (ROOT / entry["path"]).resolve() == INDEX.resolve():
                entry["bytes"], entry["sha256"] = digest(INDEX)
    MANIFEST.write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return 1 if (missing or unlisted) else 0


if __name__ == "__main__":
    sys.exit(main())
