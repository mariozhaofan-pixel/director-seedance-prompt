#!/usr/bin/env python3
"""Shared mechanical checks for one Seedance prompt; semantic quality is not certified."""

from __future__ import annotations

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


SECTIONS = [
    "【角色/场景/素材锁定】",
    "【基础风格】",
    "【运镜与时间轴】",
    "【声音设计】",
    "【画面限制】",
]

SEGMENT_CONTRACT_LABELS = [
    "前提",
    "核心关系",
    "导演意图",
    "演员指令",
    "对白规则",
]

DIRECTOR_INTENT_META_RE = re.compile(
    r"用户(?:要求|希望|提供)|根据用户|原片|原视频|"
    r"参考(?:图|图片|视频|音频|素材)(?:用途|要求)?|"
    r"上一(?:版|段|次)|剧本(?:要求|说明)|提示词|冷审|"
    r"Seedance|视频模型|生成模型|模型(?:理解|执行)|"
    r"制作(?:流程|说明)|复刻(?:原片|参考)|还原(?:原片|参考)",
    re.IGNORECASE,
)

RANGE_RE = r"（[ \t]*(\d+(?:\.\d+)?)[ \t]*[-–—][ \t]*(\d+(?:\.\d+)?)[ \t]*秒[ \t]*）"
CUT_RE = re.compile(rf"(?m)^[ \t]*CUT[ \t]+(\d+)[ \t]*{RANGE_RE}", re.IGNORECASE)
BEAT_RE = re.compile(rf"(?m)^[ \t]*BEAT[ \t]+([A-Z0-9]+)[ \t]*{RANGE_RE}", re.IGNORECASE)
CUT_LABEL_RE = re.compile(r"(?m)^[ \t]*CUT[ \t]+(\d+)\b", re.IGNORECASE)
BEAT_LABEL_RE = re.compile(r"(?m)^[ \t]*BEAT[ \t]+([A-Z0-9]+)\b", re.IGNORECASE)
TITLE_RE = re.compile(r"(?m)^###\s*第\d+段[^\n]*?(\d+(?:\.\d+)?)\s*秒")
SEGMENT_HEADING_RE = re.compile(r"(?m)^[ \t]*###[ \t]*第[ \t]*\d+[ \t]*段[^\r\n]*")
SECTION_RE = re.compile(r"(?m)^[ \t]*(【[^】\r\n]+】)[ \t]*\r?$")
TITLE_DURATION_RE = re.compile(
    r"(?<![\d.+\-–—~～至])(\d+(?:\.\d+)?)[ \t]*(?:秒[ \t]*)?"
    r"(?:[-–—~～至][ \t]*(\d+(?:\.\d+)?)[ \t]*)?秒"
)
DECIMAL_SECOND_RE = re.compile(r"(?<!\d)\d+\.\d+\s*秒")
FRAME_RE = re.compile(
    r"(?<![A-Za-z])Frame[ \t]+([+-]?\d+(?:\.\d+)?)(?:\s*帧)?(?=\s|[：:，,。；;）)]|$)",
    re.IGNORECASE,
)
REFERENCE_HANDLE_RE = re.compile(r"@[^\s，。；：、）】]+")
VISIBLE_TIMESTAMP_RE = re.compile(
    r"(?<!\d)(?:\d+(?:\.\d+)?\s*[-–—]\s*\d+(?:\.\d+)?\s*秒|"
    r"第\s*\d+(?:\.\d+)?\s*秒|\d+(?:\.\d+)?\s*秒后)"
)
CANDIDATE_SECTION_RE = re.compile(
    r"(?m)^##[ \t]+候选提示词[ \t]*(?=\r?$)"
)
H2_SECTION_RE = re.compile(r"(?m)^##[ \t]+[^#\r\n][^\r\n]*(?=\r?$)")
LINE_BREAK_RE = re.compile(r"\r\n|\n|\r")
AUDIT_SEPARATOR_RE = re.compile(r"(?:(?:\r\n)|\n|\r){2}")

TIMESTAMP_POLICIES = (
    "integer-preferred",
    "decimal-allowed",
    "integer-required",
)

TOOL_WRAPPER_PATTERNS = [
    (re.compile(r"\bExit[ \t]+code\b", re.IGNORECASE), "Exit code"),
    (re.compile(r"\bProcess[ \t]+exited\b", re.IGNORECASE), "Process exited"),
    (re.compile(r"\bOutput[ \t]*[:：]", re.IGNORECASE), "Output:"),
    (re.compile(r"\btool[ \t]+output\b", re.IGNORECASE), "tool output"),
    (re.compile(r"\btool[_ \t]+call\b", re.IGNORECASE), "tool call"),
    (re.compile(r"(?im)^\s*Command[ \t]*[:：]"), "Command:"),
]

FORBIDDEN_VISIBLE = [
    (re.compile(r"https?://", re.IGNORECASE), "visible URL"),
    (re.compile(r"\[[^\]\n]+\]\(https?://", re.IGNORECASE), "visible Markdown source link"),
    (re.compile(r"(?im)^\s*(研究增量|研究来源|来源链接|交接核验|核验结果|审阅结果)\s*[:：]"), "visible research/review appendix"),
    (re.compile(r"(?im)^\s*(VERDICT|BLOCKING_FINDINGS|OPTIONAL_FINDINGS|PROTECTED_FACTS)\s*:"), "visible cold-review record"),
    (re.compile(r"PROJECT_RULES\.md", re.IGNORECASE), "visible internal review artifact"),
    (
        re.compile(
            r"(?:画面|生成)?参考输入(?:仅使用下列|仅限以上|仅限下列)|"
            r"(?:后期[^\r\n。]*授权\s*BGM\s*母带|授权\s*BGM\s*母带[^\r\n。]*(?:后期|时码挂接))|"
            r"(?:本段)?独立冷启动|不依赖其他段落|未列出的素材|"
            r"项目窗口内分析证据|不作为(?:视频)?生成(?:参考)?输入|"
            r"(?:其余|全部环境|[\w\u4e00-\u9fff、，/]+和全部环境)(?:均|全部)?由文字(?:生成|建立)",
            re.IGNORECASE,
        ),
        "visible internal production/material-management metadata",
    ),
    (re.compile(r"(?im)^\s*(PASS|REPAIR)\s*$"), "visible validation verdict"),
]


