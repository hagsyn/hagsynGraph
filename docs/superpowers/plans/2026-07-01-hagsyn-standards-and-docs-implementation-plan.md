# Hagsyn Standards And Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 Hagsyn 建立统一的产品资料、程序设计规范、代码开发规范和 UI/视觉规范目录，并沉淀首批核心文档，形成后续持续开发的标准基础。

**Architecture:** 先在 `docs/product`、`docs/standards`、`docs/ux` 下建立标准化文档体系，再将当前项目状态、产品模块、开发方式和视觉系统固化为首批规则文档。最后基于文档回看现有产品，确保后续迭代遵循统一标准。

**Tech Stack:** Markdown, existing project docs, current FastAPI + 单文件前端架构

---

### Task 1: 建立资料目录结构

**Files:**
- Create: `docs/product/`
- Create: `docs/standards/`
- Create: `docs/ux/`

- [ ] **Step 1: 创建产品资料目录**

Run:

```bash
mkdir -p /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/product
```

- [ ] **Step 2: 创建工程规范目录**

Run:

```bash
mkdir -p /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards
```

- [ ] **Step 3: 创建 UI/UX 规范目录**

Run:

```bash
mkdir -p /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/ux
```

- [ ] **Step 4: 验证目录已创建**

Run:

```bash
find /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs -maxdepth 2 -type d | sort
```

Expected: 输出中包含 `docs/product`、`docs/standards`、`docs/ux`

### Task 2: 编写产品主线文档

**Files:**
- Create: `docs/product/00-product-positioning.md`
- Create: `docs/product/01-information-architecture.md`
- Create: `docs/product/02-module-map.md`
- Create: `docs/product/03-tooling-strategy.md`
- Create: `docs/product/04-roadmap.md`

- [ ] **Step 1: 写产品定位文档**

内容应覆盖：
- Hagsyn 当前定位
- 真实工具优先
- 不依赖 demo 数据
- Tools 与 Knowledge 的关系

- [ ] **Step 2: 写信息架构文档**

内容应覆盖：
- Dashboard / Tools / Nodes / Graph / Roadmaps 的职责
- 工具模块与知识模块的边界
- 当前页面结构原则

- [ ] **Step 3: 写模块地图文档**

内容应覆盖：
- Onboarding Layer
- Tools Layer
- Knowledge Layer
- Brand & UI System Layer

- [ ] **Step 4: 写工具策略文档**

内容应覆盖：
- 什么样的功能才能进入 Tools
- 工具目录、工具卡片、工具工作区模式
- 当前首个工具：视频压缩

- [ ] **Step 5: 写产品路线文档**

内容应覆盖：
- 先资料后实现
- 先真实工具后知识深化
- Nodes / Graph / Roadmaps 的后续进入条件

### Task 3: 编写工程规范主线文档

**Files:**
- Create: `docs/standards/00-engineering-principles.md`
- Create: `docs/standards/01-project-structure.md`
- Create: `docs/standards/02-backend-standards.md`
- Create: `docs/standards/03-frontend-standards.md`
- Create: `docs/standards/04-api-standards.md`
- Create: `docs/standards/05-data-modeling-standards.md`
- Create: `docs/standards/06-documentation-standards.md`

- [ ] **Step 1: 写工程原则文档**

内容应覆盖：
- 真实需求驱动
- 小步迭代
- 禁止 demo 数据驱动产品判断
- 文档先行的约束

- [ ] **Step 2: 写项目结构文档**

内容应覆盖：
- backend / frontend / docs 的职责
- 单文件前端阶段的边界
- 后续如何扩展

- [ ] **Step 3: 写后端规范文档**

内容应覆盖：
- 路由组织
- 工具能力拆分方式
- ffmpeg / 本地文件处理原则

- [ ] **Step 4: 写前端规范文档**

内容应覆盖：
- 工作台壳结构
- Tools 内部工作区模式
- 不轻易推翻产品壳

- [ ] **Step 5: 写 API 规范文档**

内容应覆盖：
- 命名规则
- 鉴权规则
- 返回字段风格
- 文件上传与下载接口约束

- [ ] **Step 6: 写数据模型规范文档**

内容应覆盖：
- 未来 Nodes / Graph / Roadmaps 的建模原则
- 真实对象优先
- 不为了展示制造假结构

- [ ] **Step 7: 写文档规范文档**

内容应覆盖：
- 新文档命名规则
- 哪些东西放 `product`
- 哪些东西放 `standards`
- 哪些东西放 `ux`

### Task 4: 编写 UI/UX 规范主线文档

**Files:**
- Create: `docs/ux/00-design-principles.md`
- Create: `docs/ux/01-visual-system.md`
- Create: `docs/ux/02-layout-navigation.md`
- Create: `docs/ux/03-component-standards.md`
- Create: `docs/ux/04-tool-workspace-pattern.md`
- Create: `docs/ux/05-empty-state-guidelines.md`
- Create: `docs/ux/06-brand-voice.md`

- [ ] **Step 1: 写设计原则文档**

内容应覆盖：
- 工作台产品感
- 真实工具优先
- 不做营销页化表达

- [ ] **Step 2: 写视觉系统文档**

内容应覆盖：
- 主题
- 配色
- 字体
- 圆角、边框、阴影

- [ ] **Step 3: 写布局与导航文档**

内容应覆盖：
- 三栏壳结构
- 导航高亮
- 页面层次

- [ ] **Step 4: 写组件规范文档**

内容应覆盖：
- 工具卡片
- 状态 badge
- 结果卡片
- 右侧详情区

- [ ] **Step 5: 写工具工作区模式文档**

内容应覆盖：
- Tools 列表
- 点击进入工作区
- 工作区与详情栏联动

- [ ] **Step 6: 写空状态规范文档**

内容应覆盖：
- 不再用 demo 数据填空
- 空状态如何表达“等待真实内容”
- 语气和行动提示

- [ ] **Step 7: 写品牌语气文档**

内容应覆盖：
- Hagsyn 的语气
- 产品文案风格
- 企业版扩展预留

### Task 5: 统一复核并回写 README/AGENTS 需要补充的链接

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: 检查 README 是否需要补充资料目录说明**

Run:

```bash
sed -n '1,220p' /Users/hagsyn/ai/workspace/Hagsyn-Graph/README.md
```

- [ ] **Step 2: 检查 AGENTS 是否需要补充规范目录使用约定**

Run:

```bash
sed -n '1,260p' /Users/hagsyn/ai/workspace/Hagsyn-Graph/AGENTS.md
```

- [ ] **Step 3: 如有必要，补充资料目录说明**

要求：
- 不大幅改动已有说明
- 只补“规范文档在哪”和“后续开发默认参考这些文档”

### Task 6: 最终验证

**Files:**
- Verify only

- [ ] **Step 1: 验证目录和文档齐全**

Run:

```bash
find /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/product /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/ux -maxdepth 1 -type f | sort
```

Expected: 输出包含三条主线下的全部首批文档

- [ ] **Step 2: 验证文档无明显占位词**

Run:

```bash
rg -n "TBD|TODO|待补|以后再说" /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/product /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/ux
```

Expected: 无输出

- [ ] **Step 3: Commit**

```bash
git add /Users/hagsyn/ai/workspace/Hagsyn-Graph/docs /Users/hagsyn/ai/workspace/Hagsyn-Graph/README.md /Users/hagsyn/ai/workspace/Hagsyn-Graph/AGENTS.md
git commit -m "docs: add product, engineering, and ux standards"
```
