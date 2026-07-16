# Project Structure

## 1. Current Top-Level Structure

当前项目仍围绕三条主线组织：

```txt
Hagsyn-Graph/
├── backend/
├── frontend/
└── docs/
```

- `backend/`: 本地 API、鉴权、数据访问、工具处理逻辑
- `frontend/`: 无构建静态前端壳与工具工作区
- `docs/`: 产品、标准、UX 与设计沉淀

这三部分共同服务当前 MVP，而不是独立演进的三套系统。

## 2. Backend Boundary

`backend/` 负责：

- 暴露 HTTP API
- 鉴权
- 数据持久化
- 本地文件上传、压缩、下载
- 为前端返回稳定的数据结构

当前工程结构采用“组合入口 + 领域分层”：

```txt
backend/app/
├── main.py
├── core/
├── routers/
├── services/
├── repositories/
├── models/
├── schemas/
└── seed_data.py
```

关键职责：

- `main.py`: 创建 app、注册 middleware、挂载 routers
- `core/`: 配置、数据库、鉴权依赖
- `routers/`: API 路由入口，负责请求接收、依赖注入、响应返回
- `services/`: 业务逻辑、工具执行、结果组装、管理员能力
- `repositories/`: 明确有复用价值的数据访问逻辑
- `models/`: SQLAlchemy 数据模型
- `schemas/`: Pydantic 请求/响应模型

## 3. Frontend Boundary

`frontend/` 当前采用“单入口、多资源文件、无构建链”：

```txt
frontend/
├── index.html
├── assets/
│   ├── css/
│   └── js/
└── tests/
```

- `index.html`: 统一产品壳与挂载容器
- `assets/css/`: 样式拆分，承载 base / layout / components
- `assets/js/`: 浏览器原生 ES modules，按 `api / state / components / views / tools / utils` 分层
- `tests/`: 前端壳与模块结构检查

这次拆分的目标是降低单文件职责堆叠，而不是引入构建器或框架。

## 4. Docs Boundary

`docs/` 下的目录职责如下：

```txt
docs/
├── product/
├── standards/
├── ux/
└── superpowers/
```

- `product/`: 产品定位、模块职责、路线规划
- `standards/`: 工程与代码规范
- `ux/`: 视觉与交互规范
- `superpowers/`: 本轮设计文档、计划文档等过程材料

## 5. Directory Expansion Rules

新增目录时遵循以下原则：

1. 只有当职责已经稳定时才拆目录。
2. 目录命名优先表达业务或工程职责，而不是表达技术偏好。
3. 不把同一职责拆进多个层级相近的目录中。
4. 前端继续保持“静态资源直出”，不因为拆分目录就引入构建链。
5. 后端只有在职责明显增长时才继续细分领域包，不做教科书式过度分层。

## 6. File Placement Rules

- 路由入口放 `backend/app/routers/**`
- 鉴权、配置、数据库放 `backend/app/core/**`
- 业务逻辑与工具执行放 `backend/app/services/**`
- 复用型查询逻辑放 `backend/app/repositories/**`
- 数据模型与序列化约束分别放 `backend/app/models/**` 和 `backend/app/schemas/**`
- 前端入口壳层留在 `frontend/index.html`
- 前端 API / 状态 / 组件 / view / 工具逻辑分别放 `frontend/assets/js/**`
- 长期标准文档放 `docs/standards/**`

## 7. Future Growth Direction

后续如新增更多真实工具，推荐的结构演进方向是：

1. 保持 `frontend/index.html` 为统一产品壳
2. 在 `frontend/assets/js/tools/**` 新增工具模块
3. 在 `backend/app/services/tools/**` 与 `backend/app/routers/tools.py` 扩展新工具能力
4. 当知识对象和路线逻辑明显增多后，再考虑继续细分 knowledge 领域服务

目录演进必须服务真实复杂度，而不是预先模拟大系统。
