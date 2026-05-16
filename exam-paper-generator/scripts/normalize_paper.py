import argparse

from paper_tools import load_json, normalize_paper, save_json


def main():
    parser = argparse.ArgumentParser(description="归一化试卷 JSON 结构")
    parser.add_argument("input", help="输入 JSON 文件路径")
    parser.add_argument("-o", "--output", required=True, help="输出 JSON 文件路径")
    args = parser.parse_args()

    data = load_json(args.input)
    normalized = normalize_paper(data)
    save_json(args.output, normalized)
    print(f"normalized: {args.output}")


if __name__ == "__main__":
    main()
