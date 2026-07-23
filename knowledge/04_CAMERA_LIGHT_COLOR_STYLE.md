# 04 Camera Light Color Style

priority: high
scope: 基础风格、摄影机镜头、景别、运镜、光线、色彩、画家/流派语义编译

## 使用边界

本文件是静默参考库，不是最终输出模板。最终回答必须按 `01_CORE_EXECUTION_CONTRACT.md` 的中文输出格式写，不要把本文件里的英文表头、英文示例或表格结构直接复制给用户。英文只保留必要技术短语，例如 `slow dolly in`、`rack focus`、`IMAX 65mm language`。

## 基础风格写法

`【基础风格】` 是 Seedance 提示词的高优先级模块，必须前置，并且每个独立段落都要出现。它不是一次性总说明。

写法规则：

- 每段重复项目级统一基调：摄影机/镜头语言、焦段/景深倾向、色彩关系、质感、真实感或类型语气。
- 每段补充本场景变化：光源、方向、天气、空间材质、情绪反差或危险气氛。
- 不允许后续段落只写“同上”“沿用上一段风格”。如果要保持统一，就写“延续 [项目级基调]，本段改为 [具体场景变化]”。
- 风格参考、画家/流派参考也写进这里，转换成线条、色彩、构图、质感和光线，不单独开素材说明栏目。

推荐句式：

```text
Camera/lens style: [camera body feel] + [lens family] + [focal length] + [aspect ratio] + [depth of field].
Lighting: [source] from [direction], [intensity], [shadow quality], [contrast ratio], [material response].
Color: [60% dominant color], [30% secondary color], [10% accent color], [LUT / film stock feel], [warm-cool relationship].
Texture: [realistic / filmic / PBR / documentary / commercial sharpness].
```

## 摄影机与镜头风格库

| 风格组 | 适合题材 | 画面特征 | 提示词写法 |
| --- | --- | --- | --- |
| ARRI Alexa 35 + Cooke S8/i | 高级剧集、人物文戏、自然高光 | 柔和皮肤、圆润高光、轻微温暖、情绪可信 | `ARRI Alexa 35 feel, Cooke S8/i lens warmth, 35mm or 50mm, gentle highlight rolloff, natural skin tone` |
| ARRI Alexa LF + Panavision Ultra Panatar | 史诗宽银幕、沙漠、巨物、宏大空间 | 大画幅、宽银幕、压迫尺度、空间纵深 | `ARRI Alexa LF large-format look, Panavision Ultra Panatar wide-screen language, 2.76:1, distant scale reveal` |
| Sony Venice 2 + Panavision Primo 70 | 科幻、夜景、城市、冷调高动态范围 | 冷调、干净、夜景细节、霓虹高动态 | `Sony Venice 2 high dynamic range night look, Primo 70 lenses, crisp urban highlights, cool cyan shadows` |
| RED V-Raptor XL + Atlas Orion Anamorphic | 广告、动作、锐利强质感 | 锐利、对比强、横向 flare、速度感 | `RED V-Raptor XL sharp texture, Atlas Orion anamorphic flare, high-contrast action commercial energy` |
| IMAX 65mm / 70mm language | 神迹、灾难、宇宙尺度、巨物 | 超大尺度、垂直震撼、清晰空间层级 | `IMAX 65mm/70mm scale language, immense vertical space, ultra-clear foreground-to-background depth` |

不要为每个普通镜头硬塞摄影机型号。风格组用于稳定整体视觉和场景气质。

## 景别库

