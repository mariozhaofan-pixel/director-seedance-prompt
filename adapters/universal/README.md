# Universal Multimodal LLM Adapter

这个适配器面向任何支持以下一种或多种能力的宿主模型：系统提示词、自定义 Agent、文件上传、知识库检索、图片理解、视频理解或音频理解。

“宿主模型”负责分析与编译，例如 ChatGPT、Claude、Gemini、Qwen 或本地多模态模型；“目标视频模型”负责最终生成视频，例如 Seedance、可灵、Veo、Runway、Pika 或 Sora。两者不是同一个概念。

## 方式 A：自定义 Agent / Bot

1. 将 [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md) 设为系统提示词。
2. 上传 [`knowledge/01-08`](../../knowledge/) 作为知识文件。
3. 将用户的剧本、参考图片、视频、音频、序列帧或已有提示词作为当前任务输入。
4. 默认目标视频模型是 Seedance；用户指定其他模型时按 `08_MODEL_QC_REPAIR.md` 适配。

## 方式 B：单次长上下文

按以下顺序拼接上下文：

```text
SYSTEM_PROMPT.md
knowledge/01_CORE_EXECUTION_CONTRACT.md
knowledge/02_REFERENCE_ROUTER_AND_LOCKS.md
knowledge/03_VISUAL_GRAMMAR_AND_SCENE_ROUTER.md
knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md
knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md
knowledge/06_TIMELINE_EDITING_SOUND.md
knowledge/07_STYLE_GENRE_FAMOUS_SCENE_COMPILER.md
knowledge/08_MODEL_QC_REPAIR.md
用户当前素材与要求
```

上下文不足时保留 `SYSTEM_PROMPT + 01 + 08`，再根据任务选择最相关模块，不要优先删掉角色、场景、空间方向、时间轴和目标模型约束。

## 方式 C：API / RAG

- 系统提示词固定使用 `SYSTEM_PROMPT.md`。
- 每次检索固定召回 `01` 和 `08`。
- 根据图片、视频、音频、动作、摄影、台词、类型感觉等触发词召回 `02-07`。
- 返回给模型的知识片段必须保留标题和模块来源，但最终用户输出不得泄露内部检索说明。
- 对长视频先生成关键帧、镜头边界、转录、说话人和声音事件，再交给本系统编译。

## 多模态退化策略

- 不能看图片：让用户提供画面主体、左右位置、前中后景、服装、道具、光线和冲突点。
- 不能读视频：提供关键帧、时间码、镜头表、动作路线和转录文本。
- 不能听音频：提供逐字稿、说话人、情绪、节拍点、音效事件和静默区间。
- 模型无法确认素材内容时必须说明限制，不能假装已经观看或听取。

## 最小测试

```text
目标视频模型：Seedance。
我将提供完整剧本，请输出完整的 5-15 秒分段提示词。台词必须放入对应时间轴；同空间、同人物、同一连续动作优先放在同一段。
```
