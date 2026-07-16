# Hagsyn Product Council Design

## 目标

为 Hagsyn 建立一个挂在 `hagsyn-product-brain` 之下的高层产品专家团 skill，用于在后续产品建设过程中提供统一的产品判断、模块落点判断、方案对比和阶段优先级控制能力。

该 skill 不直接替代实现型 skill，也不直接承担代码开发，而是作为产品层面的“顾问团”，帮助后续 agent 在做功能、做页面、做模块扩展时不跑偏。

---

## 一、为什么现在需要它

当前 Hagsyn 已进入一个新的阶段：

1. 不再只是做一个单工具页面
2. 已经开始形成产品骨架
3. 已经建立了产品、工程、UX 三条文档主线
4. 已经沉淀了若干项目内 skill

这意味着后续很多事情不再是“怎么写代码”，而是：

- 这个功能该不该做
- 这个功能该落在哪个模块
- 现在是先做真实工具，还是先做知识壳
- 这个方案是不是会把产品带回 demo 驱动
- 这件事是现在做，还是先留在路线里

这些问题如果没有一个统一的产品判断层，就很容易每次都在会话里临时拍脑袋决定。

因此，需要一个位于 `hagsyn-product-brain` 之下、专门负责高层产品设计判断的 skill。

---

## 二、推荐 skill 定位

推荐名称：

`hagsyn-product-council`

这个名称比 `expert` 更合适，因为它强调的是多角色共同给出判断，而不是单一权威口吻。

它的角色不是：

- 直接写代码
- 直接做前端组件
- 直接替代 `hagsyn-product-guard`
- 直接替代 `hagsyn-ui-workspace-pattern`

它的角色是：

- 给 `brain` 提供更高层的产品判断能力
- 在需求进入实现前，先做方向和方案判断
- 为后续产品路线选择提供统一输出模板

---

## 三、推荐职责范围

`hagsyn-product-council` 建议只承担 4 类职责：

### 1. 新需求评审

回答：

- 这个需求现在值不值得做
- 是否符合当前阶段
- 是否属于真实工具能力

### 2. 模块落点判断

回答：

- 这个功能应该进 `Tools` 还是 `Knowledge`
- 应该落在 `Dashboard / Tools / Nodes / Graph / Roadmaps` 哪一层

### 3. 实现方案对比

回答：

- 本地实现 vs 外部 API
- 工具工作区内嵌 vs 独立页
- MVP 先做什么，什么后做

### 4. 阶段优先级控制

回答：

- 现在是否该做这件事
- 是直接实现，还是先留壳
- 哪些事情必须延后

---

## 四、不建议让它承担的职责

当前阶段不建议让 `hagsyn-product-council` 一上来就承担以下内容：

- 商业化策略
- 增长策略
- 品牌传播策略
- 企业版市场化策略
- 复杂组织管理策略

原因不是这些不重要，而是：

- 当前 Hagsyn 仍处于真实工具和产品骨架建设阶段
- 太早把 council 做成“大而全产品委员会”，会增加大量空转判断

因此建议它保持“中等专家团”定位，而不是重型治理结构。

---

## 五、建议的专家角色构成

建议内部固定 5 个产品角色视角：

### 1. Product Strategist

负责判断：

- 是否值得做
- 是否符合当前阶段主线
- 是否应被纳入路线

### 2. UX Architect

负责判断：

- 页面和模块如何组织
- 工作区应如何承载功能
- 模块之间如何保持连续性

### 3. Tooling PM

负责判断：

- 该能力是否属于真实工具
- 输入输出是否构成闭环
- 是否适合进入 `Tools`

### 4. Knowledge Architect

负责判断：

- 是否应该进入 `Nodes / Graph / Roadmaps`
- 当前是该做壳还是该做深
- 什么算真实场景驱动

### 5. Scope Controller

负责判断：

- 是否过度扩张
- 是否偏离当前阶段
- 是否又回到 demo 驱动

---

## 六、输出格式建议

这个 skill 的输出不应是泛泛而谈，而应统一收敛成下面的结构：

1. 当前判断
2. 推荐落点
3. 推荐阶段
4. 推荐方案
5. 不建议的方向
6. 下一步建议

这样后续使用时，`brain` 就能快速消费 council 的判断结果，而不是还要从长篇讨论中抽取结论。

---

## 七、建议目录结构

按当前项目内 skill 规范，建议目录如下：

```txt
.agents/
└── skills/
    └── hagsyn-product-council/
        ├── SKILL.md
        └── references/
            ├── new-feature-evaluation.md
            ├── module-placement.md
            ├── implementation-tradeoff.md
            └── priority-and-staging.md
```

说明：

- `SKILL.md` 只保留触发条件、场景索引和总规则
- 每个 `references/*.md` 都是单独场景 SOP
- 当前不要求脚本；后续确有必要时，再单独进入 `scripts/`

---

## 八、与现有 skill 的关系

### `hagsyn-product-brain`

作为总控层，负责：

- 分类任务
- 读取文档
- 路由 skill
- 控制 stop hook

### `hagsyn-product-council`

作为顾问层，负责：

- 产品判断
- 模块落点
- 方案比较
- 阶段优先级

### `hagsyn-product-guard`

作为边界守门层，负责：

- 防 demo 驱动
- 防 Knowledge 过早膨胀
- 防产品壳被破坏

### `hagsyn-ui-workspace-pattern`

作为前端模式层，负责：

- 三栏壳
- Tools 工作区模式
- 详情栏
- 空状态诚实表达

### `hagsyn-knowledge-shell`

作为 Knowledge 壳层，负责：

- Nodes / Graph / Roadmaps 的壳层约束

---

## 九、推荐结论

推荐立即创建：

`hagsyn-product-council`

推荐采用：

- 中等专家团定位
- 不做大而全
- 只服务当前产品建设阶段

推荐先覆盖：

1. 新需求评审
2. 模块落点判断
3. 实现方案对比
4. 阶段优先级控制

这是当前最合适的切入方式。

---

## 十、实施边界

本次设计只定义：

- skill 的定位
- 角色组成
- 场景范围
- 输出结构
- 与现有 skill 的关系

本次不要求立即完成：

- 品牌委员会
- 商业化委员会
- 企业版治理模型
- 自动评分脚本

这些可以等 Hagsyn 再成熟一些后再说。
