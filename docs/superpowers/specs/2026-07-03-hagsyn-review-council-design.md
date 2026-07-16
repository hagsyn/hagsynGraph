# Hagsyn Review Council Design

## 目标

为 Hagsyn 建立一个全量变更审查专家团 `hagsyn-review-council`，用于在任务收口前统一审查代码、文档、skill、配置和验证证据，避免实现已完成但整体质量与治理仍有缺口。

该专家团不替代测试、不替代产品判断，也不替代 workflow。本质上它是一个面向交付前关口的变更质量审查层。

---

## 一、为什么现在需要它

当前项目内已经有：

- `hagsyn-product-brain` 负责总控与路由
- `hagsyn-product-council` 负责产品判断
- `hagsyn-product-guard` 负责边界守门
- `hagsyn-workflow-harness` 负责执行流程治理
- `hagsyn-testing-council` 负责测试策略与测试报告
- `hagsyn-skill-review` 负责项目内 skill 审核

但仍缺一个统一回答下面问题的角色：

- 这次变更整体是否已经可收口
- 改动里有没有明显 bug、回归风险或遗漏验证
- 代码之外的文档、skill、配置、报告是否同步到位
- 哪些问题必须先修，哪些可以带风险说明交付

如果没有这个层，流程会出现两个常见空洞：

1. 各专项都做了，但没人做全局合并视角的最后审查
2. 只有“测试过了”的结论，没有“改动质量是否过关”的结论

因此需要一个面向全量变更的 review 专家团。

---

## 二、推荐定位

推荐名称：

`hagsyn-review-council`

推荐定位：

> 一个面向 Hagsyn 交付收口的全量变更审查专家团，默认在任务完成后执行最终 review，并在高风险任务中允许中途做一次轻量预审。

它不是：

- 通用测试器
- 单纯代码风格检查器
- 另一个 workflow harness

它是：

- 全局质量审查层
- 交付前关口
- 高风险变更的提前预警器

---

## 三、推荐职责范围

`hagsyn-review-council` 承担 3 类职责：

### 1. 最终交付审查

在任务宣称完成前，统一审查：

- 代码实现是否存在明显缺陷或风险
- 文档是否与实际改动同步
- skill / 配置改动是否遵守现有治理规则
- 测试和验证证据是否足以支撑“已完成”

### 2. 高风险轻量预审

当任务命中高风险条件时，可在实现过程中提前介入一次，用于尽早指出返工成本高的问题，但不频繁打断主流程。

### 3. 全量变更结论输出

输出统一结论，而不是散落意见。  
至少回答：

- 发现了什么问题
- 哪些是必须修复项
- 哪些是剩余风险
- 当前是否可以收口

---

## 四、推荐触发策略

默认采用“最终关口为主，中途预审为辅”的模式。

### 默认必调时机

- 功能开发完成后
- bug 修复完成后
- UI 调整完成后
- 项目内 skill 新增或明显更新后

### 中途预审触发条件

只有在以下高风险情形中才建议提前介入：

- 跨多个模块、前后端联动或公共接口变更
- 涉及 `docs/product/**`、`docs/standards/**`、`.agents/skills/**`
- 涉及核心工作区壳层、主工具链路或共享数据结构
- 主 agent 判断一旦方向错了返工成本会明显偏高

这样既保留流畅度，也保留提前纠偏能力。

---

## 五、建议的审查视角

建议内部固定 5 个视角：

### 1. Implementation Reviewer

关注：

- 代码逻辑缺陷
- 回归风险
- 边界条件
- 改动是否过度扩散

### 2. Workflow Reviewer

关注：

- 本次是否按应有 workflow 收口
- 是否遗漏测试、报告、点击验证或 stop hook 前的必做动作

### 3. Documentation Reviewer

关注：

- 文档、说明、索引是否同步
- 结论是否与实际系统状态一致

### 4. Governance Reviewer

关注：

- skill、标准、配置是否遵守治理规则
- 是否出现结构漂移或规则绕开

### 5. Release Gate Reviewer

关注：

- 当前是否可以对外宣称完成
- 是否必须继续修正
- 是否需要明确保留风险

---

## 六、输出格式建议

`hagsyn-review-council` 的输出应统一成下面结构：

1. 审查范围
2. 发现的问题
3. 必须修复项
4. 剩余风险或测试缺口
5. 收口结论

如果没有问题，也要明确写：

- 未发现阻塞性问题
- 仍存在的验证边界或残余风险

避免只给“看起来没问题”这类弱结论。

---

## 七、建议目录结构

```txt
.agents/
└── skills/
    └── hagsyn-review-council/
        ├── SKILL.md
        └── references/
            ├── final-delivery-review.md
            ├── early-risk-review.md
            └── governance-surface-review.md
```

说明：

- `SKILL.md` 只保留触发条件、场景索引和总规则
- `references/` 按审查场景拆分
- 当前先不引入脚本，保持轻量

---

## 八、与现有 skill 的关系

### `hagsyn-product-brain`

负责识别何时需要调 `hagsyn-review-council`。

### `hagsyn-workflow-harness`

负责把 review-council 接入 feature / bugfix / UI / skill workflow 的收口阶段。

### `hagsyn-testing-council`

负责测试策略和测试证据；这些证据是 review-council 的输入，不替代最终审查。

### `hagsyn-skill-review`

只负责项目内 skill 结构审核；当任务是全量变更收口时，仍可由 review-council 进行总审。

---

## 九、结论

推荐新增 `hagsyn-review-council`，并将其定义为：

- 默认在任务收口前必须执行的统一审查专家团
- 仅在高风险条件下中途做一次轻量预审
- 与 testing、skill-review、workflow-harness 分工清楚但彼此联动

这样既不会把整个 agent 流程变得过于碎片化，也能把“该出手时就出手”的治理要求真正落地。
