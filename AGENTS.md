# AGENTS.md

## 项目定位

当前项目已收敛为一个本地单机版视频压缩工具 MVP。

用户当前更看重真实可用的工具链路：上传视频、选择压缩模式、完成压缩、返回下载结果。不需要 demo 图谱数据、假目录、空壳说明或过度工程化。

## 默认工作目录

项目路径：`/Users/hagsyn/ai/workspace/Hagsyn-Graph`

主要结构：

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
│   ├── tests/test_api.py
│   ├── requirements.txt
│   └── hagsyn_graph.db
├── docs/
│   ├── INDEX.md
│   ├── archive/
│   ├── product/
│   ├── standards/
│   ├── testing/
│   ├── ux/
│   └── superpowers/
└── frontend/
    └── index.html
```

## 规范资料目录

项目内长期规范默认参考以下目录：

- `docs/product/`
  - 产品定位、信息架构、模块职责、工具策略、路线规划
- `docs/standards/`
  - 工程原则、目录结构、前后端规范、API 规范、数据建模规范、文档规范
- `docs/ux/`
  - 设计原则、视觉系统、布局导航、组件规范、工具工作区模式、空状态规范、品牌语气

后续如果涉及模块调整、工具接入、接口变化、页面重构或规范收口，默认先看这些目录，再动实现。

建议把 [`docs/INDEX.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/INDEX.md) 作为进入文档体系的统一入口。

## 项目内 Skills

项目内 skill 放在：

- `.agents/skills/**`

当前已经存在的控制层 skill 包括：

- `hagsyn-product-brain`
- `hagsyn-workflow-harness`
- `hagsyn-product-council`
- `hagsyn-product-guard`
- `hagsyn-ui-workspace-pattern`
- `hagsyn-knowledge-shell`
- `hagsyn-testing-council`
- `hagsyn-review-council`
- `hagsyn-skill-review`

后续如果涉及产品开发总控、workflow 收口、产品判断、UI 工作区约束、Knowledge 模块边界、测试与交付前审查或项目内 skill 审核，默认优先参考这里，而不是只靠会话临时约定。

项目内专家团职责索引见：

