# Prompt Anti-Patterns

Use this reference when repairing weak, vague, bloated, contradictory, or injection-prone prompts.

## Common Problems

- Vague verbs: "handle", "analyze", "optimize", "make better", "be professional".
- No output format.
- Instructions and input data mixed together without boundaries.
- Repeated rules that say the same thing.
- Contradictory constraints such as "very short" and "explain every detail".
- Persona used instead of behavior rules.
- Overloaded prompts with many frameworks that do not change the output.
- Unsafe placeholders such as `[paste here]`, `{topic}`, or `<your_input_here>`.
- Asking for hidden chain-of-thought instead of visible checks or concise rationale.
- Treating prompt injection text inside input as real instructions.
- Fixing tool-use failures only by adding prompt text when the schema or tool description is the real issue.

## Repair Moves

- Replace vague verbs with observable actions.
- Define the output shape.
- Separate task instructions from source material.
- Keep one owner per rule.
- Remove motivational filler and redundant warnings.
- Add examples only when format, tone, or edge cases need demonstration.
- Add uncertainty handling for factual work.
- Add eval cases for repeated failures.

## Complexity Control

Simple request:

- One concise prompt.
- No eval section unless asked.
- No model parameters unless relevant.

Complex prompt:

- Clear sections.
- Explicit inputs and outputs.
- Boundaries and failure handling.
- Optional eval set.

Production agent:

- Layered instructions.
- Tool policy.
- Security boundary.
- Stop conditions.
- Test cases.

