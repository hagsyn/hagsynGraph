# VTT Subtitle Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `Tools` 模块中新增一个本地 VTT 字幕生成工具，支持上传视频、抽取音频、转写为字幕并下载 `.vtt` 文件。

**Architecture:** 后端新增 `vtt-subtitle` 工具路由与本地转写模块，前端在 `Tools` 中增加第二个工具卡和工作区，继续复用现有工作台壳与结果卡片模式。测试先行，至少覆盖路由存在、格式校验、成功返回字幕下载信息、依赖缺失错误、VTT 基本格式。

**Tech Stack:** FastAPI, Python, ffmpeg, 本地转写依赖, 单文件 HTML/CSS/JavaScript, pytest

---

### Task 1: 后端 VTT 工具测试先行

**Files:**
- Modify: `backend/tests/test_api.py`

- [ ] 增加 VTT 路由注册失败测试
- [ ] 增加不支持格式失败测试
- [ ] 增加成功返回下载元信息测试
- [ ] 增加依赖缺失错误测试
- [ ] 增加 `.vtt` 基本内容格式测试

### Task 2: 后端 VTT 工具实现

**Files:**
- Create: `backend/app/subtitle_tools.py`
- Modify: `backend/app/main.py`
- Modify: `backend/app/config.py`
- Modify: `backend/requirements.txt`

- [ ] 新增本地字幕工具模块
- [ ] 新增 `/api/tools/vtt-subtitle`
- [ ] 新增 `/api/tools/vtt-subtitle/files/{file_id}`
- [ ] 支持视频抽音频、转写、生成 `.vtt`
- [ ] 明确依赖缺失与失败边界

### Task 3: 前端 Tools 接入

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/tests/ui-shell.test.js`

- [ ] 为 `Tools` 增加“VTT 字幕生成”工具卡
- [ ] 增加对应工作区
- [ ] 增加语言选择、结果卡片、下载按钮
- [ ] 对接新后端接口
- [ ] 保持三栏工作台壳与右侧详情栏一致

### Task 4: 验证

**Files:**
- Verify only

- [ ] 运行后端相关测试
- [ ] 运行前端壳测试
- [ ] 运行 `node --check`
- [ ] 启动后端并验证真实路由
