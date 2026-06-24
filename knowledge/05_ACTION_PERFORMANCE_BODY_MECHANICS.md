# 05 Action Performance Body Mechanics

priority: high
scope: 动作戏、真人肢体、演员情绪、冲突因果、事故动作、表演锚定

## 动作提示词总规则

动作要有：

1. 路线：从哪里到哪里，穿过什么空间。
2. 接触点：身体、道具、机器、地面或对手在哪个点接触。
3. 力量来源：脚蹬地、肩带动、腰拧转、机器惯性、重力、风压。
4. 反击或阻力：对方、环境、道具或身体失衡如何改变动作。
5. 蓄势：高潮前的停顿、吸气、压低重心、举起道具。
6. 后果：倒退、撞击、碎片、沉默、物体位置变化、表情变化。
7. 声音确认：脚步、衣料、金属、呼吸、撞击、低频、静默。

这套规则来自动作游戏提示词的可复用部分，但应用到真人世界时要把雷电、装备、BOSS 替换成身体、道具、空间、声音和沉默。

## 身体部位动作写法

抽象：

```text
老人害怕地躲开。
```

可执行：

```text
his left foot slips backward in mud, right knee bends, shoulders twist away from the machine, left hand drops the rice bundle, eyes widen but his mouth stays half-open without a shout.
```

抽象：

```text
司机突然意识到危险。
```

可执行：

```text
his eyes flick from the rear mirror to the blind spot, right hand freezes on the reverse lever, jaw tightens, breath stops for half a second.
```

## 表情和动作分开写

角色表演要分层：

- 面部层：眼睛、眉、嘴、下颌、呼吸。
- 身体层：肩、手、脚、重心、姿态。
- 节奏层：停顿、迟疑、加速、突然停止。
- 反应层：看、听、退、抓、僵住、回头。

示例：

```text
脸部冷静无表情，身体快速、有目的地向前走。
```

```text
calm face, but both hands grip the steering wheel too tightly; shoulders are raised, breathing shallow.
```

## 动作类型库

| 动作类型 | 必须写清 | 稳定提示词内核 |
| --- | --- | --- |
| 追逐 | 追者/被追者路线、障碍、距离变化 | `screen-right chase line, foreground obstacles pass fast, distance closes from 5m to 2m` |
| 逃亡 | 出口、堵点、回头、失误 | `escape route blocked by crowd, subject pivots left, slips at threshold` |
| 贴身搏斗 | 接触点、重心、反击 | `wrist grab, shoulder turn, knee blocks escape, body weight drives both into wall` |
| 巨物角力 | 人与巨物尺度、支点、失败点 | `human hands push against metal surface, machine inertia wins` |
| 救援 | 路线、时间压力、可达性 | `rescuer enters from screen-left, cannot cross the moving belt in time` |
| 摔落 | 高度、重心、接触地面顺序 | `heel slips, hip hits first, shoulder follows, dust jumps from ground` |
| 滑铲 | 起点、腿部、地面材质、结果 | `right leg extends, left hand skims muddy ground, body slides under pipe` |
| hit and run | 接触瞬间和逃逸方向 | `rear bumper strikes left shoulder, vehicle continues screen-right for one meter` |
| 道具战斗 | 道具重量、握法、碰撞点 | `two-hand grip, shovel edge strikes wooden post, splinters fly` |
| 团队接力 | 角色顺序、交接物、失败风险 | `worker A throws rope to worker B, rope lands short in mud` |
| 空中接力 | 轨迹、高度、落点 | `tool arcs from foreground left to midground right, caught at chest height` |
| 怪物围攻 | 包围方向、缺口、主角路线 | `three creatures close from left/right/background, only foreground gap remains` |
| 群体混战 | 主方向、局部冲突、焦点主体 | `crowd flows left, two figures collide in midground, hero stays centered` |

## 动作高潮结构

动作高潮不要一开始就爆发。推荐：

1. setup：建立空间、路线、危险点。
2. pressure：危险逼近，距离缩短。
3. counter：角色尝试躲避或反击。
4. failure / reversal：动作失败、误判、被阻挡。
5. impact：接触点清楚。
6. aftermath：结果镜头，声音或沉默确认。

## 事故 / 工业安全叙事

事故类提示词重点是清楚呈现因果，不做猎奇渲染：

- 先建立危险区域和盲区。
- 让固定危险物和移动机器分开写。
- 用声音遮蔽信息：machine rumble covers warning sound。
- 用焦点路径让观众先看到危险，再看到角色没有看到。
- 接触点可以用遮挡、反应、物体停止、静默代替血腥。

示例：

```text
The fixed metal pipe remains screen-left foreground at neck height; the tractor handlebar slowly reverses from midground right toward it. Focus starts on the driver's turned head, rack focuses to the narrowing gap between pipe and handlebar. Sound narrows to engine rumble and a short cloth scrape; no graphic injury, only the machine stopping and workers freezing in background.
```

## 情绪动作映射

| 情绪 | 表演动作 | 镜头策略 |
| --- | --- | --- |
| 压抑恐惧 | 眼睛不眨、肩膀僵、呼吸变浅 | slow dolly in / low-key |
| 惊觉 | 眼神跳转、手停在按钮上 | ECU/CU + sound drop |
| 无助 | 手够不到目标、脚陷住 | wide shot shows distance |
| 决心 | 下颌收紧、重心前移 | centered MCU + push-in |
| 悔意 | 目光下落、身体后退 | held close-up + silence |
| 麻木 | 表情平、动作机械 | locked-off frame |

## 角色锚定

跨段保持角色一致时，每段都重写：

- face anchor：脸型、年龄感、发型、眼神。
- costume anchor：服装颜色、材质、磨损。
- posture anchor：站姿、走路方式、习惯动作。
- voice anchor：音色、语速、口音、情绪表达。
- flaw anchor：固执、迟疑、骄傲、粗心、过度自信。
- relationship anchor：父女、师徒、雇佣、对抗、命运感应。
