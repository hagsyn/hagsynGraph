from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db import Base
from .knowledge import new_id


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
