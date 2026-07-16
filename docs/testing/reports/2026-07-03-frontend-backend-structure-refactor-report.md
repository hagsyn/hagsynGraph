# 2026-07-03 Frontend / Backend Structure Refactor Report

## 改动目标

本轮主要完成 Hagsyn-Graph 的前后端工程结构重组：

- 后端从单入口堆叠改为 `core / routers / services / repositories / models / schemas`
- 前端从单文件页面改为 `index.html + assets/css + assets/js` 的无构建多文件结构
- 保持视频压缩、VTT 字幕生成、字幕烧录与 admin storage policy 接口兼容

## 自动验证

### Backend

命令：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest -q
```

结果：

- `39 passed`

覆盖重点：

- 结构分层测试
- tools 路由与下载元信息
- tool_runs 成功 / 失败记录
- admin storage policy 读取、保存、清理

### Frontend

命令：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
node frontend/tests/ui-shell.test.js
find frontend/assets/js -type f | sort | xargs -I{} node --check {}
```

结果：

- `ui shell test passed`
- 全部前端模块 `node --check` 通过

覆盖重点：

- `index.html` 是否正确引用 CSS / JS 模块入口
- `assets/js/**` 结构是否齐全
- 多文件模块语法是否通过

## 运行验证

### Local URLs

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173/?v=video-compressor-v1`

### 接口检查

命令：

```bash
curl -sS http://127.0.0.1:8000/api/health
```

结果：

```json
{"ok":true,"name":"Hagsyn Graph"}
```

### 浏览器交互检查

已在本地浏览器中完成以下验证：

1. 页面可正常打开并进入 `#dashboard`
2. 左侧导航可切到 `Tools`
3. `Tools` 页可见 3 个真实工具卡片
4. 点击首个“使用”后，URL 进入 `#tools/video-compress`
5. 视频压缩工作区可见文件选择、模式选择、结果卡片和最近使用记录区域

## 结论

本轮结构重组已完成基本收口：

- 新工程结构已落地
- 现有接口兼容未回归
- 前端静态入口与模块资源可加载
- 真实工具工作区仍保留在统一壳层内

## 剩余限制

- 本轮主要是结构优化，没有新增产品能力
- 视频压缩 / 字幕工具的真实文件上传执行本轮未重复做全链路长耗时手测，当前以现有 API 回归、浏览器壳层验证和下载路径兼容为主
