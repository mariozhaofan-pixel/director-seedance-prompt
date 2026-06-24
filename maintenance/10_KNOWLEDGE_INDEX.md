# 10 Knowledge Index

priority: index
scope: 多模态宿主模型检索路由、文件职责、冲突处理

本文件只供维护和人工检查使用，不上传到任何宿主模型的运行知识库。上传后可能让模型把索引说明当成输出规则，降低回答清晰度。

## 文件职责

| 文件 | 用途 | 检索触发 |
| --- | --- | --- |
| 01_CORE_EXECUTION_CONTRACT.md | 最高行为契约、Seedance 硬约束、静默流程 | 所有复杂任务 |
| 02_REFERENCE_ROUTER_AND_LOCKS.md | @图片 / @视频 / @音频 用途、图文冲突、声线锁定 | 用户上传素材、提到参考、配音、卡点 |
| 03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md | 画面结构、空间轴线、场景功能、构图、群众调度 | 剧本、事故、动作、多人物、空间复杂 |
| 04_CAMERA_LIGHT_COLOR_STYLE.md | 摄影机、镜头、运镜、光线、色彩、画家/流派风格 | 用户要电影感、摄影风格、视觉风格 |
| 05_ACTION_PERFORMANCE_BODY_MECHANICS.md | 动作戏、真人肢体、演员表演、事故因果 | 打斗、追逐、逃亡、摔落、情绪动作 |
| 06_TIMELINE_EDITING_SOUND.md | 时间轴、切镜、转场、声音叙事、音频卡点 | 多段分镜、硬切、音频、节奏、音乐 |
| 07_STYLE_GENRE_FAMOUS_SCENE_COMPILER.md | 名场面感觉、类型语法、视觉反转 | 用户说“像某电影/动漫/名场面/感觉” |
| 08_MODEL_QC_REPAIR.md | 模型适配、Seedance QC、故障修复 | 输出前检查、用户要求修复提示词 |
| 09_LIGHTWEIGHT_TEST_REPORT.md | 自检用例、预期行为 | GPT Preview 测试、回归排查 |
| 10_KNOWLEDGE_INDEX.md | 当前索引 | 不确定该读哪个文件时 |

## 检索优先级

1. 先用 `01` 判断总流程和 Seedance 硬规则。
2. 有参考素材时用 `02`。
3. 有空间、动作、事故、多人物时用 `03` 和 `05`。
4. 有镜头、光线、色彩、风格时用 `04`。
5. 有时间轴、切镜、音频时用 `06`。
6. 用户说“感觉像某片/某动漫/某名场面”时用 `07`。
7. 输出前用 `08` 做 QC。
8. Preview 或维护时用 `09`。

## 冲突处理

- Instructions > `01` > `08` > 其他知识文件。
- Seedance 硬约束高于风格、模板和名场面复刻。
- 用户当前明确要求高于旧文件中的示例，但不能违反 Seedance 硬约束。
- 参考图与剧情重大冲突时，先提问，不自行融合。
- 音频用途不明时先按用户文字判断；仍不清楚则用最小问题确认。

## 输出模式路由

用户说“完整提示词”：

```text
直接输出分段 Seedance 提示词，不展开导演分析。
```

用户说“帮我分析 / 学习 / 拆解”：

```text
先提取可复用机制，再给可执行提示词或修补建议。
```

用户说“只要提示词”：

```text
不输出分析、解释、检查表，只输出可复制提示词。
```

用户上传参考图：

```text
先做图文一致性审查；无冲突则分配维度锁定后输出。
```

用户上传音频：

```text
先判断 final BGM / silent beat guide / SFX guide / ambience bed / voice anchor。
```

用户给已有提示词：

```text
先找稳定性漏洞：抽象词、空间不清、动作过密、素材用途不清、音频泄漏、硬切混写，再给修正版。
```

## 推荐上传方式

运行知识只使用 `knowledge/01` 到 `08`。ChatGPT 使用 `adapters/chatgpt/GPT_BUILDER_SETUP.md` 配置 Instructions；其他宿主模型使用 `adapters/universal/SYSTEM_PROMPT.md`。`09_LIGHTWEIGHT_TEST_REPORT.md` 和 `10_KNOWLEDGE_INDEX.md` 只供维护，不上传。

上传后在 Preview 中运行以下最小测试：

```text
我将提供完整剧本，给我完整的分段 Seedance 视频提示词：清晨稻田，老人捡稻穗，收割机倒车进入盲区，机器声盖过提示音。
```

合格输出应包含：

- `【基础风格】`。
- `【运镜与时间轴】` 中有 screen-left/right、foreground/midground/background、focus path、sound cue、ending state。
- 事故因果清楚，不血腥。
- 每段 <=15 秒，默认 5-15 秒，连续剧情尽量拼到 12-15 秒。
- 不按每个分镜拆段；同空间、同人物/说话者、同连续动作优先放在同一 Segment block。
