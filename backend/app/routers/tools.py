from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..core.auth import require_auth
from ..core.db import get_db
from ..schemas.tools import BurnedVideoResultOut, SubtitleResultOut, ToolRunOut, VideoCompressResultOut
from ..services.tool_runs import create_tool_run, list_recent_tool_runs, mark_tool_run_failed, mark_tool_run_success
from ..services.tools.subtitle import (
    build_subtitle_result,
    burned_video_file_path,
    generate_burned_subtitle_video,
    generate_vtt_subtitle,
    save_subtitle_upload,
    subtitle_file_path,
    validate_subtitle_upload,
)
from ..services.tools.video import build_compress_result, output_file_path, run_video_compress, save_upload, validate_video_upload

router = APIRouter()


@router.get("/api/tools/runs", response_model=list[ToolRunOut])
def list_tool_runs(
    _: str = Depends(require_auth),
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=50),
    toolType: Optional[str] = Query(default=None),
):
    return list_recent_tool_runs(db, limit=limit, tool_type=toolType)


@router.post("/api/tools/video-compress", response_model=VideoCompressResultOut)
def video_compress(
    username: str = Depends(require_auth),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    mode: str = Form(...),
):
    # Router keeps orchestration thin: validate input, create run record, delegate
    # processing to the tool service, then persist the final outcome.
    suffix = validate_video_upload(file, mode)
    source_path, file_id = save_upload(file, suffix)
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


@router.get("/api/tools/video-compress/files/{file_id}")
def download_compressed_video(file_id: str, _: str = Depends(require_auth)):
    path = output_file_path(file_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Compressed file not found")
    return FileResponse(path, media_type="video/mp4", filename=f"{file_id}.mp4")


@router.post("/api/tools/vtt-subtitle", response_model=SubtitleResultOut)
def vtt_subtitle(
    username: str = Depends(require_auth),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    language: str = Form(...),
):
    # Subtitle generation has an additional dependency boundary. Keep the router
    # responsible for translating that service-side failure into an API error.
    suffix = validate_subtitle_upload(file, language)
    source_path, file_id = save_subtitle_upload(file, suffix)
    run = create_tool_run(
        db,
        tool_type="vtt-subtitle",
        username=username,
        input_file_name=file.filename or source_path.name,
        input_file_size=source_path.stat().st_size if source_path.exists() else None,
        metadata={"language": language},
    )
    try:
        output_path, segment_count = generate_vtt_subtitle(source_path, file_id, language)
        result = build_subtitle_result(file.filename or source_path.name, output_path, language, file_id, segment_count)
        mark_tool_run_success(
            db,
            run,
            output_file_name=output_path.name,
            download_url=result["downloadUrl"],
            metadata={"language": language, "segmentCount": segment_count, "subtitleFormat": "vtt"},
        )
        return result
    except RuntimeError as error:
        mark_tool_run_failed(db, run, error_message=str(error))
        if str(error) == "TRANSCRIBER_NOT_AVAILABLE":
            raise HTTPException(status_code=500, detail="Subtitle generation dependency unavailable") from error
        raise
    except Exception as error:
        mark_tool_run_failed(db, run, error_message=str(error))
        raise


@router.get("/api/tools/vtt-subtitle/files/{file_id}")
def download_vtt_subtitle(file_id: str, _: str = Depends(require_auth)):
    path = subtitle_file_path(file_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Subtitle file not found")
    return FileResponse(path, media_type="text/vtt", filename=f"{file_id}.vtt")


@router.post("/api/tools/video-subtitle-burn", response_model=BurnedVideoResultOut)
def video_subtitle_burn(
    username: str = Depends(require_auth),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    language: str = Form(...),
):
    # Burn flow reuses subtitle generation internally, but still reports itself
    # as an independent tool run so the frontend history stays honest.
    suffix = validate_subtitle_upload(file, language)
    source_path, file_id = save_subtitle_upload(file, suffix)
    run = create_tool_run(
        db,
        tool_type="video-subtitle-burn",
        username=username,
        input_file_name=file.filename or source_path.name,
        input_file_size=source_path.stat().st_size if source_path.exists() else None,
        metadata={"language": language},
    )
    try:
        output_path, segment_count = generate_burned_subtitle_video(source_path, file_id, language)
        result = {
            "fileId": file_id,
            "originalName": file.filename or source_path.name,
            "language": language,
            "outputFormat": "mp4",
            "segmentCount": segment_count,
            "outcome": "success",
            "downloadUrl": f"/api/tools/video-subtitle-burn/files/{file_id}",
        }
        mark_tool_run_success(
            db,
            run,
            output_file_name=output_path.name,
            download_url=result["downloadUrl"],
            metadata={"language": language, "segmentCount": segment_count, "outputFormat": "mp4"},
        )
        return result
    except RuntimeError as error:
        mark_tool_run_failed(db, run, error_message=str(error))
        if str(error) == "TRANSCRIBER_NOT_AVAILABLE":
            raise HTTPException(status_code=500, detail="Subtitle generation dependency unavailable") from error
        raise
    except Exception as error:
        mark_tool_run_failed(db, run, error_message=str(error))
        raise


@router.get("/api/tools/video-subtitle-burn/files/{file_id}")
def download_burned_video(file_id: str, _: str = Depends(require_auth)):
    path = burned_video_file_path(file_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Burned video file not found")
    return FileResponse(path, media_type="video/mp4", filename=f"{file_id}.mp4")
