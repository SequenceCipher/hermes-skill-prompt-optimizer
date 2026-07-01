#!/usr/bin/env python3
"""Check prompt-optimizer output artifacts for obvious rule violations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PLACEHOLDER_PATTERNS = [
    r"\[(?:paste|insert|your|input|content|topic|text)[^\]]*\]",
    r"\{(?:your|input|content|topic|text)[^}]*\}",
    r"<(?:your_)?(?:input|content|text|topic)[^>]*>",
    r"___+",
]

EXECUTION_PATTERNS = [
    "我已经帮你",
    "我已帮你",
    "以下是分析结果",
    "合同风险如下",
    "代码问题如下",
    "邮件草稿如下",
    "here is the analysis",
    "i analyzed",
    "i have reviewed",
]

FINAL_PROMPT_HEADINGS = [
    "最终提示词",
    "Optimized Prompt",
    "Final Prompt",
]

# Patterns indicating an "empty persona" prompt — just says "you are X" with no behavior rules
EMPTY_PERSONA_PATTERNS = [
    r"你是一个[^。.!]+。",
    r"you are an? [a-z]+(?!.*(?:must|should|do not|always|never|when|if.*then|output|format|要求|约束|不要|必须))",
]

# Contradiction pairs: phrases that often conflict with each other
CONTRADICTION_PAIRS = [
    (["简短", "短", "concise", "brief", "short"], ["详细", "详尽", "every detail", "comprehensive"]),
    (["一句话", "single sentence", "一句话概括"], ["分点", "列表", "bullet", "step"]),
    (["不要解释", "no explanation", "直接给"], ["说明原因", "解释", "reason", "why"]),
]

# More execution detection patterns (covering common task types)
EXECUTION_PATTERNS = [
    "我已经帮你",
    "我已帮你",
    "以下是分析结果",
    "合同风险如下",
    "代码问题如下",
    "邮件草稿如下",
    "报告如下",
    "总结如下",
    "翻译如下",
    "here is the analysis",
    "i analyzed",
    "i have reviewed",
    "here is the code",
    "i wrote",
    "生成的代码",
    "这是你的",
    "以下是你的",
]


def find_issues(text: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for pattern in PLACEHOLDER_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            issues.append(
                {
                    "code": "placeholder",
                    "message": f"Found template-like placeholder: {match.group(0)}",
                }
            )

    lower = text.lower()
    for phrase in EXECUTION_PATTERNS:
        if phrase.lower() in lower:
            issues.append(
                {
                    "code": "possible_task_execution",
                    "message": f"Possible source-task execution phrase: {phrase}",
                }
            )

    heading_count = sum(text.count(heading) for heading in FINAL_PROMPT_HEADINGS)
    if heading_count == 0:
        issues.append(
            {
                "code": "missing_final_prompt",
                "message": "No final prompt heading found.",
            }
        )
    elif heading_count > 1:
        issues.append(
            {
                "code": "multiple_final_prompts",
                "message": "Multiple final prompt headings found; output may contain competing versions.",
            }
        )

    if "改动说明" not in text and "Change Notes" not in text and "changes" not in lower:
        issues.append(
            {
                "code": "missing_change_notes",
                "message": "Default explained mode should include change notes.",
            }
        )

    # Check for contradiction pairs
    for positives, negatives in CONTRADICTION_PAIRS:
        pos_found = [p for p in positives if p.lower() in lower]
        neg_found = [n for n in negatives if n.lower() in lower]
        if pos_found and neg_found:
            issues.append(
                {
                    "code": "contradiction",
                    "message": f"Contradictory constraints detected: '{pos_found}' vs '{neg_found}'",
                }
            )

    # Check for empty persona (just "you are X" with no behavioral rules)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        if re.match(r"^你是一个[^\n]{2,20}[。.!]", line):
            # Found a "你是X" pattern — check if the rest of the text has behavior rules
            # Look for behavior-rule indicators in the ENTIRE text, not just keywords
            has_rules = any(
                kw in text
                for kw in [
                    # Direct imperative/rule keywords
                    "必须", "应当", "不要", "禁止", "要求", "约束",
                    "should", "must", "do not", "never", "always",
                    "output", "format", "返回", "输出",
                    # Behavioral structure keywords
                    "职责", "规则", "行为", "原则", "policy", "rule",
                    "约束条件", "限制", "注意", "边界",
                    # Action-oriented descriptions (indicates behavior rules exist)
                    "分析", "识别", "检查", "审查", "报告",
                    "provide", "return", "generate", "create",
                ]
            )
            if not has_rules:
                issues.append(
                    {
                        "code": "empty_persona",
                        "message": f"Empty persona detected: '{line}' — no behavioral rules follow.",
                    }
                )
            break  # only flag the first one

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check prompt optimizer artifact quality.")
    parser.add_argument("file", help="Artifact file to inspect")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")
    issues = find_issues(text)
    result = {"file": str(path), "ok": not issues, "issues": issues}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not issues:
            print("OK: no obvious prompt artifact issues found.")
        else:
            print("Issues found:")
            for issue in issues:
                print(f"- {issue['code']}: {issue['message']}")

    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())

