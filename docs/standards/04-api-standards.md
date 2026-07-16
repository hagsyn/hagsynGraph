# API Standards

## 1. API Design Goals

Hagsyn 的 API 首先服务当前本地工作台前端，其次才考虑未来扩展。因此 API 规范强调：

- 路径稳定
- 命名一致
- 鉴权清楚
- 返回结构适合前端直接消费

## 2. Base Rules

- 所有接口统一以 `/api` 开头
- 健康检查使用 `/api/health`
- 登录使用 `/api/auth/login`
- 工具能力使用 `/api/tools/*`
- 工作台实体资源使用复数名词路径，如 `/api/nodes`

避免混用动词式、页面式和资源式路径风格。

## 3. Auth Rules

除以下接口外，其余接口默认都需要 Bearer Token：

- `GET /api/health`
- `POST /api/auth/login`

前端请求示例：

```http
Authorization: Bearer hagsyn-local-dev-token
```

新增 API 时，除非它属于健康检查或登录流程，否则默认接入 `require_auth`。

## 4. Naming Rules

### Path Naming

- 使用小写字母
- 使用 `-` 连接多词工具路径
- 资源标识放路径参数中

示例：

- `/api/tools/video-compress`
- `/api/tools/video-compress/files/{file_id}`

### Field Naming

- 响应字段优先使用 `camelCase`
- 数据库模型字段可保持 `snake_case`
- 路由层负责从内部字段映射到对外字段

示例：

- `business_value` -> `businessValue`
- `source_id` -> `sourceId`
- `created_at` -> `createdAt`

## 5. Request And Response Rules

### Request

- 结构化 JSON 请求使用 Pydantic schema
- 文件上传使用 `multipart/form-data`
- 查询条件用 query params 表达

### Response

- 成功返回业务对象或状态对象
- 删除操作可返回 `{ "ok": true }`
- 不额外包一层通用 `data` 外壳，除非未来出现明确一致性需求

当前项目已经形成的返回模式应继续保持一致。

## 6. Resource Interface Rules

当前资源类接口应遵循 REST 风格：

- `POST /api/nodes`
- `GET /api/nodes`
- `GET /api/nodes/{node_id}`
- `PUT /api/nodes/{node_id}`
- `DELETE /api/nodes/{node_id}`

`edges`、`roadmaps` 等资源保持同样风格。

## 7. Tool Interface Rules

工具接口与资源接口不同，它们围绕用户动作设计，但依然要保持可预期：

- 路径以工具 ID 为中心
- 参数约束由后端控制
- 返回结果包含前端立即需要的字段

以视频压缩为例，返回应至少包含：

- 原文件名
- 模式值与模式标签
- 原始体积
- 压缩后体积
- 节省大小
- 压缩比例
- 下载地址

## 8. Error Rules

错误返回要让前端能直接做用户提示。规范如下：

- 参数错误返回 `400`
- 鉴权失败返回 `401`
- 资源缺失返回 `404`
- 执行失败返回 `500`

错误信息应尽量短而明确，不返回与用户无关的内部细节。

## 9. Compatibility Rules

接口一旦被前端使用，就不要随意变更：

- 路径
- 鉴权方式
- 关键字段名
- 核心返回结构

如果必须调整，至少同步更新：

- 前端调用逻辑
- 测试
- 对应标准文档

## 10. Validation And Documentation

新增或修改 API 后，至少完成以下两项中的一项以上：

- 更新 `backend/tests/test_api.py`
- 用 `curl` 做真实调用验证

如果改动已经触及命名、鉴权或资源边界，也应同步更新本文件。