# Advisory lint: wordings video models tend to misread. Each warning names its rewrite; the rule text lives in
# the owning knowledge module. IDs (M1, M2, ...) are stable check names. Warnings never change the verdict.
WORLD_DIRECTION_RE = re.compile(
    r"(?<![东西南北])[东南西北](?:边|侧|面|方|向|头|端)(?!西)|"
    r"[朝往向][东南西北](?![西方面边])|"
    r"\bworld[-_ ]?(?:left|right|north|south|east|west)\b|"
    r"\b(?:north|south|east|west)(?:ward)?\b",
    re.IGNORECASE,
)
STATIC_STATE_RE = re.compile(r"悬在|停在半空|停在空中|举着不动|一动不动|纹丝不动|完全静止|静止不动|定格在")
REFERENCE_PASTE_RE = re.compile(
    r"构图[^，。；\n]{0,8}(?:图片?\s*\d+|参考图?)[^，。；\n]{0,6}一致|照搬参考|和参考图一样"
)
VOICEOVER_LINE_RE = re.compile(r"(?m)^.*画外音.*$")
IMAGE_HANDLE_RE = re.compile(r"@图片(\d+)")


def lint_warnings(text: str, sections: dict[str, str], project_rules: list[dict] | None = None) -> list[str]:
    """Return advisory warnings for wordings that video models are known to misread."""
    warnings: list[str] = []
    timeline = sections.get(SECTIONS[2], "")
    lock = sections.get(SECTIONS[0], "")
    restrictions = sections.get(SECTIONS[4], "")
    spatial_text = "\n".join((lock, timeline))
    hits = sorted({m.group(0) for m in WORLD_DIRECTION_RE.finditer(spatial_text)})
    if hits:
        warnings.append("lint M1 world-direction words in prompt (translate to screen left/right, depth, camera side): "
                        + "、".join(hits[:8]))
    hits = sorted({m.group(0) for m in STATIC_STATE_RE.finditer(spatial_text)})
    if hits:
        warnings.append("lint M2 static-state wording (models freeze it; write an ongoing action that stops only when blocked/caught/missed): "
                        + "、".join(hits[:8]))
    if REFERENCE_PASTE_RE.search(text):
        warnings.append("lint M3 composition copied from a reference image (reads as a pasted still)")
    for line in VOICEOVER_LINE_RE.findall(timeline):
        if "口型" not in line and "内心OS" not in line and "嘴唇闭合" not in line:
            warnings.append("lint M4 画外音 without lip-sync note (add 人物嘴唇闭合, or write inner monologue as 角色：“（……）”)")
            break
    if restrictions and "字幕" not in restrictions:
        warnings.append("lint M11 restrictions lack a no-subtitle hygiene sentence")
    numbers = sorted({int(n) for n in IMAGE_HANDLE_RE.findall(lock)})
    if numbers and numbers != list(range(1, numbers[-1] + 1)):
        warnings.append(f"lint @图片 numbering is not contiguous: {numbers}")
    warnings.extend(extended_lint_warnings(sections))
    warnings.extend(eye_color_warnings(text))
    warnings.extend(pov_eye_mask_warnings(text))
    warnings.extend(empty_quality_warnings(text))
    warnings.extend(crew_warnings(text))
    warnings.extend(long_lens_warnings(sections))
    warnings.extend(vehicle_warnings(sections))
    for rule in project_rules or []:
        scope_text = timeline if rule.get("scope", "timeline") == "timeline" else text
        if re.search(rule["pattern"], scope_text):
            warnings.append(f"project lint {rule.get('id', 'rule')}: {rule.get('message', rule['pattern'])}")
    return warnings


ARRAY_GROWTH_RE = re.compile(r"一层比一层|一排比一排|一个比一个多|越来越多|无数|成千上万|铺天盖地")
POV_RISK_RE = re.compile(r"从画面下(?:边|缘|方)伸|画面下方伸出|镜头(?:升|降|移)到[^，。；\n]{0,8}正上方")
SENSITIVE_RE = re.compile(r"鲜血|血泊|血流|流血|血迹|满身血|一滩血")
LOCK_NAME_RE = re.compile(r"(?m)^(?:@[^｜\n]+｜)?([^：:｜\s@]{1,8})[：:]")
CUT_LINE_RE = re.compile(r"(?m)^[ \t]*CUT[ \t]+(\d+)\b.*$")
PRONOUN_RE = re.compile(r"(?<![其吉])[他她]")
NEGATED_ITEM_RE = re.compile(r"(?:不出现|不要出现|没有|不要)([^，。；\n]{2,40})")
NEGATION_PREFIX = ("不", "没", "无", "未", "别")
GENERIC_LOCK_LABELS = {"开场状态", "前提", "核心关系", "导演意图", "演员指令", "对白规则", "声音", "状态"}


def extended_lint_warnings(sections: dict[str, str]) -> list[str]:
    """Advisory checks M17–M23."""
    warnings: list[str] = []
    timeline = sections.get(SECTIONS[2], "")
    lock = sections.get(SECTIONS[0], "")
    restrictions = sections.get(SECTIONS[4], "")
    full = "\n".join(sections.values())
    hits = sorted({m.group(0) for m in ARRAY_GROWTH_RE.finditer(timeline)})
    if hits:
        warnings.append("lint M18 open-ended crowd/array wording (count the exact number instead): " + "、".join(hits))
    if POV_RISK_RE.search(timeline):
        warnings.append("lint M17 point-of-view risk phrasing (give owner to hands and directions)")
    hits = sorted({m.group(0) for m in SENSITIVE_RE.finditer(full)})
    if hits:
        warnings.append("lint M19 moderation-sensitive wording (use neutral observable wording such as 红色液体): "
                        + "、".join(hits))
    names = {name for name in LOCK_NAME_RE.findall(lock) if name not in GENERIC_LOCK_LABELS and len(name) >= 2}
    flagged = []
    for match in CUT_LINE_RE.finditer(timeline):
        line = match.group(0)
        present = [name for name in names if name in line]
        if len(present) >= 2 and PRONOUN_RE.search(line):
            flagged.append(match.group(1))
    if flagged:
        warnings.append("lint M22 他/她 in CUTs with two or more named characters (use names): CUT "
                        + "、".join(flagged))
    conflicts = set()
    for match in NEGATED_ITEM_RE.finditer(restrictions):
        for item in re.split(r"[、和与及]", match.group(1)):
            item = item.strip().removeprefix("任何")
            if not 3 <= len(item) <= 8:
                continue
            for found in re.finditer(re.escape(item), timeline):
                before = timeline[max(0, found.start() - 3):found.start()]
                if not any(token in before for token in NEGATION_PREFIX):
                    conflicts.add(item)
                    break
    if conflicts:
        warnings.append("lint M23 restriction negates words that the timeline writes positively: "
                        + "、".join(sorted(conflicts)))
    return warnings

