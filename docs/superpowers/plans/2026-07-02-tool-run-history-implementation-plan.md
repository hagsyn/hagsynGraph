# Tool Run History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 为 Hagsyn 的三个真实工具增加业务级使用记录留痕，并在 Tools 页展示最近使用记录。

**Architecture:** 新增 `ToolRun` ORM 模型和 `tool_runs.py` 服务模块，由工具路由在执行开始、成功、失败时写入状态。新增 `GET /api/tools/runs` 返回最近运行记录，前端 Tools 页读取并展示轻量历史区块，不改变现有工具执行 API 的核心返回结构。

**Tech Stack:** FastAPI, SQLAlchemy, SQLite, Pydantic, single-file HTML/CSS/JavaScript frontend

---

### Task 1: 后端模型与 schema

**Files:**
- Modify: `backend/app/models.py`
- Modify: `backend/app/schemas.py`
- Test: `backend/tests/test_api.py`

- [x] 在 `backend/tests/test_api.py` 写失败测试：`GET /api/tools/runs` 路由存在并需要鉴权

```python
def test_tool_runs_route_requires_auth():
    response = client.get("/api/tools/runs")
    assert response.status_code == 401


def test_tool_runs_route_is_registered():
    routes = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", []) or [])))
        for route in app.routes
    }
    assert ("/api/tools/runs", ("GET",)) in routes
```

- [x] 运行失败测试

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q tests/test_api.py -k 'tool_runs_route'
```

预期：路由注册测试失败。

- [x] 在 `backend/app/models.py` 新增 `ToolRun`

```python
class ToolRun(Base):
    __tablename__ = "tool_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("run"))
    tool_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="running", nullable=False, index=True)
    input_file_name: Mapped[Optional[str]] = mapped_column(String(255))
    input_file_size: Mapped[Optional[int]] = mapped_column(Integer)
    output_file_name: Mapped[Optional[str]] = mapped_column(String(255))
    download_url: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text)
```

- [x] 在 `backend/app/schemas.py` 新增输出 schema

```python
class ToolRunOut(BaseModel):
    id: str
    toolType: str
    username: str
    status: str
    inputFileName: Optional[str]
    inputFileSize: Optional[int]
    outputFileName: Optional[str]
    downloadUrl: Optional[str]
    startedAt: datetime
    completedAt: Optional[datetime]
    durationMs: Optional[int]
    errorMessage: Optional[str]
    metadata: dict = {}
```

- [x] 在 `backend/app/main.py` 先添加空查询路由让路由测试通过

```python
@app.get("/api/tools/runs", response_model=list[ToolRunOut])
def list_tool_runs(_: str = Depends(require_auth)):
    return []
