# 08 Model QC Repair

priority: highest knowledge
scope: 模型适配、Seedance 稳定性门、故障修复、最终检查

## 输出修复优先级

如果回答变得冗长、英文化、像知识库摘要，优先按以下方式修复：

1. 删除显性分析、规则解释、测试用例和 Knowledge 索引内容。
2. 把英文标题改成中文标题：`第01段`、`【基础风格】`、`【角色与场景锁定】`、`【运镜与时间轴】`、`【声音设计】`、`【画面限制】`。
3. 只保留必要英文技术短语；其他全部改成中文。
4. 输出可复制提示词，不输出“我将如何做”的说明。

## 模型适配原则

只有 Seedance 的以下规则作为硬约束：

- 每段 <=15 秒。
- 每段 <=10000 字符。
- 每段默认目标 5-15 秒，优先拼到 12-15 秒；少于 5 秒只在强边界时使用。
- 每段独立完整。
- 每段重复关键锚点。
- 不要默认一镜一段；同空间、同主要人物/说话者、同一连续动作或同一段台词优先拼成同一段。
- 只在切场景/地点、切景别或机位变化大到影响模型理解、切主要人物/说话者、切时间状态、或一段动作链结束时拆段。

其他模型规则可能随产品更新变化。用户指定非 Seedance 模型时，按用户给出的当前规则优先；如果用户没有给规则，只做保守适配。

## 常见模型倾向

| 模型 | 保守使用方式 |
| --- | --- |
| Seedance | 短段、独立完整、画面结构清楚、动作因果清楚、关键锚点重复 |
| 可灵 / Kling | 适合清楚动作和视觉冲击；复杂多人要减少同时动作 |
| Veo | 适合自然语言长描述和电影化场景；仍需锁定空间和主体 |
| Runway | 适合参考图/视频驱动和短镜头；动作不要过密 |
| Pika | 适合短小效果、风格化、转场；复杂叙事要拆段 |
| Sora | 适合更完整场景理解；仍需避免过多同时主体和含糊空间 |
| Midjourney Video | 适合强视觉风格和从图延展；动作链要简化 |

## Seedance 稳定性门

输出前逐项检查：

1. 每段是否 <=15 秒、<=10000 字符，且默认保持 5-15 秒。
2. 每段是否独立完整，不依赖上一段记忆。
3. 是否在 `【基础风格】` 前置摄影/镜头、光线、色彩。
4. 是否重复角色、服装、场景、道具、空间方向和结尾状态。
5. 是否把 screen-left/right、foreground/midground/background 写进时间轴。
6. 是否每个 time beat 只有一个主运镜。
7. 是否固定物和移动物分开写。
8. 是否焦点路径清楚：focus starts on A -> racks/pulls to B -> holds on C。
9. 是否避免画外状态突变；离画后重入需要写清。
10. 是否避免同时追踪过多人物；多人场景写主方向、反方向、拥堵点。
11. 如果有群众、后景人物、围观者、路人、队伍、兽群或 background extras，是否在每段和每个 WS/EWS/全景 time beat 重复人群锚点，且没有让后景虚化人群无故消失。
12. 是否处理反射、镜子、玻璃、文字、UI、字幕风险。
13. 是否每次切镜都有 cut reason。
14. 是否避免一镜一段：同空间、同人物/说话者、同连续动作/台词是否已经拼接；只有强边界才拆成独立提示词块。
15. 上下独立段落边界是否有视觉差异：上一段最后一拍和下一段第一拍不是同一人物 + 同一景别 + 同一构图；没有强行使用遮罩/擦镜转场衔接段落。
16. 如果有参考素材，是否每个 @素材 都说明用途和维度锁定。
17. 如果有参考音频，是否区分 final BGM / silent beat guide / SFX guide / ambience bed / voice anchor。
18. silent beat guide 是否明确 do not output this reference audio as BGM。
19. voice anchor 是否只控制声音，不控制脸、服装、地点或台词。
20. 台词、旁白、内心OS、画外音是否全部绑定到 `【运镜与时间轴】` 的具体时间段，并写清说话者、内容、画内/画外、嘴型是否运动。
21. 事故、伤害、灾难类是否清楚因果，避免不必要血腥。