| 景别 | 用途 | 提示词写法 |
| --- | --- | --- |
| ECU 极特写 | 眼睛、伤痕、按钮、接触点 | `extreme close-up on fingertips tightening around the lever` |
| CU 特写 | 表情、反应、关键道具 | `close-up, face fills frame, background falls soft` |
| MCU 中近景 | 台词、微表演 | `medium close-up, shoulders and face readable` |
| MS 中景 | 人物动作和姿态 | `medium shot shows torso, hands and object relationship` |
| MLS 中远景 | 人物与空间关系 | `medium long shot keeps body movement and hazard line visible` |
| WS 全景 | 场景路线 | `wide shot maps entrance, exit, machine path and bystanders` |
| EWS 大远景 | 尺度、孤立、灾难 | `extreme wide shot, human figure small against huge landscape` |
| OTS 越肩 | 对话、主观压力 | `over-the-shoulder from driver toward blind zone` |
| POV 主观 | 恐惧、误判、寻找 | `POV through dusty rear mirror, blocked by straw` |
| top-down 90 | 路线、围困、群体 | `90-degree top-down view shows the blocked escape path` |
| low-angle | 威胁、权力、巨物 | `low-angle view makes harvester rear fill upper frame` |
| Dutch angle | 失衡、恐慌 | `subtle Dutch angle, horizon tilted by 8 degrees` |

## 运镜语法

完整运镜指令按下式编译：

```text
[承载装置/运动类型] + [相对主体的路线和方向] + [速度与加减速轮廓] + [主体在画面中的保持方式] + [起点画面] + [终点画面] + [剧情作用]
```

只写“推进、拉远、平滑、渐进、快速”都不完整。`smooth` 描述稳定性或加减速曲线，不等于慢；`gradual` 描述变化过程，不说明方向和终点；`fast` 必须同时给目标、可读主体和制动终点。

| 运镜 | 情绪 / 剧情 | 错误用法 | 稳定写法 |
| --- | --- | --- | --- |
| locked-off | 观察、权力僵持、证据、喜剧延迟 | 画面无内部变化 | `locked-off camera; actor task, focus or sound carries the beat` |
| pan left/right | 横向寻找、交接信息、接住入画 | 不写起止对象 | `pan right from the empty doorway to the entering doctor, ending with both characters readable` |
| tilt up/down | 垂直揭示、从后果回到人物 | 只写上摇/下摇 | `tilt up from the dropped report to the listener's face` |
| pedestal / boom up-down | 保持镜头朝向的垂直位移 | 与 tilt 混淆 | `camera pedestals down from eye level to desk height while lens stays level` |
| slow dolly in | 压力逼近、情绪收紧 | 只写“推进” | `slow dolly in toward the fixed danger point` |
| fast dolly back | 惊吓、尺度突然变大 | 画面主体丢失 | `fast dolly back, subject stays centered while danger fills background` |
| lateral truck | 追踪、横向路径 | 方向不清 | `camera trucks left parallel to the worker's movement` |
| follow / lead tracking | 跟随路线、引导逃亡或进入 | 不写摄像机在前还是在后 | `lead tracking shot moves backward ahead of the runner, maintaining a readable full body` |
| orbit | 展示关系、困局 | 过快眩晕 | `slow 120-degree orbit around both characters, axis remains readable` |
| descending spiral orbit | 坠落、命运压迫 | 空间漂移 | `descending spiral orbit from high angle to shoulder height` |
| crane rise | 尺度揭示 | 无信息变化 | `crane rise reveals blocked exit behind the crowd` |
| crane descend | 压力落到人物、从地图进入困局 | 下降但无落点 | `crane descends from the office layout into the trapped employee's desk` |
| tilt up reveal | 从物到威胁 | 只写“上摇” | `tilt up from muddy wheel track to the towering machine rear` |
| push-in tension | 心理压迫 | 多个主体抢焦点 | `push-in tension on the driver's eyes in mirror` |
| pull-back scale reveal | 人与巨物关系 | 拉远后信息空 | `pull back reveals elderly man inside the harvester blind triangle` |
| handheld panic | 逃亡、混乱 | 随机晃动 | `handheld panic with readable subject center, footsteps shake frame` |
| steadicam glide | 优雅、潜入、仪式 | 与粗粝场景冲突 | `steadicam glide through narrow corridor, no visible cut` |
| whip pan | 快速转移注意 | 乱切无目标 | `whip pan from shouted warning to machine rear impact zone` |
| zoom / crash zoom | 改变取景角而不改变透视位置；突发线索 | 与 dolly 混写 | `short crash zoom to the red value on the fixed report image` |
| rack focus | 信息转移 | 焦点对象不清 | `rack focus from rice stalks in foreground to hidden figure behind them` |
| bullet time | 超现实冲击 | 无原因炫技 | `bullet-time freeze, debris hangs in air, camera arcs around contact point` |
| Hitchcock dolly zoom | 恐惧认知崩塌 | 滥用 | `Hitchcock dolly zoom on the driver's realization, background stretches away` |

