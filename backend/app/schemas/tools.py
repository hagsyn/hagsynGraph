from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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


class VideoCompressResultOut(BaseModel):
    fileId: str
    originalName: str
    mode: str
    modeLabel: str
    originalSize: int
    compressedSize: int
    savedBytes: int
    reductionRatio: float
    outcome: str
    downloadUrl: str


class SubtitleResultOut(BaseModel):
    fileId: str
    originalName: str
    language: str
    subtitleFormat: str
    segmentCount: int
    outcome: str
    downloadUrl: str


class BurnedVideoResultOut(BaseModel):
    fileId: str
    originalName: str
    language: str
    outputFormat: str
    segmentCount: int
    outcome: str
    downloadUrl: str
