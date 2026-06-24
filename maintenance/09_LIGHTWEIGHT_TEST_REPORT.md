# 09 Lightweight Test Report

date: 2026-06-15
scope: GPT 多文件知识库包轻量回归测试

本文件只供本地维护和 Preview 手动测试使用，不上传到 GPT Knowledge。上传后会污染输出格式，让 GPT 把测试用例或 PASS 标准当成用户可见回答。

## 文件上限测试

结果：PASS。

上传 Knowledge 文件为 `01` 到 `08` 共 8 个 Markdown 文件；`00_CREATE_OR_OVERWRITE_PROMPT.md` 只用于复制 Instructions，不上传；`09_LIGHTWEIGHT_TEST_REPORT.md` 和 `10_KNOWLEDGE_INDEX.md` 只供本地维护，不上传。

说明：官方 GPT 编辑页写最多 20 个文件，文件上传 FAQ 写每个 GPT 最多 10 个文件。本包按 8 个 Knowledge 文件设计，测试报告和索引留在本地，避免 GPT 检索到内部测试文本后污染可见输出。

## 测试 1：农机 / 收割机事故文案

输入摘要：

```text
老人在稻田捡稻穗，联合收割机倒车，后方盲区被稻秆遮挡，老人没有察觉。
```

期望输出：

- 不渲染血腥。
- 先建立危险几何：收割机后方、盲区、稻秆遮挡、老人位置。
- `【基础风格】` 包含摄影机/镜头 + 光线 + 色彩。
- `【运镜与时间轴】` 写 screen-left/right、foreground/midground/background、focus path、动作部位、声音 cue、ending state。
- 倒车提示音和机器轰鸣作为声音叙事。
- 必要时拆成 2-3 个 Seedance block，而不是把多个真实 hard cut 塞进一段。

PASS 标准片段：

```text
0-3s, wide shot maps the danger geometry: harvested rice rows fill foreground, the elderly man bends in midground screen-right, the harvester rear sits background center but its blind triangle is hidden by straw. Focus starts on fallen rice ears in his hand, racks to the rear wheel line. Reverse beep is partially masked by engine rumble.
```

## 测试 2：参考图与剧情冲突

输入摘要：

```text
用户上传城市夜景参考图，但剧情是白天稻田收割机事故。
```

期望输出：

- 不直接混用城市夜景和稻田。
- 先询问用户保留图片修改剧情，还是保留剧情重做参考图。

PASS 标准：

```text
我发现参考图与剧情存在冲突：参考图是城市夜景，剧情需要白天稻田和联合收割机。请选择：1. 保留参考图内容，我按图修改剧情描述；2. 保留剧情内容，我提供新的生图提示词来重做参考图。
```

## 测试 3：参考音频只控节奏

输入摘要：

```text
用户上传鼓点音频，要求只控制切镜和动作节奏，不要作为 BGM 输出。
```

期望输出：

- 出现 AUDIO RHYTHM LOCK 或等价句。
- 明确 do not output this reference audio as BGM。
- 另写最终可听声音层。
- 只用 3-6 个主要 marker。

PASS 标准：

```text
AUDIO RHYTHM LOCK: @音频1 is a silent beat guide. It controls beat grid, motion accents, impact timing, cut markers and camera-speed feel only. Do not output this reference audio as BGM; final audible sound is diegetic machine rumble, rice-straw rustle, reverse beep and a sudden sound drop.
```

## 测试 4：硬切与一镜到底矛盾

输入摘要：

```text
用户要求一镜到底，但又要求 10 个 hard cuts、多个新机位和跨地点蒙太奇。
```

期望输出：

- 先指出矛盾。
- 如果用户优先 one continuous shot，改成 internal beats、foreground occlusion、rack focus、camera movement。
- 如果用户优先 hard cut，拆成多个 Seedance block。

PASS 标准：

```text
这两个要求冲突：one continuous shot 不能同时包含多个真实 hard cut。若保留一镜到底，我会把切换改成 internal time beats 和自然遮挡；若保留硬切，我会拆成多个独立 Seedance 提示词块。
```

