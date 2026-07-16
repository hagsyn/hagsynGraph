---
name: hagsyn-review-council
description: Use when Hagsyn-Graph changes need a full-surface review across code, docs, skills, config, and verification evidence before completion, or when a high-risk task needs an early lightweight review to prevent costly rework.
---

# Hagsyn Review Council

## Trigger Conditions

Use this skill when work involves:

- 功能、缺陷、UI 或 skill 变更已经进入收口阶段，需要统一 review
- 需要判断当前改动是否可以对外宣称“已完成”
- 变更同时触及代码、文档、skill、配置或验证报告中的多个面
- 任务处于高风险状态，需要中途做一次轻量预审以提前暴露返工成本高的问题

Do not use this skill for:

- 还处于纯想法讨论、尚未形成任何实际改动的任务
- 只需要单点测试策略判断的事项
- 只做某个 skill 结构审核且无需全量变更结论的事项

## Scenario Index

Read the closest scenario SOP before acting:

1. 最终交付审查
   - `references/final-delivery-review.md`
2. 高风险轻量预审
   - `references/early-risk-review.md`
3. 治理面与多资产变更审查
   - `references/governance-surface-review.md`

If a task spans multiple scenarios, read all matching SOPs and keep the stricter release-gate rule where they overlap.

## Global Rules

1. 先看明确问题和硬风险，再给总体印象。
2. review 结论必须覆盖代码、文档、skill、配置和验证证据中与本次改动相关的部分，不只盯单一文件类型。
3. 默认在任务收口前执行最终 review；中途预审只在高风险条件下触发，避免频繁打断主流程。
4. `hagsyn-testing-council` 和 `hagsyn-skill-review` 的结论是输入，不替代最终全量变更审查。
5. 输出必须明确“可收口 / 需修正后再收口”，不能只给模糊印象。
