# Director Seedance Prompt

一个平台无关的 AI 视频电影语言编译系统。它把剧本、小说、参考图片、视频、音频、序列帧、分镜、已有提示词或粗略创意，转换为可直接使用的导演级视频提示词。

核心流程：

```text
Story -> Director -> Storyboard -> Prompt -> Video
```

系统默认静默完成导演意图、空间轴线、画面结构、摄影与灯光、演员动作、剪辑节奏、声音叙事、连续项目状态和模型预算判断，最终仍然输出清晰、中文优先、可复制的视频提示词。

它可以作为 Codex Skill、ChatGPT GPT，或任何支持系统提示词、知识文件和多模态输入的 Agent 使用。宿主模型负责理解和编译素材；Seedance、可灵、Veo、Runway、Pika、Sora 等目标视频模型负责生成视频。

## 主要能力

- 将连续剧情压缩为适合 Seedance 的 `5-15s` 独立生成段落。
- 明确前景、中景、后景、画面左右、人物路线、视线和焦点路径。
- 把抽象动作拆成肢体路线、力量来源、接触点、反作用和结果。
- 武戏按空手格斗、武器格斗、能量招式三路由静默编译；精确动作可锁定参考视频，所有攻防与招式写入对应 CUT，默认不显示单 CUT 秒数，也不另起打斗栏目。
- 选择景别、焦段、机位、运镜、光源、阴影、色彩和声音逻辑。
- 每段保持统一 `【基础风格】`，同时写出场景光线、空间材质或情绪变化。
- 用 `【角色/场景/素材锁定】` 管理角色、服装、场景、道具、声音及多模态参考素材的锁定用途。
- 在时间轴中使用已命名锁定对象，不反复堆叠 @图片/@视频/@音频。
- 续写/下一段时从已接受视频、尾帧或实际可见结尾开始；前后段、已完成和未来内容只进入制作台账。
- 静态末尾帧只锁定角色世界站位与相互距离；下一段直接切到新机位和新景别，场景由原剧本文字、已验收场景设定或原始场景图重新建立。
- 每条模型提示词只写本段生成事实，最终 CUT 只锁定可见 OUT，不写制作历史、未来排除项或后续预告。
- 机位连续性用摄影机位置、焦段、人物角度、人物大小和眼睛高度正向锁定，不堆同义否定句。
- 为每段分配主模型预算：角色一致性、动作幅度或场景密度，过载时拆段或降复杂度。
- 对生成结果使用 keep / post / edit / re-roll / rewrite 复盘，不盲目堆形容词重写。
- 将电影或动画的“感觉”翻译为原创、可执行的叙事机制，而不是照搬受保护内容。
- 在输出前检查空间漂移、角色消失、群众断裂、动作过载和相邻段落重复等问题。

## 使用方式

### Codex Skill

将整个仓库目录放入 Codex Skills 目录：

```text
~/.codex/skills/director-seedance-prompt/
```

Windows 默认位置通常为：

```text
%USERPROFILE%\.codex\skills\director-seedance-prompt\
```

重新打开 Codex 后即可使用 `$director-seedance-prompt`。

### ChatGPT GPT

按照 [`adapters/chatgpt/README.md`](adapters/chatgpt/README.md) 配置 GPT Builder：复制完整 Instructions，并上传 [`knowledge/01-08`](knowledge/) 共 8 个知识文件。

### 其他多模态大模型

按照 [`adapters/universal/README.md`](adapters/universal/README.md) 使用：

- 将 [`SYSTEM_PROMPT.md`](adapters/universal/SYSTEM_PROMPT.md) 设为系统提示词。
- 将 [`knowledge/01-08`](knowledge/) 作为知识库、Project 文件或 RAG 语料。
- 将剧本和参考素材作为当前任务输入。
- 宿主模型不能直接读取视频或音频时，提供关键帧、转录、时间码和声音事件表。

## 使用示例

```text
使用 $director-seedance-prompt。我将提供完整剧本，给我完整的分段 Seedance 视频提示词。
```

