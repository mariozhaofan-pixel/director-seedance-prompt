# ChatGPT GPT 配置

本目录用于在 ChatGPT GPT Builder 中创建或更新“电影语言操作系统”。

## 创建方式

1. 打开 GPT Builder 的配置页面。
2. 按 [GPT_BUILDER_SETUP.md](GPT_BUILDER_SETUP.md) 填写名称、描述、Instructions 和 4 个开场问题。
3. 从仓库的 [`knowledge/`](../../knowledge/) 上传 `01` 到 `08` 共 8 个 Markdown 文件。
4. 不要上传 `GPT_BUILDER_SETUP.md`、`maintenance/09_LIGHTWEIGHT_TEST_REPORT.md` 或 `maintenance/10_KNOWLEDGE_INDEX.md`。
5. 在 Preview 中用 `maintenance/09_LIGHTWEIGHT_TEST_REPORT.md` 做轻量回归测试。

## 更新已有 GPT

- 先备份旧 Instructions。
- 用 `GPT_BUILDER_SETUP.md` 中的 Instructions 全量覆盖，不要在旧规则前后增量追加。
- 删除旧 Knowledge 中重复、过时或超大单文件，再重新上传当前 `01-08`。
- 如果输出出现英文模板标题、测试说明或知识库索引，检查是否误上传了维护文件。

## 能力建议

启用图片和文件输入。视频、音频是否能直接读取取决于当前 ChatGPT 产品能力；无法直接解析时，提供关键帧、转录文本、时间码或声音事件表。
