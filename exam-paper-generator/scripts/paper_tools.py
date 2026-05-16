import json
from pathlib import Path


QUESTION_TYPE_TITLES = {
    "single_choice": "选择题",
    "multiple_choice": "多项选择题",
    "true_false": "判断题",
    "fill_blank": "填空题",
    "short_answer": "简答题",
    "calculation": "计算题",
    "application": "应用题",
    "reading": "阅读理解",
    "essay": "作文题",
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _string(value, default=""):
    if value is None:
        return default
    return str(value)


def _number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _question_defaults(question, section_index, question_index, section_type):
    qid = _string(question.get("id"), f"s{section_index + 1}q{question_index + 1}")
    qtype = _string(question.get("type"), section_type or "short_answer")
    options = question.get("options")
    if not isinstance(options, list):
        options = None
    score = _number(question.get("score"), 0)
    return {
        "id": qid,
        "type": qtype,
        "stem": _string(question.get("stem"), "（题干缺失）"),
        "options": options,
        "answer": _string(question.get("answer"), ""),
        "analysis": _string(question.get("analysis"), ""),
        "score": score,
        "difficulty": _string(question.get("difficulty"), "medium"),
        "knowledge_points": list(question.get("knowledge_points") or []),
        "material": question.get("material"),
    }


def normalize_paper(data):
    paper = dict(data or {})
    meta = dict(paper.get("meta") or {})
    title = _string(paper.get("title"), "未命名试卷")
    sections_raw = list(paper.get("sections") or [])
    normalized_sections = []
    total_score = 0.0

    for section_index, raw_section in enumerate(sections_raw):
        raw_section = dict(raw_section or {})
        section_type = _string(raw_section.get("type"), "short_answer")
        questions_raw = list(raw_section.get("questions") or [])
        questions = []
        section_score = 0.0

        for question_index, raw_question in enumerate(questions_raw):
            question = _question_defaults(raw_question or {}, section_index, question_index, section_type)
            section_score += question["score"]
            questions.append(question)

        total_score += section_score
        section_title = _string(
            raw_section.get("title"),
            f"第{section_index + 1}节 {QUESTION_TYPE_TITLES.get(section_type, section_type)}",
        )
        instructions = _string(
            raw_section.get("instructions"),
            f"共 {len(questions)} 题，共 {int(section_score) if section_score.is_integer() else section_score} 分",
        )
        normalized_sections.append(
            {
                "title": section_title,
                "type": section_type,
                "instructions": instructions,
                "total_score": section_score,
                "shared_material": raw_section.get("shared_material"),
                "questions": questions,
            }
        )

    meta.setdefault("stage", "")
    meta.setdefault("grade", "")
    meta.setdefault("subject", "")
    meta.setdefault("exam_type", "")
    meta.setdefault("duration_minutes", 0)
    meta["total_score"] = total_score

    return {
        "title": title,
        "meta": meta,
        "sections": normalized_sections,
    }


def validate_paper(data):
    errors = []

    if not isinstance(data, dict):
        return ["试卷顶层必须是对象"]

    if not _string(data.get("title")).strip():
        errors.append("缺少 title")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append("缺少 meta 或 meta 不是对象")

    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections 必须是非空数组")
        return errors

    for section_index, section in enumerate(sections):
        prefix = f"sections[{section_index}]"
        if not isinstance(section, dict):
            errors.append(f"{prefix} 不是对象")
            continue
        if not _string(section.get("title")).strip():
            errors.append(f"{prefix}.title 缺失")
        questions = section.get("questions")
        if not isinstance(questions, list) or not questions:
            errors.append(f"{prefix}.questions 必须是非空数组")
            continue
        for question_index, question in enumerate(questions):
            qprefix = f"{prefix}.questions[{question_index}]"
            if not isinstance(question, dict):
                errors.append(f"{qprefix} 不是对象")
                continue
            for field in ("id", "type", "stem"):
                if not _string(question.get(field)).strip():
                    errors.append(f"{qprefix}.{field} 缺失")
            try:
                float(question.get("score"))
            except (TypeError, ValueError):
                errors.append(f"{qprefix}.score 非法")

    return errors
