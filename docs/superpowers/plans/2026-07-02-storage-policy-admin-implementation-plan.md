# Storage Policy Admin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 Hagsyn 增加管理员可见的存储与清理策略能力，支持页面内配置、手动触发清理、以及工具链路中的即时清理。

**Architecture:** 先在后端增加本地策略文件读写与管理员接口，再把即时清理接进视频压缩和字幕生成链路。前端通过右上角设置入口展示管理员专属策略面板。测试覆盖接口、权限、清理行为和前端结构，最后补测试报告。

**Tech Stack:** FastAPI, Python, JSON config file, 单文件 HTML/CSS/JavaScript, pytest

---

### Task 1: 后端策略测试先行

**Files:**
- Modify: `backend/tests/test_api.py`

- [ ] 增加 `GET /api/admin/storage-policy` 管理员访问测试
- [ ] 增加非管理员访问拒绝测试
- [ ] 增加 `PUT /api/admin/storage-policy` 更新测试
- [ ] 增加 `POST /api/admin/storage-policy/run-cleanup` 返回清理统计测试
- [ ] 增加字幕中间 `.wav` 立即删除测试

### Task 2: 后端策略实现

**Files:**
- Create: `backend/app/storage_policy.py`
- Modify: `backend/app/config.py`
- Modify: `backend/app/main.py`
- Modify: `backend/app/video_tools.py`
- Modify: `backend/app/subtitle_tools.py`

- [ ] 实现本地策略文件读写
- [ ] 实现管理员判断（默认 `hagsyn` 为管理员）
- [ ] 新增管理员接口：
  - `GET /api/admin/storage-policy`
  - `PUT /api/admin/storage-policy`
  - `POST /api/admin/storage-policy/run-cleanup`
- [ ] 在字幕链路接入 `.wav` 立即删除
- [ ] 在失败链路接入临时文件清理

### Task 3: 前端设置入口与策略面板

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/tests/ui-shell.test.js`

- [ ] 在右上角用户菜单中接入“设置”
- [ ] 为管理员显示 `存储与清理策略` 面板
- [ ] 支持加载当前策略
- [ ] 支持保存策略
- [ ] 支持“立即清理”
- [ ] 普通用户隐藏该配置入口

### Task 4: 测试报告与规范同步

**Files:**
- Modify: `docs/testing/reports/2026-07-01-video-compress-and-vtt-tool-report.md`
- Modify: `README.md`
- Modify: `AGENTS.md`

- [ ] 补本轮清理策略与管理员设置测试结果
- [ ] 如有必要，在 README/AGENTS 补一句策略入口与管理员边界

### Task 5: 最终验证

**Files:**
- Verify only

- [ ] 运行后端相关测试
- [ ] 运行前端壳测试
- [ ] 运行 `node --check`
- [ ] 验证管理员接口可用
- [ ] 验证前端管理员设置面板结构存在
