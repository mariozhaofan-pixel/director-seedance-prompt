# Director Seedance Prompt

一个面向 AI 视频生成的电影语言编译 Skill。它把剧本、小说、参考图片、序列帧、分镜、已有提示词或粗略创意，转换为可直接使用的导演级视频提示词。

核心流程：

```text
Story -> Director -> Storyboard -> Prompt -> Video
```

系统默认静默完成导演意图、空间轴线、画面结构、摄影与灯光、演员动作、剪辑节奏和声音叙事判断，最终仍然输出清晰、中文优先、可复制的视频提示词。

## 主要能力

- 将连续剧情压缩为适合 Seedance 的 `5-15s` 独立生成段落。
- 明确前景、中景、后景、画面左右、人物路线、视线和焦点路径。
- 把抽象动作拆成肢体路线、力量来源、接触点、反作用和结果。
- 选择景别、焦段、机位、运镜、光源、阴影、色彩和声音逻辑。
- 管理角色、服装、场景、道具、声音及多模态参考素材的锁定用途。
- 将电影或动画的“感觉”翻译为原创、可执行的叙事机制，而不是照搬受保护内容。
- 在输出前检查空间漂移、角色消失、群众断裂、动作过载和相邻段落重复等问题。

## 安装

将整个仓库目录放入 Codex Skills 目录：

```text
~/.codex/skills/director-seedance-prompt/
```

Windows 默认位置通常为：

```text
C:\Users\<用户名>\.codex\skills\director-seedance-prompt\
```

重新打开 Codex 后即可使用 `$director-seedance-prompt`。

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
├── agents/
│   └── openai.yaml
└── references/
    ├── FILM_LANGUAGE_OPERATING_SYSTEM.md
    ├── cinematic-rule-library-v3.md
    └── neodomain-research-notes.md
```

- `SKILL.md`：入口、执行契约和输出纪律。
- `FILM_LANGUAGE_OPERATING_SYSTEM.md`：主要导演语言知识库与静默决策引擎。
- `cinematic-rule-library-v3.md`：兼容旧版行为的规则库。
- `neodomain-research-notes.md`：公开页面研究边界说明。

## 设计原则

1. 剧情功能优先于镜头术语。
2. 画面结构优先于抽象形容词。
3. 连续动作优先放在同一生成段落。
4. 每个切镜都必须改变信息、情绪、视角、冲突或尺度。
5. 对参考素材明确说明“控制什么”和“不控制什么”。
6. 对受版权保护的作品只提炼通用机制，默认生成原创角色、场景、对白和调度。

## 来源与声明

研究来源和延伸阅读见 [SOURCES.md](SOURCES.md)。本项目与 ByteDance、Seedance 及文中提及的摄影器材、电影公司或模型服务商不存在隶属或官方合作关系；相关名称仅用于兼容性说明、技术描述或教育性引用。

## 许可证

[MIT License](LICENSE)
