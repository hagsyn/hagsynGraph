# Hagsyn Standards And Product System Design

**目标**

将 Hagsyn 从“已有一个前端壳和首个真实工具”的状态，升级为一个具备长期可维护性的产品与规范体系：既能继续扩展真实工具，也能沉淀知识图谱相关能力，同时在项目内建立统一的产品文档、程序设计规范、代码开发规范和 UI 视觉规范目录。

**背景**

当前项目已经完成两件关键事情：

1. 保留了产品级工作台骨架：`Dashboard / Tools / Nodes / Graph / Roadmaps`
2. 将 `视频压缩` 落为 `Tools` 模块下的第一个真实工具

与此同时，用户提供了一张关于 Skill 分工的提示图，核心信息包括：

- `Onboarding Guide` 负责首次配置与用户类型识别
- `UI UX Pro Max` 负责视觉渲染、UI Styling 和视觉表达
- `Brand` 负责品牌一致性
- 整体应模块化，并符合 AI Agent 架构逻辑

这意味着 Hagsyn 后续不应再以 demo 数据驱动，而应同时建设：

- 产品层的模块体系
- 工程层的统一规范
- 体验层的视觉与交互标准

---

## 一、产品系统重新定义

Hagsyn 后续应被定义为一个由四层组成的产品系统：

### 1. Onboarding Layer

负责首次进入时的用户识别和默认配置。

目标包括：

- 识别用户属于“开发者”“数据分析师”或其他角色
- 推荐默认工作台主题与视图顺序
- 推荐适合的图谱主题、工具模块或建设方向

当前阶段先沉淀到文档，不要求立即实现。

### 2. Tools Layer

负责承载真实可执行工具，是当前产品最优先建设的能力层。

原则：

- 所有进入 `Tools` 模块的能力都必须是“真实能用”的工具
- 工具不依赖 demo 数据撑页面
- 工具应在产品壳内部工作，而不是破坏全局信息架构

当前真实工具：

- `视频压缩`

### 3. Knowledge Layer

负责承载 `Nodes / Graph / Roadmaps` 相关的知识沉淀能力。

原则：

- 保留模块结构
- 不默认灌 demo 数据
- 等待真实场景驱动后再定义节点、关系和路线结构

### 4. Brand & UI System Layer

负责统一视觉语言、组件规范、布局规则、空状态表达和品牌语气。

原则：

- 所有模块共享同一套视觉系统
- 工具页、知识页、路线页不应各自形成割裂风格
- 后续如有企业版，品牌层应具备扩展空间

---

## 二、项目内资料沉淀目录设计

建议新增如下正式目录结构：

```txt
docs/
├── product/
├── standards/
└── ux/
```

三条主线分别承担如下职责：

### `docs/product/`

存放产品定位、模块职责、功能边界、路线规划。

建议文档：

```txt
docs/product/
├── 00-product-positioning.md
├── 01-information-architecture.md
├── 02-module-map.md
├── 03-tooling-strategy.md
└── 04-roadmap.md
```

### `docs/standards/`

存放程序设计规范、工程约束、代码开发规范、接口和目录规则。

建议文档：

```txt
docs/standards/
├── 00-engineering-principles.md
├── 01-project-structure.md
├── 02-backend-standards.md
├── 03-frontend-standards.md
├── 04-api-standards.md
├── 05-data-modeling-standards.md
└── 06-documentation-standards.md
```

### `docs/ux/`

存放视觉系统、交互规范、组件规则、工具工作区模式、品牌语气。

建议文档：

```txt
docs/ux/
├── 00-design-principles.md
├── 01-visual-system.md
├── 02-layout-navigation.md
├── 03-component-standards.md
├── 04-tool-workspace-pattern.md
├── 05-empty-state-guidelines.md
└── 06-brand-voice.md
```

---

## 三、每条文档主线的职责定义

### Product 主线

解决“产品是什么、模块怎么分、后续怎么长”的问题。

重点包括：

- 当前产品定位
- 当前阶段优先级
- 模块间关系
- 什么是“真实工具”
- 后续建设顺序

### Standards 主线

解决“程序怎么设计、代码怎么写、接口怎么约束、资料怎么沉淀”的问题。

重点包括：

- 工程原则
- 目录层级
- 前后端代码边界
- API 命名与返回规范
- 数据模型扩展策略
- 文档新增/更新规则

### UX 主线

解决“页面怎么统一、视觉怎么稳定、组件怎么约束、品牌怎么表达”的问题。

重点包括：

- 颜色、字体、阴影、圆角、间距
- 导航、布局、工作台结构
- 工具卡片与工具工作区模式
- 空状态表达
- 品牌语气与页面文案

---

## 四、基于截图提示的模块吸收方式

用户提供的提示图不应被机械理解为“立刻接入多个 skill 执行器”，而应先吸收为产品设计原则。

### 1. Onboarding Guide

吸收为：

- `product` 中的模块设计原则
- 后续 `Onboarding` 模块的建设方向

当前不要求马上实现，但需要在文档里给出角色识别与默认主题推荐思路。

### 2. UI UX Pro Max: Slides / UI Styling

吸收为：

- `ux` 文档体系中的可视化表达规则
- 工具页、知识页、路线页的统一视觉标准

当前先表现为：

- 建立标准文档
- 让当前前端继续按统一视觉规范迭代

### 3. Brand

吸收为：

- `docs/ux/06-brand-voice.md`
- 后续如有企业版时可扩展视觉识别与品牌调性

当前阶段不要求设计企业品牌系统，但要留出统一语气与视觉识别规则。

---

## 五、对现有产品的优化方向

在文档体系建立后，产品本身应沿以下方向继续优化：

### Dashboard

继续强化为真实工作台首页，而不是空占位页。

应承载：

- 当前建设状态
- 已接入工具
- 规划中的工具
- 真实场景建设池
- 模块建设进度

### Tools

继续作为真实工具入口中心。

要求：

- 每个工具必须是真实可用功能
- 统一采用“工具目录 + 工具工作区 + 右侧说明”的模式

### Nodes / Graph / Roadmaps

当前保持骨架，但后续一旦进入建设，必须由真实对象和真实需求驱动，而不是为了页面饱满去制造演示数据。

---

## 六、实施顺序建议

建议分两阶段进行：

### Phase 1：资料体系落盘

目标：

- 创建 `docs/product`
- 创建 `docs/standards`
- 创建 `docs/ux`
- 生成首批基础规范文档

### Phase 2：按文档反哺产品

目标：

- 按 `docs/ux` 优化现有页面
- 按 `docs/product` 调整模块结构
- 按 `docs/standards` 收紧后续开发方式

---

## 七、范围与边界

本次设计的范围包括：

- 建立规范目录
- 建立首批核心标准文档
- 让这些文档反向约束后续产品和代码建设

本次不要求立即完成：

- Onboarding 实际功能
- 企业版 Brand 系统
- 知识图谱真实数据模型重建
- 多工具大批量接入

---

## 八、推荐结论

推荐采用如下策略：

1. 先建立 `docs/product + docs/standards + docs/ux`
2. 先沉淀规则，再继续扩产品
3. Tools 继续优先承载真实工具
4. Knowledge 相关模块等真实需求成熟后再深入

这条路线最适合当前状态：

- 避免继续被 demo 牵着走
- 避免产品和代码越做越散
- 为后续功能扩展建立稳定标准
