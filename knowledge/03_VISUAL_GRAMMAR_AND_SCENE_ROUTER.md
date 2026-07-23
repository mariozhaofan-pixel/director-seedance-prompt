# 03 Visual Grammar And Scene Router

priority: high
scope: 画面结构、空间轴线、场景功能、构图、焦点路径、群众调度

## Seedance 画面结构优先

Seedance 更容易理解可见画面结构，而不是抽象导演词。提示词必须优先描述：

- screen-left / screen-right：画面左侧、右侧有什么，谁从哪边入画或离画。
- foreground / midground / background：前景、中景、后景各自承担什么信息。
- focus path：焦点从哪个主体变到哪个主体，为什么变。
- composition：中心构图、三分法、对称、负空间、遮挡构图、引导线。
- body mechanics：身体部位如何移动，手、脚、肩、头、眼睛、重心分别做什么。
- ending state：每段最后一帧停在哪个空间状态。

不要只写“紧张地倒车”。要写：

```text
screen-left metal pipe stays fixed in foreground, midground tractor handlebar moves backward from right to left, background worker's face is hidden by the frame edge; focus starts on the handlebar joint, rack focus to the two-finger gap between neck-height pipe and handlebar, ending with both objects locked in the same plane.
```

## 画面结构编译顺序

每个 time beat 按以下顺序写：

1. 起始状态：谁在哪个画面区域。
2. 固定物：墙、管道、机器、门、车辆、货架、地面边界先写清。
3. 移动物：人、车、手、脚、道具、动物再写。
4. 焦点：focus starts on A -> racks to B -> holds on C。
5. 构图：composition type and visual hierarchy。
6. 运镜：一个主要 camera movement。
7. 动作：身体部位、路线、接触点、速度变化。
8. 结尾状态：最后一帧谁在何处，危险/信息是否清楚。

## 场景功能路由器

先判断镜头功能，再决定时长、景别和运镜。

| 场景功能 | 默认画面策略 | 默认声音策略 |
| --- | --- | --- |
| 建立空间 | EWS/WS，清楚入口出口和危险线 | 环境声先行 |
| 角色识别 | CU/MCU，脸、服装、道具锚点 | 呼吸、衣料、轻动作声 |
| 信息揭示 | foreground occlusion / rack focus / tilt reveal | 声音先行或声音变窄 |
| 危险逼近 | fixed danger object + moving subject | 低频、机械声、短静默 |
| 反应确认 | reaction cut / held close-up | 呼吸中断、环境声抽离 |
| 动作冲突 | 中景到全景，路线和接触点清楚 | impact sound + debris/cloth/footstep |
| 尺度揭示 | pull-back scale reveal / crane rise | 空间回声、低频扩张 |
| 音乐卡点 | marker-based motion accents | beat grid，不牺牲剧情可读性 |
| 产品/科普 | clean locked-off / macro insert | 清晰提示音、无混乱声层 |
| 漫画/动画 | pose clarity + exaggerated silhouette | 风格化动作音效 |

## 轴线与空间连续性

### 两层空间模型

空间连续性分成两层，不能混写：

1. **世界拓扑 World topology**：不随镜头改变的墙、门、窗、道路、工位排数、座位、桌椅朝向、人物站位、入口/出口、危险线和行动轴。
2. **画面投影 Frame projection**：由当前摄影机位置和看向方向决定的 screen-left/right、foreground/midground/background、人物正面/斜正面/背面、遮挡和可见范围。

静态末尾帧进入下一独立段时，只能向世界拓扑层提供角色站位与相互距离，不能向画面投影层提供任何参数。下一段 `CUT 1` 必须 `hard cut/direct cut` 到新摄影机起点、看向、焦段和景别；角色身份从原角色参考/文字恢复，场景从原场景文字、已验收场景设定或原始场景图恢复，再由新机位重新计算人物角度、遮挡、前中后景与 screen-left/right。

`background` 永远相对摄影机定义，不相对人物定义。人物面对某扇门，只说明门位于人物身体前方；门能否成为画面背景，取决于摄影机是否位于人物身后并朝门拍。摄影机改到门一侧反拍人物正面时，门通常位于摄影机后方或画外，人物的画面背景应变为其身体后方的工位、墙面或其他真实空间。

每个复杂场景先建立静默空间账本：

```text
世界锚点：后墙左侧门；三排工位；角色A在靠后第二排左位；角色A身体朝后墙。
行动轴：角色A <-> 后墙门，或角色A <-> 对话角色B。
```

每个 CUT 再执行摄影机变换：