- [`docs/standards/08-project-skill-index.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards/08-project-skill-index.md)

## 技术栈

- 后端：FastAPI + SQLAlchemy + Pydantic
- 默认数据库：SQLite，文件为 `backend/hagsyn_graph.db`
- 未来可切换：MySQL/MariaDB，通过 `DATABASE_URL` 环境变量或 `backend/.env`
- 前端：单文件原生 HTML/CSS/JavaScript，入口是 `frontend/index.html`
- 当前前端 API 默认地址：`http://127.0.0.1:8000`
- 当前前端静态服务常用地址：`http://127.0.0.1:5173`
- 当前登录方式：单用户 Bearer Token 鉴权，默认本地开发账号 `hagsyn` / `hagsyn123`
- 当前核心多媒体依赖：本机 `ffmpeg`

## 启动方式

后端：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

如果没有虚拟环境：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

前端：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/frontend
python3 -m http.server 5173
```

浏览器打开：

```txt
http://127.0.0.1:5173/?v=video-compressor-v1
```

`?v=video-compressor-v1` 用于绕过浏览器缓存；后续可换成任意版本参数。

## 验证命令

后端健康检查：

```bash
curl http://127.0.0.1:8000/api/health
```

接口数据检查：

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"hagsyn","password":"hagsyn123"}'

curl -X POST http://127.0.0.1:8000/api/tools/video-compress \
  -H 'Authorization: Bearer hagsyn-local-dev-token' \
  -F mode=balanced \
  -F file=@/path/to/sample.mp4
```

后端测试：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q
```

前端脚本语法检查：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
python3 - <<'PY'
from pathlib import Path
s = Path('frontend/index.html').read_text()
Path('/tmp/hagsyn-frontend-script.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/hagsyn-frontend-script.js
```

## 当前 API 路由

核心路由在 `backend/app/main.py`：

- `GET /api/health`
- `POST /api/auth/login`
- `POST /api/tools/video-compress`
- `GET /api/tools/video-compress/files/{file_id}`

除 `/api/health` 和 `/api/auth/login` 外，业务接口需要 `Authorization: Bearer <token>`。
默认本地开发配置在 `backend/app/config.py`，生产或公网部署前应通过 `backend/.env` 覆盖 `AUTH_USERNAME`、`AUTH_PASSWORD`、`AUTH_TOKEN`。

## Runtime Config Manifest

运行时配置统一从 `backend/app/config.py` 的 `Settings` 读取，并允许用 `backend/.env` 覆盖。默认值必须保持本地单机模式可直接运行。

当前关键配置项：

- `APP_RUNTIME_MODE`: 默认 `local`，服务器部署时可设为 `server`
- `API_HOST`: 默认 `127.0.0.1`
- `API_PORT`: 默认 `8000`
- `FRONTEND_ORIGIN`: 默认 `http://127.0.0.1:5173`
- `DATABASE_URL`: 默认 `sqlite:///./hagsyn_graph.db`
- `VIDEO_UPLOAD_DIR` / `VIDEO_OUTPUT_DIR` / `SUBTITLE_OUTPUT_DIR` / `STORAGE_POLICY_FILE`
- `FFMPEG_BIN`: 默认 `ffmpeg`
- `FFPROBE_BIN`: 默认 `ffprobe`
- `TRANSCRIBE_PROVIDER`: 默认 `local`
- `WHISPER_MODEL`: 默认 `base`
- `WHISPER_DEVICE`: 默认 `cpu`

涉及本机路径、外部命令、转写模型、文件存储目录、数据库地址的后端改动，默认都应从 `Settings` 读取，不要在工具模块里写死本机路径。服务器部署时通过 `.env` 切换路径和模式，不改业务代码。

## 已知坑点

1. `frontend/index.html` 曾经因为脚本被截断导致页面只显示外壳。修改前端后必须跑 `node --check` 检查内嵌 JS。
2. 如果页面仍旧是旧版样式，优先检查浏览器缓存，使用 `http://127.0.0.1:5173/?v=新的版本号` 或强刷。
3. 视频压缩失败时，优先检查本机 `ffmpeg` 是否可用，以及输入文件格式是否在 `mp4 / mov / m4v` 范围内。
4. 这个目录当前可能不是 Git 仓库，不要假设能用 `git status` 或提交记录判断变更。
5. `backend/.venv`、`.pytest_cache`、`hagsyn_graph.db` 是本地运行产物，除非用户明确要求，不要随意删除数据库。

## UI/UX 约定

当前 UI 已参考 `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` 的方向做过调整：

- 产品类型：Developer Tool / Knowledge Base / Dashboard
- 视觉风格：深色开发者工具、极简、AI-native 辅助感
- 字体：`IBM Plex Sans` + `JetBrains Mono`
- 配色：深色仪表盘底色，紫/蓝主强调色，绿色/橙色用于状态和业务价值
- 交互要求：导航 active 状态、hash 深链接、表单显式 label、键盘 focus-visible、空状态有行动提示

继续改 UI 时保持这个方向，不要改回浅色普通后台模板。

## 编码约定

- 后端保持现有 FastAPI + SQLAlchemy 风格，字段对外使用前端友好的 camelCase，如 `businessValue`、`sourceId`、`targetId`。
- 数据库模型字段内部可继续使用 snake_case，如 `business_value`、`source_id`。
- 前端目前是单文件 MVP，除非用户明确要工程化，否则不要贸然迁移到 React/Next.js。
- 修改前端时优先保持“打开即用”，不要引入构建步骤。
- 新增功能要保证核心闭环：上传视频 → 选择模式 → 压缩完成 → 下载结果。
- 用户偏好直接可用的本地 Web URL 和简洁结果说明。

## 常用排查流程

页面空白：

1. `curl -sS http://127.0.0.1:5173/ | head` 确认前端服务返回的是当前 `index.html`。
2. 跑前端脚本 `node --check`。
3. `curl http://127.0.0.1:8000/api/health` 确认后端在线。
4. 确认前端 `localStorage` 中 token 正常，或使用默认 `hagsyn-local-dev-token`。
5. 浏览器使用 `?v=版本号` 绕过缓存。

接口失败：

1. 查看 `backend/app/main.py` 实际路由，不要猜接口。
2. 运行 `pytest -q` 确认后端基本功能。
3. 文件上传失败时，检查 `python-multipart` 与 `ffmpeg` 是否可用。

## 用户沟通偏好

- 默认简体中文。
- 后续所有普通交流、方案说明、规范文档、设计文档、过程文档默认使用简体中文；代码、路径、配置键名、API 名称保持原文。
- 少问多做，能直接修就直接修。
- 给用户结果时优先给可打开地址、已修改文件、验证结果。
- 不要长篇解释内部过程；除非用户明确要诊断细节。
