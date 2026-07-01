# Eval Design

Use eval design for production prompts, repeated failures, prompts with examples, or when the user asks to test quality.

## When To Add Evals

Add a small eval set when:

- The prompt will be reused many times.
- The user reports repeated bad outputs.
- The prompt controls an agent, tool use, structured output, extraction, classification, legal/financial/medical review, or business-critical workflow.
- The user provides expected outputs or failure cases.

Do not add evals for simple one-off writing, translation, or light rewrite requests unless asked.

## Eval Case Shape

Use this compact shape:

```text
Case: <name>
Input: <representative input>
Expected behavior: <what good output must do>
Fail if: <concrete failure condition>
```

### 中文示例

```text
Case: 短合同无风险
Input: 一份3页的简单租房合同，条款常规
Expected behavior: 标注"无明显高风险条款"，列出2-3个常规条款说明
Fail if: 虚构了不存在的风险条款
```

```text
Case: 含免责条款的服务协议
Input: 一份包含"本公司对所有损失不承担责任"的服务协议
Expected behavior: 明确标注该免责条款过于宽泛，建议限定范围
Fail if: 忽略该条款或过度警告所有免责条款
```

```text
Case: 中英文混合输入
Input: "Please review this clause: The contractor shall be liable for all damages."
Expected behavior: 用用户相同的语言回复，指出"all damages"过于绝对
Fail if: 切换到不同语言回复或忽略英文部分
```

## Success Criteria

Write observable criteria:

- Output includes required fields.
- Output omits prohibited content.
- Output marks uncertainty instead of guessing.
- Output references source material when the task requires it.
- Output stays within the requested length or format.
- Output refuses or redirects unsafe requests when required.

Avoid vague criteria such as "high quality", "clear", or "professional" unless they are tied to visible behavior.

### 好的成功标准 vs 差的成功标准

| ❌ 差的 | ✅ 好的 |
|--------|--------|
| "输出质量好" | "输出包含所有必填字段" |
| "回答专业" | "对法律/医疗/财务内容标注不确定性" |
| "简洁明了" | "输出不超过500字" |
| "有帮助" | "引用了输入材料中的具体内容" |

## Failure-Driven Optimization

When the user gives a bad output:

1. Identify the failure type (wrong format, missed content, hallucination, language mismatch, etc.).
2. Convert it into an eval case.
3. Adjust the prompt minimally — change only what's necessary.
4. Add a no-regression case for behavior that already worked.

### 常见失败类型与修复策略

- **格式错误** → 在 prompt 中明确输出结构（Markdown标题、JSON字段、列表项数）
- **遗漏内容** → 添加"必须包含"清单，逐项对照
- **幻觉/编造** → 添加"只基于提供的材料"约束和"不确定时声明"规则
- **语言不匹配** → 添加"使用用户输入的语言回复"规则
- **过度冗长** → 添加字数/段落上限约束

## Stop Conditions

Stop iterating when:

- The eval cases pass.
- The failure is caused by missing source data, retrieval quality, tool schema, or model capability rather than wording.
- Further prompt complexity would make the prompt harder to maintain.

## Adding No-Regression Cases

After fixing a failure, always add a no-regression case:

```text
Case: no-regression-<original-case-name>
Input: <the exact input that previously failed>
Expected behavior: <the corrected behavior>
Fail if: <the original failure reappears>
```

This ensures the fix doesn't break in future iterations.