EYE_COLOR_RE = re.compile(
    r"(?:紫|红|蓝|绿|金|琥珀|灰白|黄|棕|褐|银|青)色?的?(?:眼睛|眼眸|眼|瞳孔|瞳仁|虹膜)|"
    r"(?:眼睛|眼眸|瞳孔|虹膜)(?:是|呈|为)?[^，。；\n]{0,4}(?:紫|红|蓝|绿|金|琥珀|黄|棕|褐|银|青)色"
)
EYE_SAFE_RE = re.compile(r"不发光|眼神光|有[^，。；\n]{0,3}瞳")
SENTENCE_SPLIT_RE = re.compile(r"[。；\n]")


def eye_color_warnings(text: str) -> list[str]:
    """M24: eye colour without a no-glow / pupil anchor tends to render as self-luminous eyes."""
    hits = []
    for sentence in SENTENCE_SPLIT_RE.split(text):
        found = EYE_COLOR_RE.search(sentence)
        if found and not EYE_SAFE_RE.search(sentence):
            hits.append(found.group(0))
    if not hits:
        return []
    return ["lint M24 eye colour without 有瞳孔/不发光 (eyes may render self-luminous): "
            + "、".join(sorted(set(hits)))]

POV_EYE_MASK_RE = re.compile(r"真实眼睛视角|眼睛视角|从眼睛(?:里|内部|中)?看出去|眼睛内部")


def pov_eye_mask_warnings(text: str) -> list[str]:
    """M28: describing a POV as seen from inside the eyes invites eyelid, lash or vignette masks."""
    hits = sorted({m.group(0) for m in POV_EYE_MASK_RE.finditer(text)})
    if not hits:
        return []
    return ["lint M28 point-of-view written as seen through the eyes (define by observer position, height "
            "and direction; clean rectangular frame): " + "、".join(hits)]

EMPTY_QUALITY_RE = re.compile(r"8K|杰作|大师级|超写实|细节拉满|奥斯卡级|电影感|高级感|氛围感|史诗感")


def empty_quality_warnings(text: str) -> list[str]:
    """M30: quality buzzwords describe nothing visible and push towards a generic polished look."""
    hits = sorted({m.group(0) for m in EMPTY_QUALITY_RE.finditer(text)})
    if not hits:
        return []
    return ["lint M30 empty quality words (replace with visible light, material, colour or action): "
            + "、".join(hits)]

CREW_RE = re.compile(
    r"摄影师|摄像师|拍摄者|摄制组|跟拍员|三脚架|稳定器|斯坦尼康|无人机|云台(?!山)|摄影车|摄像车|拍摄车|"
    r"吸盘(?:支架|架|固定|车)|摇臂车|高速摄影机|"
    # \b does not work next to Chinese characters, which count as word characters.
    r"(?i:(?<![a-z])(?:gimbal|camera car|dji)(?![a-z])|"
    r"(?<![a-z])ronin(?:[ -]?(?:4d|2|rs|s\d)|\s*(?=跟|拍|稳定|云台))|"
    r"(?<![a-z])phantom[ -]?(?:flex|veo|tmx|v\d|4k))"
)
CREW_NEGATION_RE = re.compile(
    r"(?:无|没有|不出现|不要出现)[^，。；\n]{0,6}?(?:摄影机|摄像机|相机|摄影师|摄像师|拍摄者|三脚架|稳定器)"
)
FOCAL_RE = re.compile(r"(\d{3,4})\s*(?:mm|毫米)", re.IGNORECASE)


def crew_warnings(text: str) -> list[str]:
    """M32: naming the crew or camera gear, even in a negative list, can put them in frame."""
    hits = sorted({m.group(0) for m in CREW_RE.finditer(text)}
                  | {m.group(0) for m in CREW_NEGATION_RE.finditer(text)})
    if not hits:
        return []
    return ["lint M32 crew or camera gear named in the prompt (describe framing changes instead; "
            "drop negative lists): " + "、".join(hits)]


def long_lens_warnings(sections: dict[str, str]) -> list[str]:
    """M33: CUTs at 200mm or longer must state the extreme shallow-focus result."""
    timeline = sections.get(SECTIONS[2], "")
    starts = list(CUT_LINE_RE.finditer(timeline))
    flagged = []
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(timeline)
        block = timeline[match.start():end]
        if any(int(n) >= 200 for n in FOCAL_RE.findall(block)) and "极浅景深" not in block:
            flagged.append(match.group(1))
    if not flagged:
        return []
    return ["lint M33 CUT at 200mm or longer without 超大光圈、极浅景深 (background only as unreadable "
            "out-of-focus colour blocks): CUT " + "、".join(flagged)]

