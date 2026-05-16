# 统一试卷结构

所有试卷内容在渲染前都应整理为统一结构。

## 顶层结构

```json
{
  "title": "试卷标题",
  "meta": {
    "stage": "初中",
    "grade": "初二",
    "subject": "数学",
    "exam_type": "期中试卷",
    "duration_minutes": 90,
    "total_score": 100
  },
  "sections": []
}
```

## section 结构

```json
{
  "title": "一、选择题",
  "type": "single_choice",
  "instructions": "共 10 题，每题 3 分，共 30 分",
  "total_score": 30,
  "shared_material": null,
  "questions": []
}
```

## question 结构

```json
{
  "id": "s1q1",
  "type": "single_choice",
  "stem": "题干文本",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "answer": "A",
  "analysis": "解析或评分要点",
  "score": 3,
  "difficulty": "easy",
  "knowledge_points": ["知识点 1"],
  "material": null
}
```

## 题型建议枚举

- `single_choice`
- `multiple_choice`
- `true_false`
- `fill_blank`
- `short_answer`
- `calculation`
- `application`
- `reading`
- `essay`

## 字段要求

- `title` 必填
- `meta` 必填
- `sections` 必填，且至少有一节
- 每个 section 必须有 `title`、`questions`
- 每个 question 必须有 `id`、`type`、`stem`、`score`
- 教师版渲染依赖 `answer` 和 `analysis`
- 学生版可以不显示 `answer`、`analysis`，但结构中仍建议保留
