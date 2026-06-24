# 07 Style Genre Famous Scene Compiler

priority: medium
scope: 用户说“感觉像某名场面”时的静默机制、类型场景语法、视觉冲击与反转

## 版权边界

可以学习机制，不能复制具体电影人物、台词、造型、场景和精确镜头顺序。输出时把“像某片”的感觉翻译为可迁移的视听结构。

## 名场面感觉编译器

| 用户感觉 | 可复用机制 | 提示词内核 |
| --- | --- | --- |
| 闪灵砸门式压迫 | 封闭空间、门作为薄弱边界、重复冲击、受害者反应 | `threshold horror: locked door dominates foreground, repeated impacts deform the barrier, reaction cut to trapped face` |
| 教父式权力压迫 | 低调光、静止构图、说话者不动、对方紧张 | `low-key interior power scene, seated figure remains still, practical lamp side-light, listener's hands reveal fear` |
| 黑客帝国子弹时间 | 时间冻结、轨迹可见、环绕视角 | `bullet-time freeze, debris and fabric suspended, camera arcs 180 degrees around the contact point` |
| 斯巴达 300 式图形动作 | 高反差剪影、slow-fast-slow、队形冲击 | `graphic combat silhouette, speed ramp from slow anticipation to fast strike to slow aftermath` |
| Mad Max 追逐 | 中心动作向量、车辆方向清楚、因果快切 | `center-framed chase vector, screen direction never flips, each cut confirms distance and damage` |
| Spielberg wonder | 先看反应，再揭示奇观 | `reaction first, warm backlight on face, then tilt up reveal to impossible scale` |
| Nolan scale dread | 小人物对巨物、低频、几何压迫 | `human figure small against massive structure, IMAX scale language, low-frequency pressure` |
| Kurosawa weather drama | 风雨/尘土塑造冲突方向 | `wind and rain show emotional force, fabric and dust move with conflict direction` |
| Wong Kar-wai longing | 近距离、慢速、遮挡、色彩记忆 | `close obstructed framing, slow lateral glide, saturated practical color, emotional delay` |
| Tarkovsky dream drift | 长镜头、自然元素、时间变慢 | `slow meditative tracking shot, water/fire/wind texture carries memory` |
| Fincher procedural tension | 精确构图、冷色、控制感 | `precise locked composition, cool practical light, subtle push-in on evidence` |
| Villeneuve monumental silence | 巨物、负空间、低频、少动作 | `vast negative space, restrained movement, sub-bass rumble, human scale overwhelmed` |
| John Woo standoff | 双方对称、道具指向、慢动作前奏 | `symmetrical standoff, weapons or hands aim across centerline, slow-motion fabric movement before action` |
| Bourne handheld panic | 近距离、读得清的手持、身体接触 | `handheld close combat, readable center subject, shoulder hits wall, quick reaction inserts` |
| Ghibli quiet magic | 日常细节、风、食物、温柔奇观 | `domestic texture, soft wind, small magical exception color, childlike wonder` |
| Pixar clarity | 动作姿态清晰、表情可读、因果强 | `clear pose silhouette, expressive eyes, one action idea per beat` |
| Anime impact frame | 极短定格、速度线、强轮廓 | `single impact pose, graphic speed streaks, sharp silhouette, then debris follow-through` |
| Disaster movie reveal | 正常生活被远处异常打断 | `ordinary foreground activity, background anomaly grows, sound arrives late` |
| Heist precision | 工具、时间、手势、静默 | `macro inserts of tools, synchronized hand signals, ticking sound bridge` |
| Psychological collapse | 空间变形、主观声音、焦点漂移 | `dolly zoom, muffled ambience, focus drifts from face to empty space` |

## 视觉反转机制

反转不是台词解释，而是画面信息顺序变化：

- 安全物变危险物：日常道具突然对齐成危险线。
- 背景变主体：background threat becomes focus.
- 主观误判：POV 看不见，客观镜头显示观众看见。
- 声音欺骗：听到安全提示，却被环境声盖住。
- 关系反转：保护者变阻挡者，逃生路线变封闭路线。
- 尺度反转：看似小问题，pull-back 后是巨大系统性危险。

提示词：

```text
visual reversal: the harmless rice stalks in foreground become the object that hides the blind-zone figure; focus racks through them only after the machine begins reversing.
```

## 蒙太奇与时间扭曲

| 技法 | 用途 | 写法 |
| --- | --- | --- |
| rhythmic montage | 训练、准备、调查、事故前奏 | `short montage of hands, tools, warning sign, machine vibration, each shot 0.5-1s` |
| intellectual montage | 概念对照 | `cut from locked gate to clenched hand to silent machine panel` |
| emotional montage | 情绪累积 | `faces, objects and empty spaces repeat with rising sound` |
| time compression | 压缩漫长过程 | `morning light shifts to noon through three match cuts` |
| slow-motion insert | 强调关键因果 | `slow-motion insert on the lever snapping backward` |
| speed ramp | 动作冲击 | `normal motion, sudden slow at contact, fast debris burst` |
| bullet time | 超现实冲击 | `time freezes around the impact point, camera orbits, dust suspended` |
| Hitchcock dolly zoom | 认知恐惧 | `dolly in while zooming out, background stretches away from the face` |

## 类型场景语法包

事故/安全警示：

```text
客观纪实质感，先建立危险几何关系，先让观众看到盲区，再发生接触，不渲染血腥，后果用停顿、静默和物体状态变化表达。
```

恐怖：

```text
低调动机光，先用画外声音引出危险，保留负空间，延迟揭示威胁，先给反应再给完整威胁。
```

动作：

```text
route, contact point, counter, reversal, impact, consequence; center action vector and keep screen direction stable.
```

产品/科普：

```text
clean locked-off composition, macro inserts, high-key lighting, readable material response, no narrative clutter.
```

漫画/动画：

```text
clear silhouette, pose-to-pose action, exaggerated timing, readable VFX, final held pose.
```

音乐卡点：

```text
use audio as beat grid, mark 3-6 motion accents, avoid sacrificing story readability for every beat.
```

神迹/灾难：

```text
IMAX scale language, tiny human foreground, huge background force, low-frequency rumble, slow reveal then sudden consequence.
```

悬疑调查：

```text
macro clue insert, controlled camera, cool practical light, J-cut from clue sound to investigator reaction.
```

情感文戏：

```text
Cooke-like soft lens warmth, restrained camera, face/action separated, silence or room tone carries hesitation.
```
