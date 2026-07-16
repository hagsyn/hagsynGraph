from __future__ import annotations

from sqlalchemy import select

from ..models import ToolRun


def list_tool_runs_query(*, limit: int, tool_type: str | None = None):
    statement = select(ToolRun).order_by(ToolRun.started_at.desc()).limit(limit)
    if tool_type:
        statement = (
            select(ToolRun)
            .where(ToolRun.tool_type == tool_type)
            .order_by(ToolRun.started_at.desc())
            .limit(limit)
        )
    return statement
