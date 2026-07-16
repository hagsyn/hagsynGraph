# Skill Standards

## 1. Scope

本规范适用于当前仓库下的项目内 skill，默认位置为：

- `.agents/skills/**`

## 2. Review Required

每次创建或修改 skill 后，都必须做一次 skill 审核，不能写完即视为可用。

审核重点不是“语法有没有错”，而是：

- 是否符合渐进式加载
- 是否把场景和 SOP 组织清楚
- 是否把脚本从主文档中分离出去
- 是否遵守当前仓库的统一实现约束

## 3. Progressive Disclosure

项目内 skill 必须优先采用渐进式加载。

要求：

1. `SKILL.md` 只保留：
   - 触发条件
   - 场景索引
   - 场景进入规则
   - 全局约束
2. 不把大量具体场景细节直接堆在 `SKILL.md`
3. 不使用“脚本索引”代替“场景索引”

推荐结构：

```txt
skill-name/
├── SKILL.md
├── references/
│   ├── scenario-a.md
│   ├── scenario-b.md
│   └── scenario-c.md
└── scripts/
    └── helper.py
```

## 4. Scenario-First References

每个 skill 的 `references/` 应按场景拆分，而不是按技术碎片拆分。

正确方向：

- `new-tool-page.md`
- `knowledge-shell-expansion.md`
- `skill-post-review.md`

不推荐：

- `script-list.md`
- `commands.md`
- `helpers.md`

核心原则是：让使用者先按场景定位，再在场景内部看到 SOP 和脚本调用方式。

## 5. SOP Requirement

每个场景文档必须有自己的 SOP。

每份 SOP 至少包含：

1. 适用场景
2. 前置检查
3. 执行步骤
4. 自校验步骤
5. 常见失败点

其中“自校验步骤”是强制项，不能省略。

## 6. Script Separation

如果场景中需要脚本调用：

- 脚本必须放到 `scripts/`
- 不把完整脚本直接塞进 `SKILL.md`
- 场景文档里只描述何时调用、传什么参数、如何校验结果

## 7. Python-Only Script Rule

当前项目内 skill 的脚本统一使用 Python 编写。

要求：

- 放在 `scripts/*.py`
- 不新增 Bash、Node、Ruby 脚本作为项目内 skill 默认实现

## 8. Kwargs Input Rule

项目内 skill 脚本的参数组织统一采用 kwargs 风格。

目标：

- 参数命名清晰
- 扩展时不容易破坏调用方式
- 场景文档中更容易描述

推荐方向：

```python
def run(**kwargs):
    ...
```

或者：

```python
def main(**kwargs):
    ...
```

如果需要 CLI 包装，也应在 Python 内部尽量汇总到 kwargs 风格处理。

## 9. Review Checklist

每次新增或修改 skill 后，至少检查：

1. `SKILL.md` 是否只保留索引与总规则
2. 是否按场景拆到 `references/`
3. 每个场景是否有 SOP
4. SOP 是否包含自校验步骤
5. 脚本是否独立到 `scripts/`
6. 脚本是否为 Python
7. 参数风格是否符合 kwargs 约束

## 10. Integration Rule

后续如果新增总控型 skill 或 brain skill，应默认把本规范作为 skill 创建后的审核依据，而不是每次靠口头补充。

## 11. Review Gate Rule

对于会影响代码、文档、skill、配置或验证口径的重要变更，除专项测试和 skill 审核外，收口前还应经过一次统一的全量变更 review。

推荐默认使用：

- `hagsyn-review-council`

目的不是重复测试，而是补上下面这些统一审查问题：

- 当前是否真的可以宣称完成
- 是否还有阻塞性问题或明显回归风险
- 文档、索引、skill、配置和验证证据是否同步到位

这条规则适用于重要功能开发、bug 修复、UI 调整和项目内 skill 治理。
