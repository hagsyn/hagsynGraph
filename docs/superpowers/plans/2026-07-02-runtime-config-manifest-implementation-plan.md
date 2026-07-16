# Runtime Config Manifest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 Hagsyn 建立正式的运行时配置清单，让后端从配置读取受环境影响的关键依赖和路径，并区分本地模式与服务器模式。

**Architecture:** 先扩展 `backend/app/config.py`，新增运行模式、服务地址、命令路径、转写配置、目录配置等关键项，再把高风险写死依赖（尤其 `ffmpeg / ffprobe / 转写配置 / 存储目录`）改为从 Settings 读取。最后同步 README / AGENTS / standards 和验证命令。

**Tech Stack:** Pydantic Settings, FastAPI backend, existing tool modules, Markdown docs

---

### Task 1: 扩展配置模型

**Files:**
- Modify: `backend/app/config.py`

- [x] 增加运行模式配置：
  - `app_runtime_mode`
  - `api_host`
  - `api_port`
  - `frontend_origin`
- [x] 增加命令路径配置：
  - `ffmpeg_bin`
  - `ffprobe_bin`
- [x] 增加转写配置：
  - `transcribe_provider`
  - `whisper_model`
  - `whisper_device`
- [x] 保持默认值与当前本地行为一致

### Task 2: 将高风险环境依赖改为从配置读取

**Files:**
- Modify: `backend/app/video_tools.py`
- Modify: `backend/app/subtitle_tools.py`

- [x] 将 `ffmpeg` 调用改成使用 `settings.ffmpeg_bin`
- [x] 如有 `ffprobe` 使用，统一改成 `settings.ffprobe_bin`
- [x] 将字幕转写模型和设备改为使用 Settings
- [x] 确保存储目录继续统一从 Settings 读取

### Task 3: 验证与测试补强

**Files:**
- Modify: `backend/tests/test_api.py`

- [x] 增加配置默认值验证或路径行为验证
- [x] 确保现有视频压缩 / VTT / 字幕烧录测试仍通过
- [x] 如有必要，补一条针对 `settings.ffmpeg_bin` 的回归测试

### Task 4: 文档与入口同步

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/standards/02-backend-standards.md`
- Modify: `docs/testing/reports/2026-07-01-video-compress-and-vtt-tool-report.md`

- [x] 在 README 中补 runtime config 说明
- [x] 在 AGENTS 中补“本地模式 / 服务器模式”与关键配置项入口
- [x] 在 backend standards 中补“高风险环境依赖统一从 Settings 读取”
- [x] 在测试报告中记录这轮配置化改造

### Task 5: 最终验证

**Files:**
- Verify only

- [x] 运行后端相关测试
- [x] 验证 `config.py` 新字段存在且默认值合理
- [x] 验证工具链路仍可用
- [x] 验证文档入口已同步
