# 06 Timeline Editing Sound

priority: high
scope: 时间轴、切镜、转场、音频控制、声音叙事、Seedance 15 秒压缩

## 使用边界

本文件只提供静默时间轴和声音决策。最终用户可见输出必须用中文栏目：`【基础风格】`、`【角色/场景/素材锁定】`、`【运镜与时间轴】`、`【声音设计】`、`【画面限制】`。不要输出 `hard cut block`、`Seedance packed prompt`、`Prompt:` 等英文模板标题。

`【运镜与时间轴】` 默认使用 `【角色/场景/素材锁定】` 中已经建立的锁定名，例如 `主角A`、`场景A`、`道具A`、`声线A`、`动作参考A`。不要在每个 time beat 反复写 @图片/@视频/@音频，除非新参考首次出现或需要修复参考漂移。

锁定名的作用域只到当前独立段结束。下一段必须重新建立素材用途、角色/场景/道具状态和锁定名，不能把上一段的锁定表当成模型记忆。

## 空间拓扑与轴线继承门

CUT 接力前先保留一份静默世界坐标账本：固定墙面、门窗、工位/座位、入口出口、路线、人物世界位置与朝向、行动轴和摄影机所在轴线侧。它们是继承项；foreground/background、screen-left/right、人物正背面和遮挡是当前机位的派生项，不可原样继承。

每个 CUT 进入时按以下顺序重算：

```text
继承已验收世界拓扑 -> 指定摄影机世界位置/轴线侧 -> 指定镜头看向 -> 推导人物正背面 -> 计算入镜固定物 -> 分配前中后景与 screen-left/right -> 校验 eyeline/运动方向
```

反拍不是把上一镜所有左右和背景词反过来。反拍仍要保持行动轴同侧，并根据新摄影机视锥重新判断：人物面对的物体可能落在摄影机后方而不入镜；人物身体后方的真实工位或墙面才成为新背景。若提示词同时写“人物正面面对镜头”和“人物面朝的门仍在其身后背景”，除非门、人物和摄影机确实共线且几何成立，否则判定为空间矛盾并重写。

用户验收或纠正过的门窗、排数、座位、人物朝向、通道和轴线进入 Sequence State Engine。以后每个相关段先继承这些世界锚点，再选择新机位；不能为了画面方便移动固定物或静默改变排数口径。

## 时间轴整合规则

默认可见时间轴始终使用 `CUT 1 / CUT 2 / ...`，不显示每个 CUT 的具体秒数。即使一镜到底也要写 `CUT 1`，把内部动作、对白、焦点和声音 marker 写在这个 CUT 内，不用无标签散文代替时间轴。系统仍在静默层规划总时长、对白可读性、动作相位和停顿，确保整段 `<=15秒`，并在段落标题给出建议总时长。

只有以下情况启用“精确时码模式”：用户明确要求逐秒/时间码；音频卡点或声音事件需要同步；VFX、机关、爆点或产品步骤需要精确触发；首尾帧/关键帧需要对齐；目标模型或剪辑工作流明确要求 timecode。此时才在 CUT 后补起止秒数或 marker。

默认把以下内容合并到 `【运镜与时间轴】`：

- 画面结构与构图。
- 焦点路径。
- 运镜。
- 动作部位和路线。
- 台词、旁白、内心OS、画外音所在 CUT、说话者、声音来源和画面承载；画内说话者自然 lip-sync，精确时码模式再补起止秒数。
- marker / beat。
- 声音 cue。
- 切镜理由。
- 结尾状态。

不要在同一个提示词里把这些拆成互不影响的栏目，因为它们都受时间变化影响。

## CUT 因果与镜头接力引擎

先区分作用域：本节的“上一镜/下一镜”只指**同一独立段内的相邻 CUT**。跨独立段时，下一段 `CUT 1` 必须按零记忆冷启动重新写人物、位置、朝向、道具、开场动作相位和声音来源；不得用“承接上一段、继续、仍然、停止、收好、沿来时路线”代替完整开场。上一段 `OUT state` 只进入静默状态账本，再被改写成本段可独立理解的 `IN state`。

