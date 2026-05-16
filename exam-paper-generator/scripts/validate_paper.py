import argparse
import sys

from paper_tools import load_json, normalize_paper, validate_paper


def main():
    parser = argparse.ArgumentParser(description="校验完整试卷结构")
    parser.add_argument("input", help="输入 JSON 文件路径")
    args = parser.parse_args()

    data = load_json(args.input)
    normalized = normalize_paper(data)
    errors = validate_paper(normalized)

    if errors:
        print("paper validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    section_count = len(normalized["sections"])
    question_count = sum(len(section["questions"]) for section in normalized["sections"])
    print(f"paper validation passed: sections={section_count}, questions={question_count}")


if __name__ == "__main__":
    main()
