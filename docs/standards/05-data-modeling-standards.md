# Data Modeling Standards

## 1. Modeling Goals

Hagsyn 的数据模型需要同时服务两个方向：

1. 当前已经生效的本地工作台能力
2. 后续可能进入实现的 `Nodes / Graph / Roadmaps`

因此建模标准必须兼顾“现在能用”和“未来可扩展”，但不能为了未来假设而扭曲当前实现。

## 2. Real Object First

数据模型只能承载真实对象、真实关系、真实建设任务。

允许：

- 记录真实 node
- 记录真实工具与项目关系
- 记录真实 roadmap steps

不允许：

- 为了演示图谱视觉效果制造大量无业务意义的节点
- 为了让 Dashboard 看起来更满而批量灌伪数据
- 在尚无真实使用场景时过度建模复杂关系

## 3. Internal And External Naming

当前约定：

- ORM 模型字段使用 `snake_case`
- API 对外字段使用 `camelCase`

示例：

- `business_value`
- `target_user`
- `step_order`

对外分别映射为：

- `businessValue`
- `targetUser`
- `order`

这个分层必须保持，避免把数据库命名风格直接泄漏到前端。

## 4. ID Strategy

当前模型主键采用带前缀的字符串 ID，例如：

- `node_xxx`
- `tag_xxx`
- `edge_xxx`
- `roadmap_xxx`
- `step_xxx`

规范如下：

- ID 必须稳定且对前端可传输
- 前缀应表达资源类型
- 不依赖数据库自增 ID 暴露给前端

## 5. Timestamp Strategy

涉及持久化实体时，默认包含：

- `created_at`
- `updated_at`

规范如下：

- 创建时间在插入时写入
- 更新时间在修改时自动更新
- 对外序列化为 `createdAt`、`updatedAt`

## 6. Relationship Rules

当前已有关系类型包括：

- `Node` 与 `Tag` 的多对多关系，通过 `NodeTag`
- `Edge` 连接两个 `Node`
- `Roadmap` 与 `RoadmapStep` 的一对多关系
- `RoadmapStep` 可选关联 `Node`

关系建模标准：

1. 关系必须表达真实语义
2. 中间表只承担关系职责，不附带无关字段
3. 级联删除策略要与产品边界一致

当前已有 `ondelete` 策略可以继续作为默认参考。

## 7. Enum-Like Field Rules

当前存在多类有限集合字段，例如：

- `Node.type`
- `Node.status`
- `RoadmapStep.status`

规范如下：

- 在 schema 层明确允许值
- 新增取值前先确认前端是否需要显示、筛选或映射
- 不能随意在数据库中写入文档外的新值

## 8. Tool Data Boundary

像视频压缩这样的本地工具，其运行过程未必都要入库。当前阶段遵循：

- 只有真正需要长期保留和查询的数据才建模
- 临时上传文件与输出文件优先走文件系统
- 不为了“看起来完整”而给每个工具先设计数据库表

也就是说，工具运行元数据默认不入库，除非后续明确需要历史记录、审计或任务列表。

当产品已经明确需要历史记录、审计或任务列表时，工具运行元数据可以建模为长期实体。当前标准模型为 `ToolRun`：

- 只记录运行摘要，不保存文件内容
- 记录工具类型、用户、状态、输入文件、输出下载地址、耗时、错误信息和轻量 metadata
- 成功和失败都应留痕
- 文件清理策略可以删除实际文件，但不应直接删除历史记录
- API 对外字段继续使用 `camelCase`

## 9. Evolution Rules

未来新增模型时，优先问清楚：

1. 这是长期实体，还是一次性执行过程。
2. 这个关系是否真的需要查询和展示。
3. 这类数据是否已经能被当前前端消费。

如果三个问题里有两个以上答案仍不明确，先写进产品或标准文档，不急着落表。

## 10. Migration Awareness

当前默认数据库是 SQLite，未来可切换 MySQL/MariaDB。因此建模时要避免依赖只在单一数据库上好用的技巧。

推荐保持：

- 基础字段类型清晰
- 约束简单直接
- 关系可迁移

如果后续引入显式迁移工具，应同步补充迁移规范；在此之前，模型改动需要谨慎，并确保本地测试和数据兼容性可接受。