`CUT` 不是镜头术语清单，而是一个明确变化单位。每个 CUT 只承担一个**明确变化**，但画面里允许出现多个辅助变化：肢体、焦点、运镜、材质、光影、环境和声音都可以同时或先后改变，只要它们共同建立、推进、确认或接力这个明确变化。判断标准不是“画面里只能有一个东西变化”，而是能否用一句话说清“这一镜究竟改变了什么”。

例如 CUT 的明确变化是“翼兽由高空盘旋转入贴地俯冲”，同镜可以同时出现翼拍下压、镜头下降、影子扫过地面、焦点转向巨口、风声增强和尘屑被卷起。只有当又出现同等级的新动作目标或结果，例如“巨口咬中盾牌”或“守卫被撞离地面”，才交给后续 CUT 独立读取。

一镜到底是唯一格式边界：仍按总规则标为 `CUT 1`，但在这个不间断镜头内部使用 `BEAT A / BEAT B / BEAT C`。每个 BEAT 只承担一个明确变化，允许多个因果辅助变化，并用持续运镜、动作、焦点、材质或声音接到下一 BEAT，不制造真实切镜。

静默编译契约：

```text
上一镜末端可见状态 -> 本 CUT 从同一动作相位接入 -> 一个明确变化 + 多个因果辅助变化 -> 末端接力载体 -> 下一 CUT 接收
```

每个 CUT 内部都要能回答：

- `IN state`：上一镜末端是谁、哪个部位/道具正在怎样运动，焦点、声音和 screen direction 停在哪里。
- `EXPLICIT CHANGE`：本镜要让观众明确读到的核心变化是什么，例如距离缩短、武器接触、人物倒地、焦点转移、遮挡完成、空间尺度揭示；允许多个身体、焦点、材质、环境和声音变化共同服务它。
- `RELAY CARRIER`：什么已经可见并仍在运动，能够把观看方向交给下一镜。
- `OUT state`：人物、道具、构图、焦点、运动方向和声音停在什么可继承状态。

优先使用以下接力：

- 动作相位接力：上一镜在抬臂、翼拍、迈步、扑近、挥砍或坠落中切出；下一镜从同一相位、同一速度趋势和同一受力方向继续，不重演准备动作。
- 方向接力：上一镜末端向 screen-right、向镜头、向下或绕主体旋转；下一镜延续该方向。若故意反向表达阻力或反转，先用接触、反应或空间重建说明方向变化。
- 力量/材质接力：力量来源 -> 路径 -> 接触 -> 材质反应 -> 残留。下一镜优先从接触点、飞散物、烟雾、裂纹、涟漪或余振进入。
- 视线/焦点接力：角色视线、道具指向或 `rack focus` 在上一镜末端锁定新对象；下一镜让该对象成为画面主体或结果承受者。
- 自然遮挡接力：巨口、翼面、衣料、门框、烟尘、人物或真实前景物在运动中覆盖画面，下一镜由同一材质、方向或速度打开。遮挡必须是剧情内真实运动，不是为了连接而硬加的 wipe。
- 声音接力：下一镜声音先行形成 J-cut，或上一镜碰撞、呼吸、轰鸣延续形成 L-cut；声音必须指向下一主体、空间或后果。

稳定写法：

```text
CUT 2，从上一镜末端仍向 screen-right 扇落的翼面接入；低机位横向跟拍让翼尖掠过前景并完成一次主变化：巨兽由盘旋变为贴地扑近。翼面短暂覆盖镜头，下一 CUT 从同方向逼近的巨口接收；结尾保持巨口占据 foreground center、目标位于 midground screen-right。
```

CUT 数量由有动机的状态交接决定，不由固定镜头数决定。切点必须落在主变化已经可读、接力载体已经进入画面且下一镜有明确接收者的时刻。

## 台词 / 旁白时间轴绑定规则

台词不是独立文案清单，而是镜头事件。默认不要输出独立的 `【台词】`、`【台词/旁白】` 栏目，除非用户明确要求只整理台词表。

每一句台词、旁白、内心OS、画外音都必须写进 `【运镜与时间轴】` 的一个 CUT，或按自然语义节点分配到多个连续 CUT，并至少包含：

