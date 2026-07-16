# 2026-07-01 视频压缩与 VTT 工具测试报告

## 范围

本轮覆盖两个真实工具能力：

1. 视频压缩
2. VTT 字幕生成

## 问题与修复

### 1. 视频压缩路由 404

- 表现：前端点击压缩后返回 `{"detail":"Not Found"}`
- 根因：本机运行中的后端进程未加载到最新路由版本
- 修复：重启后端到最新代码版本，并补充路由注册回归测试

### 2. 视频压缩结果语义失真

- 表现：压缩后文件更大时，页面仍显示 `节省体积 0 B / 压缩比例 0%`
- 根因：后端把 `savedBytes` 强行钳成非负值，前端未区分结果状态
- 修复：
  - 后端返回真实正负变化值
  - 新增 `outcome`
  - 前端按 `smaller / larger / same` 显示不同结果文案

### 3. VTT 工具接入

- 表现：新增第二个真实工具，并完成本地转写依赖安装
- 修复：
  - 接入 `/api/tools/vtt-subtitle`
  - 接入下载路由
  - 前端增加 `VTT 字幕生成` 工具卡与工作区

### 4. VTT 页面内容错位与交互反馈问题

- 表现：
  - 页面渲染时存在模板字符串中的反引号错误
  - 上传区点击后缺少明确反馈，容易让用户误以为“没反应”
- 修复：
  - 清除 VTT 工作区中的反引号模板错误
  - 增加真实网页点击验证
  - 增加上传区状态提示、未选文件前禁用提交按钮、处理中进度反馈

### 5. VTT 输出质量首轮优化

- 表现：
  - 字幕虽然是合法 VTT，但初版整段文本切分较粗
- 修复：
  - 增加 `render_vtt_lines`
  - 增加文本清洗与按标点/长度切分
  - 补充 VTT 结构和长文本拆分测试

### 6. 管理员存储策略设置面板闭环

- 表现：
  - 后端存储策略接口已完成，但前端最初仍以 `localStorage` 骨架模拟为主
  - 用户点击设置时若后端不可用，会体感成“没有反应”
- 修复：
  - 前端改为真实调用管理员接口：
    - `GET /api/admin/storage-policy`
    - `PUT /api/admin/storage-policy`
    - `POST /api/admin/storage-policy/run-cleanup`
  - 设置面板改为先打开，再异步加载后端策略
  - 后端不可用时，在面板内显示明确错误状态而不是静默失败
  - 通过真实网页点击验证确认管理员设置面板可正常打开并加载后端值

### 7. 视频字幕烧录工具接入

- 表现：
  - 新增第三个真实工具，用于上传视频、自动生成字幕并烧录进视频
- 修复 / 新增：
  - 新增后端接口：
    - `POST /api/tools/video-subtitle-burn`
    - `GET /api/tools/video-subtitle-burn/files/{file_id}`
  - 前端 `Tools` 中新增“视频字幕烧录”工具卡与工作区
  - 通过真实网页点击验证，确认第三张工具卡可见、可进入、无控制台错误

### 8. Runtime config manifest 接入

- 表现：
  - 后端原先直接调用系统默认 `ffmpeg`
  - 字幕转写模型和设备写死为 `base` / `cpu`
  - 本地模式和服务器模式没有正式配置入口
- 修复 / 新增：
  - 在 `backend/app/config.py` 中新增运行模式、服务地址、命令路径和转写配置
  - 视频压缩改为读取 `settings.ffmpeg_bin`
  - VTT 生成和字幕烧录改为读取 `settings.ffmpeg_bin`
  - Whisper 模型和设备改为读取 `settings.whisper_model` / `settings.whisper_device`
  - README、AGENTS 和后端标准同步运行时配置约束

## 新增/更新的自动测试

### 后端

