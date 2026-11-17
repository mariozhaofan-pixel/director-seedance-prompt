#!/usr/bin/env python3
"""Compatibility CLI/API for the Seedance combat profile.

All parsing and validation lives in validate_prompt.py. Existing commands and
seal_review_packet.py keep the combat defaults and text PASS/error protocol.
"""
from __future__ import annotations

import validate_prompt as _shared
from validate_prompt import *  # Re-export the established helper API.


def parse_args(argv: list[str] | None = None):
    return _shared.parse_args(argv, default_profile="combat")


def main(argv: list[str] | None = None) -> int:
    return _shared.main(argv, default_profile="combat")


if __name__ == "__main__":
    raise SystemExit(main())