```

- [x] 运行路由测试确认通过

```bash
pytest -q tests/test_api.py -k 'tool_runs_route'
```

预期：`2 passed`。

### Task 2: 工具运行记录服务模块

**Files:**
- Create: `backend/app/tool_runs.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_api.py`

- [x] 在 `backend/tests/test_api.py` 写服务级失败测试：手动创建运行记录后 API 返回 camelCase 结构

```python
def test_tool_runs_api_returns_recent_records(tmp_path: Path):
    response = client.get("/api/tools/runs", headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

- [x] 创建 `backend/app/tool_runs.py`

```python
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ToolRun
from .schemas import ToolRunOut


def _metadata_dump(metadata: dict[str, Any] | None) -> str:
    return json.dumps(metadata or {}, ensure_ascii=True)


def _metadata_load(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def create_tool_run(db: Session, *, tool_type: str, username: str, input_file_name: str | None, input_file_size: int | None, metadata: dict[str, Any] | None = None) -> ToolRun:
    run = ToolRun(
        tool_type=tool_type,
        username=username,
        status="running",
        input_file_name=input_file_name,
        input_file_size=input_file_size,
        metadata_json=_metadata_dump(metadata),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def mark_tool_run_success(db: Session, run: ToolRun, *, output_file_name: str | None, download_url: str | None, metadata: dict[str, Any] | None = None) -> ToolRun:
    completed_at = datetime.utcnow()
    run.status = "success"
    run.completed_at = completed_at
    run.duration_ms = int((completed_at - run.started_at).total_seconds() * 1000)
    run.output_file_name = output_file_name
    run.download_url = download_url
    run.error_message = None
    merged_metadata = {**_metadata_load(run.metadata_json), **(metadata or {})}
    run.metadata_json = _metadata_dump(merged_metadata)
    db.commit()
    db.refresh(run)
    return run


def mark_tool_run_failed(db: Session, run: ToolRun, *, error_message: str) -> ToolRun:
    completed_at = datetime.utcnow()
    run.status = "failed"
    run.completed_at = completed_at
    run.duration_ms = int((completed_at - run.started_at).total_seconds() * 1000)
    run.error_message = error_message[:1000]
    db.commit()
    db.refresh(run)
    return run


def serialize_tool_run(run: ToolRun) -> ToolRunOut:
    return ToolRunOut(
        id=run.id,
        toolType=run.tool_type,
        username=run.username,
        status=run.status,
        inputFileName=run.input_file_name,
        inputFileSize=run.input_file_size,
        outputFileName=run.output_file_name,
        downloadUrl=run.download_url,
        startedAt=run.started_at,
        completedAt=run.completed_at,
        durationMs=run.duration_ms,
        errorMessage=run.error_message,
        metadata=_metadata_load(run.metadata_json),
    )


def list_recent_tool_runs(db: Session, *, limit: int = 10, tool_type: str | None = None) -> list[ToolRunOut]:
    safe_limit = max(1, min(limit, 50))
    statement = select(ToolRun).order_by(ToolRun.started_at.desc()).limit(safe_limit)
    if tool_type:
        statement = select(ToolRun).where(ToolRun.tool_type == tool_type).order_by(ToolRun.started_at.desc()).limit(safe_limit)
    return [serialize_tool_run(run) for run in db.scalars(statement).all()]
```

- [x] 在 `backend/app/main.py` 导入并接入查询

```python
from .schemas import ..., ToolRunOut
from .tool_runs import list_recent_tool_runs


@app.get("/api/tools/runs", response_model=list[ToolRunOut])
def list_tool_runs(
    _: str = Depends(require_auth),
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=50),
    toolType: Optional[str] = Query(default=None),
):
    return list_recent_tool_runs(db, limit=limit, tool_type=toolType)
```

- [x] 运行测试

```bash
pytest -q tests/test_api.py -k 'tool_runs'
```

预期：当前新增路由相关测试通过。

### Task 3: 三个工具接入运行记录

**Files:**
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_api.py`

- [x] 写失败测试：视频压缩成功后生成 `success` 记录

```python
def test_video_compress_creates_success_tool_run_record(tmp_path: Path):
    _set_storage_paths(tmp_path)
    sample = b"0" * 100

    def fake_run(source_path: Path, file_id: str, mode: str) -> Path:
        output_path = Path(settings.video_output_dir) / f"{file_id}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"1" * 80)
        return output_path

    with patch("app.main.run_video_compress", side_effect=fake_run):
        response = client.post(
            "/api/tools/video-compress",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", sample, "video/mp4")},
            data={"mode": "balanced"},
        )

    assert response.status_code == 200
    runs = client.get("/api/tools/runs", headers=AUTH_HEADERS, params={"toolType": "video-compress"}).json()
    assert runs[0]["toolType"] == "video-compress"
    assert runs[0]["status"] == "success"
    assert runs[0]["inputFileName"] == "sample.mp4"
    assert runs[0]["downloadUrl"].startswith("/api/tools/video-compress/files/")
```

- [x] 写失败测试：字幕烧录失败后生成 `failed` 记录

```python
def test_video_subtitle_burn_creates_failed_tool_run_record(tmp_path: Path):
    _set_storage_paths(tmp_path)
    with patch("app.main.generate_burned_subtitle_video", side_effect=RuntimeError("TRANSCRIBER_NOT_AVAILABLE")):
        response = client.post(
            "/api/tools/video-subtitle-burn",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", b"video", "video/mp4")},
            data={"language": "auto"},
        )

    assert response.status_code == 500
    runs = client.get("/api/tools/runs", headers=AUTH_HEADERS, params={"toolType": "video-subtitle-burn"}).json()
    assert runs[0]["status"] == "failed"
    assert runs[0]["errorMessage"]
```

- [x] 修改 `backend/app/main.py` 工具路由签名，注入 `username` 和 `db`

```python
def video_compress(
    username: str = Depends(require_auth),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    mode: str = Form(...),
):
```

同样改：

- `vtt_subtitle`
- `video_subtitle_burn`

- [x] 在三个路由中创建 run，成功后 mark success，异常时 mark failed 后继续抛出原错误

视频压缩示例：

```python
run = create_tool_run(
    db,
    tool_type="video-compress",
    username=username,
    input_file_name=file.filename or source_path.name,
    input_file_size=source_path.stat().st_size if source_path.exists() else None,
    metadata={"mode": mode},
)
try:
    output_path = run_video_compress(source_path, file_id, mode)
    result = build_compress_result(file.filename or source_path.name, source_path, output_path, mode, file_id)
    mark_tool_run_success(
        db,
        run,
        output_file_name=output_path.name,
        download_url=result["downloadUrl"],
        metadata={
            "mode": mode,
            "originalSize": result["originalSize"],
            "outputSize": result["compressedSize"],
            "outcome": result["outcome"],
        },
    )
    return result
except Exception as error:
    mark_tool_run_failed(db, run, error_message=str(error))
    raise
```

- [x] 运行后端测试

```bash
pytest -q tests/test_api.py -k 'tool_run or video_compress or vtt_subtitle or video_subtitle_burn'
```

预期：相关测试通过。

### Task 4: 前端最近使用记录区块

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/tests/ui-shell.test.js`

- [x] 在 `frontend/tests/ui-shell.test.js` 写失败断言

```javascript
expectIncludes('最近使用记录', 'missing tool run history section');
expectIncludes('/api/tools/runs', 'missing tool run history API hookup');
expectIncludes('function loadToolRuns()', 'missing tool run history loader');
expectIncludes('id="toolRunHistory"', 'missing tool run history mount');
```

- [x] 在 `frontend/index.html` 新增状态变量

```javascript
let toolRuns = [];
```

- [x] 新增工具运行记录加载函数

```javascript
async function loadToolRuns(){
  try{
    toolRuns = await api('/api/tools/runs?limit=8');
  }catch(error){
    console.error(error);
    toolRuns = [];
  }
  renderToolRunHistory();
}
```

- [x] 新增渲染函数

```javascript
function renderToolRunHistory(){
  const root = document.getElementById('toolRunHistory');
  if(!root) return;
  if(!toolRuns.length){
    root.innerHTML = '<div class="empty">当前还没有工具使用记录。运行任意工具后，这里会显示最近记录。</div>';
    return;
  }
  root.innerHTML = toolRuns.map(run=>`<div class="roadline"><div><strong>${esc(toolLabel(run.toolType))} · ${esc(run.status)}</strong><div class="helper">${esc(run.inputFileName || '未记录文件名')} · ${formatDateTime(run.startedAt)} · ${run.durationMs ?? '-'} ms</div></div>${run.downloadUrl ? `<button class="button ghost" type="button" onclick="downloadRunArtifact('${esc(run.downloadUrl)}')">下载结果</button>` : '<span class="status-badge wait">无下载</span>'}</div>`).join('');
}
```

- [x] 新增辅助函数

```javascript
function toolLabel(toolType){
  const tool = tools.find(item=>item.id===toolType);
  return tool ? tool.title : toolType;
}
```

- [x] 在 Tools 页模板里加入历史区块

```html
<div class="card">
  <div class="section-title"><h2>最近使用记录</h2><span class="helper">记录真实工具执行结果</span></div>
  <div id="toolRunHistory"></div>
</div>
```

- [x] 在 `render.tools()` 完成后调用 `loadToolRuns()`

```javascript
loadToolRuns();
```

- [x] 运行前端结构测试和脚本检查

```bash
node frontend/tests/ui-shell.test.js
python3 - <<'PY'
from pathlib import Path
s = Path('frontend/index.html').read_text()
Path('/tmp/hagsyn-frontend-script.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/hagsyn-frontend-script.js
```

预期：全部通过。

### Task 5: 文档与最终验证

**Files:**
- Modify: `docs/testing/reports/2026-07-01-video-compress-and-vtt-tool-report.md`
- Modify: `docs/standards/05-data-modeling-standards.md`
- Verify only: backend/frontend commands

- [x] 在 `docs/standards/05-data-modeling-standards.md` 的 Tool Data Boundary 后补充：当明确需要历史记录、审计或任务列表时，工具运行元数据可以建模为 `ToolRun`

- [x] 在测试报告追加本轮记录：
  - 问题：当前只有文件留痕，没有业务运行记录
  - 修复：新增 `ToolRun`、`GET /api/tools/runs`、三个工具接入记录、前端最近记录
  - 验证命令与结果

- [x] 运行完整后端测试

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
source .venv/bin/activate
pytest -q
```

预期：全部通过。

- [x] 运行前端结构和脚本检查

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
node frontend/tests/ui-shell.test.js
python3 - <<'PY'
from pathlib import Path
s = Path('frontend/index.html').read_text()
Path('/tmp/hagsyn-frontend-script.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/hagsyn-frontend-script.js
```

预期：全部通过。

- [x] 浏览器验证：
  - 打开 `http://127.0.0.1:5173/?v=tool-run-history#tools`
  - 确认 Tools 页有 `最近使用记录`
  - 执行一次工具后刷新记录区块
  - 确认成功记录显示工具名、文件名、状态、耗时、下载入口

---

## Self-Review

- Spec coverage: 已覆盖模型、API、三工具接入、前端展示、清理边界、失败记录和验证。
- Placeholder scan: 无 `TBD` / `TODO` / “稍后实现”类占位。
- Type consistency: 使用 `ToolRun` / `ToolRunOut` / `toolType` / `downloadUrl` 命名，与现有 snake_case ORM + camelCase API 规则一致。
