# Hagsyn Product Council Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在项目内创建 `hagsyn-product-council` skill，让 `hagsyn-product-brain` 在处理产品开发任务时获得统一的产品判断、模块落点判断、实现方案对比和阶段优先级控制能力。

**Architecture:** 先创建 `.agents/skills/hagsyn-product-council/` 的基础结构，保持 `SKILL.md` 轻量，只保留触发条件、场景索引与总规则。具体场景拆到 `references/`，每个场景都有 SOP 和自校验步骤。最后更新相关标准和 `brain` 路由，并按 `hagsyn-skill-review` 规则完成验收。

**Tech Stack:** Markdown, existing project-local skills, existing docs standards

---

### Task 1: 创建 product-council skill 骨架

**Files:**
- Create: `.agents/skills/hagsyn-product-council/SKILL.md`
- Create: `.agents/skills/hagsyn-product-council/references/`

- [ ] **Step 1: 创建 skill 目录**

Run:

```bash
mkdir -p /Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-council/references
```

- [ ] **Step 2: 编写轻量入口 `SKILL.md`**

要求：
- frontmatter 包含 `name` 与 `description`
- 只保留触发条件、场景索引、总规则
- 不在主文件堆详细流程

- [ ] **Step 3: 自检入口文件**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('/Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-council/SKILL.md').read_text()
print('name:' in text, 'description:' in text, 'Scenario Index' in text)
PY
```

Expected: `True True True`

### Task 2: 编写 4 个场景 SOP

**Files:**
- Create: `.agents/skills/hagsyn-product-council/references/new-feature-evaluation.md`
- Create: `.agents/skills/hagsyn-product-council/references/module-placement.md`
- Create: `.agents/skills/hagsyn-product-council/references/implementation-tradeoff.md`
- Create: `.agents/skills/hagsyn-product-council/references/priority-and-staging.md`

- [ ] **Step 1: 编写“新需求评审”场景**

要求：
- 适用场景
- 前置检查
- 执行步骤
- 自校验步骤
- 常见失败点

- [ ] **Step 2: 编写“模块落点判断”场景**

要求：
- 覆盖 `Tools / Dashboard / Nodes / Graph / Roadmaps`
- 明确什么时候进入 `Knowledge`

- [ ] **Step 3: 编写“实现方案对比”场景**

要求：
- 覆盖本地实现 vs 外部 API
- 工作区内嵌 vs 独立页
- MVP 先做什么

- [ ] **Step 4: 编写“阶段优先级控制”场景**

要求：
- 覆盖现在做 / 后做 / 先留壳
- 防止 scope 膨胀

- [ ] **Step 5: 验证 4 个 references 都符合 SOP 结构**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
base = Path('/Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-council/references')
for ref in sorted(base.glob('*.md')):
    text = ref.read_text()
    checks = ['适用场景','前置检查','执行步骤','自校验步骤','常见失败点']
    print(ref.name, all(token in text for token in checks))
PY
```

Expected: 每个文件输出 `True`

### Task 3: 接入现有控制层

**Files:**
- Modify: `.agents/skills/hagsyn-product-brain/SKILL.md`
- Modify: `docs/standards/07-skill-standards.md`

- [ ] **Step 1: 在 brain 中接入 product-council**

要求：
- 在 lower-level skill routing 中加入 `hagsyn-product-council`
- 在适当场景中说明何时应调用它

- [ ] **Step 2: 如有必要，补 skill standards 的协同说明**

要求：
- 不重写整个 standards 文档
- 只补“高层产品判断 skill 也应遵循同一审核规范”

- [ ] **Step 3: 自检 brain 与 standards 更新**

Run:

```bash
rg -n "hagsyn-product-council" /Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-brain/SKILL.md /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards/07-skill-standards.md
```

Expected: 至少命中 `brain`，如补充了 standards 则同时命中

### Task 4: 按 hagsyn-skill-review 规则验收

**Files:**
- Verify only

- [ ] **Step 1: 检查主文件是否保持轻量**

Run:

```bash
sed -n '1,220p' /Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-council/SKILL.md
```

Expected: 只包含触发条件、场景索引、总规则

- [ ] **Step 2: 检查 references 是否按场景拆分**

Run:

```bash
find /Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-council/references -maxdepth 1 -type f | sort
```

Expected: 4 个场景文件都在

- [ ] **Step 3: 检查是否存在违规占位词**

Run:

```bash
rg -n "TODO|TBD|script-list|commands.md|helpers.md" /Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-council
```

Expected: 无输出

- [ ] **Step 4: Commit**

```bash
git add /Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-council /Users/hagsyn/ai/workspace/Hagsyn-Graph/.agents/skills/hagsyn-product-brain/SKILL.md /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards/07-skill-standards.md
git commit -m "skills: add hagsyn product council"
```
