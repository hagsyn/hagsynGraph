# Hagsyn Workflow Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 Hagsyn 建立一个重型 `workflow harness`，把新功能开发、bug 修复、UI 调整、skill 治理四条常规事项固化成可执行 workflow，并接入现有 `brain / council / guard / testing-council / skill-review` 体系。

**Architecture:** 先创建 `.agents/skills/hagsyn-workflow-harness/`，保持 `SKILL.md` 轻量，只保留触发条件、workflow 索引与总规则。将四条 workflow 分别拆到 `references/`，每条都包含 SOP 与自校验。随后把 `hagsyn-product-brain` 接入该 harness，并补 standards / testing 报告中的对应记录。

**Tech Stack:** Markdown, existing project-local skills, docs standards, testing reports

---

### Task 1: 创建 harness 入口与目录

**Files:**
- Create: `.agents/skills/hagsyn-workflow-harness/SKILL.md`
- Create: `.agents/skills/hagsyn-workflow-harness/references/`

- [ ] 创建 `hagsyn-workflow-harness` 目录
- [ ] 编写轻量 `SKILL.md`
- [ ] 确保 `SKILL.md` 只保留：
  - 触发条件
  - workflow 索引
  - 总规则
- [ ] 自检 frontmatter 与索引存在

### Task 2: 编写新功能开发 workflow

**Files:**
- Create: `.agents/skills/hagsyn-workflow-harness/references/feature-development-workflow.md`

- [ ] 写清适用场景
- [ ] 写清前置检查
- [ ] 写清执行步骤
- [ ] 写清自校验步骤
- [ ] 写清常见失败点
- [ ] 明确要求：
  - 读 docs
  - 需要时调 council / guard / ui-pattern
  - 必须做 API / 前端 / 点击验证
  - 必须写测试报告

### Task 3: 编写 bug 修复 workflow

**Files:**
- Create: `.agents/skills/hagsyn-workflow-harness/references/bugfix-workflow.md`

- [ ] 写清复现 -> 根因 -> 回归测试 -> 修复 -> 验证 -> 测试报告 的链路
- [ ] 明确不能跳过根因调查
- [ ] 明确没有回归测试不算完成

### Task 4: 编写 UI 调整 workflow

**Files:**
- Create: `.agents/skills/hagsyn-workflow-harness/references/ui-adjustment-workflow.md`

- [ ] 写清 UX 文档优先
- [ ] 写清工作台壳保护
- [ ] 写清前端壳测试 + `node --check` + 网页点击验证
- [ ] 写清状态文案要与真实可用性一致

### Task 5: 编写 skill 治理 workflow

**Files:**
- Create: `.agents/skills/hagsyn-workflow-harness/references/skill-governance-workflow.md`

- [ ] 写清 skill 新建 / 修改后的审核顺序
- [ ] 写清 `SKILL.md + references + scripts` 规范
- [ ] 写清必须调 `hagsyn-skill-review`
- [ ] 写清 skill 变更报告要求

### Task 6: 接入现有控制层

**Files:**
- Modify: `.agents/skills/hagsyn-product-brain/SKILL.md`
- Modify: `docs/standards/07-skill-standards.md`

- [ ] 在 `brain` 中加入 `hagsyn-workflow-harness`
- [ ] 说明它负责 workflow 执行而不是高层产品判断
- [ ] 如有必要，在 standards 里补一句 harness 也是项目内 skill 治理对象

### Task 7: 测试报告与入口同步

**Files:**
- Modify: `docs/testing/reports/2026-07-01-video-compress-and-vtt-tool-report.md`
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] 如有必要，在 README / AGENTS 补 `.agents/skills/hagsyn-workflow-harness`
- [ ] 在测试报告中记录 harness 建设进入项目控制层

### Task 8: 最终验收

**Files:**
- Verify only

- [ ] 验证 `SKILL.md` 有 frontmatter 和 workflow 索引
- [ ] 验证 4 个 workflow 文件都在
- [ ] 验证每个 workflow 都包含：
  - 适用场景
  - 前置检查
  - 执行步骤
  - 自校验步骤
  - 常见失败点
- [ ] 验证没有 `TODO / TBD / script-list / commands.md / helpers.md`
- [ ] 验证 `brain` 已接上 harness
