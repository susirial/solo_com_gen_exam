# 考卷生成 Skill 计划 Spec

## Why
当前仓库已经有一份围绕考卷生成模块的技术说明，但还没有把这套能力沉淀为可复用的 Agent Skill 方案。先产出一份面向 Skill 设计与落地的计划文档，可以把 Anthropic Skills 的规范要求、触发策略、结构约束和验证方法整理清楚，避免直接写 Skill 时返工。

## What Changes
- 新增一份“考卷生成 Skill 生成计划文档”的规格与任务定义
- 计划文档必须基于现有《考卷生成说明》提炼 Skill 的职责边界、触发条件、输入输出、资源组织和评估方案
- 计划文档必须吸收 `anthropics/skills` 仓库中的通用要求，包括 `SKILL.md` 前置元数据、渐进式加载、资源分层和测试思路
- 计划文档必须明确第一阶段只做 Skill 方案设计，不直接进入 Skill 实现

## Impact
- Affected specs: `plan-exam-paper-skill`
- Affected code: `.trae/specs/plan-exam-paper-skill/spec.md`、`.trae/specs/plan-exam-paper-skill/tasks.md`、`.trae/specs/plan-exam-paper-skill/checklist.md`，以及后续预计会影响的 `SKILL.md`、`references/`、`evals/` 等 Skill 目录结构

## ADDED Requirements
### Requirement: 生成考卷 Skill 计划文档
系统 SHALL 先生成一份“考卷生成 Skill 生成计划文档”的规格化方案，用于指导后续 Skill 的编写、评审与验证。

#### Scenario: 基于现有说明文档提炼 Skill 范围
- **WHEN** 用户要求围绕《考卷生成说明》先生成 Skill 计划文档
- **THEN** 规格必须把现有考卷生成能力拆解为适合 Agent Skill 的职责、边界和使用场景

#### Scenario: 对齐 Anthropic Skills 基本结构
- **WHEN** 计划文档定义目标 Skill 的交付形态
- **THEN** 文档必须明确 Skill 至少包含 `SKILL.md`，并说明 `name`、`description` 是必需元数据

#### Scenario: 对齐渐进式加载与资源分层
- **WHEN** 计划文档描述 Skill 的内部结构
- **THEN** 文档必须说明元数据、`SKILL.md` 正文、以及可选资源目录如 `references/`、`assets/`、`scripts/` 的职责划分

#### Scenario: 对齐触发描述最佳实践
- **WHEN** 计划文档定义 Skill 的触发条件
- **THEN** 文档必须要求在 `description` 中同时描述“做什么”和“何时触发”，并覆盖常见用户表达而不是只写一个窄触发词

#### Scenario: 对齐 Skill 指令最佳实践
- **WHEN** 计划文档定义 `SKILL.md` 正文的写法
- **THEN** 文档必须要求正文使用可执行、偏祈使句的步骤说明，避免空泛口号式描述，并在必要时给出输出模板、示例和边界条件

#### Scenario: 对齐验证与评估要求
- **WHEN** 计划文档描述后续 Skill 的验收方式
- **THEN** 文档必须包含测试提示词、评估维度和是否需要 `evals/evals.json` 的判定原则

### Requirement: 计划文档必须限定当前阶段边界
系统 SHALL 将本次变更限定为 Skill 生成计划阶段，不在本次 Spec 中承诺直接产出最终 Skill 实现。

#### Scenario: 用户当前只要求计划文档
- **WHEN** 用户请求“先生成一个 skill 生成计划文档”
- **THEN** 规格与任务必须聚焦于计划文档，不得把实际 Skill 编写当作本阶段已完成内容

### Requirement: 计划文档必须体现考卷生成领域特性
系统 SHALL 结合《考卷生成说明》中已有的生成、重生、编辑、组卷和渲染链路，定义考卷生成 Skill 的领域特征。

#### Scenario: 提炼考卷生成工作流
- **WHEN** 计划文档分析领域能力
- **THEN** 文档必须覆盖至少以下能力：题目生成、单题重生、题目编辑、整卷组装、输出形态说明

#### Scenario: 识别外部依赖和边界
- **WHEN** 计划文档描述 Skill 的使用前提
- **THEN** 文档必须指出当前代码快照缺失的数据模型、模板和上层接口，并将这些缺口纳入后续 Skill 设计风险或待确认项

## MODIFIED Requirements
### Requirement: 无
当前不存在需要修改的既有规格，属于新建变更。

## REMOVED Requirements
### Requirement: 无
**Reason**: 当前为新增规格，不涉及移除旧要求。
**Migration**: 无
