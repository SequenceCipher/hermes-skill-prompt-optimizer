# Model Adapters

Use these adapters only when the user names a model family or asks for cross-model portability.

## Universal

- Use Markdown sections.
- Define task, input, output, constraints, and uncertainty handling.
- Keep roles light unless a role changes behavior.
- Prefer positive instructions.

## GPT / OpenAI

- For API prompts, separate system, developer, and user content.
- Prefer native structured outputs, JSON schema, or tool schemas when available; do not rely only on "output valid JSON" text for production use.
- Keep durable policy outside the user payload.
- For tool use, put behavior policy in the prompt and exact argument shape in tool/schema definitions.

## Claude

- XML-style tags can help separate instructions, context, examples, and input when the prompt is complex.
- Place long context before the final task question.
- Use explicit boundaries such as `<instructions>`, `<context>`, `<examples>`, and `<output_format>` only when they reduce ambiguity.

## Gemini

- Use clear sectioning with Persona, Task, Context, and Format when useful.
- State grounding requirements for research, document QA, or factual synthesis.
- Avoid overly nested structures for simple tasks.

## DeepSeek / Qwen / Llama

- Keep instructions direct and compact.
- Provide concrete output examples for structured tasks.
- Avoid long persona framing.
- Use plain delimiters and explicit schemas for extraction, classification, and code tasks.

## Cross-Model Portability

When no target model is known:

- Write a portable base prompt.
- Add short adapter notes only if the user asked for them.
- Do not overfit wording to one vendor.

