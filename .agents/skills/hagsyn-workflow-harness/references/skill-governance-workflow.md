# Skill Governance Workflow SOP

## 适用场景

当 `.agents/skills/**` 下发生以下任一情况时使用本 workflow：

- 新增项目内 skill
- 更新现有 skill 的 `SKILL.md`
- 为 skill 新增、改写或重组 `references/` 场景 SOP
- 新增、迁移或调整 skill 配套脚本、校验方式、治理约束

如果只是普通业务代码改动且不触及 skill 资产，不使用本 workflow。

## 前置检查

1. 确认目标是项目内 skill，而不是全局个人 skill 或外部插件。
2. 确认本次改动涉及哪些 skill 文件，提前圈定允许修改的范围。
3. 读取现有治理基线，至少覆盖：
   - `.agents/skills/hagsyn-product-brain/references/skill-governance.md`
   - `.agents/skills/hagsyn-skill-review/SKILL.md`
4. 检查 `SKILL.md` 是否应保持轻量，只承担触发条件、场景索引、总规则和路由说明。
5. 如果有脚本变更，确认脚本是否应放在 `scripts/`，并保持 Python-only、kwargs-style 参数约定。

## 执行步骤

1. 先按场景梳理 skill 的真实用途，判断哪些内容属于入口路由，哪些内容应下沉到 `references/` SOP。
2. 保持 `SKILL.md` 轻量化，不把完整执行手册、长篇校验细节或脚本说明重新塞回入口文件。
3. 为每个独立场景补齐或更新对应 SOP，至少包含：
   - 适用场景
   - 前置检查
   - 执行步骤
   - 自校验步骤
   - 常见失败点
4. 如有脚本支持：
   - 将脚本放入 `scripts/`
   - 使用 Python 实现
   - 明确 kwargs-style 调用方式
5. 完成内容修改后，必须执行 `hagsyn-skill-review`，检查：
   - `SKILL.md` 是否足够轻
   - 场景是否按 `references/` 组织
   - SOP 是否完整
   - 脚本位置、语言和参数风格是否合规
6. 若本次 skill 治理还联动了索引、标准、README、AGENTS 或其他治理面资产，在收口前再调用 `hagsyn-review-council` 做一次全量变更审查。
7. 根据 `hagsyn-skill-review` 结果修正问题，不把“已写完”当成“已治理完成”。
8. 收口时输出一份治理报告，至少说明：
   - 改了哪些 skill 文件
   - 哪些规则已满足
   - 运行了什么 review / 自检
   - 还有哪些风险或待后续收口项

## 自校验步骤

1. `SKILL.md` 是否仍然只承担轻量入口职责，没有变回大而全手册。
2. 新增或变更的场景是否已经拆成独立 SOP，而不是散落在不同文件中。
3. 每个 SOP 是否都包含完整的五段结构。
4. 如有脚本，是否已放在 `scripts/`，且为 Python-only、kwargs-style。
5. 是否已经实际执行 `hagsyn-skill-review`，而不是只口头声称会 review。
6. 若本次不只是单一 skill 结构调整，是否已经过 `hagsyn-review-council` 做全量收口审查？
7. 是否已经形成治理报告，能让主 agent 或后续维护者快速理解本次 skill 变更状态。
8. 是否全程避免回滚他人改动，并对现有文件结构做了兼容式更新。

## 常见失败点

- 只改 `SKILL.md`，没有把执行细节下沉到 `references/`。
- 有场景步骤但没有自校验，导致 SOP 只能看不能落地。
- 新增脚本直接用 Bash/JS，或参数接口继续依赖脆弱的位置参数。
- 写完 skill 后跳过 `hagsyn-skill-review`，直接宣称完成。
- 联动修改了索引和标准，却没有做全量治理面 review。
- 没有输出治理报告，后续无法快速判断 skill 是否真的已合规。
- 顺手改动无关 skill、README 或项目文档，扩大了治理范围。
