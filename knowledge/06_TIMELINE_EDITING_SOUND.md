# 06 Timeline Editing Sound

priority: high
scope: 时间轴、切镜、转场、音频控制、声音叙事、Seedance 15 秒压缩

## 使用边界

本文件只提供静默时间轴和声音决策。最终用户可见输出必须用中文栏目：`【基础风格】`、`【角色与场景锁定】`、`【运镜与时间轴】`、`【声音设计】`、`【画面限制】`。不要输出 `hard cut block`、`Seedance packed prompt`、`Prompt:` 等英文模板标题。

## 时间轴整合规则

默认把以下内容合并到 `【运镜与时间轴】`：

- 画面结构与构图。
- 焦点路径。
- 运镜。
- 动作部位和路线。
- 台词、旁白、内心OS、画外音的具体出现时间、说话者、声音来源、嘴型状态。
- marker / beat。
- 声音 cue。
- 切镜理由。
- 结尾状态。

不要在同一个提示词里把这些拆成互不影响的栏目，因为它们都受时间变化影响。

## 台词 / 旁白时间轴绑定规则

台词不是独立文案清单，而是镜头事件。默认不要输出独立的 `【台词】`、`【台词/旁白】` 栏目，除非用户明确要求只整理台词表。

每一句台词、旁白、内心OS、画外音都必须写进 `【运镜与时间轴】` 的对应时间段，并至少包含：

- 时间范围：这句话从哪一秒开始，到哪一秒结束。
- 说话者：角色名、旁白、画外人声、内心OS。
- 具体内容：保留用户原台词，不擅自改写。
- 声音来源：画内说话、画外旁白、内心OS、广播/电话/录音。
- 嘴型状态：画内台词写“嘴唇轻微开合 / lip-sync”；旁白、画外音和内心OS写“嘴不动 / no lip-sync”。
- 画面承载：说话时镜头看脸、看手、看物件、看反应者，还是看空间。

稳定句式：

```text
4-7s，中近景保持在老人 screen-right 的弯腰背影，焦点从他手里的稻穗转到 background center 的收割机尾部。旁白在画外说：“他没有意识到，自己已经走进盲区。”这是 non-diegetic narration，老人嘴不动；机器轰鸣压过倒车提示音。
```

```text
8-11s，驾驶员老张在驾驶室内 screen-left 回头看后视镜，嘴唇轻微开合，说：“后面没人吧？”这是画内台词，有 lip-sync；焦点随后 rack focus 到后窗外被稻秆遮挡的盲区。
```

## Seedance 生成段落拼接规则

分镜是导演思考单位，Seedance 段落是模型生成单位。输出时不要默认一镜一段。

拼接优先级：

- 同一个空间内发生的连续事件，优先放进同一段。
- 同一个人物连续说话、观察、反应或行动，优先放进同一段。
- 一段连续动作从准备、推进、阻力、结果到反应，优先放进同一段。
- 声音桥、动作匹配、目光匹配、焦点转移可以作为段内 internal beats，不必单独拆段。
- 默认段长 5-15 秒，能稳定读懂时尽量拼到 12-15 秒。
- 低于 5 秒视为过碎，只有强边界才能低于 5 秒。

提前分段边界：

- 切场景/地点。
- 切景别或机位变化大到模型在同段内难以保持空间连续。
- 切主要人物、切说话者、切 POV 所属。
- 切时间状态，如回忆、梦境、闪回、隔天。
- 一段动作链已经完成，下一段动作目标发生变化。
- 需要重新建立危险线、空间轴线或群众路线。

## 上下段落边界规则

每个独立 Seedance 段落都必须能单独生成，但上下段不应该像同一镜头硬拆。上一段最后一拍和下一段第一拍要有明确差异：

- 避免同一人物 + 同一景别 + 同一构图连续出现在两个段落边界。
- 下一段开头至少改变一项：景别、机位、主体、动作状态、空间尺度、信息焦点、声音状态。
- 不要为了衔接段落而强行使用遮罩、foreground occlusion、fabric wipe、黑闪或白闪。只有当画面里真实人物、车辆、布料、柱子、稻秆等自然经过镜头，并且对剧情有用时才写遮挡转场。
- 段落衔接优先靠“上一段 ending state + 下一段 opening re-anchor”，而不是靠转场特效。
- 仍然优先在 5-15 秒内完整叙述同空间、同人物、同动作链；不要为了制造开尾差异而把可连续理解的动作拆碎。

稳定写法：

```text
第01段最后：12-15s, MS holds on the old man frozen in midground, background harvester still approaching, engine rumble dominates.
第02段开头：0-2s, WS from a higher field-side angle re-establishes the whole danger triangle: old man now small in screen-right midground, harvester rear fills background center, blurred field workers remain visible near screen-left ridge.
```

## 镜头时长选择

| 时长 | 适合功能 | 注意 |
| --- | --- | --- |
| 0.5-1s | 打斗、追逐、闪回、惊吓、快速信息 | 只放一个清楚动作或反应 |
| 1-2s | 日常对话、连续动作分解、关键展示 | 最稳定的短节奏 |
| 2-3s | 多人同框、人物姿态、场景转场、次要情节推进 | 可含一个焦点转移 |
| 3-5s | 情绪渲染、氛围营造、重要场景、尺度揭示 | 必须有内部变化 |
| 5-8s | 独白、一镜到底、沉浸体验、情绪爆发 | 每 2-3 秒加 marker |
| 8-15s | 复杂长镜头、救援/追逐、转变、场景完整动作链 | 用 3-6 个 internal beats |