- CUT 归属：这句话从哪个 CUT 开始、是否跨 CUT 连续、在哪个 CUT 结束；只有精确时码模式才写起止秒数。
- 说话者：角色名、旁白、画外人声、内心OS。
- 具体内容：保留用户原台词，不擅自改写。
- 声音来源：画内说话、画外旁白、内心OS、广播/电话/录音。
- 发声与口型：画内说话者自然 lip-sync；旁白、画外音和内心OS只标清声音来源，默认不添加画面人物口型限制。仅在复盘已经出现声音误配，或同框多个潜在发声者造成真实歧义时，补一条最短的归属锁定。
- 画面承载：说话时镜头看脸、看手、看物件、看反应者，还是看空间。
- 听者反应：每个仍在画内的听者至少有视线/表情反应，再加一种手、道具、呼吸、肩线、重心、脚步或衣料反应；只写当前真实发生的正向动作。

### 台词跨 CUT 连续规则

- 一句台词可以自然跨 CUT。切点优先落在逗号、分句、关键词、揭露点、反转点或听者理解发生变化的位置，不按字数机械截断。
- 这里的跨 CUT 仅限同一独立段。默认不让一句台词、一次呼吸、电话声或 sound bridge 跨越两个可分别提交的提示词块；优先把完整发声链打包在一段内。确需拆段时，下一段重新点名说话者/声音源、接通状态和当前准确语句，不写“继续上一段台词”。
- 前一 CUT 写清“角色A开始说”及准确前半句；后一 CUT 写清“角色A同一人声连续/继续说完”及准确后半句。声音不中断、不重启、不重复已经说过的词。
- 切到听者、道具、危险物或空间时，使用 J-cut/L-cut 或等价自然语言保持同一说话者归属。角色A仍在画内时继续自然 lip-sync；角色A离画后标明“角色A画外同一人声继续”。
- 动作、听者反应、焦点转移、构图变化和必要运镜优先发生在台词进行期间，不按“先说完 -> 再动作 -> 再反应”串行拉长。
- 只有沉默、迟疑、吞咽、震惊、权力停顿或反应本身改变剧情时，才为它保留独立明显时长；普通动作和普通反应读清后立即接下一变化。

稳定写法：

```text
CUT 1，角色A把文件推到桌面中央后开始自然 lip-sync 说：“我不是来问你有没有做过，”镜头随文件横移到角色B手边；角色B拇指压住页角。
CUT 2，角色A画外同一人声以 L-cut 连续说完：“我是来问你为什么留下证据。”画面切到角色B，焦点从文件抬到他的眼睛；角色A说到“证据”时，角色B握力收紧，句尾停在角色B已经理解威胁的新状态。
```

## 对白、动作与镜头协同

对白不是覆盖在镜头上的音轨。静默安排每句台词的内部相位：

```text
PRE-LINE：什么动作、目光、声音或空间变化让角色现在必须开口。
LINE ENTRY：角色在动作哪个阶段开始说，不默认从 CUT 第一帧开口。
UNDER-LINE ACTION：说话时仍能自然完成的手、道具、步伐、距离或工作动作。
SEMANTIC TURN：哪一个词义节点改变听者、焦点、构图或权力。
POST-LINE STATE：句尾人物、道具、距离、视线、焦点和声音进入什么新状态。
```

规则：

- 先让动作产生说话动机，再让句子进入；例如吞咽后才评价、递物尚未停时开口、走到门槛才威胁、听见异响后中断原动作再回答。
- 说话动作必须符合身体条件。角色全速冲刺、屏息潜伏、被扼住或完成复杂发力时，不安排自然长句；改为短句、喘息后说、动作前说或动作结果后说。
- 镜头画面归属于当前信息和情绪的承受者，不机械归属于发声者。保留清楚声音来源后，可用 J-cut、L-cut、焦点转移或 reaction cut 在关键语义节点交给听者、道具或危险空间。
- 全景/多人 CUT 先定义注意力层级：前景主动作，中景语义反应，后景持续任务或环境压力。各层错峰变化；听者不统一停手、转头或点头。
- 台词句尾必须改变一个可继承状态，并成为继续持镜或切镜的理由。句尾不让演员回到中性站姿，也不为了切镜强行加遮罩。
- 慢节奏或情绪渲染可使用有动机的 locked-off/hold，并用呼吸变化、握力、视线、重心、道具动作以及焦点、光影、环境或声音变化推动节拍，明确下一状态或切镜条件。
- 动作声、道具声和生理声必须落在对应动作发生的同一 CUT 与同一先后位置；`【声音设计】` 只总结声音层，不得把落位、碰撞、吞咽、脚步或呼吸声挪到动作之前或之后。