CAR_SUBJECT_RE = re.compile(
    r"汽车|轿车|跑车|赛车|越野车|SUV|MPV|皮卡|卡车|货车|面包车|出租车|网约车|私家车|警车|敞篷车|轿跑|旅行车|房车|吉普|"
    r"车辆|车型|轮毂",
    re.IGNORECASE,
)
VEHICLE_CONTEXT_RE = re.compile(CAR_SUBJECT_RE.pattern + r"|车身|车头|车门|车窗|驾驶|副驾|方向盘", re.IGNORECASE)
CABIN_ACTION_RE = re.compile(r"驾驶座|驾驶位|驾驶者|司机|方向盘|开车|上车|坐进车|副驾")
DRIVE_SIDE_LOCK_RE = re.compile(r"左舵|右舵|左驾|右驾|驾驶座在|驾驶位在|方向盘在车[^，。；\n]{0,2}[左右]")
VEHICLE_SIDE_RE = re.compile(
    r"(?:车身|车辆|车子|(?<![行马火停])车)的?[左右](?:侧|边|面)|"
    r"[左右][前后](?:车门|门|车轮|轮|翼子板|大灯|尾灯|车窗)|"
    r"驾驶侧|副驾(?:驶)?侧"
)
SCREEN_PROJECTION_RE = re.compile(
    r"画面?[左右]|画面(?:中|深处)|screen[- ](?:left|right)|前景|后景|"
    r"(?:朝|正对|背对|背离|面向|对着)镜头",
    re.IGNORECASE,
)
NOSE_DIRECTION_RE = re.compile(r"车头(?:始终|一直|仍|保持)?(?:朝向?|指向)画面?([左右])")
VISIBLE_SIDE = r"驾驶侧|副驾(?:驶)?侧|车身[左右]侧"
VISIBLE_SIDE_RE = re.compile(
    rf"(?:camera|镜头)[^，。；\n]{{0,16}}?({VISIBLE_SIDE})|"
    rf"(?:拍到|看到|露出)[^，。；\n]{{0,8}}?({VISIBLE_SIDE})|"
    rf"({VISIBLE_SIDE})[^，。；\n]{{0,8}}?(?:正对|朝向|面向|对着)镜头",
    re.IGNORECASE,
)
INTERIOR_CAMERA_RE = re.compile(r"车内|座舱|驾驶舱|副驾座|仪表台|后座")
LEFT_DRIVE_RE = re.compile(r"左舵|左驾|(?:驾驶座|驾驶位|方向盘)在车身?左")
RIGHT_DRIVE_RE = re.compile(r"右舵|右驾|(?:驾驶座|驾驶位|方向盘)在车身?右")


def nose_side_warnings(lock: str, timeline: str) -> list[str]:
    """M36: from outside, the visible side of a car is the side its nose points to on screen."""
    if sum(1 for line in lock.splitlines() if CAR_SUBJECT_RE.search(line)) > 1:
        return []
    left, right = LEFT_DRIVE_RE.search(lock), RIGHT_DRIVE_RE.search(lock)
    drive = "左" if left and not right else "右" if right and not left else None
    starts = list(CUT_LINE_RE.finditer(timeline))
    flagged = []
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(timeline)
        block = timeline[match.start():end]
        noses = set(NOSE_DIRECTION_RE.findall(block))
        if len(noses) != 1:
            continue
        nose = noses.pop()
        for sentence in SENTENCE_SPLIT_RE.split(block):
            if INTERIOR_CAMERA_RE.search(sentence):
                continue
            for found in VISIBLE_SIDE_RE.finditer(sentence):
                word = next(group for group in found.groups() if group)
                if word.startswith("车身"):
                    side = word[2]
                elif drive is None:
                    continue
                elif word == "驾驶侧":
                    side = drive
                else:
                    side = "右" if drive == "左" else "左"
                if side != nose and match.group(1) not in flagged:
                    flagged.append(match.group(1))
    if not flagged:
        return []
    return ["lint M36 visible vehicle side contradicts the nose direction (from outside, nose screen-left shows "
            "the car's left side and nose screen-right its right side; a left-hand-drive car shows its driver "
            "side only with the nose screen-left): CUT " + "、".join(flagged)]


def vehicle_warnings(sections: dict[str, str]) -> list[str]:
    """M34/M35/M36: drive-side lock, screen projection and nose-to-side geometry for car subjects (05G)."""
    lock = sections.get(SECTIONS[0], "")
    timeline = sections.get(SECTIONS[2], "")
    warnings: list[str] = []
    if CAR_SUBJECT_RE.search(lock) and CABIN_ACTION_RE.search(timeline) and not DRIVE_SIDE_LOCK_RE.search(lock):
        warnings.append("lint M34 car with driver or cabin action but no 左舵/右舵 in the vehicle main line "
                        "(drive side may flip between CUTs)")
    if not VEHICLE_CONTEXT_RE.search(lock + timeline):
        return warnings
    hits = []
    for sentence in SENTENCE_SPLIT_RE.split(timeline):
        found = VEHICLE_SIDE_RE.search(sentence)
        if found and not SCREEN_PROJECTION_RE.search(sentence):
            hits.append(found.group(0))
    if hits:
        warnings.append("lint M35 vehicle-local side without a screen projection in the same sentence "
                        "(add 画左/画右, 朝镜头 or foreground/background): " + "、".join(sorted(set(hits))))
    warnings.extend(nose_side_warnings(lock, timeline))
    return warnings

# Speech rates from 06: Chinese about 5.5 audible characters/s; Japanese about 8 morae/s in dialogue.
SPEECH_RATES = {"zh": Decimal("5.5"), "ja": Decimal("8")}
SPEECH_MARGIN = Decimal("0.5")
# Only quotes introduced by a colon or a speech verb count as dialogue; quoted signs and labels do not.
QUOTED_SPEECH_RE = re.compile(
    r"(?:[：:]|(?:说|问|喊|叫|答|念|道|唱|嘀咕|低语|喃喃)[^“「『。；\n]{0,8}?)[“「『]([^”」』\n]+)[”」』]"
)
SMALL_KANA = set("ぁぃぅぇぉゃゅょゎァィゥェォャュョヮ")


def spoken_units(line: str, lang: str) -> int:
    """Rough audible units: Chinese characters, or Japanese morae with each kanji counted as 2."""
    latin = 2 * len(re.findall(r"[A-Za-z]+", line)) + len(re.findall(r"\d", line))
    if lang == "ja":
        kana = sum(1 for ch in line if ("ぁ" <= ch <= "ー") and ch not in SMALL_KANA and ch != "・")
        return kana + 2 * len(re.findall(r"[一-鿿]", line)) + latin
    return len(re.findall(r"[一-鿿]", line)) + latin