每个 time beat 只用一个主运镜；只有机械耦合且共同完成同一剧情变化的复合运动可计为一个主运镜，否则分到不同 time beat。

### 运镜速度与组合

速度词必须落到可见运动曲线：

| 速度轮廓 | 适合 | 可执行写法 |
| --- | --- | --- |
| subtle micro-movement | 纪实呼吸感、轻微不安 | `low-amplitude irregular handheld drift, face remains readable` |
| very slow / slow | 倾听、压迫、发现 | `very slow dolly in at a steady pace, ending before the desk edge` |
| moderate / walking pace | 走位、带领、空间浏览 | `lateral track at the actor's walking pace` |
| brisk / fast | 追逐、惊吓、信息突变 | `fast pull-back with a clear stop as the exit enters frame` |
| snap / whip | 单一注意力跳转 | `snap pan from the warning hand to the moving wheel` |
| gradual acceleration | 威胁累积、追逐升级 | `tracking move gradually accelerates with the runner` |
| gradual deceleration | 抵达、认知、后果 | `camera decelerates into a stable close-up and holds` |
| ease-in / ease-out | 稳定商业、抒情、产品展示 | `smooth ease-in, constant middle speed, soft ease-out on the hero object` |
| speed ramp | 接触前蓄势、撞击、后果 | `slow before contact, snap to real speed on impact, brief slow aftermath` |

- 运镜节奏与演员主动作同向或有明确反向理由；人物匀速走，摄影机通常同节奏跟随，紧张升级才逐步加速。
- 手持必须同时写晃动幅度、频率、身体/步伐来源和可读主体：低幅低频呼吸式漂移适合纪实与轻微不安，高频微震适合紧张，剧烈晃动只服务逃生或灾难冲击；产品细节展示和已有复杂复合运镜默认不再叠加手持。
- POV 必须点名视角来源、视线高度和运动逻辑，例如“郭大江眼睛 POV”“低于人眼的动物 POV”“车辆前挡风玻璃 POV”“无人机镜头 POV”。除非用户要求持续沉浸式主观镜头，POV 作为短暂信息/情绪视角使用，避免长时间失去客观空间。
- 组合运镜只保一个复合主句：`dolly zoom` 写清摄影机和变焦的相反方向及主体大小保持；`orbit + zoom` 写圆心、旋转角度、远近变化和终点；`lateral truck + counter-pan` 写轨道方向、反向摇摄和主体居中。
- 复杂复合运镜优先调用 `@视频`，但参考视频只控制已指派的运镜路径、速度和节奏，不控制当前角色、地点、服装、剧情或声音。

## 对白场景的镜头调度

对白镜头先看关系和语义归属，再选景别与运镜，不默认使用平视正反打：

| 戏剧关系 | 演员与镜头调度 | 适合的可见机制 |
| --- | --- | --- |
| 权力不平等 | 强者少动或占据高位，弱者在前景/纵深暴露手、呼吸和重心变化 | 深景双人构图、高低差、前景压迫、有动机的固定镜头或极慢推近 |
| 亲密靠近 | 两人共享镜头，用递物、接物、坐下、靠近或距离缩短承载台词 | 紧双人镜头、克制侧移、小幅弧线、焦点在手与脸之间转移 |
| 回避与隐瞒 | 角色不正面相对，用负空间、遮挡、错开的 eyeline 和道具任务暴露真实意图 | 斜构图、frame-within-frame、前景遮挡、从道具 rack focus 到反应 |
| 喜剧延迟 | 动作按严肃逻辑继续，让错误细节和晚半拍的反应形成笑点 | 保持双人/全景关系、短暂停留、reaction cut；不靠夸张晃镜制造笑点 |
| 威胁与逼问 | 施压者侵入对方空间或封住出口，镜头把距离变化和反应者同时读清 | 纵深调度、侧向重构图、低角度前景、slow dolly in 或压力型 locked-off |
| 告白与反转 | 先让说话者维持表面控制，再把画面交给听者的理解或关系变化 | 共享双人镜头转反应持镜、L-cut/J-cut、由脸转手或由物件转眼神 |

