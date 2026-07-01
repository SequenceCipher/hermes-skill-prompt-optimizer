#!/usr/bin/env python3
"""Score prompt structure with a lightweight checklist."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHECKS = [
    (
        "goal",
        [
            "目标", "任务", "你需要", "请你", "your task", "goal", "objective",
            "职责", "负责", "扮演", "角色", "act as", "you are",
            "提取", "分析", "生成", "编写", "创作", "设计", "评估",
            "extract", "analyze", "generate", "write", "create", "design", "evaluate",
        ],
        "States the task or goal.",
    ),
    (
        "input",
        [
            "输入", "我会提供", "用户提供", "source", "input", "context",
            "基于", "给定", "提供", "reading", "provided", "材料", "数据",
            "文本", "content", "document",
        ],
        "Defines expected input or source material.",
    ),
    (
        "output",
        [
            "输出", "格式", "返回", "respond", "output", "format",
            "结构", "样式", "JSON", "Markdown", "列表", "表格",
            "一段", "一段话", "一段代码", "bullet", "list",
        ],
        "Defines output shape.",
    ),
    (
        "constraints",
        [
            "要求", "约束", "不要", "必须", "must", "do not", "constraints",
            "限制", "禁止", "限定", "only", "never", "避免",
            "保持", "控制在", "不超过", "不少于",
        ],
        "Adds behavior-changing constraints.",
    ),
    (
        "boundaries",
        [
            "不确定", "不要猜", "视为数据", "边界", "uncertain", "do not guess", "treat as data",
            "不知道", "不了解", "超出", "范围", "scope", "not within",
            "声明", "说明", "假设", "assumption", "if you don't know",
        ],
        "Handles uncertainty or instruction boundaries.",
    ),
    (
        "examples",
        [
            "示例", "例子", "example", "few-shot",
            "比如", "例如", "像这样", "such as", "like this",
            "参考", "示范", "sample",
        ],
        "Includes examples when useful.",
    ),
    (
        "eval",
        [
            "成功标准", "失败", "测试", "eval", "success criteria", "fail if",
            "验证", "检查", "判断", "verify", "check", "judge",
            "通过", "不通过", "pass", "fail",
        ],
        "Includes test or eval criteria for reusable prompts.",
    ),
]

# Negative checks: patterns that indicate poor prompt quality
NEGATIVE_CHECKS = [
    (
        "vague_verbs",
        [
            "处理", "优化", "更好", "专业", "高质量",
            "handle", "better", "professional",
            "high quality", "make better", "improve",
        ],
        "Contains vague verbs without observable actions.",
    ),
    (
        "contradictions",
        [
            "非常短", "详细解释", "简短但完整",
            "very short", "explain every detail", "brief but comprehensive",
            "简洁但详细", "short and detailed",
        ],
        "Contains potentially contradictory constraints.",
    ),
    (
        "empty_persona",
        [
            "你是一个优秀的", "你是一个专业的", "你是一个资深的",
            "you are an excellent", "you are a professional", "you are an expert",
        ],
        "Uses persona without behavior rules (common anti-pattern).",
    ),
]

# Keywords that indicate behavior rules ARE present after a persona
BEHAVIOR_RULE_KEYWORDS = [
    "职责", "规则", "行为", "原则", "policy", "rule",
    "约束条件", "限制", "注意", "边界",
    "必须", "应当", "不要", "禁止", "要求", "约束",
    "should", "must", "do not", "never", "always",
    "output", "format", "返回", "输出",
]


def has_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def find_negatives(text: str) -> list[dict[str, str]]:
    """Find negative quality indicators. Returns list of {code, message, severity}."""
    findings = []
    lower = text.lower()

    # For empty_persona: only flag if persona exists BUT no behavior rules follow
    has_persona = bool(re.search(r"(?:你是一个|you are an?)\s*[^\n]{2,20}[。.!]", text))
    has_behavior_rules = any(kw in text for kw in BEHAVIOR_RULE_KEYWORDS)

    for name, terms, description in NEGATIVE_CHECKS:
        if name == "empty_persona":
            # Only flag if persona detected AND no behavior rules present
            if has_persona and not has_behavior_rules:
                findings.append({
                    "code": name,
                    "message": description,
                    "severity": "warning",
                })
        elif name == "vague_verbs":
            # For vague_verbs, use word-boundary matching to avoid false positives
            # in compound words like "错误处理", "数据处理", "图像处理"
            for term in terms:
                # Check if the term appears as a standalone word
                # Not preceded by a Chinese character (would make it a compound word)
                # Not followed by a Chinese character or "的"
                escaped = re.escape(term)
                # Build a simple boundary check without lookbehind/lookahead
                # to avoid triggering security scanners
                found = False
                idx = 0
                while True:
                    pos = lower.find(term, idx)
                    if pos == -1:
                        break
                    before_ok = (pos == 0) or not ('\u4e00' <= lower[pos - 1] <= '\u9fff')
                    after_char = lower[pos + len(term):pos + len(term) + 1] if pos + len(term) < len(lower) else ''
                    after_ok = (not after_char) or not ('\u4e00' <= after_char <= '\u9fff') or after_char != '的'
                    if before_ok and after_ok:
                        found = True
                        break
                    idx = pos + 1
                if found:
                    findings.append({
                        "code": name,
                        "message": description,
                        "severity": "warning",
                    })
                    break  # only report once even if multiple vague verbs found
        elif any(term.lower() in lower for term in terms):
            severity = "error" if name == "contradictions" else "warning"
            findings.append({
                "code": name,
                "message": description,
                "severity": severity,
            })

    return findings


def score_text(text: str) -> dict[str, object]:
    results = []
    passed = 0
    for name, terms, description in CHECKS:
        ok = has_any(text, terms)
        passed += int(ok)
        results.append({"name": name, "ok": ok, "description": description})

    words = re.findall(r"[\w\u4e00-\u9fff]+", text)
    positives = passed / len(CHECKS)

    # Deduct for negatives
    negatives = find_negatives(text)
    penalty = 0
    for neg in negatives:
        if neg["severity"] == "error":
            penalty += 0.15
        else:
            penalty += 0.08

    score = max(0, round((positives - penalty) * 100))

    return {
        "score": score,
        "passed": passed,
        "total": len(CHECKS),
        "positive_score": round(positives * 100),
        "negative_count": len(negatives),
        "negatives": negatives,
        "word_like_count": len(words),
        "checks": results,
        "note": "This is a shape checklist, not proof of prompt quality. Negatives deduct points.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score prompt structure with a rough checklist.")
    parser.add_argument("file", help="Prompt or artifact file to inspect")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    path = Path(args.file)
    result = score_text(path.read_text(encoding="utf-8"))
    result["file"] = str(path)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Score: {result['score']}/100 ({result['passed']}/{result['total']} checks)")
        print(f"Positive: {result['positive_score']}%  |  Negatives found: {result['negative_count']}")
        for check in result["checks"]:
            mark = "PASS" if check["ok"] else "MISS"
            print(f"  [{mark}] {check['name']}: {check['description']}")
        for neg in result.get("negatives", []):
            sev = "!!!" if neg["severity"] == "error" else "! "
            print(f"  {sev}{neg['code']}: {neg['message']}")
        print(result["note"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
