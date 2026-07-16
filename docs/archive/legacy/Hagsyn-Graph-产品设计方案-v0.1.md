# Hagsyn Graph

> **产品设计方案 v0.1**  
> 一个面向个人 AI 工具沉淀、路线规划与知识图谱可视化的工作台。

---

## 文档信息

| 项目 | 内容 |
|---|---|
| 产品名称 | Hagsyn Graph |
| 中文定位 | Hagsyn AI 作战地图 / 知识工具地图 |
| 所属品牌 | Hagsyn |
| 产品阶段 | v0.1 MVP |
| 使用场景 | 个人自用，后续扩展为可分享、可协作、可运营产品 |
| 技术方向 | Next.js + FastAPI + MySQL/MariaDB |

---

## 产品摘要

**Hagsyn Graph** 是 Hagsyn 平台下的个人知识图谱产品，用于沉淀 AI 工具、模型、框架、项目、资源与学习路线，并通过可视化关系图帮助用户发现技术路径、项目机会和商业化方向。

v0.1 不追求“全自动知识图谱”，而是先完成一个**手动可维护、结构化、可视化**的个人 AI 工具知识库。

---

## 阅读摘要

这份 v0.1 方案主要确定三件事：

- **做什么**：个人 AI 工具路线图与知识图谱工作台。
- **怎么做**：先手动维护节点、关系和路线图，不急着做全自动知识图谱。
- **怎么落地**：前端 `Next.js`，后端 `FastAPI`，数据库 `MySQL/MariaDB`，个人服务器轻量部署。

---

## 1. 产品定位

### 1.1 一句话定位

一个用于沉淀 AI 工具、模型、项目、教程、商业机会，并用知识图谱方式展示它们关系的个人 AI 作战地图。

### 1.2 核心价值

- 统一沉淀 AI 工具、项目、模型、框架、教程、人物、公司和应用场景。
- 用图谱方式展示它们之间的关系，例如依赖、替代、集成、适用场景和学习路径。
- 最终形成个人 AI 工具雷达、学习路线图和项目机会库。

### 1.3 v0.1 目标

先做成一个可手动维护的结构化知识库，支持录入节点、建立关系、查看图谱和维护路线图。

---

## 2. 核心使用场景

### 2.1 记录 AI 工具

示例工具：

- Hermes Agent
- Dify
- n8n
- Cursor
- Claude Code
- LangChain

每个工具可记录：

- 简介
- 官网 / GitHub
- 标签
- 适合场景
- 学习状态
- 商业价值
- 重要程度
- 我的笔记

### 2.2 建立工具关系

示例关系：

- Hermes Agent `uses` Python
- Dify `solves` 知识库问答
- Dify `solves` AI 漫剧制作
- n8n `integrates_with` 飞书
- LangChain `depends_on` Agent / RAG 框架
- Dify `alternative_to` Flowise

Hagsyn Graph 不是简单收藏夹，而是逐步形成个人技术判断系统。

### 2.3 规划学习路线

示例路线：**AI Agent 商业化路线**

1. LLM API
2. Prompt Engineering
3. RAG
4. Function Calling
5. Dify
6. n8n
7. Hermes Agent
8. 企业知识库问答
9. 自动日报周报
10. 服务打包与报价

每个步骤可以绑定已有节点，并标记状态：待学习、学习中、已使用、已掌握。

### 2.4 整理项目机会

示例项目：

- AI 漫剧
- 猪油炒饭记账系统
- 企业知识库助手
- 小红书内容助手
- 自动日报周报助手

每个项目可以关联工具、场景、技能、商业化程度和下一步行动。

---

## 3. v0.1 功能范围

### 3.1 节点管理

支持新增、编辑、删除、查看节点。

**节点类型**

| 类型 | 说明 | 示例 |
|---|---|---|
| `tool` | 工具 | Dify、Hermes Agent |
| `model` | 模型 | GPT、Claude、Qwen、Flux |
| `framework` | 框架 | RAG、Agent、MCP、Workflow |
| `use_case` | 场景 | 知识库问答、AI 漫剧、办公自动化 |
| `project` | 项目 | AI 漫剧、记账系统、知识库助手 |
| `resource` | 资源 | 文档、教程、GitHub、论文 |
| `skill` | 能力 | Prompt、部署、评测、图像生成 |
| `roadmap` | 路线 | AI Agent 入门路线、商业化路线 |

**节点字段**

```ts
{
  id: string
  title: string
  type: "tool" | "model" | "framework" | "use_case" | "project" | "resource" | "skill" | "roadmap"
  description: string
  tags: string[]
  url?: string
  status: "todo" | "learning" | "used" | "mastered"
  importance: 1 | 2 | 3 | 4 | 5
  businessValue: 1 | 2 | 3 | 4 | 5
  note?: string
  createdAt: string
  updatedAt: string
}
```

