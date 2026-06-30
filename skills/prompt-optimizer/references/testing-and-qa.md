# Testing & QA Notes

## Script Limitations

### `score_prompt_shape.py` — Known Gaps

- `vague_verbs` uses Unicode boundary matching to avoid false positives in compound words (e.g., "错误处理"). However, standalone uses of "处理", "优化" in a positive context may still trigger. Treat as advisory, not a defect.
- `empty_persona` correctly suppresses when a persona line is followed by behavior rules. It may still miss edge cases where rules use indirect phrasing (e.g., implied rules without explicit keywords).
- Score is purely structural — a prompt can score 0/100 but still work well for simple one-off tasks.

### `check_prompt_artifact.py` — Known Gaps

- Contradiction detection only checks predefined pairs. Custom contradictions in user prompts are not caught.
- Empty persona detection is limited to the first `你是X。` line. Multi-persona prompts only get one check.
- Execution detection relies on phrase matching; prompts that describe task execution (e.g., "说明：以下是分析结果") may trigger false positives.

## Test History

### 2026-06-30 — Full 6-scenario validation

All scenarios passed check script (no issues). Scores ranged 63-78/100.

| # | Scenario | Score | Key Finding |
|---|----------|-------|-------------|
| 1 | Rough request → photo renamer | 63 | Missing eval/examples — acceptable for one-off |
| 2 | System prompt — "can fabricate answers" | 78 | Successfully caught and removed dangerous instruction |
| 3 | Agent instruction — code reviewer | 78 | Added tool policy, boundaries, stop conditions |
| 4 | Failure-driven — contract analyzer | 78 | All 7 checks passed; hallucination prevention added |
| 5 | Structured output — JSON extractor | 63 | Clean schema, no examples needed for technical prompt |
| 6 | Injection attack defense | 78 | empty_persona false-positive fixed via BEHAVIOR_RULE_KEYWORDS |

## Pitfalls Discovered

1. **empty_persona false-positive**: When a prompt starts with "你是XX" followed by a "职责" or "分析" section, the old checker incorrectly flagged it as empty persona. Fix: expand behavior-rule keyword list to include structural indicators ("职责", "规则", "分析", "识别", "审查").
2. **goal detection gap**: Task verbs like "提取", "分析", "生成" were not recognized as goal signals. Fix: added to CHECKS goal keyword list.
3. **vague_verbs compound word false-positive**: "错误处理" triggered vague_verbs because "处理" matched. Fix: Unicode boundary matching to exclude compound words.
4. **vague_verbs task verb overlap**: "分析" and "生成" are both goal signals AND vague verbs. Fix: removed from vague_verbs list; they belong in goal detection only.
