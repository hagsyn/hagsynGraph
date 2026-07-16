---
name: hagsyn-product-council
description: Use when evaluating new product ideas, deciding module placement, or making early product-structure judgments in Hagsyn-Graph before implementation scope is fixed.
---

# Hagsyn Product Council

## Trigger Conditions

Use this skill when work involves:

- 新需求评审、能力立项、需求入口收敛
- 判断能力应放入哪个现有模块
- 模块边界、信息架构或产品骨架层面的早期决策
- 在实现前先判断“该不该做、放哪做、做到什么程度”

Do not use this skill for:

- 已经明确落在单一模块内的实现细节
- 纯后端、纯前端、纯数据库的局部改动
- 只需要执行既定方案而不需要再做产品判断的任务

## Scenario Index

Read the closest scenario SOP before acting:

1. 新需求评审
   - `references/new-feature-evaluation.md`
2. 模块落点判断
   - `references/module-placement.md`
3. 实现方案对比
   - `references/implementation-tradeoff.md`
4. 阶段优先级控制
   - `references/priority-and-staging.md`

If a task spans multiple scenarios, read all matching SOPs and keep the stricter product-boundary rule where they overlap.

## Global Rules

1. 优先复用现有一级模块，不轻易新增并列入口。
2. 先判断真实用户任务与真实交付结果，再判断页面或模块归属。
3. 当前产品重心仍然是 `Tools` 的真实可执行价值，`Knowledge` 继续保持克制。
4. 不要为了信息架构完整感引入假能力、假数据或过早展开的模块叙事。
5. 输出结论时必须说明判断依据、保留边界和仍待验证的前提。