- 视频压缩路由注册测试
- 视频压缩结果变大时的回归测试
- VTT 路由注册测试
- VTT 格式拒绝测试
- VTT 成功返回元信息测试
- VTT 依赖缺失错误测试
- VTT 基本格式输出测试
- VTT 长文本拆分测试
- 视频字幕烧录路由注册测试
- 视频字幕烧录格式拒绝测试
- 视频字幕烧录成功返回元信息测试
- 视频字幕烧录依赖缺失错误测试
- Runtime config 默认值测试
- 视频压缩使用 `settings.ffmpeg_bin` 的回归测试
- VTT 字幕生成使用 `settings.ffmpeg_bin`、`settings.whisper_model` 和 `settings.whisper_device` 的回归测试

### 前端

- 第二个工具卡存在性测试
- 语言选择器存在性测试
- 防止 Tools 页面始终默认渲染视频压缩工作区的结构测试

## 执行结果

### 后端

运行：

```bash
./.venv/bin/pytest -q tests/test_api.py -k 'video_compress or vtt_subtitle or routes_are_registered'
```

结果：

- `8 passed`

本轮 runtime config 追加验证：

```bash
./.venv/bin/pytest -q
```

结果：

- `30 passed`

### 前端

运行：

```bash
node /Users/hagsyn/ai/workspace/Hagsyn-Graph/frontend/tests/ui-shell.test.js
node --check /tmp/hagsyn-frontend-script.js
```

结果：

- 前端壳测试通过
- 内嵌脚本语法检查通过

### 网页点击验证

补充验证：

- 真实点击 `Tools -> VTT 字幕生成 -> 使用`
- 初次验证抓到模板字符串中的 `.vtt` 反引号问题，浏览器 pageerror 复现
- 修复后再次做网页点击验证，页面成功进入工作区，控制台与 pageerror 清空
- 后续补了前端处理中状态反馈：按钮 loading + 伪进度条 + 完成态切换
- 继续补了上传区交互反馈：未选文件前禁用提交按钮、选中文件状态显示、系统文件选择器提示文案
- 管理员设置面板真实点击验证通过，面板可打开并从后端加载当前策略值
- 视频字幕烧录工具真实点击验证通过，第三张工具卡可见并可进入工作区

## 当前状态

- 视频压缩已修复 404 和结果语义问题
- VTT 字幕工具已接入并完成最小本地转写闭环
- 视频字幕烧录工具已接入并完成最小烧录闭环
- `.agents/skills` 下已建立测试治理 skill、产品治理 skill 和 workflow harness

## 2026-07-02 ffmpeg-full 切换后验证

### 配置读取验证

运行：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
python - <<'PY'
from app.config import settings
print(f'APP_RUNTIME_MODE={settings.app_runtime_mode}')
print(f'FFMPEG_BIN={settings.ffmpeg_bin}')
print(f'FFPROBE_BIN={settings.ffprobe_bin}')
PY
```

结果：

- `APP_RUNTIME_MODE=local`
- `FFMPEG_BIN=/opt/homebrew/Cellar/ffmpeg-full/8.1.1/bin/ffmpeg`
- `FFPROBE_BIN=/opt/homebrew/Cellar/ffmpeg-full/8.1.1/bin/ffprobe`

### 二进制能力验证

运行：

```bash
/opt/homebrew/Cellar/ffmpeg-full/8.1.1/bin/ffmpeg -hide_banner -filters | rg 'subtitles| ass '
```

结果：

- 存在 `ass` filter
- 存在 `subtitles` filter
- 说明当前 Hagsyn 指向的 `ffmpeg-full` 具备字幕烧录所需的 `libass` 能力

### 后端回归验证

运行：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q
```

结果：

- `30 passed`

### 真实字幕滤镜验证

运行方式：

- 使用当前 `settings.ffmpeg_bin` 生成一个 2 秒样例 `mp4`
- 生成一个本地 `caption.srt`
- 使用 `-vf subtitles=filename=...` 烧录字幕

结果：

- `ffmpeg_bin=/opt/homebrew/Cellar/ffmpeg-full/8.1.1/bin/ffmpeg`
- `returncode=0`
- `output_exists=True`
- `output_size=5797`

结论：