```text
摄影机起点/所在侧 -> 镜头看向 -> 人物正/背/侧面 -> 入镜固定物 -> 前中后景 -> screen-left/right -> 视线与运动方向
```

办公室示例：

- 摄影机位于办公室前侧并朝后墙拍：角色A背对/斜背镜头，后墙门可位于 background。
- 摄影机位于后墙一侧并朝办公室前侧反拍：角色A正面/斜正面，后墙门位于摄影机后方或画外，角色A背景是更靠办公室前侧的工位与同事。
- 摄影机位于角色A肩后：角色A肩背在 foreground，门可在 background；只有这个几何条件成立时才能写“角色面对的门位于背景”。

### 继承与过轴规则

- 180 degree rule：先锁角色-角色、角色-门、角色-危险物或运动路线形成的行动轴，再锁摄影机位于轴线哪一侧。常规 CUT 保持同侧；过轴必须使用中性正轴镜头、可见摄影机/人物移动穿轴、明确空间再建立或用户指定的有动机越轴。
- eyeline match：角色世界朝向不因切镜改变。新机位需要重新计算画面中的视线方向，不能机械复制上一镜的 screen-left/right。
- screen direction：继承的是世界运动路线和轴线侧，不是上一镜的文字标签。每次反拍、侧拍、俯拍后都从摄影机变换重新计算 screen-left/right。
- entrance/exit：入口和出口的世界位置固定；入画/离画边随机位变化重新计算。
- danger line：机器、车辆、刀具、金属管、悬崖、门缝等危险线先锁世界位置，再计算它在当前画面的层级和方向。
- 已验收锁：用户确认过的门窗位置、排数口径、人物座位/朝向、通道和轴线进入连续性正史。后续 CUT 与独立段必须继承；只有用户修改场景或镜头明确展示位置变化时才能更新。
- 参考场景图可以锁世界拓扑、材质和已见布局，但不能迫使所有新机位沿用参考图的前景/背景或 screen-left/right。新角度必须按同一拓扑重建画面投影。

## 构图模板

| 构图 | 用途 | 提示词写法 |
| --- | --- | --- |
| centered composition | 英雄、威胁、仪式、产品 | subject centered, background symmetry locks attention |
| rule of thirds | 日常、对话、纪录感 | face on left third, empty danger space on right third |
| negative space | 孤独、未知威胁 | subject small in lower-left, empty dark space dominates upper-right |
| foreground occlusion | 偷看、转场、压迫 | foreground object wipes across frame, revealing subject behind it |
| leading lines | 路径、命运、危险 | greenhouse pipes form converging lines toward the danger point |
| deep staging | 多人、多层信息 | foreground tool, midground character, background threat all readable |
| top-down map | 群体、路线、困局 | 90-degree top-down view shows escape routes and blocked path |
| low-angle dominance | 权力、巨物、机器压迫 | low-angle frame makes machine fill upper half of image |

## 群像与调度

群体不能随机乱动。必须写：

- 主方向：人群总体向哪里移动。
- 反方向：谁逆流、谁停住、谁回头。
- 拥堵点：门口、桥口、摊位、车辆旁、台阶。
- 逃生路线：哪条路可走，哪条路被堵。
- 反应层级：前景惊慌、中景推挤、背景迟疑或围观。
- 持续锚点：如果人群、后景人物、路人、围观者、队伍或兽群已经进入画面，后续 time beat、切全景、切回全景、切到反应镜头时必须重复他们的位置、密度和方向。后景可以虚化，但要写成“background crowd remains softly blurred but visible”，不能让人群无故消失。
- 变化理由：人群离开、散开、被遮挡或被切出画面时，必须写清离开方向、遮挡物、镜头裁切或剧情原因。

提示词：

```text
crowd blocking is directional: most villagers run from screen-right to screen-left toward the field exit, one elderly man moves against the flow in midground, foreground workers stop at the blocked dirt path, background harvester remains a fixed heavy mass.
```

全景/后景持续写法：

```text
WS wide shot: foreground villagers keep pushing toward the narrow exit, midground protagonist stands against the flow, background crowd remains softly blurred but visible across the market lane, density stays high and no background extras disappear between cuts.
```

## 美术与生活痕迹

场景不要空。每个场景至少有 3 类生活痕迹：

- 使用痕迹：泥、灰、磨损、划痕、油污、脚印。
- 阶层差异：衣料、工具、家具、交通工具的新旧程度。
- 文化逻辑：材料、符号、颜色、宗教或地方工艺要一致。
- 道具用途：道具必须服务剧情，不做随机装饰。
