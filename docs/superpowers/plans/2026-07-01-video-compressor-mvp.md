# Video Compressor MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前 Hagsyn Graph 前后端收敛为一个本地单机版视频压缩工具 MVP，清理 demo 数据入口，支持上传常见视频格式、选择压缩模式、压缩完成后展示结果卡片并下载。

**Architecture:** 后端新增同步视频压缩接口和文件下载接口，使用本机 `ffmpeg` 完成压缩，并将文件暂存到本地目录。前端改为单页工具界面，围绕上传、模式选择、结果展示组织交互，不再使用知识图谱 seed/demo 主流程。

**Tech Stack:** FastAPI, SQLAlchemy (保留现有依赖但本功能不依赖数据库), 原生 HTML/CSS/JavaScript, ffmpeg, pytest

---

### Task 1: 后端视频压缩能力

**Files:**
- Create: `backend/app/video_tools.py`
- Modify: `backend/app/config.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_api.py`

- [ ] 新增失败测试，覆盖非法格式拒绝、成功压缩返回下载信息。
- [ ] 运行指定测试，确认当前失败。
- [ ] 实现上传校验、三种压缩模式映射、结果文件输出、下载接口。
- [ ] 重新运行后端测试，确认通过。

### Task 2: 前端改为视频压缩工具界面

**Files:**
- Modify: `frontend/index.html`
- Test: `frontend/tests/ui-shell.test.js`

- [ ] 新增失败测试，要求页面存在上传区、模式选择区、结果卡片容器，且不再包含 seed/demo 入口。
- [ ] 运行前端壳测试，确认失败。
- [ ] 重构页面为单工具界面，接入后端压缩与下载流程，移除 demo 数据按钮和图谱主流程。
- [ ] 运行前端壳测试和 `node --check`，确认通过。

### Task 3: 文档和启动说明更新

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] 更新项目定位、启动说明和验证命令，补充 `ffmpeg` 依赖说明与压缩接口主流程。
- [ ] 自查文案，确保不再把项目描述成 demo 图谱工作台。
