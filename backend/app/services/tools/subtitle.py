from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from ...core.config import settings
from ..storage_policy import (
    cleanup_file,
    cleanup_files,
    should_cleanup_failed_temporary_files,
    should_delete_intermediate_audio,
)

ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v"}
ALLOWED_SUBTITLE_LANGUAGES = {"auto", "zh", "en"}


def ensure_subtitle_dirs() -> tuple[Path, Path]:
    upload_dir = Path(settings.video_upload_dir)
    output_dir = Path(settings.subtitle_output_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir, output_dir


def validate_subtitle_upload(file: UploadFile, language: str) -> str:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported video format")
    if language not in ALLOWED_SUBTITLE_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported subtitle language")
    return suffix


def save_subtitle_upload(file: UploadFile, suffix: str) -> tuple[Path, str]:
    upload_dir, _ = ensure_subtitle_dirs()
    file_id = uuid4().hex[:16]
    source_path = upload_dir / f"{file_id}{suffix}"
    with source_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return source_path, file_id


def generate_vtt_subtitle(source_path: Path, file_id: str, language: str) -> tuple[Path, int]:
    try:
        from faster_whisper import WhisperModel
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("TRANSCRIBER_NOT_AVAILABLE") from exc

    _, output_dir = ensure_subtitle_dirs()
    audio_path = output_dir / f"{file_id}.wav"
    output_path = output_dir / f"{file_id}.vtt"

    # Extracting to a mono wav keeps the transcription step predictable and avoids
    # coupling the model call to arbitrary video container formats.
    extract_command = [
        settings.ffmpeg_bin,
        "-y",
        "-i",
        str(source_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(audio_path),
    ]
    result = subprocess.run(extract_command, capture_output=True, text=True)
    if result.returncode != 0:
        if should_cleanup_failed_temporary_files():
            cleanup_files([audio_path, source_path])
        raise HTTPException(status_code=500, detail="Audio extraction failed")

    try:
        model = WhisperModel(settings.whisper_model, device=settings.whisper_device, compute_type="int8")
        segments, _ = model.transcribe(str(audio_path), language=None if language == "auto" else language)
        normalized_segments = [
            {"start": segment.start, "end": segment.end, "text": segment.text.strip()}
            for segment in segments
            if segment.text and segment.text.strip()
        ]
        rows = render_vtt_lines(normalized_segments)
        segment_count = sum(1 for line in rows if " --> " in line)
        output_path.write_text("\n".join(rows), encoding="utf-8")
        return output_path, segment_count
    except Exception:
        if should_cleanup_failed_temporary_files():
            cleanup_files([audio_path, output_path, source_path])
        raise
    finally:
        if should_delete_intermediate_audio():
            cleanup_file(audio_path)


def generate_burned_subtitle_video(source_path: Path, file_id: str, language: str) -> tuple[Path, int]:
    _, output_dir = ensure_subtitle_dirs()
    subtitle_path, segment_count = generate_vtt_subtitle(source_path, file_id, language)
    srt_path = output_dir / f"{file_id}.srt"
    burned_path = output_dir / f"{file_id}.mp4"

    # ffmpeg subtitle burn expects an SRT-style filter input, so we normalize the
    # generated VTT back into timed text blocks first.
    vtt_lines = subtitle_path.read_text(encoding="utf-8").splitlines()
    segment_blocks = _segments_from_vtt_lines(vtt_lines)
    srt_path.write_text("\n".join(render_srt_lines(segment_blocks)), encoding="utf-8")
    escaped_subtitle_path = (
        srt_path.as_posix()
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace(",", "\\,")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("'", "\\'")
        .replace(" ", "\\ ")
    )
    subtitle_filter = f"subtitles=filename='{escaped_subtitle_path}'"
    command = [
        settings.ffmpeg_bin,
        "-y",
        "-i",
        str(source_path),
        "-vf",
        subtitle_filter,
        "-c:a",
        "copy",
        str(burned_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        if should_cleanup_failed_temporary_files():
            cleanup_files([burned_path, subtitle_path, srt_path, source_path])
        stderr = result.stderr.strip()
        meaningful_tail = "\n".join(stderr.splitlines()[-8:])
        raise HTTPException(status_code=500, detail=f"Subtitle burn failed: {meaningful_tail[:800]}")
    cleanup_file(srt_path)
    return burned_path, segment_count


def build_subtitle_result(original_name: str, output_path: Path, language: str, file_id: str, segment_count: int) -> dict:
    return {
        "fileId": file_id,
        "originalName": original_name,
        "language": language,
        "subtitleFormat": "vtt",
        "segmentCount": segment_count,
        "outcome": "success",
        "downloadUrl": f"/api/tools/vtt-subtitle/files/{file_id}",
    }


def subtitle_file_path(file_id: str) -> Path:
    _, output_dir = ensure_subtitle_dirs()
    return output_dir / f"{file_id}.vtt"


def burned_video_file_path(file_id: str) -> Path:
    _, output_dir = ensure_subtitle_dirs()
    return output_dir / f"{file_id}.mp4"


def render_vtt_lines(segments: list[dict], max_chars_per_line: int = 24) -> list[str]:
    rows = ["WEBVTT", ""]
    for segment in segments:
        text = _normalize_subtitle_text(segment["text"])
        if not text:
            continue
        rows.append(f"{_vtt_ts(segment['start'])} --> {_vtt_ts(segment['end'])}")
        for line in _wrap_subtitle_text(text, max_chars_per_line=max_chars_per_line):
            rows.append(line)
        rows.append("")
    return rows


def render_srt_lines(segments: list[dict], max_chars_per_line: int = 24) -> list[str]:
    rows: list[str] = []
    for idx, segment in enumerate(segments, start=1):
        text = _normalize_subtitle_text(segment["text"])
        if not text:
            continue
        rows.append(str(idx))
        rows.append(f"{_srt_ts(segment['start'])} --> {_srt_ts(segment['end'])}")
        for line in _wrap_subtitle_text(text, max_chars_per_line=max_chars_per_line):
            rows.append(line)
        rows.append("")
    return rows


def _vtt_ts(value: float) -> str:
    total_ms = int(round(value * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def _srt_ts(value: float) -> str:
    total_ms = int(round(value * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def _normalize_subtitle_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def _wrap_subtitle_text(text: str, max_chars_per_line: int = 24) -> list[str]:
    if len(text) <= max_chars_per_line:
        return [text]

    # Prefer splitting near punctuation so generated subtitles read more like
    # caption lines than arbitrary fixed-width chunks.
    punctuation = "，。！？；：,.!?;:"
    lines: list[str] = []
    remaining = text
    while len(remaining) > max_chars_per_line:
        split_at = max_chars_per_line
        for idx in range(max_chars_per_line - 1, max(0, max_chars_per_line // 2), -1):
            if remaining[idx] in punctuation:
                split_at = idx + 1
                break
        lines.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()
    if remaining:
        lines.append(remaining)
    return lines


def _segments_from_vtt_lines(lines: list[str]) -> list[dict]:
    # Parse the simple WEBVTT structure we generate ourselves instead of pulling
    # in a heavier subtitle parser dependency for one conversion path.
    segments: list[dict] = []
    current = None
    text_parts: list[str] = []
    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT":
            if current and text_parts:
                current["text"] = " ".join(text_parts)
                segments.append(current)
            current = None
            text_parts = []
            continue
        if " --> " in line:
            start, end = line.split(" --> ", 1)
            current = {"start": _parse_vtt_ts(start), "end": _parse_vtt_ts(end)}
            text_parts = []
        elif current is not None:
            text_parts.append(line)
    if current and text_parts:
        current["text"] = " ".join(text_parts)
        segments.append(current)
    return segments


def _parse_vtt_ts(value: str) -> float:
    hms, ms = value.split(".")
    hours, minutes, seconds = [int(part) for part in hms.split(":")]
    return hours * 3600 + minutes * 60 + seconds + int(ms) / 1000
