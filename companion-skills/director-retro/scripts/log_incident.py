#!/usr/bin/env python3
"""Append one incident card to a project-layer incident log (事故日志.md)."""

from __future__ import annotations

import argparse
import datetime as _dt
from pathlib import Path

LAYERS = ("skill缺规则", "skill有规则没执行", "模型能力限制", "平台限制", "项目偏好", "剧本问题", "待定")


def render(date: str, segment: str, quote: str, symptom: str, layer: str, fix: str, verified: str) -> str:
    return (f"\n## {date}｜{segment}\n"
            f"- 用户原话：{quote}\n"
            f"- 症状：{symptom}\n"
            f"- 根因层：{layer}\n"
            f"- 改法：{fix}\n"
            f"- 验证：{verified}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--segment", required=True, help="e.g. 第七集第08段 v1")
    parser.add_argument("--quote", required=True, help="the user's exact words")
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--layer", choices=LAYERS, default="待定")
    parser.add_argument("--fix", default="待定")
    parser.add_argument("--verified", default="待验证")
    parser.add_argument("--date", default=_dt.date.today().isoformat())
    args = parser.parse_args(argv)
    if not args.log.exists():
        args.log.parent.mkdir(parents=True, exist_ok=True)
        args.log.write_text("# 事故日志\n", encoding="utf-8")
    with args.log.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(render(args.date, args.segment, args.quote, args.symptom, args.layer, args.fix, args.verified))
    print(str(args.log))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