- Hagsyn 后端已读取 `backend/.env` 中配置的 `ffmpeg-full`
- 当前 `ffmpeg-full` 支持 `subtitles/libass`
- 自动回归和真实字幕滤镜处理均通过
- 这次切换只作用于 Hagsyn 后端配置，不改变系统全局 `PATH`

## 2026-07-02 视频字幕烧录进度反馈修复

### 问题表现

- 用户在页面点击“视频字幕烧录”后，按钮进入 `烧录中...`
- 结果卡片右上角显示 `正在烧录`
- 但结果卡片区域没有明确进度条或阶段提示，长任务执行时容易误以为页面无反馈

### 根因

- `VTT 字幕生成` 工作区已有 `subtitleProgressShell`、`subtitleProgressText`、`subtitleProgressFill`
- `视频字幕烧录` 工作区缺少对应的 `burnProgressShell`、`burnProgressText`、`burnProgressFill`
- 烧录提交流程只更新按钮文案和状态文字，没有启动阶段式进度反馈
- 另外完成后 `setBurnSubmitting(false)` 会把状态覆盖回 `等待上传`，需要保持完成态

### 修复

- 在 `frontend/index.html` 的烧录结果卡片中加入阶段式进度条
- 新增 `setBurnProgress`、`startBurnPseudoProgress`、`finishBurnPseudoProgress`
- 烧录提交时显示阶段文案：
  - 正在上传视频
  - 正在生成字幕
  - 正在烧录字幕到视频
  - 正在整理下载结果
- 完成后保持 `烧录完成`，不再被提交状态复位覆盖

### 回归测试与验证

运行：

```bash
node frontend/tests/ui-shell.test.js
```

结果：

- `ui shell test passed`

运行：

```bash
python3 - <<'PY'
from pathlib import Path
s = Path('frontend/index.html').read_text()
Path('/tmp/hagsyn-frontend-script.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/hagsyn-frontend-script.js
```

结果：

- 内嵌脚本语法检查通过

运行：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q
```

结果：

- `30 passed`

浏览器交互验证：

- 使用独立 Chrome 打开 `#tools/video-subtitle-burn`
- 上传本地样例视频
- 拦截 `/api/tools/video-subtitle-burn` 并延迟返回，稳定观察执行中状态

结果：

- 执行中：
  - `status=正在烧录`
  - `text=正在上传视频并准备字幕烧录...`
  - `width=6%`
  - `visible=true`
  - `button=烧录中...`
- 完成后：
  - `status=烧录完成`
  - `text=字幕烧录完成`
  - `width=100%`
  - `segmentCount=2`
  - `downloadPath=/api/tools/video-subtitle-burn/files/progress-demo`
- 控制台错误：无

## 2026-07-02 Tools 工作区收回修复

### 问题表现

- 用户点击 `使用` 后，工具工作区在工具目录下方展开
- 展开后页面没有明确的收回/关闭入口
- 用户只能通过切换路由或重新点击导航离开，当前工作区无法在 Tools 页内收起

### 根因

- Tools 工作区打开状态由 URL hash 表示，例如 `#tools/vtt-subtitle`
- `openTool(toolId)` 只负责进入 `#tools/<toolId>`
- 前端缺少对应的 `closeToolWorkspace()` 将 hash 恢复为 `#tools`
- 工作区共享外壳也缺少收回按钮

### 修复

- 新增 `closeToolWorkspace()`，调用 `show('tools')`
- 暴露 `window.closeToolWorkspace`
- 在 `#toolWorkspace` 共享外壳上方增加 `收回工作区` 按钮
- 收回后 hash 回到 `#tools`，工作区隐藏，并恢复工具目录空状态提示

### 回归测试与验证

运行：

```bash
node frontend/tests/ui-shell.test.js
```

结果：

- `ui shell test passed`

运行：

```bash
python3 - <<'PY'
from pathlib import Path
s = Path('frontend/index.html').read_text()
Path('/tmp/hagsyn-frontend-script.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/hagsyn-frontend-script.js
```

结果：

- 内嵌脚本语法检查通过