## 测试 5：动作提示词稳定性

输入摘要：

```text
角色冲向对手，躲避攻击，反击，最终胜利。
```

期望输出：

- 写路线、接触点、反击、蓄势、结尾后果。
- 不只写“激烈打斗”。

PASS 标准片段：

```text
2-5s, the fighter runs from screen-left foreground to midground center; right foot plants hard, left shoulder dips under the incoming swing, left hand pushes the opponent's wrist away. Contact point is wrist against forearm; cloth rustle and one sharp foot scrape confirm the dodge.
```

## 测试 6：剧本分段打包

输入摘要：

```text
用户提供完整事故剧本，希望输出分段提示词。
```

期望输出：

- 不按每个分镜输出一段。
- 优先把同空间、同人物、同一连续动作或同一段台词拼成 5-15 秒 Seedance 段落。
- 低于 5 秒的段落只允许出现在强边界：切场景、切景别/机位变化大到影响理解、切人物/说话者、切时间状态、或动作链结束。

PASS 标准：

```text
第01段｜12-15秒｜稻田同一空间内：建立收割机、老人、盲区、倒车声和危险距离，用 4 个 internal beats 完成，不拆成 4 个独立提示词。
第02段｜6-10秒｜动作结果与反应确认，因动作链结束而单独成段。
```

## 测试 7：中文输出体验

输入摘要：

```text
用户提供普通中文剧本，要求“给我完整分段提示词”。
```

期望输出：

- 标题使用 `### 第01段｜8-15秒｜[场景功能]`。
- 栏目使用 `【基础风格】`、`【角色与场景锁定】`、`【运镜与时间轴】`、`【声音设计】`、`【画面限制】`。
- 不输出 `Segment 01`、`Shot 01`、`STYLE LOCK`、`VISUAL ANCHOR`、`CAMERA/LENS LOOK`、`Prompt:`。
- 英文只保留必要短术语，例如 `slow dolly in` 或 `rack focus`，不能整段英文。

PASS 标准：

```text
### 第01段｜12-15秒｜稻田危险区域建立
【基础风格】
【角色与场景锁定】
【运镜与时间轴】
【声音设计】
【画面限制】
```

## 发现与修补

本包已补强以下潜在漏洞：

- 把画面结构、构图、焦点路径和结尾状态并入时间轴。
- `【基础风格】` 强制前置摄影机/镜头、光线、色彩。
- 参考音频分为 final BGM、silent beat guide、SFX guide、ambience bed、voice anchor。
- 图文冲突必须先提问。
- hard cut 与 one continuous shot 不再混写。
- 动作必须按路线、接触点、反击、蓄势、后果和声音确认编译。
- 新增 Seedance 段落拼接规则：不再默认一镜一段，优先把连续剧情拼成 5-15 秒生成段落。
- 新增中文输出体验闸：最终回答不再使用英文模板标题，测试报告和索引文件不上传到 GPT Knowledge。

## 本地验证结果

结果：PASS。

- Knowledge 上传文件数量：`01` 到 `08` 共 8 个；`00` 只作为创建/覆盖提示词，不上传；`09/10` 本地维护不上传。
- 关键规则检索：`AUDIO RHYTHM LOCK`、`VOICE LOCK`、`screen-left`、`foreground`、`hard cut`、`one continuous shot`、`基础风格`、`图文一致性`、`Hitchcock`、`bullet-time`、`180 degree`、`eyeline` 均可检索。
- 分段打包规则检索：`生成段落`、`5-15秒`、`12-15秒`、`不要默认一镜一段`、`同空间`、`同主要人物`、`同一连续动作`、`动作链结束` 均可检索。
- 文本质量检查：未命中待办标记、乱码替换符或旧编码残留。
- Codex Skill 校验：在 Skill Creator 环境中运行 `quick_validate.py <skill-directory>`，预期返回 `Skill is valid!`。
