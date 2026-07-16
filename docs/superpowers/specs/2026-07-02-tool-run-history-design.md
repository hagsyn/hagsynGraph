# Tool Run History Design

## 目标

为 Hagsyn 增加正式的工具使用记录留痕能力，让每次真实工具执行都能留下可查询的业务级记录。

当前已有文件级留痕，例如上传文件、压缩结果、字幕结果会保存在本地 storage 目录中。但这不足以回答：

- 谁在什么时候用了哪个工具
- 输入文件是什么
- 执行是否成功
- 输出文件在哪里
- 执行耗时多久
- 失败原因是什么

本设计目标是补齐这层业务级历史记录，而不是实现完整任务队列或审计平台。

---

## 一、当前状态

当前已经存在：

- `backend/storage/uploads/`
- `backend/storage/compressed/`
- `backend/storage/subtitles/`
- 管理员存储清理策略
- 前端工具工作区结果卡片

当前不存在：

- 工具运行历史表
- 工具运行历史 API
- 工具维度的最近使用记录
- 成功 / 失败 / 耗时统计
- 输入输出文件摘要查询

因此当前只能从文件系统推断“可能执行过”，不能从产品层回答“发生过什么运行”。

---

## 二、产品边界

该能力属于：

- `Tools`

不属于：

- `Knowledge`
- `Nodes`
- `Graph`
- `Roadmaps`

本次做：

1. 后端记录工具运行历史
2. 三个已有工具接入记录：
   - `video-compress`
   - `vtt-subtitle`
   - `video-subtitle-burn`
3. 提供最近运行记录 API
4. 前端 Tools 页展示最近使用记录
5. 记录成功和失败状态

本次不做：

- 异步任务队列
- 后台 worker
- 任务取消
- 多用户审计后台
- 文件内容预览
- 复杂筛选统计
- 历史记录批量删除

---

## 三、数据模型

新增 ORM 模型：

- `ToolRun`

建议表名：

- `tool_runs`

字段：

- `id`: 字符串主键，前缀 `run_`
- `tool_type`: 工具 ID，例如 `video-compress`
- `username`: 当前执行用户
- `status`: `running` / `success` / `failed`
- `input_file_name`: 原始上传文件名
- `input_file_size`: 上传文件大小
- `output_file_name`: 输出文件名，可为空
- `download_url`: 下载地址，可为空
- `started_at`: 开始时间
- `completed_at`: 完成时间，可为空
- `duration_ms`: 耗时毫秒，可为空
- `error_message`: 失败原因，可为空
- `metadata_json`: JSON 字符串，记录模式、语言、片段数、压缩结果等轻量元数据

命名约定：

- ORM 字段使用 `snake_case`
- API 字段使用 `camelCase`

---

## 四、后端设计

新增模块：

- `backend/app/tool_runs.py`

职责：

1. `create_tool_run`
2. `mark_tool_run_success`
3. `mark_tool_run_failed`
4. `serialize_tool_run`

路由接入：

- 每个工具接口开始处理后创建 `running` 记录
- 成功后更新为 `success`
- 捕获明确失败后更新为 `failed`
- 失败仍按现有 HTTP 错误返回，不改变前端错误语义

新增 API：

- `GET /api/tools/runs`

查询参数：

- `limit`: 默认 `10`，最大 `50`
- `toolType`: 可选，按工具过滤

返回：

- 最近运行记录列表，按 `started_at desc`

---

## 五、前端设计

在 `Tools` 页面增加一个轻量区块：

- `最近使用记录`

位置：

- 工具目录下方或工作区下方
- 不压过主工具工作区

展示字段：

- 工具名称
- 状态
- 输入文件名
- 开始时间
- 耗时
- 下载入口（成功且有下载地址时）

当前前端保持单文件结构，不引入新框架。

失败记录应显示失败状态，但不要把错误堆成大段日志。

---

## 六、文件清理关系

工具使用记录和文件清理策略分离。

也就是说：

- 清理策略可以删除输出文件
- 历史记录仍可保留
- 如果下载文件已经不存在，下载接口继续返回 `404`
- 前端历史记录可以显示“文件可能已清理”

本轮不做历史记录自动清理。后续如果记录量变大，再新增保留天数配置。

---

## 七、错误处理

工具执行失败时：

1. 创建或保留当前 run 记录
2. 写入：
   - `status=failed`
   - `completed_at`
   - `duration_ms`
   - `error_message`
3. 继续按现有接口返回错误

记录失败本身不应遮蔽原始工具错误。

如果历史记录写入失败，本轮建议让接口返回 500，因为当前是本地 SQLite 工具工作台，数据库不可写说明环境本身异常。

---

## 八、测试策略

后端测试：

1. 工具运行成功后生成 `success` 记录
2. 工具运行失败后生成 `failed` 记录
3. `GET /api/tools/runs` 返回最近记录
4. `limit` 生效
5. `toolType` 过滤生效

前端测试：

1. Tools 页面包含 `最近使用记录`
2. 前端调用 `/api/tools/runs`
3. 成功记录展示下载入口
4. 失败记录展示失败状态

验证：

- `pytest -q`
- `node frontend/tests/ui-shell.test.js`
- `node --check /tmp/hagsyn-frontend-script.js`
- 浏览器真实打开 Tools 页确认记录区块不遮挡工具工作区

---

## 九、成功标准

本任务完成后：

1. 三个工具执行都会留下业务级 run 记录
2. 成功和失败都有记录
3. 前端 Tools 页能看到最近使用记录
4. 不改变现有工具接口核心返回结构
5. 不引入异步任务队列
6. 后端和前端验证通过
7. 测试报告记录本轮历史留痕能力
