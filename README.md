# Hagsyn Video Compressor MVP

当前项目已收敛为一个本地单机版视频压缩工具 MVP。

当前 MVP 已包含：

- 上传常见视频格式 `mp4 / mov / m4v`
- 三种压缩模式：`平衡压缩 / 高压缩 / 高质量`
- FastAPI 同步压缩接口
- 本机 `ffmpeg` 压缩执行
- 压缩完成结果卡片
- 压缩后文件下载
- 单用户 Bearer Token 鉴权

## 目录结构

```txt
Hagsyn-Graph/
├── README.md
├── .agents/
│   └── skills/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   └── config.py
│   ├── tests/
│   │   └── test_api.py
│   └── requirements.txt
├── docs/
│   ├── INDEX.md
│   ├── archive/
│   ├── product/
│   ├── standards/
│   ├── testing/
│   └── ux/
└── frontend/
    └── index.html
```

## 规范资料

项目内已建立三条长期资料主线：

- `docs/product/`
  - 产品定位、信息架构、模块地图、工具策略、产品路线
- `docs/standards/`
  - 程序设计规范、代码开发规范、API 规范、数据建模规范、文档规范
- `docs/ux/`
  - UI 视觉规范、布局导航规范、组件规范、工具工作区模式、品牌语气

后续新增功能、调整模块或扩展工具时，默认先参考这三条文档主线，而不是直接凭临时口头约定推进。

如果要快速查看整个资料体系，从 [`docs/INDEX.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/INDEX.md) 开始。

## 项目内 Skills

当前仓库还建立了项目内 skill 控制层：

- `.agents/skills/hagsyn-product-brain/`
- `.agents/skills/hagsyn-workflow-harness/`
- `.agents/skills/hagsyn-product-council/`
- `.agents/skills/hagsyn-product-guard/`
- `.agents/skills/hagsyn-ui-workspace-pattern/`
- `.agents/skills/hagsyn-knowledge-shell/`
- `.agents/skills/hagsyn-testing-council/`
- `.agents/skills/hagsyn-review-council/`
- `.agents/skills/hagsyn-skill-review/`

这些 skill 用于约束后续产品开发、workflow 执行顺序、产品边界、UI 工作区模式、Knowledge 模块边界、测试与交付前全量审查，以及项目内 skill 自身的审核流程。

如果要看职责索引，从 [`docs/standards/08-project-skill-index.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards/08-project-skill-index.md) 开始。

## 本地启动

请先确认本机已安装 `ffmpeg`：

```bash
ffmpeg -version
```

推荐直接使用统一脚本：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
sh hagsyn-server.sh start
```

常用命令：

```bash
sh hagsyn-server.sh start
sh hagsyn-server.sh restart
sh hagsyn-server.sh stop
sh hagsyn-server.sh status

sh hagsyn-server.sh -front start
sh hagsyn-server.sh -front restart
sh hagsyn-server.sh -front stop
sh hagsyn-server.sh -front status

sh hagsyn-server.sh -backup start
sh hagsyn-server.sh -backup restart
sh hagsyn-server.sh -backup stop
sh hagsyn-server.sh -backup status
```

说明：

- 不带参数时，默认同时操作前端和后端
- `-front` 只操作前端静态服务
- `-backup` 只操作后端服务
- `-all` 和 `-mix` 也可用，等价于默认同时操作前后端
- 日志默认写入 `.runtime/logs/`

## 运行时配置

后端配置统一定义在 `backend/app/config.py`，并可通过 `backend/.env` 覆盖。当前默认是本地单机模式：

```env
APP_RUNTIME_MODE=local
API_HOST=127.0.0.1
API_PORT=8000
FRONTEND_ORIGIN=http://127.0.0.1:5173
DATABASE_URL=sqlite:///./hagsyn_graph.db
FFMPEG_BIN=ffmpeg
FFPROBE_BIN=ffprobe
TRANSCRIBE_PROVIDER=local
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
```

如果部署到服务器，优先通过 `.env` 调整这些值，而不是改业务代码。例如服务器上的 `ffmpeg` 路径不同，可以设置：

```env
APP_RUNTIME_MODE=server
FFMPEG_BIN=/usr/bin/ffmpeg
FFPROBE_BIN=/usr/bin/ffprobe
```

文件目录、鉴权账号和数据库也都应继续通过配置覆盖，保持同一套后端代码可在本地模式和服务器模式下运行。

### 1. 启动后端

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

健康检查：

```bash
curl http://127.0.0.1:8000/api/health
```

### 2. 打开前端

直接打开：

```txt
/Users/hagsyn/ai/workspace/Hagsyn-Graph/frontend/index.html
```

或用本地静态服务：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/frontend
python3 -m http.server 5173
```

浏览器访问：

```txt
http://127.0.0.1:5173/?v=video-compressor-v1
```

## 用户登录鉴权

当前 MVP 使用单用户登录，默认本地开发账号：

```txt
用户名：hagsyn
密码：hagsyn123
```

登录成功后，前端会把 token 存到 `localStorage`，并在请求中发送：

```txt
Authorization: Bearer hagsyn-local-dev-token
```

生产或公网部署前，请在 `backend/.env` 中覆盖默认账号、密码和 token：

```env
AUTH_USERNAME=hagsyn
AUTH_PASSWORD=换成强密码
AUTH_TOKEN=换成足够长的随机字符串
```

登录接口：

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"hagsyn","password":"hagsyn123"}'
```

除 `/api/health` 和 `/api/auth/login` 外，业务接口都需要 Bearer Token。

## 视频压缩接口

压缩接口：

```bash
curl -X POST http://127.0.0.1:8000/api/tools/video-compress \
  -H 'Authorization: Bearer hagsyn-local-dev-token' \
  -F mode=balanced \
  -F file=@/path/to/sample.mp4
```

下载接口：

```txt
GET /api/tools/video-compress/files/{file_id}
```

## 测试

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q
```

## v0.1 说明

这是当前真实可运行的首个工具型 MVP，重点是跑通“上传视频 → 选择压缩模式 → 后端本地压缩 → 展示结果卡片 → 下载文件”的核心闭环。后续可以继续增加更多真实工具能力，而不是继续维护 demo 数据。