def speech_capacity_warnings(timeline: str, duration: Decimal, lang: str) -> list[str]:
    """M37: quoted dialogue that may not fit its CUT (timed) or the whole segment (untimed); estimate only."""
    rate = SPEECH_RATES[lang]
    labels = list(CUT_LABEL_RE.finditer(timeline))
    timed = {m.start(): (Decimal(m.group(2)), Decimal(m.group(3))) for m in CUT_RE.finditer(timeline)}
    warnings, total = [], Decimal(0)
    for index, label in enumerate(labels):
        end = labels[index + 1].start() if index + 1 < len(labels) else len(timeline)
        block = timeline[label.start():end]
        units = sum(spoken_units(line, lang) for line in QUOTED_SPEECH_RE.findall(block))
        need = Decimal(units) / rate
        total += need
        if units and label.start() in timed:
            start, stop = timed[label.start()]
            if stop - start < need + SPEECH_MARGIN:
                warnings.append(
                    f"lint M37 dialogue may not fit CUT {label.group(1)}: about {units} {lang} units at "
                    f"{format_decimal(rate)}/s need {need:.1f}s plus {format_decimal(SPEECH_MARGIN)}s, CUT is "
                    f"{format_decimal(stop - start)}s (rough estimate; pauses come on top)"
                )
    if total and not timed and duration < total + SPEECH_MARGIN:
        warnings.append(
            f"lint M37 dialogue may not fit the segment: about {total:.1f}s of {lang} speech plus "
            f"{format_decimal(SPEECH_MARGIN)}s in {format_decimal(duration)}s (rough estimate; pauses come on top)"
        )
    return warnings


def load_project_lint(path: str) -> list[dict]:
    """Load a project-layer lint file: {"rules": [{"id", "pattern", "message", "scope"}]}."""
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    rules = data.get("rules") if isinstance(data, dict) else None
    if not isinstance(rules, list):
        raise ValueError("project lint file must contain a 'rules' array")
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("pattern"), str):
            raise ValueError("each project lint rule needs a string 'pattern'")
        re.compile(rule["pattern"])
        if rule.get("scope", "timeline") not in ("timeline", "all"):
            raise ValueError("project lint scope must be 'timeline' or 'all'")
    return rules

def positive_decimal(value: str) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError(f"invalid decimal value: {value}") from exc
    if not parsed.is_finite() or parsed <= 0:
        raise argparse.ArgumentTypeError("value must be a finite number greater than 0")
    return parsed


def parse_args(
    argv: list[str] | None = None, *, default_profile: str = "general"
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="UTF-8 prompt file; omit to read stdin")
    parser.add_argument(
        "--duration",
        type=positive_decimal,
        required=True,
        help="expected exact seconds; decimal durations are supported",
    )
    parser.add_argument("--version", choices=("2.0", "2.5"), default="2.5")
    parser.add_argument("--profile", choices=("general", "combat"), default=default_profile)
    parser.add_argument(
        "--timeline", choices=("auto", "timed", "untimed"), default="auto",
        help="resolved display policy; auto means untimed except Seedance 2.5 combat",
    )
    parser.add_argument("--mode", choices=("auto", "cut", "onetake"), default="auto")
    parser.add_argument(
        "--timestamp-policy",
        choices=TIMESTAMP_POLICIES,
        default="integer-preferred",
        help="Seedance 2.5 timestamp granularity policy",
    )
    parser.add_argument(
        "--fps",
        type=positive_decimal,
        default=Decimal("24"),
        help="frame rate used to bound optional Frame T帧 events (default: 24)",
    )
    parser.add_argument(
        "--project-rules",
        metavar="PATH",
        help="PROJECT_RULES.md audit packet; requires --candidate",
    )
    parser.add_argument(
        "--candidate",
        metavar="PATH",
        help=(
            "exact candidate file for audit comparison; also used as the prompt "
            "input when positional input is omitted"
        ),
    )
    parser.add_argument(
        "--reference-handle-policy",
        choices=("any-section", "lock-only"),
        default="any-section",
        help=(
            "project-specific @handle policy; lock-only requires every handle "
            "to appear once and only in the first lock section"
        ),
    )
    parser.add_argument(
        "--project-lint",
        metavar="PATH",
        help="project-layer lint JSON (knowledge/02K_PROJECT_SLOT.md); matches are warnings",
    )
    parser.add_argument(
        "--speech-lang",
        choices=tuple(SPEECH_RATES),
        help="opt-in rough dialogue capacity check per CUT (zh 5.5 chars/s, ja about 8 morae/s); warnings only",
    )
    parser.add_argument("--max-chars", type=int, default=10000)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable result including unverified checks")
    args = parser.parse_args(argv)
    if args.max_chars <= 0:
        parser.error("--max-chars must be greater than 0")
    if bool(args.project_rules) != bool(args.candidate):
        parser.error("--project-rules and --candidate must be supplied together")
    return args


def read_exact_text(path: str) -> str:
    """Read UTF-8 without universal-newline translation; tolerate one leading BOM."""
    return Path(path).read_bytes().decode("utf-8-sig")


def read_text(path: str | None) -> str:
    if path:
        return read_exact_text(path)
    return sys.stdin.read()


def format_decimal(value: Decimal) -> str:
    return format(value, "f")


def is_integer_value(value: Decimal) -> bool:
    return value == value.to_integral_value()


