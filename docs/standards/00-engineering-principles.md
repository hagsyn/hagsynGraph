# Engineering Principles

## 1. Scope First

Hagsyn 当前是一个本地单机版工具工作台，核心目标是持续交付真实可用的工具能力。所有工程决策都应先回答两个问题：

1. 这次改动是否直接服务当前用户真实使用场景。
2. 这次改动是否保持了“打开即用、可本地验证、可继续扩展”的产品边界。

当前阶段优先级高于一切的闭环是：上传视频、选择压缩模式、完成压缩、返回下载结果。

## 2. Real Capability Over Demo

- 不用 demo 数据判断产品价值。
- 不为了填满页面制造伪节点、伪图谱、伪路线图。
- 可以保留模块骨架，但只有在真实对象和真实需求出现后才进入实现。

`Dashboard / Tools / Nodes / Graph / Roadmaps` 可以作为产品信息架构长期保留，但是否继续深挖，必须由真实工作流驱动。

## 3. Small, Verifiable Steps

- 优先做小步迭代，不做一次性大重构。
- 每次交付都要能用已有命令完成本地自检。
- 文档、接口、实现三者保持一致；如果实现边界变了，标准文档应同步更新。

当前项目最重要的验证方式包括：

- `curl http://127.0.0.1:8000/api/health`
- `pytest -q`
- `node --check` 检查 `frontend/index.html` 内嵌脚本

## 4. Preserve The Product Shell

当前前端虽然是单文件实现，但它已经承担产品壳职责：导航、主题、工具入口、右侧详情区、弹框和状态反馈都在这个壳内完成。

因此：

- 新工具优先接入现有 `Tools` 工作区模式。
- 非明确需求下，不推翻现有导航和页面层级。
- 不把单个工具实现成独立站点式页面。

## 5. Prefer Existing Patterns

后端当前采用 FastAPI + SQLAlchemy + Pydantic，前端采用单文件 HTML/CSS/JavaScript。新增能力优先遵循现有模式：

- 后端路由继续放在 `backend/app/main.py`，复杂工具逻辑拆到独立模块。
- 数据模型字段内部使用 `snake_case`，对外接口优先使用前端友好的 `camelCase`。
- 前端保持无构建步骤、直接可运行。

只有当现有模式已经明显阻碍交付时，才考虑工程化升级。

## 6. Local-First Runtime

当前运行环境以本机为主，依赖包括：

- SQLite
- 本地文件系统
- `ffmpeg`
- 本地静态服务与本地 API 服务

因此工程标准默认围绕本地可维护性设计：

- 文件落地路径要清晰。
- 出错信息要有明确边界。
- 不引入当前阶段并不需要的队列、对象存储、分布式调度或复杂部署抽象。

## 7. Documentation Is Part Of The System

标准文档不是补充材料，而是当前产品的一部分。涉及目录边界、API 约束、数据建模方向、文档归档方式的变化时，应优先维护 `docs/standards/**`，而不是让口头共识长期漂移。

## 8. Extension Without Premature Generalization

Hagsyn 需要为后续工具扩展、知识对象建设和产品升级留出空间，但不能提前把未来方案全部落进今天的实现。

推荐做法：

- 先把扩展点写进文档。
- 等真实需求稳定后，再把扩展点落成代码。
- 当前实现只承担已确认的使用价值。
