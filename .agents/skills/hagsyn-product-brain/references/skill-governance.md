# Skill Governance SOP

## 适用场景

当 `.agents/skills/**` 下新增或修改项目内 skill 时使用。

## 前置检查

1. 确认这是项目内 skill，而不是外部全局 skill
2. 确认 skill 是否已经存在 `SKILL.md`
3. 确认是否新增了 `references/` 或 `scripts/`

## 执行步骤

1. 先检查 `SKILL.md` 是否只保留：
   - 触发条件
   - 场景索引
   - 总规则
2. 将具体场景拆到 `references/`，按场景而不是脚本组织
3. 为每个场景写 SOP，至少包含：
   - 适用场景
   - 前置检查
   - 执行步骤
   - 自校验步骤
   - 常见失败点
4. 如有脚本调用：
   - 脚本放到 `scripts/`
   - 使用 Python
   - 参数组织遵循 kwargs 风格
5. 完成后必须触发 `hagsyn-skill-review`

## 自校验步骤

1. `SKILL.md` 是否已足够轻量
2. 场景是否已独立放在 `references/`
3. 每个场景是否有 SOP 和自校验
4. 脚本是否全部隔离到 `scripts/`
5. 脚本是否为 Python
6. 参数风格是否明确为 kwargs
7. 是否已走 `hagsyn-skill-review`

## 常见失败点

- 把完整执行细节继续堆回 `SKILL.md`
- 用脚本列表代替场景索引
- 场景有步骤但没有自校验
- 混入 bash 或 js 脚本
- 写完 skill 就直接算完成，没有审核
