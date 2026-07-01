# 灵启 Lingqi — Prompt Optimizer Skill

> Optimize, rewrite, and structure prompts without executing the task inside the prompt.

灵启是一个跨平台的 Prompt 优化工具，将粗糙的自然语言请求、现有 prompt、system prompt、agent 指令等优化为结构清晰、行为可控的高质量提示词。**它只做 prompt 优化，不会执行 prompt 中描述的任务。**

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](#)
[![Version](https://img.shields.io/badge/version-1.2.0-green)](CHANGELOG.md)

</div>

## ✨ 功能特性

- **粗糙请求优化**：将日常对话式的请求转化为结构化的 prompt
- **System Prompt 优化**：改进 AI 助手的系统指令和行为规则
- **Agent 指令优化**：为工具调用型 AI 创建清晰的边界和操作规范
- **失败案例修复**：基于实际失败经验迭代优化 prompt
- **结构化输出**：生成 JSON、表格等格式化输出的 prompt
- **多平台支持**：Hermes Agent、Claude Code、Codex、OpenCode

## 支持的输入类型

| 类型 | 说明 |
|------|------|
| `rough-request` | 自然语言任务想法，尚未形成 prompt |
| `existing-prompt` | 想要改进的已有 prompt |
| `system-or-developer` | System prompt、Developer prompt、GPT/Gem/Assistant 指令 |
| `agent` | 工具调用、编码、工作流或自主 agent 指令 |
| `api-or-structured` | 结构化输出、JSON、提取、分类、工具或 API 调用的 prompt |
| `failure-driven` | 附带失败输出的 prompt，用于针对性修复 |

## 输出模式

| 模式 | 适用场景 |
|------|----------|
| `explained`（默认） | 普通 prompt 优化，输出最终提示词 + 改动说明 |
| `simple` | 只需要最终 prompt，不含解释 |
| `engineering` | System / Developer / Agent / API prompt |
| `eval` | 反复失败、生产环境、附带测试用例的 prompt |

## 📦 安装

### Hermes Agent

```bash
# 方式一：通过 Skills Hub 搜索安装
hermes skills search lingqi
hermes skills install lingqi

# 方式二：通过 raw URL 直接安装
hermes skills install https://raw.githubusercontent.com/SequenceCipher/hermes-skill-lingqi/main/SKILL.md --name lingqi
```

### Claude Code

将 SKILL.md 的内容放入 `.claude/skills/lingqi.md`：

```bash
mkdir -p .claude/skills
curl -sL https://raw.githubusercontent.com/SequenceCipher/hermes-skill-lingqi/main/SKILL.md \
  > .claude/skills/lingqi.md
```

Claude Code 会自动加载 `.claude/skills/*.md` 作为 skills。

### OpenCode

```bash
# 加载为附加文件
opencode run "优化这个 prompt..." \
  -f SKILL.md
```

### 手动安装

```bash
# 下载整个仓库
git clone https://github.com/SequenceCipher/hermes-skill-lingqi.git
cd hermes-skill-lingqi
```

所有文件均可独立使用 — `SKILL.md` 是核心，`references/` 和 `scripts/` 为可选增强。

## 📁 项目结构

```
hermes-skill-lingqi/
├── SKILL.md              # 核心技能定义（所有平台通用）
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

## 🔧 使用示例

**输入**（粗糙请求）：
> 我想让 AI 帮我优化一个 prompt

**优化后**（explained 模式）：
```
## 最终提示词

你是一个 Prompt 优化专家，专门帮助用户改进他们的提示词...

## 改动说明

- 明确了角色定义和行为规则
- 添加了输入分类和输出模式选择
- 补充了自检查验步骤
```

## ✅ 验证

内置了两个验证脚本：

```bash
# 检查优化后的 prompt 是否存在明显问题
python3 scripts/check_prompt_artifact.py optimized-prompt.md

# 获取 prompt 的结构评分（满分 100）
python3 scripts/score_prompt_shape.py optimized-prompt.md
```

## 🛡️ 安全特性

- **Prompt 注入防护**：将隐藏指令视为数据而非可执行命令
- **数据边界保护**：明确区分 AI 指令和用户数据
- **隐私保护**：不收集或传输任何用户数据
- **本地运行**：所有处理都在本地完成

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🔗 相关链接

- [Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs)
- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code/overview)
- [OpenAI Codex 文档](https://github.com/openai/codex)

---

<div align="center">

**Made with ❤️ by SequenceCipher**

⭐ Star this repo if you find it useful!

</div>
