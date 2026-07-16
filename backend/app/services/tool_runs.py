from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from ..models import ToolRun
from ..repositories.tool_runs import list_tool_runs_query
from ..schemas.tools import ToolRunOut


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


def create_tool_run(
    db: Session,
    *,
    tool_type: str,
    username: str,
    input_file_name: str | None,
    input_file_size: int | None,
    metadata: dict[str, Any] | None = None,
) -> ToolRun:
    # Tool runs are persisted immediately so even long-running or failed tools
    # still leave a truthful execution trace for the frontend history panel.
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


def mark_tool_run_success(
    db: Session,
    run: ToolRun,
    *,
    output_file_name: str | None,
    download_url: str | None,
    metadata: dict[str, Any] | None = None,
) -> ToolRun:
    # Success metadata is merged instead of replaced so the final record keeps
    # both submission-time inputs and completion-time outputs in one payload.
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
    # Keep failure payloads bounded so tool history remains readable and we do
    # not accidentally persist huge stderr blobs into the database.
    completed_at = datetime.utcnow()
    run.status = "failed"
    run.completed_at = completed_at
    run.duration_ms = int((completed_at - run.started_at).total_seconds() * 1000)
    run.error_message = error_message[:1000]
    db.commit()
    db.refresh(run)
    return run


def serialize_tool_run(run: ToolRun) -> ToolRunOut:
    # API responses should never expose the internal metadata_json storage shape.
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
    statement = list_tool_runs_query(limit=safe_limit, tool_type=tool_type)
    return [serialize_tool_run(run) for run in db.scalars(statement).all()]
