# Maintenance Files

本目录供维护者测试和检查知识库，不属于宿主模型的运行知识：

- `09_LIGHTWEIGHT_TEST_REPORT.md`：回归测试输入、预期行为和验收标准。
- `10_KNOWLEDGE_INDEX.md`：模块职责、检索路由和冲突排查索引。

不要把本目录上传到 ChatGPT Knowledge、Claude Project Knowledge、Gemini Gem、RAG 运行语料或其他 Agent 知识库。模型检索到测试用例和索引文字后，可能把 `PASS` 标准、内部文件名或英文模板泄露到用户输出。

维护流程：更新运行规则后，补充对应测试用例；在目标宿主模型的预览环境中运行测试，但只上传 `knowledge/01-08`。
