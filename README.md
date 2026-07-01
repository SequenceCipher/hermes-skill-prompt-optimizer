# 灵启 Lingqi — Prompt Optimizer Skill

> Optimize, rewrite, and structure prompts without executing the task inside the prompt.

灵启是一个 Hermes Agent skill，用于将粗糙的自然语言请求、现有 prompt、system prompt、agent 指令等优化为结构清晰、行为可控的高质量提示词。**它只做 prompt 优化，不会执行 prompt 中描述的任务。**

## 支持的输入类型

- 粗糙的自然语言请求（rough request）
- 已有 prompt 的改进（existing prompt）
- System / Developer / Assistant 指令
- Tool-using / Coding / Workflow agent 指令
- Structured output / JSON / API prompt
- 附带失败示例的 prompt（failure-driven）

## 输出模式

| 模式 | 适用场景 |
|------|----------|
| `explained`（默认） | 普通 prompt 优化，输出最终提示词 + 改动说明 |
| `simple` | 只需要最终 prompt，不含解释 |
| `engineering` | System / Developer / Agent / API prompt |
| `eval` | 反复失败、生产环境、附带测试用例的 prompt |

## 安装

```bash
hermes skills install SequenceCipher/hermes-skill-lingqi
```

或者手动克隆到 `~/.hermes/skills/lingqi/`。

## 验证

内置了两个验证脚本：

- `scripts/check_prompt_artifact.py <file>` — 检查 artifact 是否存在占位符、矛盾约束、意外执行源任务等问题
- `scripts/score_prompt_shape.py <file>` — 对 prompt 结构打分（7 项 checklist），仅作结构参考

## License

MIT
