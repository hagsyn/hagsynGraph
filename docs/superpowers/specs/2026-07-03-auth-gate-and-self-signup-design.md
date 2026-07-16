# Hagsyn Auth Gate And Self Signup Design

## Summary

为 Hagsyn-Graph 增加真实用户认证入口，要求未登录用户不能直接进入工作台壳或工具工作区，必须先登录或注册。当前采用最小可用账号体系：公网用户可自助注册，注册字段仅包含用户名、密码、手机号；手机号当前只做格式与唯一性校验，不接短信验证码。

该能力属于现有工作台壳的前置入口，不新增一级模块，不改变 `Dashboard / Tools / Nodes / Graph / Roadmaps` 作为登录后主工作区的骨架。

## Product Decision

### 1. Entry And Redirect

- 未登录用户访问任意业务路由时，统一重定向到 `/#login`
- 注册页使用 `/#register`
- 登录成功后默认进入 `/#dashboard`
- 已登录用户访问 `/#login` 或 `/#register` 时，重定向到 `/#dashboard`

### 2. Scope

本轮纳入实现：

- 登录
- 注册
- 基于真实用户表的 token 鉴权
- 登录态前端路由守卫
- 用户菜单显示真实用户信息
- 普通用户与管理员权限分层

本轮不纳入实现：

- 短信验证码
- 找回密码
- 修改密码
- 多角色运营后台
- 复杂权限系统

## Backend Design

### 1. User Model

新增 `User` 实体，最小字段：

- `id`
- `username`
- `phone`
- `password_hash`
- `status`
- `created_at`
- `updated_at`

约束：

- `username` 唯一
- `phone` 唯一

### 2. Auth API

新增或调整接口：

- `POST /api/auth/register`
  - 入参：`username`、`phone`、`password`、`confirmPassword`
  - 成功后直接返回登录成功态：`token + user`
- `POST /api/auth/login`
  - 入参：`account`、`password`
  - `account` 支持用户名或手机号
  - 成功后返回：`token + user`
- `GET /api/auth/me`
  - 返回当前登录用户基础信息

### 3. Password Rule

密码校验规则：

- 长度至少 8 位
- 必须同时包含字母和数字
- 不能与用户名相同
- `password` 与 `confirmPassword` 必须一致

密码只保存哈希值，不保存明文。

### 4. Token Strategy

- 现有固定单用户 token 方案改为真实用户 token
- `require_auth` 需能解析 token 并返回当前用户身份
- 管理员能力继续保留，但不再依赖“所有用户共用一个用户名”
- 管理员判断可基于配置中的管理员用户名白名单

### 5. Permission Boundary

匿名可访问：

- `GET /api/health`
- `POST /api/auth/login`
- `POST /api/auth/register`

登录后可访问：

- `Tools`
- `Nodes`
- `Graph`
- `Roadmaps`
- `Dashboard`

管理员专属：

- `/api/admin/storage-policy*`

## Frontend Design

### 1. Route Guard

前端初始化时先检查：

- 当前 hash 路由
- 本地 token 是否存在
- `GET /api/auth/me` 是否有效

规则：

- 未登录且当前不是 `/#login` / `/#register` -> 重定向到 `/#login`
- 已登录且当前是 `/#login` / `/#register` -> 重定向到 `/#dashboard`

### 2. Auth Shell

登录前不显示完整工作台内容。

未登录态显示认证页，仍复用现有深色开发者工具方向，但只保留轻量壳：

- 左侧可保留品牌信息
- 中间为登录 / 注册表单
- 不展示真实工具入口与工作区内容

### 3. Auth Views

新增两个前端路由视图：

- `/#login`
- `/#register`

登录表单字段：

- 用户名或手机号
- 密码

注册表单字段：

- 用户名
- 手机号
- 密码
- 确认密码

### 4. Login Success Behavior

登录或注册成功后：

- 写入 token
- 写入当前用户基础信息
- 跳转到 `/#dashboard`

登出后：

- 清除 token 与本地用户信息
- 跳转到 `/#login`

## Test And Acceptance

### Backend

至少覆盖：

- 注册成功
- 用户名重复失败
- 手机号重复失败
- 密码不合法失败
- 用户名登录成功
- 手机号登录成功
- 未登录访问受保护接口返回 `401`
- 普通用户访问管理员接口返回 `403`

### Frontend

至少覆盖：

- 未登录访问 `/#dashboard` 自动跳 `/#login`
- 未登录访问 `/#tools/video-compress` 自动跳 `/#login`
- 登录 / 注册切换可用
- 注册成功后进入 `/#dashboard`
- 登出后跳回 `/#login`
- 已登录访问 `/#login` 自动跳 `/#dashboard`

### Acceptance

- 新用户可自助注册
- 未登录无法直接进入工作台
- 登录成功后可正常进入现有工具工作区
- 管理员功能不向普通注册用户暴露

## Assumptions

- 当前阶段仍是单实例应用，用户数据先落本地数据库
- 手机号只做登记与唯一性校验，不做验证码校验
- 本轮先不引入完整 RBAC，只保留普通用户 / 管理员两层
- 没有安全短信验证链路前，本轮不提供在线“忘记密码”能力