### 3.2 关系管理

支持新增、删除关系。

| 关系类型 | 含义 |
|---|---|
| `uses` | 项目使用某个工具 |
| `depends_on` | 工具依赖模型、框架或能力 |
| `alternative_to` | 两个工具互为替代 |
| `belongs_to` | 资源属于某个主题 |
| `solves` | 工具解决某个场景 |
| `requires_skill` | 使用工具需要某种能力 |
| `next_step` | 学习路线下一步 |
| `inspired_by` | 项目灵感来源 |
| `integrates_with` | 工具之间可以集成 |
| `recommended_for` | 推荐用于某类场景或用户 |

**关系字段**

```ts
{
  id: string
  sourceId: string
  targetId: string
  relation: string
  note?: string
  createdAt: string
  updatedAt: string
}
```

### 3.3 图谱可视化

第一版使用 `React Flow`。

功能：

- 显示节点和关系线
- 节点可拖拽
- 支持缩放
- 点击节点查看详情
- 按类型、标签、学习状态筛选

v0.1 不做复杂自动布局，先保证能看、能点、能筛选。

### 3.4 节点列表

提供表格视图和卡片视图。

支持：

- 关键词搜索
- 类型筛选
- 标签筛选
- 状态筛选
- 商业价值排序
- 重要度排序

### 3.5 路线图管理

支持创建路线图、添加步骤、调整顺序、标记学习状态，并将步骤关联到已有节点。

**路线字段**

```ts
{
  id: string
  title: string
  description: string
  targetUser: string
  goal: string
  createdAt: string
  updatedAt: string
}
```

**路线步骤字段**

```ts
{
  id: string
  roadmapId: string
  nodeId?: string
  title: string
  description?: string
  order: number
  status: "todo" | "learning" | "done"
}
```

---

## 4. 页面设计

### 4.1 页面导航

v0.1 先做 5 个页面：

| 页面 | 作用 |
|---|---|
| Dashboard | 总览当前知识库状态 |
| Tools | 工具目录，专门管理 AI 工具 |
| Nodes | 管理所有知识节点 |
| Graph | 可视化查看节点关系 |
| Roadmaps | 管理学习路线和项目路线 |

后续可扩展：Projects、Resources、Tags、Insights。

### 4.2 Dashboard 首页

展示模块：

- 节点总数
- 工具数量
- 项目数量
- 资源数量
- 路线数量
- 最近新增 5 个节点
- 当前重点方向
- 高商业价值工具
- 待研究工具

### 4.3 Tools 工具目录页

Tools 是 v0.1 的高频入口，专门展示和管理 `tool` 类型节点。

页面布局：

- 顶部：搜索框 + 新增工具按钮
- 左侧：标签、状态、商业价值、重要度筛选
- 中间：工具卡片 / 工具表格
- 右侧或弹窗：工具详情

工具字段：名称、简介、官网 / GitHub、标签、适合场景、学习状态、重要度、商业价值、我的笔记。

### 4.4 Nodes 节点页

Nodes 是全量知识节点管理页，包含工具、模型、框架、场景、项目、资源、能力和路线。

页面布局：

- 顶部：搜索框 + 新增节点按钮
- 左侧：筛选条件
- 中间：表格 / 卡片列表
- 右侧或弹窗：节点详情

新增节点表单：名称、类型、简介、链接、标签、状态、重要度、商业价值、笔记。

### 4.5 Graph 图谱页

页面布局：

- 左侧：筛选栏
- 中间：图谱画布
- 右侧：节点详情

图谱规则：

- 不同类型节点使用不同颜色
- 节点大小根据 `importance`
- 边显示关系类型
- 支持拖拽、缩放、聚焦

### 4.6 Roadmaps 路线图页

页面布局：

- 左侧：路线列表
- 中间：路线阶段 / 步骤
- 右侧：步骤详情

功能：创建路线、添加步骤、调整顺序、标记状态、绑定节点。

---

## 5. 技术方案

### 5.1 前端

- `Next.js`
- `React`
- `TypeScript`
- `Tailwind CSS`
- `shadcn/ui`
- `React Flow`

### 5.2 后端

- `Python`
- `FastAPI`
- `SQLAlchemy 2.0`
- `Pydantic`
- `Alembic`

### 5.3 数据库

- `MariaDB` 或 `MySQL`

v0.1 表：

- `nodes`
- `edges`
- `tags`
- `node_tags`
- `roadmaps`
- `roadmap_steps`

