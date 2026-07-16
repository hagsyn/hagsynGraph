# Hagsyn Review Council Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 Hagsyn 新增一个全量变更审查专家团 `hagsyn-review-council`，并把它接入项目内索引、skill 标准和 workflow 收口链路。

**Architecture:** 先新增 `.agents/skills/hagsyn-review-council/`，保持 `SKILL.md` 轻量，只保留触发条件、场景索引和总规则。再补一份项目内专家团职责索引文档，并把 `product-brain`、`workflow-harness`、`docs/INDEX.md`、`README.md`、`AGENTS.md` 一并接上。

**Tech Stack:** Markdown, project-local skills, docs standards

---

### Task 1: 编写 review-council 设计与职责文档

**Files:**
- Create: `docs/superpowers/specs/2026-07-03-hagsyn-review-council-design.md`
- Create: `docs/standards/08-project-skill-index.md`

- [ ] 写明 `hagsyn-review-council` 的定位、职责、触发方式和与现有 skill 的关系
- [ ] 在专家团索引文档中补全 9 个项目内 skill 的职责、触发场景和协作关系

### Task 2: 创建 review-council skill 骨架

**Files:**
- Create: `.agents/skills/hagsyn-review-council/SKILL.md`
- Create: `.agents/skills/hagsyn-review-council/references/final-delivery-review.md`
- Create: `.agents/skills/hagsyn-review-council/references/early-risk-review.md`
- Create: `.agents/skills/hagsyn-review-council/references/governance-surface-review.md`

- [ ] 编写轻量 `SKILL.md`
- [ ] 为最终交付审查、高风险轻量预审、治理面审查分别编写 SOP
- [ ] 确保每个 SOP 都包含适用场景、前置检查、执行步骤、自校验步骤、常见失败点

### Task 3: 接入索引与标准

**Files:**
- Modify: `docs/INDEX.md`
- Modify: `docs/standards/07-skill-standards.md`
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] 在文档索引中加入项目内专家团职责索引
- [ ] 在项目入口说明中补上 `hagsyn-review-council`
- [ ] 在 skill 标准中补充“重要变更收口前应经过统一 review”的约束

### Task 4: 接入总控与 workflow 路由

**Files:**
- Modify: `.agents/skills/hagsyn-product-brain/SKILL.md`
- Modify: `.agents/skills/hagsyn-workflow-harness/SKILL.md`
- Modify: `.agents/skills/hagsyn-workflow-harness/references/feature-development-workflow.md`
- Modify: `.agents/skills/hagsyn-workflow-harness/references/bugfix-workflow.md`
- Modify: `.agents/skills/hagsyn-workflow-harness/references/ui-adjustment-workflow.md`
- Modify: `.agents/skills/hagsyn-workflow-harness/references/skill-governance-workflow.md`

- [ ] 在 `product-brain` 中加入 review-council 路由说明
- [ ] 在 `workflow-harness` 中加入 review-council 收口要求
- [ ] 在四条 workflow SOP 中加入最终 review 或高风险预审触发说明

### Task 5: 最终自检

**Files:**
- Verify only

- [ ] 检查 `hagsyn-review-council/SKILL.md` 是否保持轻量
- [ ] 检查 3 个场景 SOP 是否完整
- [ ] 检查索引、README、AGENTS、标准文档是否已同步
- [ ] 检查 `product-brain` 与 `workflow-harness` 是否都已接入 review-council
- [ ] 检查没有 `TODO / TBD / script-list / commands.md / helpers.md`
