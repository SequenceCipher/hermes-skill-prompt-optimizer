# Prompt Optimizer Skill for Hermes Agent

<div align="center">

**智能提示词优化工具** — 将粗糙的请求、现有提示词、系统指令转化为清晰、可执行的优质 prompt

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20|%20macOS%20|%20Linux-blue)](#)
[![Version](https://img.shields.io/badge/version-1.2.0-green)](CHANGELOG.md)

</div>

## 📋 简介

Prompt Optimizer 是一个 Hermes Agent 技能，帮助你优化各种类型的提示词。无论你是想让 AI 更好地回答问题、生成代码、还是执行复杂任务，这个工具都能让你的 prompt 更加清晰、有效。

## ✨ 功能特性

- **粗糙请求优化**：将日常对话式的请求转化为结构化的 prompt
- **系统提示词优化**：改进 AI 助手的系统指令和行为规则
- **Agent 指令优化**：为工具调用型 AI 创建清晰的边界和操作规范
- **失败案例修复**：基于实际失败经验迭代优化 prompt
- **结构化输出**：生成 JSON、表格等格式化输出的 prompt
- **安全边界**：防止 prompt 注入攻击，保护 AI 行为边界

## 🚀 快速开始

### 安装

```bash
# 通过 URL 安装
hermes skills install https://raw.githubusercontent.com/SequenceCipher/hermes-skill-prompt-optimizer/main/SKILL.md --name prompt-optimizer

# 或通过 skills hub 搜索安装
hermes skills search prompt-optimizer
hermes skills install prompt-optimizer
```

### 使用方法

在 Hermes Agent 中直接要求优化你的 prompt：

```
帮我优化这个提示词：[你的原始 prompt]
```

或者使用快捷方式：

```
$prompt-optimizer [你的原始 prompt]
```

### 示例

**输入**：
> 我想让 AI 帮我写一个 Python 脚本，用来批量重命名文件夹里的照片

**优化后**：
> 你是一个 Python 脚本编写专家。请帮我生成一个批量重命名照片的 Python 脚本。
> 
> **任务描述**：
> - 遍历指定文件夹中的所有图片文件（支持 JPG/JPEG/PNG/HEIC/GIF 格式）
> - 从图片文件的 EXIF 元数据中提取拍摄日期（DateTimeOriginal）
> - 如果 EXIF 中无可用的拍摄日期，则使用文件修改时间作为备选
> - 按照 `YYYYMMDD_HHMMSS_原文件名` 的格式重命名文件
> - 生成一份重命名日志文件，记录每个文件的原名、新名和使用的日期来源
> 
> **约束**：
> - 脚本需要先预览重命名结果，不直接修改文件（提供一个 `--dry-run` 标志）
> - 遇到重名文件时自动添加序号后缀
> - 包含完整的错误处理和用户友好的命令行提示

## 📁 项目结构

```
hermes-skill-prompt-optimizer/
├── SKILL.md              # 主技能文件（Hermes Agent 加载）
├── README.md             # 项目说明文档
├── CHANGELOG.md          # 版本变更记录
├── LICENSE               # MIT 许可证
├── agents/               # 特定平台的 Agent 配置
│   └── openai.yaml       # OpenAI Codex 配置
├── references/           # 参考文档
│   ├── agent-prompts.md  # Agent 指令最佳实践
│   ├── anti-patterns.md  # 常见反模式和修复方法
│   ├── eval-design.md    # 评估设计和成功标准
│   ├── model-adapters.md # 模型适配指南
│   ├── output-modes.md   # 输出模式说明
│   └── testing-and-qa.md # 测试记录和已知限制
└── scripts/              # 验证脚本
    ├── check_prompt_artifact.py    # Prompt 质量检查
    └── score_prompt_shape.py       # Prompt 结构评分
```

## 🔧 高级用法

### 不同输出模式

根据需求选择不同的优化深度：

- **基础优化**：仅改进语言表达和结构
- **工程级优化**：添加安全边界、错误处理、输出格式
- **Agent 优化**：为工具调用型 AI 创建完整的行为规范
- **评估优化**：添加测试用例和质量标准

### 使用验证脚本

```bash
# 检查优化后的 prompt 是否存在明显问题
python3 scripts/check_prompt_artifact.py optimized-prompt.md

# 获取 prompt 的结构评分
python3 scripts/score_prompt_shape.py optimized-prompt.md
```

### 自定义配置

编辑 `agents/openai.yaml` 可以针对特定 AI 模型优化 prompt 格式。

## 🛡️ 安全特性

- **Prompt 注入防护**：自动检测和防御恶意指令注入
- **数据边界保护**：明确区分 AI 指令和用户数据
- **隐私保护**：不收集或传输任何用户数据
- **本地运行**：所有处理都在本地完成，无需网络连接

## 📊 版本历史

详见 [CHANGELOG.md](CHANGELOG.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🔗 相关链接

- [Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs)
- [Prompt Engineering 指南](references/agent-prompts.md)
- [反模式参考](references/anti-patterns.md)

---

<div align="center">

**Made with ❤️ by SequenceCipher for the Hermes Agent community**

⭐ Star this repo if you find it useful!

</div>