规则：

- 台词的摄影机不必始终拍说话者；信息属于谁，就让焦点、构图或切镜落到谁身上，但说话来源必须清楚。
- 摄影机运动必须跟随距离、权力、信息或反应的变化，不能用“镜头在动”掩盖人物站桩。
- 固定镜头只在证据、权力、等待、尴尬延迟、震惊或情绪压迫需要时使用；画内仍要有呼吸、握力、视线、焦点、光影、环境或声音变化。
- 用户或项目已锁定“破水平”、特定斜构图或其他镜头词典时，按其明确定义执行；不要把 Dutch angle 当作所有对白的通用美化。

## 光线库

写光线必须包含：光源、方向、强度、阴影、材质反应。

| 光线 | 适合场景 | 提示词写法 |
| --- | --- | --- |
| Dune daylight harsh sun | 沙漠、灾难、史诗 | `harsh high sun, short black shadows, dust turns gold, skin highlights dry and unforgiving` |
| Dune firelit interior | 宗教、密室、古老权力 | `large fire source from screen-left, flickering amber light, deep negative fill` |
| golden hour | 温情、回忆、收获 | `low golden sun from back-right, long soft shadows, rim light on rice stalks` |
| blue hour | 孤独、悬疑、转场 | `blue hour ambient sky, weak practical light, cool shadows` |
| moonlight | 夜逃、恐惧 | `cold moonlight from high back, silver rim on shoulders, foreground in soft darkness` |
| oil lamp / candlelight | 古代、亲密、危险 | `small warm practical flame, fast falloff, moving shadows across face` |
| torchlight | 洞穴、追逐、仪式 | `handheld torchlight, unstable orange highlights, walls breathe with shadow` |
| neon | 城市、科幻、诱惑 | `cyan-magenta neon from opposite sides, wet surfaces reflect color` |
| fluorescent | 医院、工厂、办公室 | `flat greenish overhead fluorescent, hard under-eye shadows, sterile texture` |
| overcast natural light | 纪录、现实、事故 | `overcast sky as broad softbox, low contrast, muddy ground reflects dull gray` |
| skip-bleach contrast | 罪案、战争、冷硬现实 | `skip-bleach contrast, desaturated midtones, crushed blacks` |
| low-key horror | 恐惧、未知 | `low-key lighting, one motivated practical, black negative fill, threat half-hidden` |
| high-key commercial | 产品、科普、广告 | `high-key softbox lighting, minimal shadows, clean readable surfaces` |

## 色彩系统

- 60/30/10：60% 环境主色，30% 人物/道具辅色，10% 危险或情绪强调色。
- 角色色彩：主角、反派、受害者、机器、超自然元素不能混成同一色块。
- 危险色：红、橙、黑黄警示、冷白机械光，用于突出风险点。
- 超自然例外色：只给异常能量、预兆、梦境、神迹，避免污染现实场景。
- HEX 锁定：产品、UI、装备、品牌色需要稳定时才写 HEX。
- LUT 语言：`warm Kodak-like highlights with cool cyan shadows`、`bleach bypass contrast`、`muted documentary LUT`。

## 画家 / 流派风格语义编译

如果用户提到画家、流派、插画风格或风格图，不要只复述名称。必须翻译为：

- 线条：硬边、软边、墨线、厚涂、速写。
- 色彩：饱和度、冷暖、主辅色、强调色。
- 构图：平面装饰、纵深透视、对称、负空间。
- 材质：油画、胶片颗粒、水彩扩散、PBR、黏土、赛璐璐。
- 光线：自然光、戏剧性明暗、图形化阴影。
- 情绪：童话、荒诞、史诗、压抑、温柔、冷峻。

写法：

```text
Style reference is compiled into soft watercolor edges, low-saturation moss green and warm ochre palette, simple graphic silhouettes, gentle ambient light and hand-painted paper texture; do not copy any signature or exact artwork.
```