## 故障修复矩阵

| 问题 | 原因 | 修复 |
| --- | --- | --- |
| 角色漂移 | 每段未重复身份/服装锚点 | 每段加 face/costume/posture anchor |
| 分段过碎 | 把每个分镜都输出成独立提示词 | 把同空间、同人物、同动作链、同说话者的 beats 拼成 5-15 秒段落 |
| 场景漂移 | 没有固定空间结构 | 写 foreground/midground/background 和 fixed objects |
| 后景人群消失 | 只在第一镜写了群众，后续全景/反应镜头未重复 | 每段和每个 WS/EWS/全景 beat 重复 crowd density、位置层级、主方向、拥堵点；写 background crowd remains softly blurred but visible |
| 段落边界重复 | 上段结尾和下段开头同人物同景别同构图 | 下一段开头改景别/机位/主体/动作状态/空间尺度/信息焦点，重新锚定空间 |
| 强行遮罩转场 | 每段都用前景遮挡或 fabric wipe 衔接 | 删除默认遮罩转场，改用 ending state + opening re-anchor；只有真实物体自然经过镜头时才保留 |
| 动作变乱 | 同时动作太多 | 每个 beat 一个动作目标，拆段 |
| 运镜混乱 | 一段多种主运镜 | 保留一个主运镜，其他改成后续 beat |
| 切镜后方向错 | 未重锚 screen direction | 每个 hard cut 后重写 screen-left/right |
| 参考图被过度套用 | 没有维度锁定 | 写 controls only / does not control |
| 音频把画面带偏 | 没有说明音频用途 | 写“音频节奏锁定”和最终可听声音层 |
| 人声导致嘴型误动 | 旁白/内心独白与画面说话混淆 | 写清“旁白/内心独白不让画面角色对口型” |
| 台词脱离时间轴 | 单独列 `【台词】`，模型不知道何时谁说 | 把每句台词写回对应秒点：说话者 + 内容 + 画内/画外 + 嘴型状态 + 画面承载 |
| 文字乱码 | 要求模型生成复杂文字 | 除非必须，写 no readable text；必要文字简短并锁定 |
| 血腥过度 | 接触点写成伤口细节 | 改为遮挡、反应、停机、静默、物体位置变化 |
| 光线空泛 | 只写暖光/冷光 | 补光源、方向、强度、阴影、材质反应 |
| 风格不稳定 | 风格名堆叠 | 编译为线条、色彩、光线、材质、构图 |

## 输出前最终检查

完整提示词至少满足：

- 有 `【基础风格】`。
- 有 `【场景/角色/素材锁定】` 或等价信息。
- 有 `【运镜与时间轴】`，且时间轴包含画面结构、焦点路径、动作和结尾状态。
- 如果有台词、旁白、内心OS或画外音，它们都已经出现在 `【运镜与时间轴】` 的具体秒点中，而不是独立台词清单。
- 有 `【声音设计】` 或等价声音层。
- 有 `【画面清洁】`。
- 如果用户要求多个段落，每段都有独立提示词，而不是只写“同上”。
- 如果用户只要最终提示词，不输出冗长分析。

## 输出修复句式

如果原提示词太抽象：

```text
把“镜头推进到危险处”改成 “slow dolly in from shoulder-height wide shot toward the fixed danger gap; focus racks from the driver's eyes to the metal pipe aligned with the handlebar.”
```

如果原提示词动作太乱：

```text
拆成 three beats: route -> contact point -> consequence. Do not ask the model to perform chase, fall, rescue and reaction in the same second.
```

如果原提示词切镜太密：

```text
Use 5-15s packed Seedance segments with internal markers; split only at strong scene, camera-readability, character/speaker, time-state, or completed-action boundaries.
```
