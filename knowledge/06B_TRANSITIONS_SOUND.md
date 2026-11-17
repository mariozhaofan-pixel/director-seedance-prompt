# 06B Transitions Sound

priority: high
scope: 按需具体转场选择、主观时空/状态匹配、声音叙事层库与音频卡点

## 使用边界

需要选择具体转场、编排梦境/记忆/幻觉/状态对照，或需要扩展声音层、声音先行/静默机制、音乐与事件卡点时加载。普通CUT接力、对白/OS定位、声音基线和容量由 [06_TIMELINE_EDITING_SOUND.md](06_TIMELINE_EDITING_SOUND.md) 负责，不因每段有声音栏就自动加载本库。

本文件补充当前CUT/BEAT内的选择，不更改五栏合同、不增加审核步骤。战斗慢动作和接触时序以 [06A_COMBAT_TIMING.md](06A_COMBAT_TIMING.md) 为唯一细则；非战斗场景不加载06A。

## 转场库

| 转场 | 用途 | 稳定写法 |
| --- | --- | --- |
| hard cut | 信息/冲突/时空/情绪明确改变，或必须阻止上一 setup 延展 | `在视线转移的一刻 hard cut，从新角度露出盲区` |
| smash cut | 突然反差、惊吓、结果 | `从安静的手部动作 smash cut 到轰响的机器尾部` |
| match cut | 形状/动作连续 | `从圆形车轮 match cut 到圆形的丰收落日` |
| match on action | 动作连续剪辑 | `在拉杆的动作中切，下一镜接着同一只手的运动` |
| reaction cut | 后果确认 | `reaction cut 到工人僵住的脸` |
| J-cut | 声音先于画面 | `倒车提示音在收割机入画之前先响起` |
| L-cut | 声音延续到下镜 | `机器轰鸣延续到无声的反应镜上` |
| white flash | 爆炸、记忆、强光 | `焊花带出一次短促 white flash，随后进入新镜` |
| black flash | 眩晕、断片 | `撞击后一帧 black flash，接着声音发闷` |
| foreground occlusion | 遮罩转场、路过遮挡 | `稻秆横过前景，遮满后露出机器尾部` |
| fabric wipe | 人群、衣物、转场 | `工人的外套掠过镜头，形成自然的 fabric wipe` |
| sound bridge | 场景连接 | `同一段低频轰鸣把田地和医院走廊连起来` |
| psychic echo cut | 创伤、预感、记忆 | `在相同的手势上切，声音变远` |
| montage cutting | 时间压缩 | `工具、脸、尘土、警示牌的短 montage` |
| slow-motion insert | 非战斗局部结果，或战斗原子窗内的同一不间断强调 | `在当前不间断的镜头里，对从手中掉落的稻束做 slow motion` |
| speed ramp | 动作高潮 | `正常速度 -> 接触时放慢 -> 碎屑快速迸开` |

转场限制：foreground occlusion、fabric wipe、black flash、white flash 只能用于段内或剧情强动机的切点，不作为独立段之间的默认连接方式。遮挡转场不能替代切镜理由；动作/视线/视觉重心/声音已经足够承接时，不额外叠加遮罩。

打斗中的 `slow-motion insert` 不是自动新增CUT；若它覆盖决定性接触，必须服从06A的战斗慢动作原子窗，不能在降速、接触和第一拍反作用之间制造剪辑边界。

## 主观时空与状态匹配转场路由

当记忆、梦境、幻觉、预感、感染前后、年龄/身份状态对照或同一地点的不同时态由相同动作、姿态、物体形状、构图重心或声音触发时，先判断戏剧功能：观众需要感到“这是同一个人/动作/空间被另一种状态覆盖”，优先在当前camera setup中做状态匹配；需要突然断裂、换观察者或揭示新空间时才使用真实 CUT。

1. **冻结不变量元组**：在转场开始前锁定 `subject identity + world anchor + screen x/y + shot size + body pose/limb angles + gaze + silhouette + camera position/path + lens + framing`。若camera继续运动，两层状态必须沿同一 `C(t)` 和同一投影轨迹同步移动；不能一层移动而另一层定格。
2. **只改状态变量**：`overlay match dissolve` 用于现实A逐渐替换为记忆B，只改变剧本授权的肤色/健康、衣物清洁度、灯光、天气、布景完整度、背景活动或材质状态；人物位置、尺寸、姿态和构图保持匹配。转场完成后画面只剩目标状态，不能长期生成两个实体。
3. **双层记忆重影**：`double-exposure memory overlap` 保留现实层，同时让同一身份的记忆层在相同身体/道具锚点上短暂显现。逐层写清各自状态、动作差异、可见前后关系、出现峰值和消退终点；重影结束后只剩指定现实层，不能把记忆层误作新增角色或平行身体。
4. **CUT与BEAT边界**：无切镜的叠化/重影写在同一 `CUT N` 内，例如 `BEAT B（6-7秒，无切镜）`；CUT时码覆盖整个setup，BEAT在其内部连续分配。`match cut/psychic echo cut` 属于真实剪切，只有主动选择断裂时使用，不能拿它替代用户或导演设计的 `match dissolve/overlap`。
5. **动作与声音接力**：转场前先让触发物在画内可读，转换期间保持姿态/运动相位和视觉重心，声音按主观认知渐变，例如拖步声转成健康脚步、环境声变远、呼喊以L-cut压回现实。回到现实后的第一项动作必须从冻结相位或明确的新状态继续，不重演触发动作。

用“母题首次建立 -> 状态匹配转换 -> 记忆动作推进 -> 有理由返回现实 -> 现实选择/后果”组织整段。不要把每次回忆都默认拆成完整新setup；也不要为了减少CUT而强行锁死camera，连续运动只要两层状态共享同一camera路径和投影即可。

当一个不可逆选择必须通过随后发生的接近、接触和后果才获得情绪力量时，把这条因果链视为一个待证明的导演单元：优先在同一setup中用camera跟随、弧移、推近、构图重排或焦点交接完成，不为分别确认“决定、拥抱、接触、反应、余波”而机械切镜。只有当前机位确实无法证明新的关键信息，或有意断裂本身就是叙事动作时才切；每个新增setup都必须获得旧setup无法提供的证据。

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

### 声音卫生补充

- 不自动加甩镜呼啸、变焦提示音、揭示重击、魔法电子音或煽情音效；画面炫不等于要配“音效”。上表的魔法/能量声、UI 声只用于剧情里真实存在的声源。
- 画幅呼吸感和肩扛视感不带出拍摄者的脚步、喘息、操机声或器材碰撞声；脚步与呼吸要明确属于画面里的角色。
- 要做遮挡转场时，树、衣料、雪、烟或火实际进入镜头、覆盖并最终遮满画面，写清来源与运动，不用凭空的黑屏或白屏冒充遮挡；独立段之间的转场限制仍按上方转场库。
- 低声不等于世界静音，死寂也可以留极低的风声和呼吸。

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

2.0 通常只用 3-6 个主要 marker；2.5 可随 30 秒结构扩展到约 5-10 个主要 marker，数量不是硬目标。两版都只标真正改变动作、切点或情绪状态的重音，不逐帧卡点；剧情可读性优先于音乐卡点。
