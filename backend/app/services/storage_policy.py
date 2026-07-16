from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from ..core.config import settings
from ..core.db import SessionLocal
from ..models import ToolRun
from ..schemas.admin import CleanupResult, StoragePolicy


def storage_policy_path() -> Path:
    return Path(settings.storage_policy_file)


def load_storage_policy() -> StoragePolicy:
    # Missing policy file is treated as first-run initialization, not an error.
    path = storage_policy_path()
    if not path.exists():
        policy = StoragePolicy()
        save_storage_policy(policy)
        return policy
    data = json.loads(path.read_text(encoding="utf-8"))
    return StoragePolicy.model_validate(data)


def save_storage_policy(policy: StoragePolicy) -> StoragePolicy:
    path = storage_policy_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(policy.model_dump(), ensure_ascii=True, indent=2), encoding="utf-8")
    return policy


def is_admin_username(username: str) -> bool:
    return username in settings.admin_users


def should_cleanup_failed_temporary_files() -> bool:
    return load_storage_policy().cleanupFailedTemporaryFiles


def should_delete_intermediate_audio() -> bool:
    return load_storage_policy().deleteIntermediateAudio


def cleanup_file(path: Path | None) -> None:
    if path is None:
        return
    try:
        if path.exists():
            path.unlink()
    except OSError:
        pass


def cleanup_files(paths: list[Path | None]) -> None:
    for path in paths:
        cleanup_file(path)


def cleanup_tool_runs(*, now_ts: float, retention_hours: int) -> int:
    # Tool run retention is managed separately from file cleanup because the DB
    # record lifetime and artifact lifetime are related but not identical.
    cutoff = datetime.utcfromtimestamp(now_ts - retention_hours * 3600)
    db = SessionLocal()
    try:
        deleted = db.query(ToolRun).filter(ToolRun.started_at <= cutoff).delete(synchronize_session=False)
        db.commit()
        return deleted
    finally:
        db.close()


def run_storage_cleanup(policy: StoragePolicy | None = None) -> CleanupResult:
    current_policy = policy or load_storage_policy()
    # Each directory can keep its own retention horizon while still sharing one
    # cleanup pass and one returned admin summary.
    directories = [
        (Path(settings.video_upload_dir), current_policy.uploadRetentionHours),
        (Path(settings.video_output_dir), current_policy.compressedRetentionHours),
        (Path(settings.subtitle_output_dir), current_policy.subtitleRetentionHours),
    ]
    now = time.time()
    files_deleted = 0
    bytes_freed = 0
    touched_dirs: list[str] = []
    for base_dir, retention_hours in directories:
        base_dir.mkdir(parents=True, exist_ok=True)
        touched_dirs.append(str(base_dir))
        cutoff = now - retention_hours * 3600
        for path in base_dir.iterdir():
            if not path.is_file():
                continue
            if path.stat().st_mtime > cutoff:
                continue
            size = path.stat().st_size
            cleanup_file(path)
            files_deleted += 1
            bytes_freed += size

    tool_runs_deleted = cleanup_tool_runs(now_ts=now, retention_hours=current_policy.toolRunRetentionHours)
    return CleanupResult(
        filesDeleted=files_deleted,
        bytesFreed=bytes_freed,
        toolRunsDeleted=tool_runs_deleted,
        directories=touched_dirs,
    )


def coerce_storage_policy(payload: dict[str, Any]) -> StoragePolicy:
    return StoragePolicy.model_validate(payload)