个人自用不需要上 Neo4j，关系图谱先用普通关系型数据库即可。

### 5.4 部署

服务器：`2核2G` 可跑个人版。

```txt
Nginx
├── Next.js 前端
├── FastAPI 后端
└── MariaDB/MySQL
```

运行方式：

- 前端：`PM2`
- 后端：`systemd` 或 `PM2`
- 数据库：系统服务
- 反代：`Nginx`
- 内存：开启 `2G swap`

---

## 6. API 草案

### 6.1 Nodes

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/nodes` | 创建节点 |
| `GET` | `/api/nodes` | 获取节点列表 |
| `GET` | `/api/nodes/{id}` | 获取节点详情 |
| `PUT` | `/api/nodes/{id}` | 更新节点 |
| `DELETE` | `/api/nodes/{id}` | 删除节点 |

创建节点示例：

```json
{
  "title": "Hermes Agent",
  "type": "tool",
  "description": "一个支持多平台网关、工具调用和技能系统的 AI Agent 框架",
  "tags": ["agent", "automation", "tool-use"],
  "url": "https://github.com/NousResearch/hermes-agent",
  "status": "used",
  "importance": 5,
  "businessValue": 4,
  "note": "可以作为个人小马哥助手底座"
}
```

列表查询参数：

```txt
keyword
type
status
tag
minImportance
minBusinessValue
```

### 6.2 Edges

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/edges` | 创建关系 |
| `GET` | `/api/edges` | 获取关系列表 |
| `DELETE` | `/api/edges/{id}` | 删除关系 |

创建关系示例：

```json
{
  "sourceId": "project-ai-drama",
  "targetId": "comfyui",
  "relation": "uses",
  "note": "AI 漫剧项目使用 Dify 做图片生成"
}
```

### 6.3 Roadmaps

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/roadmaps` | 创建路线 |
| `GET` | `/api/roadmaps` | 获取路线列表 |
| `GET` | `/api/roadmaps/{id}` | 获取路线详情 |
| `POST` | `/api/roadmaps/{id}/steps` | 新增路线步骤 |
| `PUT` | `/api/roadmaps/{id}/steps/reorder` | 调整步骤顺序 |

创建路线示例：

```json
{
  "title": "AI Agent 商业化路线",
  "description": "从基础 API 到自动化项目交付的学习路线",
  "targetUser": "独立开发者",
  "goal": "能够交付企业知识库问答和自动化助手"
}
```

新增路线步骤示例：

```json
{
  "title": "学习 Function Calling",
  "description": "理解工具调用、参数结构和执行流程",
  "nodeId": "function-calling",
  "status": "todo"
}
```

---

## 7. 数据表设计

### 7.1 `nodes`

```sql
CREATE TABLE nodes (
  id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,
  description TEXT,
  url TEXT,
  status VARCHAR(50) NOT NULL DEFAULT 'todo',
  importance TINYINT NOT NULL DEFAULT 3,
  business_value TINYINT NOT NULL DEFAULT 3,
  note TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### 7.2 `edges`

```sql
CREATE TABLE edges (
  id VARCHAR(64) PRIMARY KEY,
  source_id VARCHAR(64) NOT NULL,
  target_id VARCHAR(64) NOT NULL,
  relation VARCHAR(80) NOT NULL,
  note TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  FOREIGN KEY (source_id) REFERENCES nodes(id),
  FOREIGN KEY (target_id) REFERENCES nodes(id)
);
```

### 7.3 `tags`

```sql
CREATE TABLE tags (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  created_at DATETIME NOT NULL
);
```

### 7.4 `node_tags`

```sql
CREATE TABLE node_tags (
  node_id VARCHAR(64) NOT NULL,
  tag_id VARCHAR(64) NOT NULL,
  PRIMARY KEY (node_id, tag_id),
  FOREIGN KEY (node_id) REFERENCES nodes(id),
  FOREIGN KEY (tag_id) REFERENCES tags(id)
);
```

### 7.5 `roadmaps`

```sql
CREATE TABLE roadmaps (
  id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  target_user VARCHAR(255),
  goal TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

### 7.6 `roadmap_steps`

```sql
CREATE TABLE roadmap_steps (
  id VARCHAR(64) PRIMARY KEY,
  roadmap_id VARCHAR(64) NOT NULL,
  node_id VARCHAR(64),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  step_order INT NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'todo',
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id),
  FOREIGN KEY (node_id) REFERENCES nodes(id)
);
```

---

## 8. 视觉风格

### 8.1 整体风格

方向：暗色科技风。

关键词：Linear、Vercel、Raycast、AI 工具雷达、个人作战地图。

### 8.2 色彩建议

| 类型 | 色值 |
|---|---|
| 背景 | `#09090B`、`#111827`、`#18181B` |
| 主文字 | `#F9FAFB` |
| 次级文字 | `#A1A1AA` |
| 弱文字 | `#71717A` |
| 蓝色强调 | `#3B82F6` |
| 紫色强调 | `#8B5CF6` |
| 青色强调 | `#06B6D4` |
| 绿色强调 | `#22C55E` |
| 橙色强调 | `#F97316` |