稳定句式：

```text
CUT 2，中近景保持在老人 screen-right 的弯腰背影，焦点从他手里的稻穗转到 background center 的收割机尾部。画外旁白说：“他没有意识到，自己已经走进盲区。”老人右手继续捡拾，肩背随呼吸轻微起伏；机器轰鸣压过倒车提示音。
```

```text
CUT 3，驾驶员老张在驾驶室内 screen-left 回头看后视镜，自然 lip-sync 说：“后面没人吧？”焦点随后 rack focus 到后窗外被稻秆遮挡的盲区。副驾驶若仍在画内，手指压住摊开的作业单，抬眼沿后视镜方向看向后窗。
```

对白稳定句式：

```text
CUT 2，50mm斜向紧双人镜头。角色A走到桌边，把唯一道具推到两人之间后才开始自然 lip-sync 说：“[原台词]”；说到[语义节点]时，右手离开道具并收回身侧。角色B位于 midground screen-right，先继续原有任务，听到[语义节点]后手指停在半途，视线由道具移到角色A，再握紧道具。焦点随这次反应从角色A转到角色B；句尾角色A停在桌外，角色B掌握道具，新的距离和权力状态成为切镜理由。
```

## Seedance 生成段落拼接规则

分镜是导演思考单位，Seedance 段落是模型生成单位。输出时不要默认一镜一段。

拼接优先级：

- 同一个空间内发生的连续事件，优先放进同一段。
- 同一个人物连续说话、观察、反应或行动，优先放进同一段。
- 一段连续动作从准备、推进、阻力、结果到反应，优先放进同一段。
- 声音桥、动作匹配、目光匹配、焦点转移可以作为段内 `CUT`，不必单独拆段。
- 先估算每个剧情节拍的最短可读时长，再按空间、人物/说话者、动作链、对话链、时间状态和轴线连续性，把相邻节拍拼成一个 `<=15秒` 整段。连续内容优先装满同一生成容器，但时长来自更多剧情节拍，不能来自拉长单个动作、普通反应或空镜。
- 两个候选生成段初算合计 `>15秒且<20秒` 时，默认先尝试压缩成一个约13-15秒整段：台词在自然语义节点跨 CUT 连续，动作、听者反应、焦点和构图与台词并行，删除重复空间建立、重复表情确认、装饰性运镜和结尾空 hold。
- 只有压缩后仍超过15秒，或出现切地点、切时间、主要人物/说话者更换、机位系统严重冲突、空间需要重新建立、完整因果链结束等强边界时才拆段。5-7秒短段必须能说明强边界或确实没有可兼容相邻节拍；多段项目还要重新分配 CUT，避免留下可并回前后段的短尾段。
- 低于 5 秒视为过碎，只有强边界才能低于 5 秒。

提前分段边界：

- 切场景/地点。
- 切景别或机位变化大到模型在同段内难以保持空间连续。
- 切主要人物、切说话者、切 POV 所属。
- 切时间状态，如回忆、梦境、闪回、隔天。
- 一段动作链已经完成，下一段动作目标发生变化。
- 需要重新建立危险线、空间轴线或群众路线。

## 节拍防火墙

长项目、多段剧本、续写、extend、下一段、修尾时，先把故事节拍静默分为四类：

| 类别 | 含义 | 输出规则 |
| --- | --- | --- |
| 已发生 | 用户已接受的视频/尾帧已经表现过 | 不重复演，只可作为开场状态或背景事实 |
| 本段执行 | 当前 5-15 秒需要完成的动作/信息 | 写进 `【运镜与时间轴】` |
| 未来保留 | 下一段或后续段落才该发生 | 本段不出现，必要时写“停在...之前” |
| 暂不显示 | 会剧透、混乱或超载当前段 | 完全不写进提示词 |

