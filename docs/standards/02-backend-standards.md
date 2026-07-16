# Backend Standards

## 1. Backend Role

后端负责把本地工具能力包装成可被前端稳定调用的 API，同时管理鉴权、数据持久化和文件处理。当前不是通用平台后端，也不是分布式服务集群。

因此后端标准优先关注：

- 简单直接
- 可本地运行
- 失败边界明确
- 接口结构稳定

## 2. Composition Root

`backend/app/main.py` 只作为应用装配入口，负责：

- 创建 `FastAPI` app
- 注册 middleware
- `include_router(...)`
- 初始化数据库元数据

不要把业务路由、复杂序列化、工具执行逻辑重新堆回 `main.py`。

## 3. Route Organization

当前路由按能力域拆到 `backend/app/routers/**`：

- `health.py`
- `auth.py`
- `tools.py`
- `admin.py`
- `dashboard.py`
- `knowledge.py`

规范如下：

1. 工具类接口统一挂在 `/api/tools/*` 下。
2. 管理员接口统一挂在 `/api/admin/*` 下。
3. 面向工作台对象的数据接口使用资源式路径，如 `/api/nodes`。
4. `routers` 只做参数接收、依赖注入、错误边界和响应返回。

## 4. Core / Service / Repository Split

后端代码拆分遵循“入口薄、服务稳、仓储轻”的规则：

- `core/`: 配置、数据库、鉴权依赖
- `services/`: 业务逻辑、工具执行、结果组装、管理员能力
- `repositories/`: 只放明确有复用价值的数据访问逻辑

约束：

1. 业务流程优先放 `services/**`，不要散落在 router 中。
2. 不是所有模型都必须强行建 repository；仅在查询逻辑复用明显时抽取。
3. 兼容层文件可以保留，但真实实现以新分层为准。

## 5. Tool Domain Pattern

新增工具时默认复用以下模式：

- 路由入口：`routers/tools.py`
- 工具实现：`services/tools/<tool>.py`
- 运行记录：`services/tool_runs.py`
- 相关数据访问：按需进入 `repositories/**`

工具服务负责：

1. 输入校验
2. 文件保存
3. 外部命令调用
4. 结果组装
5. 失败清理

## 6. File Processing Standard

视频压缩与字幕工具属于本地文件处理流程，必须遵守以下规则：

1. 先校验输入扩展名和模式/语言参数
2. 先保存原始上传文件，再执行处理
3. 输出文件与源文件分目录管理
4. 下载接口只暴露 `file_id`，不暴露真实物理路径

## 7. Runtime Config Standard

运行时依赖统一从 `backend/app/core/config.py` 的 `settings` 读取。

必须配置化的内容包括：

- 运行模式：`app_runtime_mode`
- 服务地址：`api_host` / `api_port` / `frontend_origin`
- 数据库地址：`database_url`
- 文件目录：`video_upload_dir` / `video_output_dir` / `subtitle_output_dir` / `storage_policy_file`
- 外部命令：`ffmpeg_bin` / `ffprobe_bin`
- 转写能力：`transcribe_provider` / `whisper_model` / `whisper_device`

默认值应保持本地开发无需额外配置即可运行。服务器部署时通过 `.env` 覆盖配置，不通过修改业务代码适配环境。

## 8. Data Access Standard

当前数据访问以 SQLAlchemy Session 为主。规范如下：

- 路由通过 `Depends(get_db)` 获取会话
- 创建/更新后显式 `commit`
- 需要返回最新状态时使用 `refresh`
- 关联对象同步应集中到可复用服务函数中，例如 `sync_tags`

避免在多个路由里复制同一段模型同步逻辑。

## 9. Validation and Error Handling

参数校验优先放在两层：

1. `schemas/**` 中做结构与字段约束
2. `services/**` 中做运行时约束，例如扩展名、模式、依赖可用性

当前项目优先返回可读的 HTTP 错误：

- `400`: 参数不合法或输入不支持
- `401`: 未认证或认证失败
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 后端执行失败

## 10. Testing Standard

后端改动默认至少覆盖：

- `pytest -q`
- 受影响接口的 mock 或 API 级回归
- 关键工具成功/失败路径
- `tool_runs` 与 admin storage policy 相关回归

如果改动触及工具执行链路，优先补或调整测试，而不是只靠真实 `ffmpeg` 手测收口。
