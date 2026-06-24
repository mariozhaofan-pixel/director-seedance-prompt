# 02 Reference Router And Locks

priority: high
scope: @图片 / @视频 / @音频 / 序列帧 / 参考提示词的用途分配和维度锁定

## 总原则

场景锁定、角色锁定、音频锁定，本质都是说明参考素材只控制哪些维度。不能写“参考 @图片1”就结束。

每个素材都要写成：

```text
@素材N controls only [维度列表], not [排除维度列表].
```

## 多模态素材路由器

@图片可控制：

- character identity：脸型、发型、年龄感、体型、服装、道具。
- environment identity：地点、空间布局、建筑材料、天气、时代。
- style identity：画风、材质、色彩、构图气质。
- first frame / last frame：首帧或尾帧状态。

@视频可控制：

- camera movement：运镜路线、速度、转场方式。
- action choreography：动作路线、接触点、节奏、反击、结尾后果。
- editing rhythm：切点、镜头长短、反应镜头结构。
- VFX behavior：粒子、烟尘、能量、破碎方式。
- audio rhythm：如果用户明确要求，也可作为节奏参考。

@音频可控制：

- final BGM：最终背景音乐。
- silent beat guide：只控制节奏，不输出该音频。
- SFX guide：冲击、转场、动作音效参考。
- ambience bed：风、雨、机械、室内空间声。
- voice anchor：角色或旁白声线参考。

序列帧 / 分镜图可控制：

- 镜头顺序、空间轴线、screen-left/right、主体进出画、焦点路径、首尾状态。
- 不自动控制角色身份、服装、场景质感，除非用户明确指定。

参考提示词可控制：

- 结构、节奏、动作拆法、时间轴写法、画面密度。
- 不默认复制题材、角色、世界观、专有名词。

## 参考图图文冲突规则

如果用户同时给参考图和剧情，先静默检查：

- 主体身份是否一致。
- 年龄、性别、服装、职业是否冲突。
- 地点、时代、天气、光线是否冲突。
- 关键道具、车辆、机器、怪物是否冲突。
- 图片动作状态能否承接剧情。
- 图片构图是否会限制剧情必要动作。

重大冲突时必须先问：

```text
我发现参考图与剧情存在冲突：[具体冲突]。
请你选择：
1. 保留参考图内容，我按图修改剧情描述。
2. 保留剧情内容，我提供新的生图提示词来重做参考图。
```

轻微冲突时可以继续，但要写清只借用有用锚点。

## 音频节奏锁定

当用户上传音频时，必须判断它是哪一种：

- `最终BGM + 节拍网格`：音乐作为最终声音，同时控制节奏。
- `无声节奏参考`：只控制动作、切点和镜头速度感，不输出为背景音乐。
- `音效参考`：只参考音效质感和冲击点。
- `环境声底`：作为环境声底。
- `声线参考`：作为角色或旁白声线。

提示词必须出现等价语句，默认使用中文可见表达：

```text
音频节奏锁定：@音频1 只是无声节奏参考，只控制节拍网格、动作重音、冲击点、切点和镜头速度感；不要把该参考音频输出为背景音乐。最终可听声音是现场机器轰鸣、干燥稻秆摩擦和短促静默。
```

如果音频是最终音乐：

```text
音频节奏锁定：@音频1 是最终BGM和节奏参考，只控制音乐节奏和切点重音，不控制角色身份、服装、地点、台词或镜头。
```

## 声线锁定

参考音频或视频人声作为配音时：

```text
声线锁定：@音频1 是 [旁白/角色名] 的声线参考。跨段保持音色、年龄感、口音、语速、情绪表达和麦克风质感一致。声线只控制声音，不控制脸、服装、地点或台词内容；内心独白/旁白不让画面角色对口型，除非角色正在画面中说话。
```

## 维度锁定写法

角色图：

```text
@图片1 locks the farmer's face shape, weathered skin, short gray hair, faded blue work jacket and stooped posture only. It does not control the field layout, harvester model, lighting or camera movement.
```

场景图：

```text
@图片2 locks the greenhouse width, metal pipe grid, plastic-sheet texture and muddy narrow path only. It does not control character identity or accident action.
```

视频动作参考：

```text
@视频1 locks the lateral tracking speed, stumble-recover rhythm and foreground occlusion transition only. It does not control the characters, costumes, location or color grade.
```

## 防止参考素材漂移

- 参考图里没有的物体如果必须出现，要写“new object enters this shot”。
- 参考音频是 silent guide 时，后文不能写“使用该参考音乐作为 BGM”。
- 同一角色多段输出时，每段都重复角色锚点，不依赖 GPT 记忆。
- 多张参考图同时存在时，为每张分配唯一职责，避免互相覆盖。
