# Hagsyn AI Workspace

Hagsyn 是一个面向真实任务的 AI 工作台。

它不是单一工具页，也不是知识图谱演示站，而是一个保留统一产品骨架、优先承载真实工具，并为后续知识沉淀预留结构空间的本地工作台产品。

当前 README 采用产品规划口径，不把仓库简单定义成某一个现状中的单点工具。

## 产品定位

Hagsyn 当前的核心方向是：

- 保持 `Dashboard / Tools / Nodes / Graph / Roadmaps` 的工作台骨架
- 以 `Tools` 作为当前第一优先级的真实执行层
- 让 `Nodes / Graph / Roadmaps` 作为后续知识沉淀的长期模块
- 用统一的前后端和文档体系支撑后续持续扩展

一句话来说：

> Hagsyn 是一个 AI 工作台，先把真实能用的工具放进来，再围绕实际使用过程沉淀知识、关系和路线。

## 当前模块骨架

当前产品骨架包括：

- `Dashboard`
  - 工作台首页与状态总览
- `Tools`
  - 真实工具目录与工具工作区
- `Nodes`
  - 知识对象承载位
- `Graph`
  - 对象关系承载位
- `Roadmaps`
  - 路线与阶段目标承载位

其中：

- `Tools` 是当前主线
- `Knowledge` 相关模块保留结构，但不依赖 demo 数据伪造活跃度

## 建设原则

- 真实工具优先，不做只看起来完整的展示型壳子
- 所有能力尽量落在统一工作台内，而不是各自长成割裂页面
- 先保住产品骨架，再逐步扩展工具与知识能力
- 文档、标准、UX 和项目内 skill 一起作为长期治理基线

## 目录结构

```txt
Hagsyn-Graph/
├── README.md
├── .agents/
│   └── skills/
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── deploy/
├── docs/
│   ├── INDEX.md
│   ├── product/
│   ├── standards/
│   ├── testing/
│   └── ux/
├── frontend/
│   ├── assets/
│   ├── tests/
│   └── index.html
└── hagsyn-server.sh
```

## 文档体系

项目内长期文档主线包括：

- `docs/product/`
  - 产品定位、信息架构、模块地图、工具策略、路线规划
- `docs/standards/`
  - 工程原则、前后端规范、API、数据建模、文档与 skill 规范
- `docs/ux/`
  - 视觉系统、布局导航、组件规范、工具工作区模式、品牌语气
- `docs/testing/`
  - 功能测试报告与交互验证记录

统一入口：

- [`docs/INDEX.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/INDEX.md)

## 项目内 Skills

当前仓库已建立项目内治理 skill，包括：

- `hagsyn-product-brain`
- `hagsyn-product-council`
- `hagsyn-product-guard`
- `hagsyn-workflow-harness`
- `hagsyn-ui-workspace-pattern`
- `hagsyn-knowledge-shell`
- `hagsyn-testing-council`
- `hagsyn-review-council`
- `hagsyn-skill-review`
- `hagsyn-git-push-receipt`
- `hagsyn-cd-receipt`

职责索引见：

- [`docs/standards/08-project-skill-index.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/standards/08-project-skill-index.md)

## 本地启动

推荐先确认本机已安装 `ffmpeg`：

```bash
ffmpeg -version
```

统一启动脚本：

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

- 默认同时操作前端和后端
- `-front` 只操作前端静态服务
- `-backup` 只操作后端服务
- 日志默认写入 `.runtime/logs/`

## 运行时配置

后端配置统一定义在 `backend/app/config.py`，并允许通过 `backend/.env` 覆盖。

当前默认配置示例：

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

部署到服务器时，优先通过 `.env` 覆盖，不直接改业务代码。

## 本地访问

后端健康检查：

```bash
curl http://127.0.0.1:8000/api/health
```

前端静态服务：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/frontend
python3 -m http.server 5173
```

浏览器访问：

```txt
http://127.0.0.1:5173/?v=hagsyn-workspace
```

## 登录与接口

当前本地开发默认账号：

```txt
用户名：hagsyn
密码：hagsyn123
```

登录接口：

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"hagsyn","password":"hagsyn123"}'
```

除 `/api/health` 和 `/api/auth/login` 外，业务接口需要 Bearer Token。

## 当前说明

当前仓库里已经有若干真实工具与工作区实现，但 README 的定位以产品规划和工作台主线为准，不以某一个阶段性的单点工具现状来定义整个项目。

更具体的产品口径，请优先查看：

- [`docs/product/00-product-positioning.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/product/00-product-positioning.md)
- [`docs/product/01-information-architecture.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/product/01-information-architecture.md)
- [`docs/product/02-module-map.md`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/docs/product/02-module-map.md)