规则：

- 故事背景可以影响表演、布光、声音和镜头压力，但不能让本段提前完成未来剧情。
- 如果上一段实际生成结果提前完成了计划中的未来动作，把该动作改为“已发生”，后续不再重复。
- 如果上一段没有完成计划中的动作，下一段从实际停住的位置继续，不假装计划已经发生。
- 当前段必须有可见 endpoint，方便下一段继承。

## 续写与实际结尾优先

续写、下一段、extend、repair tail 必须从已接受视频、已接受尾帧或用户给出的精确可见结尾描述开始。

静默状态账本可记录“上一段已发生/未来保留”，但可复制的视频提示词只写当前开场的可见状态、当前动作和结尾状态，不写制作历史。稳定写法：

```text
CUT 1：老人位于 screen-right midground，腰背仍向前弯，右手停在稻穗上方；收割机尾部占据 background center，并沿 background -> midground 的既定方向缓慢逼近。镜头只表现危险距离继续缩短，结尾让固定盲区边界和老人位置同时可读。
```

如果用户只给原计划，没有给实际生成结果：

```text
我可以继续做下一段，但需要上一段实际结尾作为开场状态。请上传已接受视频/尾帧，或用一句话描述最后画面中人物位置、动作、镜头和声音状态。
```

上一段视频或尾帧作为参考时，画面本身承载状态。文字只补：

- 当前段动作。
- 结尾状态。
- 静态画面无法显示的 open motion、camera phase、audio phase。
- 易漂移的角色/服装/场景锁。
- 已完成动作和未来保留动作。

最后一项只留在静默账本或提示词外的制作备注中。可复制提示词不得出现“上一段已经”“不要重演”“下一段再发生”等历史说明；它只陈述当前时刻是什么、现在发生什么、最终停在哪里。

部分验收规则：

- 用户可把一条视频只验收到某个剪辑点；剪辑点后的原始尾部视为未接受，不进入正史。
- 下一段继承剪掉后的最后可见状态、动作相位、镜头相位和声音相位。
- 用户选择后期修时，下一段继承后期完成后的状态，而不是原素材中的待修瑕疵。

## 上下段落边界规则

每个独立 Seedance 段落都必须能单独生成，但上下段不应该像同一镜头硬拆。上一段最后一拍和下一段第一拍要有明确差异：

- 避免同一人物 + 同一景别 + 同一构图连续出现在两个段落边界。
- 下一段开头至少改变一项：景别、机位、主体、动作状态、空间尺度、信息焦点、声音状态。
- 不要为了衔接段落而强行使用遮罩、foreground occlusion、fabric wipe、黑闪或白闪。只有当画面里真实人物、车辆、布料、柱子、稻秆等自然经过镜头，并且对剧情有用时才写遮挡转场。
- 段落衔接优先靠“上一段 ending state + 下一段 opening re-anchor”，而不是靠转场特效。
- 仍然优先在 5-15 秒内完整叙述同空间、同人物、同动作链；不要为了制造开尾差异而把可连续理解的动作拆碎。
- `opening re-anchor` 必须是一句可独立执行的正向现状：点名角色、身体部位/道具、对象、位置、方向和当前动作相位。它不能只是“继续走”“停止吹气”“收好东西”“门回落”“文件下垂”或代词指代。
- 跨段 `opening re-anchor` 还要重复已验收世界拓扑与行动轴，并按本段首镜机位重新计算人物正背面、可见固定物、前中后景和 screen-left/right；不能直接复制上一段末镜的背景描述。

稳定写法：

```text
第01段最后 CUT：MS holds on the old man frozen in midground, background harvester still approaching, engine rumble dominates.
第02段开头 CUT：WS from a higher field-side angle re-establishes the whole danger triangle: old man now small in screen-right midground, harvester rear fills background center, blurred field workers remain visible near screen-left ridge.
```

## 镜头时长选择（仅静默规划）