def check_segment_contract(
    timeline: str,
    version: str,
    errors: list[str],
) -> None:
    """Require one ordered, non-empty 2.5 segment contract before the first CUT."""
    if version != "2.5":
        return

    first_cut = CUT_LABEL_RE.search(timeline)
    positions: list[int] = []
    for label in SEGMENT_CONTRACT_LABELS:
        pattern = re.compile(
            rf"(?m)^[ \t]*{re.escape(label)}[ \t]*[：:][ \t]*([^\r\n]*)\r?$"
        )
        matches = list(pattern.finditer(timeline))
        if len(matches) != 1:
            errors.append(
                f"Seedance 2.5 timeline contract label {label} occurs "
                f"{len(matches)} times, expected 1"
            )
            continue
        match = matches[0]
        if not match.group(1).strip():
            errors.append(f"Seedance 2.5 timeline contract label {label} must be non-empty")
        if first_cut and match.start() > first_cut.start():
            errors.append(
                f"Seedance 2.5 timeline contract label {label} must appear "
                "before the first CUT"
            )
        if label == "导演意图":
            contaminated = DIRECTOR_INTENT_META_RE.search(match.group(1))
            if contaminated:
                errors.append(
                    "Seedance 2.5 director intent must be the compiler-authored "
                    "dramatic interpretation, not user/source/workflow metadata; "
                    f"found {contaminated.group(0)}"
                )
        positions.append(match.start())

    if len(positions) == len(SEGMENT_CONTRACT_LABELS) and positions != sorted(positions):
        errors.append(
            "Seedance 2.5 timeline contract labels must be ordered: "
            + " / ".join(SEGMENT_CONTRACT_LABELS)
        )


def check_ranges(
    label: str,
    ranges: list[tuple[Decimal, Decimal]],
    duration: Decimal,
    errors: list[str],
) -> None:
    if not ranges:
        errors.append(f"no {label} time ranges found")
        return
    if ranges[0][0] != 0:
        errors.append(
            f"{label} timeline starts at {format_decimal(ranges[0][0])}, expected 0"
        )
    for index, (start, end) in enumerate(ranges):
        if end <= start:
            errors.append(
                f"{label} range {index + 1} is non-positive: "
                f"{format_decimal(start)}-{format_decimal(end)}"
            )
        if index:
            previous_start, previous_end = ranges[index - 1]
            if start < previous_start:
                errors.append(
                    f"{label} range {index + 1} is out of chronological order: "
                    f"{format_decimal(start)} follows {format_decimal(previous_start)}"
                )
            if start > previous_end:
                errors.append(
                    f"{label} gap between {format_decimal(previous_end)} "
                    f"and {format_decimal(start)}"
                )
            elif start < previous_end:
                errors.append(
                    f"{label} overlap between {format_decimal(previous_end)} "
                    f"and {format_decimal(start)}"
                )
    if ranges[-1][1] != duration:
        errors.append(
            f"{label} timeline ends at {format_decimal(ranges[-1][1])}, "
            f"expected {format_decimal(duration)}"
        )


def check_frame_events(
    timeline: str,
    duration: Decimal,
    fps: Decimal,
    errors: list[str],
) -> None:
    frame_boundary = duration * fps
    for match in FRAME_RE.finditer(timeline):
        frame = Decimal(match.group(1))
        if not is_integer_value(frame):
            errors.append(f"Frame {match.group(1)} must use a whole-frame index")
            continue
        if frame < 0:
            errors.append(f"Frame {format_decimal(frame)} must be nonnegative")
        elif frame > frame_boundary:
            errors.append(
                f"Frame {format_decimal(frame)} exceeds duration boundary "
                f"{format_decimal(frame_boundary)} frames at {format_decimal(fps)} fps"
            )


def check_reference_handles(text: str, policy: str, errors: list[str]) -> None:
    if policy != "lock-only":
        return
    headers = list(SECTION_RE.finditer(text))
    lock_headers = [match for match in headers if match.group(1) == SECTIONS[0]]
    if len(lock_headers) != 1:
        return
    lock_header = lock_headers[0]
    next_header = next((match for match in headers if match.start() > lock_header.start()), None)
    lock_end = next_header.start() if next_header else len(text)
    lock_text = text[lock_header.end():lock_end]
    later_text = text[:lock_header.start()] + text[lock_end:]
    lock_handles = REFERENCE_HANDLE_RE.findall(lock_text)
    later_handles = REFERENCE_HANDLE_RE.findall(later_text)
    if later_handles:
        errors.append(
            "reference-handle policy lock-only forbids @handles after the lock "
            f"section: {', '.join(sorted(set(later_handles)))}"
        )
    duplicates = sorted(
        handle
        for handle in set(lock_handles + later_handles)
        if (lock_handles + later_handles).count(handle) != 1
    )
    if duplicates:
        errors.append(
            "reference-handle policy lock-only requires each @handle exactly once: "
            + ", ".join(duplicates)
        )


def check_audit_package(
    project_rules: str,
    candidate: str,
    errors: list[str],
) -> None:
    for source_label, source_text in (
        ("PROJECT_RULES", project_rules),
        ("candidate", candidate),
    ):
        for pattern, wrapper_label in TOOL_WRAPPER_PATTERNS:
            if pattern.search(source_text):
                errors.append(
                    f"{source_label} contains forbidden tool wrapper token: {wrapper_label}"
                )

    candidate_headers = list(CANDIDATE_SECTION_RE.finditer(project_rules))
    if len(candidate_headers) != 1:
        errors.append(
            "PROJECT_RULES must contain exactly one '## 候选提示词' section; "
            f"found {len(candidate_headers)}"
        )
        return

    header = candidate_headers[0]
    header_break = LINE_BREAK_RE.match(project_rules, header.end())
    if not header_break:
        errors.append("PROJECT_RULES candidate section heading must end with a line break")
        return

    candidate_start = header_break.end()
    next_section = H2_SECTION_RE.search(project_rules, candidate_start)
    section_end = next_section.start() if next_section else len(project_rules)
    if not project_rules.startswith(candidate, candidate_start):
        errors.append(
            "PROJECT_RULES candidate EXACT_MATCH failed: embedded candidate differs "
            "from --candidate"
        )
        return

    separator = project_rules[candidate_start + len(candidate) : section_end]
    expected_separator = bool(next_section)
    separator_ok = (
        AUDIT_SEPARATOR_RE.fullmatch(separator) is not None
        if expected_separator
        else separator == ""
    )
    if not separator_ok:
        errors.append(
            "PROJECT_RULES candidate EXACT_MATCH failed: extra or missing characters "
            "at the candidate section boundary"
        )
    outside_candidate = (
        project_rules[:candidate_start]
        + project_rules[candidate_start + len(candidate) :]
    )
    if re.search(r"(?m)^###\s*第\d+段", outside_candidate):
        errors.append(
            "PROJECT_RULES contains a stale candidate-like segment heading outside "
            "the unique embedded candidate"
        )



