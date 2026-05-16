import argparse
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from paper_tools import load_json, normalize_paper, validate_paper


def build_environment(template_dir):
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "htm"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )


def main():
    parser = argparse.ArgumentParser(description="渲染教师版或学生版 HTML")
    parser.add_argument("input", help="输入试卷 JSON 文件路径")
    parser.add_argument("--variant", choices=["teacher", "student"], required=True, help="渲染版本")
    parser.add_argument("-o", "--output", required=True, help="输出 HTML 文件路径")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    template_dir = script_dir.parent / "assets" / "templates"
    template_name = "teacher.html.j2" if args.variant == "teacher" else "student.html.j2"

    paper = normalize_paper(load_json(args.input))
    errors = validate_paper(paper)
    if errors:
        raise SystemExit("无法渲染 HTML，试卷结构不合法:\n- " + "\n- ".join(errors))

    env = build_environment(template_dir)
    template = env.get_template(template_name)
    html = template.render(paper=paper, variant=args.variant)
    Path(args.output).write_text(html, encoding="utf-8")
    print(f"rendered {args.variant} html: {args.output}")


if __name__ == "__main__":
    main()