### 8.3 节点颜色

| 节点类型 | 颜色 |
|---|---|
| `tool` | 蓝色 |
| `model` | 紫色 |
| `framework` | 青色 |
| `use_case` | 绿色 |
| `project` | 橙色 |
| `resource` | 灰色 |
| `skill` | 粉色 |
| `roadmap` | 黄色 |

---

## 9. 开发顺序

### 第 1 阶段：项目骨架

目标：跑通前后端和数据库。

1. 创建 Next.js 项目
2. 创建 FastAPI 项目
3. 配置 MySQL/MariaDB
4. 接入 SQLAlchemy
5. 建立基础数据表
6. 打通前端请求后端 API

### 第 2 阶段：节点管理

目标：可以管理 AI 工具和知识节点。

1. 节点数据模型
2. 节点创建接口
3. 节点列表接口
4. 节点详情接口
5. 节点编辑接口
6. 节点删除接口
7. 前端节点列表页
8. 前端新增 / 编辑表单

### 第 3 阶段：关系管理

目标：可以建立节点之间的关系。

1. 关系数据模型
2. 创建关系接口
3. 删除关系接口
4. 节点详情展示关联关系
5. 前端新增关系表单

### 第 4 阶段：图谱页

目标：可以用图谱查看节点关系。

1. 接入 React Flow
2. 将 nodes 转成图谱节点
3. 将 edges 转成图谱连线
4. 支持点击节点查看详情
5. 支持按类型筛选
6. 支持按标签筛选

### 第 5 阶段：路线图

目标：可以维护学习路线。

1. 路线数据模型
2. 路线 CRUD
3. 路线步骤 CRUD
4. 步骤排序
5. 步骤状态标记
6. 前端路线页

### 第 6 阶段：部署

目标：部署到 2核2G 服务器。

1. 配置服务器环境
2. 安装 Node.js / Python / MariaDB / Nginx
3. 配置 swap
4. 部署前端
5. 部署后端
6. 配置 Nginx 反代
7. 配置进程守护
8. 配置数据库备份

---

## 10. 暂不包含功能

为了避免 v0.1 过重，暂时不做：

- 多用户协作
- 公开分享页
- 权限系统
- 评论系统
- AI 自动抓取 URL
- AI 自动生成路线
- AI 自动推荐关系
- Neo4j 图数据库
- 3D 图谱
- Obsidian / Notion / 飞书同步
- 复杂数据看板

这些功能放到 v0.2 / v0.3。

---

## 11. 后续版本规划

### v0.2：AI 辅助录入

- 粘贴 URL 自动提取标题、摘要、标签
- 粘贴 GitHub 链接自动读取项目介绍
- AI 自动推荐节点类型
- AI 自动生成工具简介
- AI 自动推荐关联节点

### v0.3：知识路线增强

- 自动生成学习路线
- 工具对比页面
- 商业化机会评分
- 项目模板库
- 可导出路线图

### v0.4：分享与协作

- 公开分享图谱
- 公开分享路线图
- 多用户登录
- 协作编辑
- 评论和收藏

---

## 12. 验收标准

v0.1 完成后，应能做到：

1. 可以新增一个工具节点，例如 `Hermes Agent`
2. 可以给它打标签，例如 `agent`、`automation`
3. 可以设置状态，例如 `used`
4. 可以设置商业价值和重要度
5. 可以新增一个项目节点，例如 `AI 漫剧`
6. 可以建立关系：`AI 漫剧 uses Dify`
7. 可以在图谱页面看到这些节点和关系
8. 可以创建一条路线，例如 `AI Agent 商业化路线`
9. 可以往路线里添加步骤
10. 可以标记步骤学习状态

---

## 13. 最小可启动版本

### 13.1 五个页面

1. `Dashboard`
2. `Tools`
3. `Nodes`
4. `Graph`
5. `Roadmaps`

### 13.2 六张表

1. `nodes`
2. `edges`
3. `tags`
4. `node_tags`
5. `roadmaps`
6. `roadmap_steps`

### 13.3 三个核心闭环

1. 录入节点
2. 建立关系
3. 图谱展示

这就是 Hagsyn Graph v0.1 的核心。