def parse_sections(text: str, errors: list[str]) -> dict[str, str]:
    """Only standalone heading lines create sections; prose references do not."""
    headers = list(SECTION_RE.finditer(text))
    names = [match.group(1) for match in headers]
    for section in SECTIONS:
        count = names.count(section)
        if count != 1:
            errors.append(f"section {section} occurs {count} times, expected 1 standalone heading")
    if all(names.count(section) == 1 for section in SECTIONS):
        if [name for name in names if name in SECTIONS] != SECTIONS:
            errors.append("five sections are out of order")
    extras = [name for name in names if name not in SECTIONS]
    if extras:
        errors.append(f"unexpected visible section(s): {', '.join(extras)}")
    sections: dict[str, str] = {}
    for index, match in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        body = text[match.end():end]
        name = match.group(1)
        if name in SECTIONS and name not in sections:
            sections[name] = body
            if not body.strip():
                errors.append(f"section {name} must be non-empty")
    return sections


def check_title(
    text: str, duration: Decimal, duration_limit: Decimal, version: str,
    exact_required: bool, errors: list[str],
) -> None:
    heading = SEGMENT_HEADING_RE.match(text)
    if heading is None:
        return
    matches = list(TITLE_DURATION_RE.finditer(heading.group(0)))
    if len(matches) != 1:
        errors.append("segment heading must contain exactly one duration or duration range")
        return
    match = matches[0]
    low = Decimal(match.group(1))
    high = Decimal(match.group(2)) if match.group(2) is not None else low
    is_range = match.group(2) is not None
    if low <= 0 or high <= 0 or high < low:
        errors.append("title duration range must be positive and ordered")
    for endpoint in sorted({low, high}):
        if endpoint > duration_limit:
            errors.append(
                f"title duration {format_decimal(endpoint)} exceeds Seedance "
                f"{version} limit of {format_decimal(duration_limit)} seconds"
            )
    if is_range:
        if exact_required:
            errors.append("combat or timed prompts require an exact title duration, not a range")
        elif not low <= duration <= high:
            errors.append(f"expected duration {format_decimal(duration)} is outside title duration range")
    else:
        mismatch = low != duration if version == "2.5" else abs(low - duration) > Decimal("0.011")
        if mismatch:
            errors.append(f"title duration is {format_decimal(low)}, expected {format_decimal(duration)}")


def check_label_order(timeline: str, errors: list[str]) -> None:
    cut_matches = list(CUT_LABEL_RE.finditer(timeline))
    numbers = [int(match.group(1)) for match in cut_matches]
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append("CUT labels must be unique and sequential from CUT 1")
    # BEAT numbering may restart at each new CUT.
    for index, cut in enumerate(cut_matches):
        end = cut_matches[index + 1].start() if index + 1 < len(cut_matches) else len(timeline)
        labels = [value.upper() for value in BEAT_LABEL_RE.findall(timeline[cut.end():end])]
        if len(labels) != len(set(labels)):
            errors.append(f"BEAT labels must be unique within CUT {cut.group(1)}")
        if labels and all(label.isdigit() for label in labels):
            values = [int(label) for label in labels]
            if values != sorted(set(values)):
                errors.append(f"BEAT labels must be ordered within CUT {cut.group(1)}")
        elif labels and all(label.isalpha() for label in labels):
            values = [(len(label), label) for label in labels]
            if values != sorted(set(values)):
                errors.append(f"BEAT labels must be ordered within CUT {cut.group(1)}")
    if cut_matches and BEAT_LABEL_RE.search(timeline[:cut_matches[0].start()]):
        errors.append("BEAT labels must appear inside a CUT")


