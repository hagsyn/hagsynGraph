# Hagsyn Workflow Harness Design

## 目标

为 Hagsyn 建立一个重型、尽量自动执行的 `workflow harness`，把高频、重复、容易走偏的开发动作固化成 workflow，使后续产品开发不再依赖临场记忆和人工补漏。

该 harness 的目标不是替代现有的 `brain / council / guard / testing-council / skill-review`，而是把这些能力组织成一套**可重复执行的流程控制系统**。

---

## 一、为什么需要 workflow harness

当前项目已经具备：

- 产品主线文档
- 工程规范文档
- UI/UX 规范文档
- 多个项目内 skill
- stop hook 规则
- 测试专家团
- skill 审核规则

但这些能力目前仍然更像“分散的规则和工具”，不是统一的流程执行器。

实际暴露出来的问题包括：

- 功能开发时容易漏测试
- 页面改完后容易忘记做真实点击验证
- 某些状态文案与真实可用性不一致
- bug 修复后未必自动补回归
- skill 新建后可能不经过完整审核
- 会话容易停在半程汇报，而不是继续把当前流程跑完

这些问题都说明：项目已经不只是需要 skill，而是需要一个**流程治理层**。

---

## 二、推荐定位

推荐名称：

`hagsyn-workflow-harness`

推荐定位：

> 一个面向 Hagsyn 的流程执行中枢，用于把常规开发事项转换成结构化 workflow，并尽量自动推动检查、验证、报告和 stop hook 决策。

这个 harness 不是：

- 单一技能库
- 单一判断器
- 单一实现器

它是：

- workflow 选择器
- 阶段门禁器
- 偏航纠正器
- 执行链编排器

---

## 三、推荐架构关系

### `hagsyn-product-brain`

负责：

- 高层分类
- 读取文档
- stop hook
- 决定是否需要调用 harness

### `hagsyn-workflow-harness`

负责：

- 选择 workflow
- 推动顺序执行
- 检查哪些步骤不可跳过
- 要求验证和报告落盘

### 其他 skill 的角色

- `hagsyn-product-council`
  - 产品判断
- `hagsyn-product-guard`
  - 产品边界守门
- `hagsyn-ui-workspace-pattern`
  - 工作区 UI 模式守门
- `hagsyn-knowledge-shell`
  - Knowledge 模块壳层守门
- `hagsyn-testing-council`
  - 测试策略与测试报告守门
- `hagsyn-skill-review`
  - skill 规范审核

一句话就是：

**brain 决策，harness 执行。**

---

## 四、第一版要覆盖的 4 条流程

第一版直接把以下 4 条流程一起纳入设计：

1. 新功能开发 workflow
2. bug 修复 workflow
3. UI 调整 workflow
4. skill 治理 workflow

这四条一起设计，是为了统一语言和边界。  
但实现优先级可以先放在前两条：

- 新功能开发
- bug 修复

---

## 五、Workflow 1：新功能开发

适用范围：

- 新工具
- 新模块能力
- 新交互链路
- 真实需求进入实现

推荐链路：

1. 分类任务
2. 读取 `docs/product / docs/standards / docs/ux`
3. 判断模块落点
4. 如有必要，调用 `hagsyn-product-council`
5. 落 spec / plan
6. 实现
7. API 验证
8. 前端结构验证
9. 网页点击验证
10. 测试报告落盘
11. stop hook 判断是否继续

强约束：

- 没有测试不算完成
- 没有测试报告不算完成
- 没有点击验证的前端变更不算完成

---

## 六、Workflow 2：Bug 修复

适用范围：

- 接口报错
- 页面行为异常
- 文案与真实状态不一致
- 缺陷回归

推荐链路：

1. 复现问题
2. 定位根因
3. 补回归测试
4. 修复实现
5. 跑受影响 API 测试
6. 跑前端结构或脚本检查
7. 必要时做真实网页点击验证
8. 更新测试报告
9. stop hook 判断是否继续

强约束：

- 没有回归测试，不算完成
- 根因不清，不允许直接拍修复

---

## 七、Workflow 3：UI 调整

适用范围：

- 页面布局变化
- 工作区模式变化
- 状态区、详情区、菜单、设置面板等视觉交互变化

推荐链路：

1. 读取 `docs/ux/**`
2. 判断是否会破坏当前工作台壳
3. 如有需要，调用 `hagsyn-ui-workspace-pattern`
4. 实现
5. 前端壳测试
6. `node --check`
7. 真实网页点击验证
8. 测试报告落盘
9. stop hook 判断是否继续

强约束：

- 用户可见交互变化不能只靠接口测试
- 状态文案必须和真实可用性一致

---

## 八、Workflow 4：Skill 治理

适用范围：

- 新建项目内 skill
- 修改项目内 skill
- skill 结构重构

推荐链路：

1. 创建或修改 skill
2. 保持 `SKILL.md` 轻量
3. 场景拆到 `references/`
4. 如有脚本，放到 `scripts/`
5. 调 `hagsyn-skill-review`
6. 如有需要，更新 standards
7. 补 skill 变更报告
8. stop hook 判断是否继续

强约束：

- 新 skill 不经审核，不算完成
- 场景必须有 SOP
- SOP 必须带自校验

---

## 九、自动化程度建议

你已经明确选择“尽量全自动，能执行的都执行”，所以第一版 harness 应尽量推动这些动作自动发生：

### 默认自动推进

- 自动判断该走哪条 workflow
- 自动要求读取规范文档
- 自动判断是否该调下层 skill
- 自动要求测试
- 自动要求测试报告
- 自动要求 stop hook 执行

### 不替代用户做的事情

- 最终业务方向拍板
- 需要业务输入的关键判断
- 外部资源授权

也就是说，它应尽量自动推进，但不越过真正属于用户的业务决定。

---

## 十、建议目录结构

推荐目录：

```txt
.agents/
└── skills/
    └── hagsyn-workflow-harness/
        ├── SKILL.md
        └── references/
            ├── feature-development-workflow.md
            ├── bugfix-workflow.md
            ├── ui-adjustment-workflow.md
            └── skill-governance-workflow.md
```

说明：

- `SKILL.md` 只保留触发条件、workflow 索引、总规则
- `references/` 存 4 条 workflow 的 SOP
- 当前不强制加 `scripts/`
- 后续如果真需要自动化脚本，再按 Python + kwargs 规则接入

---

## 十一、第一版实现优先级

虽然 4 条流程一起设计，但第一版实现建议优先顺序为：

### 第一优先级

1. 新功能开发 workflow
2. bug 修复 workflow

### 第二优先级

3. UI 调整 workflow
4. skill 治理 workflow

原因：

- 这两条最贴当前主线
- 最能立刻减少走偏和漏项

---

## 十二、推荐结论

推荐立即创建：

`hagsyn-workflow-harness`

并采用：

- 重型 workflow 中枢定位
- 四条流程一起设计
- 前两条优先实现
- 以“自动推进常规事项”为核心目标

这是当前 Hagsyn 从“有一组 skill”进化为“有一套流程治理能力”的正确方向。
