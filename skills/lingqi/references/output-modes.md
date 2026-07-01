# Output Modes

Choose the smallest output mode that satisfies the user's intent.

## simple

Use only when the user explicitly asks for only the final prompt, such as "只给我最终版" or "no explanation".

Return one fenced text block with the optimized prompt. Do not add commentary.

## explained

Default mode.

Return:

```text
## 最终提示词

<optimized prompt>

## 改动说明

- <short behavior-level change>
- <short behavior-level change>
```

Keep change notes short. Explain what changed, not a general prompt-engineering lesson.

## engineering

Use for system prompts, developer prompts, agent instructions, tool-use prompts, structured-output prompts, API prompts, and prompts intended for repeated operational use.

Return:

```text
## Target

## Success Criteria

## Optimized Prompt

## Eval Set

## Residual Risks
```

Include only sections with useful content. Do not invent deployment details.

## eval

Use when the user provides failures, bad outputs, examples, or asks how to measure prompt quality.

Return a revised prompt plus a small eval set. Each eval case should include input, expected behavior, and pass/fail criteria.

## Missing Inputs

Default behavior: make the optimized prompt ask the target model to request missing content.

Allowed:

```text
准备好后，请让我粘贴合同文本。
```

Avoid by default:

```text
[paste contract here]
{your_input}
<input>
```

Use `{{待填写：字段名 | 示例 | 默认值}}` only when the user explicitly asks for a reusable template.