def validate_prompt(
    raw_text: str, *, duration: Decimal, version: str = "2.5",
    profile: str = "general", timeline: str = "auto", mode: str = "auto",
    timestamp_policy: str = "integer-preferred", fps: Decimal = Decimal("24"),
    max_chars: int = 10000, reference_handle_policy: str = "any-section",
    project_lint: list[dict] | None = None, speech_lang: str | None = None,
) -> dict[str, object]:
    """Validate one candidate without I/O. The caller supplies resolved policies.

    Untimed text cannot prove internal 0..T coverage; this remains explicitly
    unverified even when all visible mechanical checks pass.
    """
    text = raw_text.strip()
    errors: list[str] = []
    warnings: list[str] = []
    checked = ["single_segment", "five_sections", "character_limit", "title_duration",
               "version_duration_limit", "label_order", "visible_metadata"]
    not_verified = ["semantic_quality", "action_and_dialogue_duration_feasibility"]
    resolved_timeline = timeline
    if timeline == "auto":
        resolved_timeline = "timed" if version == "2.5" and profile == "combat" else "untimed"
    if version == "2.0" and resolved_timeline == "timed":
        errors.append("Seedance 2.0 does not support a timed timeline; use untimed CUT/BEAT")
    duration_limit = Decimal("15" if version == "2.0" else "30")
    if duration > duration_limit:
        errors.append(
            f"duration {format_decimal(duration)} exceeds Seedance "
            f"{version} limit of {format_decimal(duration_limit)} seconds"
        )
    if not duration.is_finite() or duration <= 0:
        errors.append("duration must be finite and positive")
    if not text:
        errors.append("prompt is empty")
    # Count the actual submitted text, including whitespace; the UTF-8 BOM is
    # removed by read_exact_text and is not part of a copied model prompt.
    if len(raw_text) > max_chars:
        errors.append(f"prompt has {len(raw_text)} characters, limit is {max_chars}")
    if SEGMENT_HEADING_RE.match(text) is None:
        errors.append("prompt-only envelope must start with a segment heading")
    segment_headings = SEGMENT_HEADING_RE.findall(text)
    if len(segment_headings) != 1:
        errors.append(
            "prompt-only cold-review candidate must contain exactly one "
            f"independent segment envelope; found {len(segment_headings)}"
        )
    sections = parse_sections(text, errors)
    check_reference_handles(text, reference_handle_policy, errors)
    if reference_handle_policy == "lock-only":
        checked.append("reference_handle_placement")
    for pattern, label in FORBIDDEN_VISIBLE:
        if pattern.search(text):
            errors.append(label)
    check_title(text, duration, duration_limit, version,
                profile == "combat" or resolved_timeline == "timed", errors)

    timeline_text = sections.get(SECTIONS[2], "")
    cut_matches = CUT_RE.findall(timeline_text)
    beat_matches = BEAT_RE.findall(timeline_text)
    cut_labels = CUT_LABEL_RE.findall(timeline_text)
    beat_labels = BEAT_LABEL_RE.findall(timeline_text)
    cuts = [(Decimal(start), Decimal(end)) for _, start, end in cut_matches]
    beats = [(Decimal(start), Decimal(end)) for _, start, end in beat_matches]
    check_label_order(timeline_text, errors)
    check_segment_contract(timeline_text, version, errors)
    if version == "2.5":
        checked.append("segment_contract")
    resolved_mode = mode
    if mode == "auto":
        resolved_mode = "onetake" if len(cut_labels) == 1 and (beat_labels or profile == "general") else "cut"
    if not cut_labels:
        errors.append("timeline requires at least one CUT label")

    frame_matches = list(FRAME_RE.finditer(timeline_text))
    if resolved_timeline == "untimed":
        checked.append("untimed_display_policy")
        not_verified.extend(["timeline_coverage_0_to_T", "timeline_gaps_and_overlaps", "frame_event_bounds"])
        if cut_matches or beat_matches or frame_matches or VISIBLE_TIMESTAMP_RE.search(timeline_text):
            errors.append(f"Seedance {version} timeline must use untimed CUT/BEAT labels and relative phases")
        if resolved_mode == "onetake":
            if len(cut_labels) != 1:
                errors.append(f"{version} one-take mode requires exactly 1 untimed CUT, found {len(cut_labels)}")
            if profile == "combat" and not beat_labels:
                errors.append(f"{version} one-take mode requires ordered untimed BEAT labels")
        elif profile == "combat" and len(cut_labels) < 2:
            errors.append(f"{version} multi-CUT mode requires at least 2 untimed CUTs, found {len(cut_labels)}")
    else:
        checked.extend(["timeline_coverage_0_to_T", "timeline_gaps_and_overlaps", "frame_event_bounds", "timestamp_granularity"])
        check_frame_events(timeline_text, duration, fps, errors)
        if len(cuts) != len(cut_labels):
            errors.append(
                "Seedance 2.5 requires a valid time range for every CUT; "
                f"found {len(cuts)} timed ranges for {len(cut_labels)} labels"
            )
        range_tokens = [token for match in (*cut_matches, *beat_matches) for token in match[1:]]
        uses_decimal_timestamps = (
            not is_integer_value(duration)
            or any("." in token for token in range_tokens)
            or bool(DECIMAL_SECOND_RE.search(timeline_text))
        )
        if uses_decimal_timestamps or frame_matches:
            if timestamp_policy == "integer-required":
                errors.append("Seedance 2.5 subsecond/frame timestamps violate resolved timestamp policy integer-required")
            elif timestamp_policy == "integer-preferred":
                warnings.append("Seedance 2.5 uses decimal-second or Frame timestamps under integer-preferred policy")
        if resolved_mode == "onetake":
            if len(beats) != len(beat_labels):
                errors.append(
                    "Seedance 2.5 one-take mode requires a valid time range for every BEAT; "
                    f"found {len(beats)} timed ranges for {len(beat_labels)} labels"
                )
            if len(cuts) != 1:
                errors.append(f"2.5 one-take mode requires exactly 1 timed CUT, found {len(cuts)}")
            if profile == "combat" or beat_labels:
                check_ranges("BEAT", beats, duration, errors)
                checked.append("onetake_beat_coverage")
        elif profile == "combat" and len(cuts) < 2:
            errors.append(f"2.5 multi-CUT mode requires at least 2 timed CUTs, found {len(cuts)}")
        check_ranges("CUT", cuts, duration, errors)
    warnings.extend(lint_warnings(text, sections, project_lint))
    checked.append("advisory_lint")
    if speech_lang:
        warnings.extend(speech_capacity_warnings(timeline_text, duration, speech_lang))
        checked.append("dialogue_capacity_estimate")
    if project_lint:
        checked.append("project_lint")
    return {
        "verdict": "FAIL" if errors else "PASS", "profile": profile,
        "version": version, "timeline": resolved_timeline, "mode": resolved_mode,
        "duration": format_decimal(duration), "characters": len(raw_text),
        "errors": errors, "warnings": warnings, "checked": checked,
        "not_verified": not_verified,
    }


def main(argv: list[str] | None = None, *, default_profile: str = "general") -> int:
    args = parse_args(argv, default_profile=default_profile)
    try:
        audit_candidate = read_exact_text(args.candidate) if args.candidate else None
        raw_text = read_exact_text(args.input) if args.input else (
            audit_candidate if audit_candidate is not None else read_text(None)
        )
        result = validate_prompt(
            raw_text, duration=args.duration, version=args.version, profile=args.profile,
            timeline=args.timeline, mode=args.mode, timestamp_policy=args.timestamp_policy,
            fps=args.fps, max_chars=args.max_chars, reference_handle_policy=args.reference_handle_policy,
            project_lint=load_project_lint(args.project_lint) if args.project_lint else None,
            speech_lang=args.speech_lang,
        )
        if args.project_rules:
            assert audit_candidate is not None
            check_audit_package(read_exact_text(args.project_rules), audit_candidate, result["errors"])
            if args.input and raw_text != audit_candidate:
                result["errors"].append(
                    "positional input differs from --candidate; audit and validation must use the same exact prompt"
                )
            result["checked"].append("audit_package_exact_match")
            result["verdict"] = "FAIL" if result["errors"] else "PASS"
    except (OSError, UnicodeError, ValueError, re.error) as exc:
        result = {"verdict": "FAIL", "errors": [str(exc)], "warnings": [],
                  "checked": [], "not_verified": ["input_unreadable"]}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for warning in result["warnings"]:
            print(f"WARNING: {warning}", file=sys.stderr)
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        if result["verdict"] == "PASS":
            print("PASS")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
