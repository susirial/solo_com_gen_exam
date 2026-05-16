import argparse
import json
import sys
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def validate_plan(plan):
    errors = []

    if not isinstance(plan, dict):
        return ["方案顶层必须是对象"]

    sections = plan.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections 必须是非空数组")
        return errors

    summed_score = 0.0
    for index, section in enumerate(sections):
        prefix = f"sections[{index}]"
        if not isinstance(section, dict):
            errors.append(f"{prefix} 不是对象")
            continue
        if not str(section.get("title") or "").strip():
            errors.append(f"{prefix}.title 缺失")
        count = number(section.get("count"), -1)
        score_per_question = number(section.get("score_per_question"), -1)
        total_score = number(section.get("total_score"), -1)
        if count <= 0:
            errors.append(f"{prefix}.count 必须大于 0")
        if score_per_question < 0:
            errors.append(f"{prefix}.score_per_question 非法")
        if total_score < 0:
            errors.append(f"{prefix}.total_score 非法")
        if count > 0 and score_per_question >= 0 and total_score >= 0:
            expected = count * score_per_question
            if abs(expected - total_score) > 1e-6:
                errors.append(f"{prefix} 总分不匹配，期望 {expected}，实际 {total_score}")
        summed_score += max(total_score, 0)

    declared_total = plan.get("total_score")
    if declared_total is not None:
        declared_total = number(declared_total, -1)
        if declared_total >= 0 and abs(declared_total - summed_score) > 1e-6:
            errors.append(f"试卷总分不匹配，sections 合计 {summed_score}，声明值 {declared_total}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="校验组卷方案")
    parser.add_argument("input", help="输入 JSON 文件路径")
    args = parser.parse_args()

    plan = load_json(args.input)
    errors = validate_plan(plan)
    if errors:
        print("plan validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("plan validation passed")


if __name__ == "__main__":
    main()