运行：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q
```

结果：

- `30 passed`

浏览器交互验证：

- 打开 `#tools/vtt-subtitle`
- 确认 `收回工作区` 按钮可见
- 点击后 hash 变为 `#tools`
- `#toolWorkspace` 进入 hidden 状态
- 再次点击 `视频字幕烧录` 的 `使用` 后，hash 变为 `#tools/video-subtitle-burn`，收回按钮仍可见

结果：

- 打开前：`hash=#tools/vtt-subtitle`
- 收回后：`hash=#tools`
- 收回后关闭按钮不存在，工作区隐藏
- 再打开：`hash=#tools/video-subtitle-burn`
- 控制台未发现可复现功能错误

## 2026-07-02 工具使用记录留痕

### 问题表现

- 当前只有文件产物层面的留痕，例如上传文件、压缩结果、字幕结果
- 没有业务级工具运行历史
- 无法从产品层回答：
  - 谁在什么时候运行了哪个工具
  - 输入文件是什么
  - 执行是否成功
  - 输出下载地址是什么
  - 失败原因是什么

### 修复

- 新增 `ToolRun` 模型，对应 `tool_runs` 表
- 新增 `backend/app/tool_runs.py` 服务模块
- 新增 `GET /api/tools/runs`
- 三个工具接入运行记录：
  - `video-compress`
  - `vtt-subtitle`
  - `video-subtitle-burn`
- 成功运行记录 `success`
- 失败运行记录 `failed`
- Tools 页面新增 `最近使用记录` 区块
- 数据建模标准补充 `ToolRun` 建模边界

### 回归测试与验证

运行：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q tests/test_api.py -k 'tool_runs or video_compress or vtt_subtitle or video_subtitle_burn'
```

结果：

- `21 passed`

完整后端回归：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q
```

结果：

- `35 passed`

运行：

```bash
node frontend/tests/ui-shell.test.js
```

结果：

- `ui shell test passed`

运行：

```bash
python3 - <<'PY'
from pathlib import Path
s = Path('frontend/index.html').read_text()
Path('/tmp/hagsyn-frontend-script.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/hagsyn-frontend-script.js
```

结果：

- 内嵌脚本语法检查通过

### 当前边界

- 本轮只做最近记录展示，不做复杂筛选统计
- 历史记录和文件清理策略分离：文件可被清理，历史记录仍保留
- 如果历史记录里的下载文件已被清理，下载接口继续返回 `404`

### 浏览器验证

- 重启本地后端后，`GET /api/tools/runs?limit=3` 返回 `200`
- 打开 `http://127.0.0.1:5173/?v=tool-run-history-20260702b#tools`
- Tools 页显示 `最近使用记录`
- 当前可见一条 `视频字幕烧录 · failed` 记录
- 工具目录仍可见，工作区默认隐藏

## 2026-07-02 工具使用记录清理机制

### 问题表现

- `ToolRun` 已经入库并在 Tools 页展示
- 但当前清理策略只处理文件，不处理历史记录
- 如果长期使用，`tool_runs` 会无限增长

### 修复

- 在 `StoragePolicy` 中新增：
  - `toolRunRetentionHours`
- 默认值：
  - `720` 小时（30 天）
- 手动清理和自动清理共用同一条记录清理逻辑
- `CleanupResult` 新增：
  - `toolRunsDeleted`
- 管理员设置面板新增：
  - `工具使用记录保留时长（小时）`

### 回归测试与验证

运行：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q tests/test_api.py -k 'storage_policy or cleanup_tool_runs'
```

结果：

- `6 passed`

运行：

```bash
node frontend/tests/ui-shell.test.js
```

结果：

- `ui shell test passed`

运行：

```bash
python3 - <<'PY'
from pathlib import Path
s = Path('frontend/index.html').read_text()
Path('/tmp/hagsyn-frontend-script.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/hagsyn-frontend-script.js
```

结果：

- 内嵌脚本语法检查通过

### 当前边界

- 本轮只支持按保留时长删除过期记录
- 不做按工具类型、状态、用户的定向删除
- 不做单独的历史记录清理入口，统一挂在现有存储与清理策略内