| 时长 | 适合功能 | 注意 |
| --- | --- | --- |
| 0.5-1s | 打斗、追逐、闪回、惊吓、快速信息 | 只放一个清楚动作或反应 |
| 1-2s | 日常对话、连续动作分解、关键展示 | 最稳定的短节奏 |
| 2-3s | 多人同框、人物姿态、场景转场、次要情节推进 | 可含一个焦点转移 |
| 3-5s | 情绪渲染、氛围营造、重要场景、尺度揭示 | 必须有内部变化 |
| 5-8s | 独白、一镜到底、沉浸体验、情绪爆发 | 每 2-3 秒加 marker |
| 8-15s | 复杂长镜头、救援/追逐、转变、场景完整动作链 | 用 3-6 个 internal beats |

### 可读性时长门

- 0.5-1 秒只承担一个插入、接触、闪光、短反应或自然遮挡，不承载“接近 + 蓄力 + 碰撞 + 反应 + 转场”的复合任务。
- 先按准确台词的自然语速确定最小骨架时长，再把可发声的走位、递物、视线、焦点、听者反应和环境变化叠在台词之下；台词允许跨 CUT 连续，不为每个动作或反应追加独立长镜头。
- 复杂肢体发力、接触后的反作用、关键情绪识别和空间尺度揭示只保留达到可读性的最短时间；读清后立即推进，不用慢动作或持镜填满 15 秒。
- 同一主变化的准备、执行和确认可压进一个 CUT；动作目标、信息归属或结果承受者改变时，另起 CUT。
- 计划超过容量时，先删除重复建立、装饰性运镜和冗余反应，再让动作与台词并行、让同一台词跨 CUT 延续；两个候选段合计大于15秒且小于20秒时优先压成一个13-15秒段。计划低于15秒时继续检查是否有相邻兼容节拍可以装入；没有可兼容内容时才结束，绝不靠拉长单一动作补时长。

只有剧情密度确实需要占满 15 秒时，才使用以下内部规划；内容提前完成就提前结束，不直接复制到默认可见输出：

```text
0-2s establish / lock space
2-5s pressure or action begins
5-9s conflict / reveal / reversal
9-12s climax / consequence
12-15s only if unresolved consequence, dialogue, or transition still requires it; otherwise stop earlier
```

## 切镜理由

每次切镜必须回答至少一个理由：

- 信息变化：观众需要看到新信息。
- 情绪变化：角色心理状态改变。
- 视角变化：从客观转主观，或从主角转旁观者。
- 冲突升级：危险距离缩短、力量关系变化。
- 尺度揭示：从局部到整体，或从人到巨物。
- 动作结果确认：冲击后需要看到后果。

切镜理由说明“为什么现在要换视角”，镜头接力说明“下一镜怎样从这里继续”。两者必须同时成立：主变化未读清不切，接力载体未出现不抢切，下一镜没有接收者不空切。

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

默认在 `【声音设计】` 开头写“无背景音乐”，随后列出现场声、动作声、环境声、台词和必要声音事件。用户明确要求 BGM 或将参考音乐指定为 final BGM 时，用指定音乐覆盖该默认项。

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

默认句式将接入状态、一个主变化、接力载体和结尾状态自然写进中文，不机械暴露字段名：

```text
CUT N，从上一镜末端的[动作相位/运动方向/焦点/声音]接入；[景别、机位、主运镜]跟随[主体]完成一个明确变化：[状态A -> 状态B]，同时以[肢体/焦点/材质/环境/声音辅助变化]建立、推进或确认它。[翼拍/巨口/肢体或武器路线/视线/焦点/材质/自然前景遮挡/声音]在镜尾把注意力交给[下一主体、物件、空间或后果]；结尾停在[可继承的画面与声音状态]。
```

```text
CUT 1，建立危险几何：fixed metal pipe in screen-left foreground，tractor handlebar in midground right，driver turned backward but still seated。Camera locked-off at shoulder height，35mm lens，focus holds on the narrowing gap。Engine rumble masks all small sounds。

CUT 2，slow dolly in toward the gap；focus racks from driver's eyes to the pipe-handlebar alignment。His right hand keeps pulling the reverse lever，left shoulder twists，rear wheel moves only half a meter。A short metallic scrape becomes the main sound cue。

CUT 3，reaction cut reason：information changes from machine movement to human consequence。Workers in background freeze，sound drops to low-frequency rumble and breathless silence，ending state holds on the stopped machine and fixed pipe with no graphic injury。
```
