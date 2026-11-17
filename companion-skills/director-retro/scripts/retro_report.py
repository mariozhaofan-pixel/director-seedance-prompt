#!/usr/bin/env python3
"""Summarise a project-layer incident log by root-cause layer and list promotion candidates."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

CARD_RE = re.compile(r"(?m)^##\s+(?P<title>.+)$")
FIELD_RE = re.compile(r"(?m)^-\s*(?P<key>用户原话|症状|根因层|改法|验证)：(?P<value>.*)$")
SEPARATOR_CELL_RE = re.compile(r":?-{3,}:?")
DESTINATION = {
    "skill缺规则": "项目规则.md",
    "skill有规则没执行": "lint补充.json 或编译卡检查（不新增规则）",
    "模型能力限制": "项目规则.md（附规避写法）",
    "平台限制": "项目规则.md F 组",
    "项目偏好": "项目规则.md",
    "剧本问题": "交编剧，不写进导演层",
    "待定": "复盘时请用户判断",
}
# Hand-written logs add notes to the layer ("平台限制（内容审核）", "skill 有规则但没执行（02A …）").
LAYER_PATTERNS = (
    (re.compile(r"剧本"), "剧本问题"),
    (re.compile(r"没执行|未执行"), "skill有规则没执行"),
    (re.compile(r"缺规则"), "skill缺规则"),
    (re.compile(r"^平台"), "平台限制"),
    (re.compile(r"^模型"), "模型能力限制"),
    (re.compile(r"项目偏好"), "项目偏好"),
)
PENDING_RE = re.compile(r"^待|未验证")
VALID_RE = re.compile(r"^有效|已验证|验收")
INVALID_RE = re.compile(r"^无效|仍不|未通过|失败")


def layer_of(raw: str | None) -> str:
    text = re.sub(r"\s+", "", raw or "")
    if not text:
        return "待定"
    if text in DESTINATION:
        return text
    for pattern, layer in LAYER_PATTERNS:
        if pattern.search(text):
            return layer
    # Unknown layers keep their own name so similar rows still group together.
    return re.split(r"[（(：:＋+，,]", text, maxsplit=1)[0] or "待定"


def status_of(raw: str | None) -> str:
    text = (raw or "").strip()
    if PENDING_RE.search(text):
        return "待验证"
    if VALID_RE.search(text):
        return "有效"
    if INVALID_RE.search(text):
        return "无效"
    return "待验证"


def column_key(header: str) -> str | None:
    for key in ("用户原话", "症状", "根因层", "改法"):
        if key in header:
            return key
    if "验证" in header:
        return "验证"
    if "段号" in header:
        return "段号"
    if "日期" in header:
        return "日期"
    return None


def parse_tables(text: str) -> list[dict]:
    """Rows of any Markdown table whose header names 根因层 plus 症状 or 改法 (the 02K column layout)."""
    cards = []
    header: list[str | None] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            header = None
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if all(SEPARATOR_CELL_RE.fullmatch(cell) for cell in cells if cell):
            continue
        if header is None:
            keys = [column_key(cell) for cell in cells]
            if "根因层" in keys and ("症状" in keys or "改法" in keys):
                header = keys
            continue
        row = {key: value for key, value in zip(header, cells) if key}
        title = " ".join(row[key] for key in ("日期", "段号") if row.get(key)) or "（未写段号）"
        card = {"title": title}
        card.update({key: value for key, value in row.items() if key not in ("日期", "段号")})
        cards.append(card)
    return cards


def parse(text: str) -> list[dict]:
    cards = []
    matches = list(CARD_RE.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        fields = {m.group("key"): m.group("value").strip() for m in FIELD_RE.finditer(body)}
        if fields:  # a plain section heading in a table-format log is not a card
            cards.append({"title": match.group("title").strip(), **fields})
    return cards + parse_tables(text)


def report(cards: list[dict]) -> str:
    groups: dict[str, list[dict]] = defaultdict(list)
    for card in cards:
        groups[layer_of(card.get("根因层"))].append(card)
    lines = ["# 复盘汇总", "", f"共 {len(cards)} 条事故卡。", "", "| 根因层 | 条数 | 去处 |", "| --- | --- | --- |"]
    for layer, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"| {layer} | {len(items)} | {DESTINATION.get(layer, '复盘时请用户判断')} |")
    lines += ["", "## 提升候选（验证有效、且不是剧本问题）", ""]
    candidates = [c for c in cards
                  if status_of(c.get("验证")) == "有效" and layer_of(c.get("根因层")) != "剧本问题"]
    if not candidates:
        lines.append("- 暂无。验证栏为“有效”的事故卡才进入候选。")
    for card in candidates:
        layer = layer_of(card.get("根因层"))
        lines.append(f"- {card['title']}｜{layer}｜症状：{card.get('症状', '')}｜改法：{card.get('改法', '')}"
                     f" → 建议写入：{DESTINATION.get(layer, '复盘时请用户判断')}")
    pending = [c for c in cards if status_of(c.get("验证")) == "待验证"]
    if pending:
        lines += ["", "## 待验证", ""]
        lines += [f"- {c['title']}｜改法：{c.get('改法', '')}" for c in pending]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    text = report(parse(args.log.read_text(encoding="utf-8-sig")))
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(str(args.out))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
