# Runtime Config Manifest Design

## 目标

为 Hagsyn 建立一份正式的运行时配置清单（runtime config manifest），用于统一管理：

- 本地模式
- 服务器模式
- 工具命令路径
- 转写依赖
- 文件存储目录
- 鉴权与管理员配置
- 数据库配置

目标不是立刻把产品重构成云平台，而是让当前代码不再把“本地机器特定事实”硬写死在实现里。

---

## 一、为什么现在要做

当前 Hagsyn 已经具备多个真实工具能力：

- 视频压缩
- VTT 字幕生成
- 视频字幕烧录（链路推进中）

这些工具已经明显依赖运行环境差异，例如：

- `ffmpeg`
- `ffprobe`
- 本地转写引擎
- 模型文件
- 上传目录
- 输出目录
- 本地数据库

如果这些东西继续零散地写在代码里，就会带来两个问题：

1. 本地开发没问题，但一上服务器就失真
2. 后续切环境时需要改代码，而不是改配置

因此，现在就应该建立正式配置清单。

---

## 二、设计原则

运行时配置体系应遵循以下原则：

### 1. 默认值保持当前本地行为

也就是说，新增配置后：

- 当前本地开发不需要额外折腾就能继续运行

### 2. 服务器切换靠配置，不靠改代码

目标是：

- 本地模式和服务器模式共用同一套实现
- 不同环境只切配置

### 3. 受环境影响的能力都应配置化

凡是会因为“机器不同”而变化的内容，都不应写死。

### 4. 配置项数量要适度

不是所有东西都要抽成配置，重点抽那些：

- 真受环境影响
- 后续很可能要变
- 会影响工具可用性

---

## 三、当前已存在配置

当前已存在的配置基础在：

- [`backend/app/config.py`](../../backend/app/config.py)

已经有：

- `app_name`
- `database_url`
- `auth_username`
- `auth_password`
- `auth_token`
- `video_upload_dir`
- `video_output_dir`
- `subtitle_output_dir`
- `storage_policy_file`
- `admin_users`

这些可以视为 runtime config manifest 的初始基础。

---

## 四、推荐新增配置清单

### A. 运行模式

- `APP_RUNTIME_MODE`
  - `local`
  - `server`

用途：

- 区分当前是本机工具工作台模式还是服务器部署模式

---

### B. 服务地址

- `API_HOST`
- `API_PORT`
- `FRONTEND_ORIGIN`

用途：

- 规范本地/服务器模式下服务访问方式

当前本地默认建议值：

- `API_HOST=127.0.0.1`
- `API_PORT=8000`
- `FRONTEND_ORIGIN=http://127.0.0.1:5173`

---

### C. 数据库

- `DATABASE_URL`

当前默认值：

- `sqlite:///./hagsyn_graph.db`

当前真实状态：

- 仍然是 SQLite 本地文件

未来服务器建议：

- 可切到 MySQL / MariaDB

---

### D. 鉴权与管理员

- `AUTH_USERNAME`
- `AUTH_PASSWORD`
- `AUTH_TOKEN`
- `ADMIN_USERS`

当前默认值保持不变：

- `hagsyn`
- `hagsyn123`
- `hagsyn-local-dev-token`
- `["hagsyn"]`

---

### E. 文件目录

- `UPLOAD_DIR`
- `COMPRESSED_DIR`
- `SUBTITLE_DIR`
- `STORAGE_POLICY_FILE`

当前本地默认值建议对齐现有实现：

- `./storage/uploads`
- `./storage/compressed`
- `./storage/subtitles`
- `./storage/storage_policy.json`

用途：

- 本地和服务器可使用不同挂载目录

---

### F. 工具命令路径

- `FFMPEG_BIN`
- `FFPROBE_BIN`

这是当前最重要的新增配置之一。

原因：

- 当前机器已经存在多个 `ffmpeg`
- 不同环境里 `ffmpeg` 能力不同
- 视频字幕烧录工具对 `subtitles/libass` 能力高度敏感

当前本地推荐值可以先指向：

- 普通默认系统 `ffmpeg`
  或
- 显式指定支持 `subtitles/libass` 的版本

后续服务器模式可直接改路径，不改代码。

---

### G. 转写引擎

- `TRANSCRIBE_PROVIDER`
  - `local`
  - `api`
- `WHISPER_MODEL`
  - `base`
  - `small`
  - 其他
- `WHISPER_DEVICE`
  - `cpu`
  - `gpu`

当前本地建议默认：

- `TRANSCRIBE_PROVIDER=local`
- `WHISPER_MODEL=base`
- `WHISPER_DEVICE=cpu`

用途：

- 以后切服务器、切模型、切 provider 都不需要改业务代码

---

## 五、本地模式与服务器模式

### 本地模式

特点：

- 本地 SQLite
- 本地 `ffmpeg`
- 本地 `faster-whisper`
- 本地文件系统
- 本地管理员 `hagsyn`

适合：

- 当前阶段
- 开发验证
- 单机工具工作台

### 服务器模式

特点：

- 服务地址可变
- 数据库可替换
- 存储目录可挂载
- 命令路径不可假设与本机一致
- 模型和算力需要单独规划

适合：

- 正式部署
- 多用户使用
- 更稳定的文件生命周期管理

---

## 六、推荐代码接入方式

### 第一阶段

只做配置清单和 Settings 扩展，不立刻重写所有业务逻辑。

### 第二阶段

优先把以下高风险写死项改成从配置里取：

1. `ffmpeg` 路径
2. `ffprobe` 路径
3. 存储目录
4. 转写 provider / model / device

### 第三阶段

再逐步把：

- 前端默认 API 地址
- 运行模式说明
- 部署模式差异

同步到文档和实现里。

---

## 七、推荐结论

建议立即建立一份正式 runtime config manifest。

原则是：

- 默认值保持当前本地行为
- 后端统一从配置取
- 以后本地 / 服务器通过配置适配

最应优先配置化的项是：

1. `FFMPEG_BIN`
2. `FFPROBE_BIN`
3. `TRANSCRIBE_PROVIDER`
4. `WHISPER_MODEL`
5. `WHISPER_DEVICE`
6. 存储目录相关配置

这会显著降低后续服务器部署时的代码改造成本。