```text
使用 $director-seedance-prompt。分析我上传的参考图和剧情，检查冲突后生成连续分镜提示词。
```

```text
使用 $director-seedance-prompt。修复这段提示词的空间关系、动作接触点、运镜和台词时间轴。
```

```text
使用 $director-seedance-prompt。把这个粗略创意编译成具有悬疑电影感的 15 秒 Seedance 提示词。
```

## 目录结构

```text
director-seedance-prompt/
├── SKILL.md
├── knowledge/                    # 跨平台运行知识库 01-08
├── adapters/
│   ├── chatgpt/                  # GPT Builder 配置
│   └── universal/                # 通用多模态 LLM 系统提示词
├── maintenance/                  # 回归测试与维护索引，不上传
├── agents/
│   └── openai.yaml
└── references/
    ├── FILM_LANGUAGE_OPERATING_SYSTEM.md
    ├── cinematic-rule-library-v3.md
    └── neodomain-research-notes.md
```

- `SKILL.md`：入口、执行契约和输出纪律。
- `knowledge/`：ChatGPT 与其他宿主模型共用的模块化运行知识。
- `adapters/chatgpt/`：GPT Builder 创建和覆盖说明。
- `adapters/universal/`：平台无关的系统提示词、RAG 与长上下文接入方法。
- `maintenance/`：公开的回归测试和维护索引，不作为模型运行知识。
- `FILM_LANGUAGE_OPERATING_SYSTEM.md`：主要导演语言知识库与静默决策引擎。
- `cinematic-rule-library-v3.md`：兼容旧版行为的规则库。
- `neodomain-research-notes.md`：公开页面研究边界说明。

## 设计原则

1. 剧情功能优先于镜头术语。
2. 画面结构优先于抽象形容词。
3. 连续动作优先放在同一生成段落。
4. 每个切镜都必须改变信息、情绪、视角、冲突或尺度。
5. 每个独立段落都有 `【基础风格】`，不能只写“同上”。
6. 对参考素材默认只说明“控制什么”；只有存在冲突、漂移、授权、声线或音频泄漏风险时，才补充“不控制什么”。
7. 对受版权保护的作品只提炼通用机制，默认生成原创角色、场景、对白和调度。

## 兼容性边界

- 支持系统提示词和文件检索的宿主模型可以直接使用完整模块。
- 只支持长上下文的模型可以按 `SYSTEM_PROMPT -> 01 -> 08 -> 任务相关模块` 拼接。
- 多模态能力取决于宿主平台；系统不会假装已经读取无法访问的图片、视频或音频。
- 输出可用率仍受宿主模型推理能力、目标视频模型版本、素材质量和上下文长度影响。

## 来源与声明

研究来源和延伸阅读见 [SOURCES.md](SOURCES.md)。本项目与 ByteDance、Seedance 及文中提及的摄影器材、电影公司或模型服务商不存在隶属或官方合作关系；相关名称仅用于兼容性说明、技术描述或教育性引用。

## 版权与使用限制

Copyright (c) 2026 MARIOZHAOFAN. All rights reserved.

本仓库为 source-available 项目。代码、提示词结构、知识库、规则文本、适配器说明和文档均受版权保护；公开可见不代表放弃版权，也不代表允许自由再发布或商业使用。

未获得作者书面授权前，禁止以下行为：

- 复制、改名、换壳、整理后在其他仓库、网站、网盘、社群、课程或模板库中再发布。
- 将本项目整体或部分打包为付费产品、商业服务、SaaS、API、插件、GPT/Agent 商品、培训资料、代运营方案或商业交付物。
- 删除版权声明、联系方式或来源说明后分发。
- 将本项目的核心规则、知识库、提示词结构或适配器文档用于商业转售、再授权、批量交付或未授权模型/数据集训练。

允许个人学习、本地研究、非商业试用，以及通过本仓库提交 issue / PR 参与改进。商业合作、再发布、二次授权或例外许可请先联系作者。

联系方式：MARIOZHAOFAN（微信）

完整条款见 [LICENSE](LICENSE)。
