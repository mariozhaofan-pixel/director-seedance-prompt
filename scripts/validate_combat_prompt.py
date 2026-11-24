#!/usr/bin/env python3
"""Compatibility CLI for the Seedance combat profile.

All parsing and validation lives in validate_prompt.py; this entry only changes
the default profile to combat and keeps the text PASS/error protocol.
"""
from __future__ import annotations

import validate_prompt as _shared


def parse_args(argv: list[str] | None = None):
    return _shared.parse_args(argv, default_profile="combat")


def main(argv: list[str] | None = None) -> int:
    return _shared.main(argv, default_profile="combat")


if __name__ == "__main__":
    raise SystemExit(main())
