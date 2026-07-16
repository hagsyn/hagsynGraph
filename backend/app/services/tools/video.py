from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from ...core.config import settings
from ..storage_policy import cleanup_file, should_cleanup_failed_temporary_files

ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v"}
COMPRESSION_MODES = {
    "balanced": {"crf": "28", "preset": "medium", "label": "平衡压缩"},
    "smaller": {"crf": "32", "preset": "slow", "label": "高压缩"},
    "quality": {"crf": "24", "preset": "medium", "label": "高质量"},
}


def ensure_storage_dirs() -> tuple[Path, Path]:
    upload_dir = Path(settings.video_upload_dir)
    output_dir = Path(settings.video_output_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir, output_dir


def validate_video_upload(file: UploadFile, mode: str) -> str:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported video format")
    if mode not in COMPRESSION_MODES:
        raise HTTPException(status_code=400, detail="Unsupported compression mode")
    return suffix


def save_upload(file: UploadFile, suffix: str) -> tuple[Path, str]:
    upload_dir, _ = ensure_storage_dirs()
    file_id = uuid4().hex[:16]
    source_path = upload_dir / f"{file_id}{suffix}"
    with source_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return source_path, file_id


def run_video_compress(source_path: Path, file_id: str, mode: str) -> Path:
    _, output_dir = ensure_storage_dirs()
    output_path = output_dir / f"{file_id}.mp4"
    config = COMPRESSION_MODES[mode]
    command = [
        settings.ffmpeg_bin,
        "-y",
        "-i",
        str(source_path),
        "-vcodec",
        "libx264",
        "-preset",
        config["preset"],
        "-crf",
        config["crf"],
        "-acodec",
        "aac",
        "-b:a",
        "128k",
        str(output_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        cleanup_file(output_path if should_cleanup_failed_temporary_files() else None)
        cleanup_file(source_path if should_cleanup_failed_temporary_files() else None)
        raise HTTPException(status_code=500, detail="Video compression failed")
    return output_path


def build_compress_result(original_name: str, source_path: Path, output_path: Path, mode: str, file_id: str) -> dict:
    original_size = source_path.stat().st_size
    compressed_size = output_path.stat().st_size
    saved_bytes = original_size - compressed_size
    reduction_ratio = round((saved_bytes / original_size) * 100, 2) if original_size else 0
    outcome = "smaller" if saved_bytes > 0 else "larger" if saved_bytes < 0 else "same"
    return {
        "fileId": file_id,
        "originalName": original_name,
        "mode": mode,
        "modeLabel": COMPRESSION_MODES[mode]["label"],
        "originalSize": original_size,
        "compressedSize": compressed_size,
        "savedBytes": saved_bytes,
        "reductionRatio": reduction_ratio,
        "outcome": outcome,
        "downloadUrl": f"/api/tools/video-compress/files/{file_id}",
    }


def output_file_path(file_id: str) -> Path:
    _, output_dir = ensure_storage_dirs()
    return output_dir / f"{file_id}.mp4"
