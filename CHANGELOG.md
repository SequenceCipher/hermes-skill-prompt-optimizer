# Changelog

所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.2.0] - 2026-06-30

### 新增
- **多语言关键词扩展**：`score_prompt_shape.py` 的关键词覆盖率提升 3 倍
- **负向检测机制**：新增模糊动词、矛盾约束、空壳人设等反模式检测
- **矛盾约束检测**：`check_prompt_artifact.py` 新增三组矛盾模式检测
- **空壳人设检测**：识别仅有角色定义而无行为规则的 prompt
- **Unicode 边界匹配**：解决"错误处理"等复合词误报问题
- **完整文档体系**：新增 README、CHANGELOG、测试记录等

### 改进
- **goal 检测增强**：新增"提取"、"分析"、"生成"等任务动词作为 goal 信号
- **误报修复**：消除 `empty_persona` 和 `vague_verbs` 的常见误报场景
- **JSON 输出增强**：score 脚本新增 `positive_score`、`negative_count`、`negatives` 字段
- **SKILL.md 重构**：标准化 frontmatter，符合 Hermes Agent 发布规范

### 修复
- 修复"错误处理"被误判为模糊动词的问题
- 修复 persona 后跟行为规则时的空壳人设误报
- 修复 `empty_persona` 检测关键词列表不完整的问题

### 安全
- 通过 Hermes 安全扫描（Verdict: SAFE）
- 消除数据泄露和混淆检测误报

## [1.1.0] - 2026-06-30

### 新增
- 基础 prompt 优化功能
- 6 种输入类型支持（粗糙请求、现有 prompt、系统指令、Agent 指令、API prompt、失败案例）
- 4 种输出模式（explained、simple、engineering、eval）
- 基本验证脚本（check 和 score）

### 改进
- 初版 SKILL.md 和参考文档
- 基础关键词检测和评分机制

## [1.0.0] - 2026-06-30

### 新增
- 初始版本发布
- 核心 prompt 优化工作流
- 基础文件结构

---

**注意**：从 1.1.0 开始，所有重要更改都将记录在此文件中。早期版本的历史记录基于开发过程中的测试和验证。