Seedance 15 秒常用：

```text
0-2s establish / lock space
2-5s pressure or action begins
5-9s conflict / reveal / reversal
9-12s climax / consequence
12-15s ending state / hold / transition cue
```

## 切镜理由

每次切镜必须回答至少一个理由：

- 信息变化：观众需要看到新信息。
- 情绪变化：角色心理状态改变。
- 视角变化：从客观转主观，或从主角转旁观者。
- 冲突升级：危险距离缩短、力量关系变化。
- 尺度揭示：从局部到整体，或从人到巨物。
- 动作结果确认：冲击后需要看到后果。

没有理由的切镜会降低 Seedance 稳定性。

## 硬切与长镜头

如果用户要求 one continuous shot：

```text
one continuous shot, no hard cut, no jump cut, no montage, no black flash, no hidden transition.
```

如果需要强边界切分，例如切场景/地点、切景别或机位变化大到影响模型理解、切主要人物/说话者、切时间状态、或一段动作链结束：

```text
Split into separate 5-15s Seedance prompt blocks. Each block repeats character, scene, direction, lighting and ending state.
```

同一条 Seedance 提示词内可以有 internal beats。近景、反应、焦点转移、声音桥、同动作链里的简单 cut marker 可以留在同段内；不要塞入多个互相冲突的地点、人物焦点或动作链。

## 转场库

| 转场 | 用途 | 稳定写法 |
| --- | --- | --- |
| hard cut | 信息或冲突明确改变 | `hard cut because the viewer must see the blind spot from a new angle` |
| smash cut | 突然反差、惊吓、结果 | `smash cut from quiet hand movement to loud machine rear` |
| match cut | 形状/动作连续 | `match cut from circular wheel to round harvest sun` |
| match on action | 动作连续剪辑 | `cut on the lever pull, next shot continues the same hand motion` |
| reaction cut | 后果确认 | `reaction cut to worker's frozen face` |
| J-cut | 声音先于画面 | `reverse beep begins before the harvester appears` |
| L-cut | 声音延续到下镜 | `machine rumble continues over the silent reaction shot` |
| white flash | 爆炸、记忆、强光 | `brief white flash from welding spark, then new shot` |
| black flash | 眩晕、断片 | `one-frame black flash after impact, then muffled sound` |
| foreground occlusion | 隐藏切换、路过遮挡 | `rice stalks wipe across foreground and reveal the machine rear` |
| fabric wipe | 人群、衣物、转场 | `worker's jacket crosses lens as natural wipe` |
| sound bridge | 场景连接 | `same low-frequency rumble bridges field to hospital corridor` |
| psychic echo cut | 创伤、预感、记忆 | `cut on identical hand gesture, sound becomes distant` |
| montage cutting | 时间压缩 | `short montage of tools, faces, dust, warning sign` |
| slow-motion insert | 关键接触点 | `slow-motion insert on rice bundle falling from hand` |
| speed ramp | 动作高潮 | `normal speed -> slow at contact -> fast debris burst` |

转场限制：foreground occlusion、fabric wipe、black flash、white flash 只能用于段内或剧情强动机的切点，不作为每个 15 秒段落之间的默认连接方式。

## 声音设计库

声音要承担叙事，不只是气氛。

| 声音层 | 示例 | 用途 |
| --- | --- | --- |
| 环境声 | wind hum, insects, room tone, field ambience | 建立空间 |
| 动作声 | cloth rustle, footstep in mud, hand grip squeak | 确认动作 |
| 生理声 | shallow breath, heartbeat, swallow | 主观压力 |
| 怪物声 | deep whale-like moan, chittering scuttle | 非人威胁 |
| 机械声 | engine rumble, hydraulic hiss, reverse beep | 危险来源 |
| 魔法/能量声 | energy burst, sub-bass pulse | 超自然例外 |
| UI 声 | electronic bling, timer tick | 游戏/产品/界面 |
| 低频灾难声 | low-frequency rumble, distant impact | 巨物/灾难 |
| 空间回声 | corridor reverb, cave slapback | 空间大小 |
| 静默 | sudden silence, sound drops out | 冲击、失语 |
| 真空坠落 | muffled air, no impact until cut | 超现实或主观 |
| 声音先行 | off-screen warning, reverse beep | 提前制造信息 |
| 戛然而止 | music cuts dead, engine stops | 后果确认 |

## 音频卡点规则

音频可控制：

- beat grid：时间点。
- motion accents：动作重音。
- impact timing：撞击/接触点。
- cut markers：切点。
- camera-speed feel：运镜速度感。

音频不能自动控制：

- 角色身份。
- 场景地点。
- 服装道具。
- 台词内容。
- 剧情因果。

只用 3-6 个主要 marker，不要逐帧卡点。剧情可读性优先于音乐卡点。

## 提示词时间轴句式

```text
0-2s, establish the danger geometry: fixed metal pipe in screen-left foreground, tractor handlebar in midground right, driver turned backward but still seated. Camera locked-off at shoulder height, 35mm lens, focus holds on the narrowing gap. Engine rumble masks all small sounds.

2-5s, slow dolly in toward the gap; focus racks from driver's eyes to the pipe-handlebar alignment. His right hand keeps pulling the reverse lever, left shoulder twists, rear wheel moves only half a meter. A short metallic scrape becomes the main sound cue.

5-7s, reaction cut reason: information changes from machine movement to human consequence. Workers in background freeze, sound drops to low-frequency rumble and breathless silence, ending state holds on the stopped machine and fixed pipe with no graphic injury.
```
