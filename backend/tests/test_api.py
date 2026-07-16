import os
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from unittest.mock import patch

from fastapi.testclient import TestClient

import app.subtitle_tools as subtitle_tools_module
import app.video_tools as video_tools_module
from app.storage_policy import cleanup_tool_runs
from app.config import Settings
from app.database import SessionLocal
from app.main import app
from app.models import ToolRun
from app.config import settings
from app.subtitle_tools import render_srt_lines, render_vtt_lines

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer hagsyn-local-dev-token"}


def test_runtime_config_defaults_match_local_mode():
    local_defaults = Settings(_env_file=None)
    assert local_defaults.app_runtime_mode == "local"
    assert local_defaults.api_host == "127.0.0.1"
    assert local_defaults.api_port == 8000
    assert local_defaults.frontend_origin == "http://127.0.0.1:5173"
    assert local_defaults.auth_token_ttl_hours == 24 * 7
    assert local_defaults.ffmpeg_bin == "ffmpeg"
    assert local_defaults.ffprobe_bin == "ffprobe"
    assert local_defaults.transcribe_provider == "local"
    assert local_defaults.whisper_model == "base"
    assert local_defaults.whisper_device == "cpu"


def _set_storage_paths(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    upload_dir = tmp_path / "uploads"
    compressed_dir = tmp_path / "compressed"
    subtitle_dir = tmp_path / "subtitles"
    policy_file = tmp_path / "storage_policy.json"
    settings.video_upload_dir = str(upload_dir)
    settings.video_output_dir = str(compressed_dir)
    settings.subtitle_output_dir = str(subtitle_dir)
    settings.storage_policy_file = str(policy_file)
    return upload_dir, compressed_dir, subtitle_dir, policy_file


def _clear_tool_runs() -> None:
    db = SessionLocal()
    try:
        db.query(ToolRun).delete()
        db.commit()
    finally:
        db.close()


def _unique_user_payload() -> dict[str, str]:
    suffix = str(uuid4().int % 100000000).zfill(8)
    return {
        "username": f"tester_{suffix}",
        "phone": f"138{suffix}",
        "password": "StrongPass123",
        "confirmPassword": "StrongPass123",
    }


def test_login_returns_token():
    response = client.post("/api/auth/login", json={"account": "hagsyn", "password": "hagsyn123"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["token"].startswith("hg.")
    assert payload["user"]["username"] == "hagsyn"
    assert payload["user"]["isAdmin"] is True


def test_register_login_me_flow_supports_phone_login():
    payload = _unique_user_payload()

    register_response = client.post("/api/auth/register", json=payload)
    assert register_response.status_code == 200
    register_body = register_response.json()
    assert register_body["token"].startswith("hg.")
    assert register_body["user"]["username"] == payload["username"]
    assert register_body["user"]["phone"] == payload["phone"]
    assert register_body["user"]["isAdmin"] is False

    login_response = client.post(
        "/api/auth/login",
        json={"account": payload["phone"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    assert token

    me_response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    me_body = me_response.json()
    assert me_body["username"] == payload["username"]
    assert me_body["phone"] == payload["phone"]
    assert me_body["isAdmin"] is False


def test_register_rejects_invalid_phone():
    payload = _unique_user_payload()
    payload["phone"] = "12345"

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 422


def test_register_rejects_duplicate_username_or_phone():
    payload = _unique_user_payload()

    first_response = client.post("/api/auth/register", json=payload)
    assert first_response.status_code == 200

    duplicate_username_response = client.post(
        "/api/auth/register",
        json={**_unique_user_payload(), "username": payload["username"]},
    )
    assert duplicate_username_response.status_code == 409

    duplicate_phone_response = client.post(
        "/api/auth/register",
        json={**_unique_user_payload(), "phone": payload["phone"]},
    )
    assert duplicate_phone_response.status_code == 409


def test_me_requires_valid_token():
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid-token"})

    assert response.status_code == 401


def test_me_rejects_expired_token(monkeypatch):
    import app.services.auth as auth_service

    register_response = client.post("/api/auth/register", json=_unique_user_payload())
    assert register_response.status_code == 200
    token = register_response.json()["token"]
    token_payload = auth_service.parse_access_token(token)
    assert token_payload is not None

    monkeypatch.setattr(auth_service.time, "time", lambda: token_payload.exp + 1)
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401


def test_register_integrity_error_maps_to_conflict(monkeypatch):
    from sqlalchemy.exc import IntegrityError

    original_commit = SessionLocal.class_.commit
    call_state = {"count": 0}

    def flaky_commit(session):
        call_state["count"] += 1
        if call_state["count"] == 1:
            raise IntegrityError("insert", {}, Exception("UNIQUE constraint failed: users.username"))
        return original_commit(session)

    monkeypatch.setattr(SessionLocal.class_, "commit", flaky_commit)
    response = client.post("/api/auth/register", json=_unique_user_payload())

    assert response.status_code == 409


def test_admin_storage_policy_rejects_registered_non_admin_user():
    payload = _unique_user_payload()
    register_response = client.post("/api/auth/register", json=payload)
    assert register_response.status_code == 200

    login_response = client.post(
        "/api/auth/login",
        json={"account": payload["username"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]

    response = client.get("/api/admin/storage-policy", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403


def test_nodes_require_auth():
    response = client.get("/api/nodes")
    assert response.status_code == 401


def test_create_node_and_list_by_type():
    response = client.post("/api/nodes", headers=AUTH_HEADERS, json={
        "title": "Hermes Agent",
        "type": "tool",
        "description": "AI agent framework",
        "tags": ["agent", "automation"],
        "status": "used",
        "importance": 5,
        "businessValue": 4,
    })
    assert response.status_code == 200
    node = response.json()
    assert node["title"] == "Hermes Agent"
    assert node["tags"] == ["agent", "automation"]

    list_response = client.get("/api/nodes", headers=AUTH_HEADERS, params={"type": "tool"})
    assert list_response.status_code == 200
    assert any(item["id"] == node["id"] for item in list_response.json())


def test_create_edge_between_nodes():
    source = client.post("/api/nodes", headers=AUTH_HEADERS, json={"title": "AI 漫剧", "type": "project"}).json()
    target = client.post("/api/nodes", headers=AUTH_HEADERS, json={"title": "ComfyUI", "type": "tool"}).json()

    response = client.post("/api/edges", headers=AUTH_HEADERS, json={
        "sourceId": source["id"],
        "targetId": target["id"],
        "relation": "uses",
    })
    assert response.status_code == 200
    assert response.json()["relation"] == "uses"


def test_create_roadmap_with_step():
    roadmap_response = client.post("/api/roadmaps", headers=AUTH_HEADERS, json={
        "title": "AI Agent 商业化路线",
        "goal": "交付知识库问答和自动化助手",
    })
    assert roadmap_response.status_code == 200
    roadmap = roadmap_response.json()

    step_response = client.post(f"/api/roadmaps/{roadmap['id']}/steps", headers=AUTH_HEADERS, json={
        "title": "学习 Function Calling",
        "status": "todo",
    })
    assert step_response.status_code == 200
    assert step_response.json()["steps"][0]["title"] == "学习 Function Calling"


def test_seed_populates_curated_chinese_dataset():
    response = client.post("/api/seed", headers=AUTH_HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert payload["nodes"] >= 35
    assert payload["edges"] >= 20
    assert payload["roadmaps"] >= 3

    nodes = client.get("/api/nodes", headers=AUTH_HEADERS).json()
    titles = {item["title"] for item in nodes}
    assert "Hagsyn Graph" in titles
    assert "知识库问答" in titles
    assert "Prompt Engineering" in titles

    roadmaps = client.get("/api/roadmaps", headers=AUTH_HEADERS).json()
    roadmap_titles = {item["title"] for item in roadmaps}
    assert "AI 工具学习路线" in roadmap_titles


def test_video_compress_rejects_unsupported_extension():
    response = client.post(
        "/api/tools/video-compress",
        headers=AUTH_HEADERS,
        files={"file": ("note.txt", b"hello", "text/plain")},
        data={"mode": "balanced"},
    )
    assert response.status_code == 400
    assert "Unsupported video format" in response.text


def test_tool_runs_route_requires_auth():
    response = client.get("/api/tools/runs")
    assert response.status_code == 401


def test_tool_runs_route_is_registered():
    routes = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", []) or [])))
        for route in app.routes
    }
    assert ("/api/tools/runs", ("GET",)) in routes


def test_tool_runs_api_returns_recent_records_with_filter_and_limit():
    _clear_tool_runs()
    db = SessionLocal()
    try:
        first = ToolRun(
            tool_type="video-compress",
            username="hagsyn",
            status="success",
            input_file_name="first.mp4",
            input_file_size=10,
            output_file_name="first-out.mp4",
            download_url="/api/tools/video-compress/files/first",
            metadata_json='{"mode":"balanced"}',
        )
        second = ToolRun(
            tool_type="vtt-subtitle",
            username="hagsyn",
            status="failed",
            input_file_name="second.mp4",
            input_file_size=20,
            error_message="boom",
            metadata_json='{"language":"zh"}',
        )
        db.add_all([first, second])
        db.commit()
    finally:
        db.close()

    response = client.get(
        "/api/tools/runs",
        headers=AUTH_HEADERS,
        params={"toolType": "video-compress", "limit": 1},
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["toolType"] == "video-compress"
    assert payload[0]["inputFileName"] == "first.mp4"
    assert payload[0]["downloadUrl"] == "/api/tools/video-compress/files/first"
    assert payload[0]["metadata"]["mode"] == "balanced"


def test_video_compress_returns_download_metadata():
    sample = (
        b"\x00\x00\x00\x20ftypisom\x00\x00\x02\x00isomiso2avc1mp41"
        b"\x00\x00\x00\x08free\x00\x00\x00\x08mdat"
    )
    def fake_run(source_path: Path, file_id: str, mode: str) -> Path:
        output_path = source_path.parent.parent / "compressed" / f"{file_id}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(sample + b"compressed")
        return output_path

    with patch("app.routers.tools.run_video_compress", side_effect=fake_run):
        response = client.post(
            "/api/tools/video-compress",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", sample, "video/mp4")},
            data={"mode": "balanced"},
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "balanced"
    assert payload["downloadUrl"].startswith("/api/tools/video-compress/files/")
    assert payload["originalName"] == "sample.mp4"


def test_video_compress_routes_are_registered():
    routes = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", []) or [])))
        for route in app.routes
    }
    assert ("/api/tools/video-compress", ("POST",)) in routes
    assert ("/api/tools/video-compress/files/{file_id}", ("GET",)) in routes


def test_video_compress_marks_larger_output_without_fake_savings():
    sample = b"0" * 100

    def fake_run(source_path: Path, file_id: str, mode: str) -> Path:
        output_path = source_path.parent.parent / "compressed" / f"{file_id}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"1" * 160)
        return output_path

    with patch("app.routers.tools.run_video_compress", side_effect=fake_run):
        response = client.post(
            "/api/tools/video-compress",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", sample, "video/mp4")},
            data={"mode": "balanced"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["compressedSize"] > payload["originalSize"]
    assert payload["savedBytes"] < 0
    assert payload["reductionRatio"] < 0
    assert payload["outcome"] == "larger"


def test_video_compress_creates_success_tool_run_record(tmp_path: Path):
    _clear_tool_runs()
    _set_storage_paths(tmp_path)
    sample = b"0" * 100

    def fake_run(source_path: Path, file_id: str, mode: str) -> Path:
        output_path = Path(settings.video_output_dir) / f"{file_id}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"1" * 80)
        return output_path

    with patch("app.routers.tools.run_video_compress", side_effect=fake_run):
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
    assert runs[0]["inputFileSize"] == 100
    assert runs[0]["downloadUrl"].startswith("/api/tools/video-compress/files/")
    assert runs[0]["metadata"]["mode"] == "balanced"
    assert runs[0]["metadata"]["outcome"] == "smaller"


def test_video_compress_uses_configured_ffmpeg_bin(tmp_path: Path):
    _, compressed_dir, _, _ = _set_storage_paths(tmp_path)
    source_path = tmp_path / "source.mp4"
    source_path.write_bytes(b"video")
    original_ffmpeg_bin = settings.ffmpeg_bin
    try:
        settings.ffmpeg_bin = "/custom/bin/ffmpeg"

        def fake_run(command, capture_output=True, text=True):
            Path(command[-1]).write_bytes(b"compressed")

            class Result:
                returncode = 0

            return Result()

        with patch("app.video_tools.subprocess.run", side_effect=fake_run) as run_mock:
            output_path = video_tools_module.run_video_compress(source_path, "demo", "balanced")
    finally:
        settings.ffmpeg_bin = original_ffmpeg_bin

    assert output_path == compressed_dir / "demo.mp4"
    assert run_mock.call_args.args[0][0] == "/custom/bin/ffmpeg"


def test_vtt_subtitle_routes_are_registered():
    routes = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", []) or [])))
        for route in app.routes
    }
    assert ("/api/tools/vtt-subtitle", ("POST",)) in routes
    assert ("/api/tools/vtt-subtitle/files/{file_id}", ("GET",)) in routes


def test_vtt_subtitle_rejects_unsupported_extension():
    response = client.post(
        "/api/tools/vtt-subtitle",
        headers=AUTH_HEADERS,
        files={"file": ("note.txt", b"hello", "text/plain")},
        data={"language": "auto"},
    )
    assert response.status_code == 400
    assert "Unsupported video format" in response.text


def test_vtt_subtitle_returns_download_metadata():
    sample = b"0" * 100

    def fake_generate(source_path: Path, file_id: str, language: str):
        output_path = source_path.parent.parent / "subtitles" / f"{file_id}.vtt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nhello world\n")
        return output_path, 1

    with patch("app.routers.tools.generate_vtt_subtitle", side_effect=fake_generate):
        response = client.post(
            "/api/tools/vtt-subtitle",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", sample, "video/mp4")},
            data={"language": "auto"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["subtitleFormat"] == "vtt"
    assert payload["segmentCount"] == 1
    assert payload["downloadUrl"].startswith("/api/tools/vtt-subtitle/files/")


def test_vtt_subtitle_reports_missing_transcription_dependency():
    sample = b"0" * 100

    with patch("app.routers.tools.generate_vtt_subtitle", side_effect=RuntimeError("TRANSCRIBER_NOT_AVAILABLE")):
        response = client.post(
            "/api/tools/vtt-subtitle",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", sample, "video/mp4")},
            data={"language": "auto"},
        )

    assert response.status_code == 500
    assert "Subtitle generation dependency unavailable" in response.text


def test_video_subtitle_burn_routes_are_registered():
    routes = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", []) or [])))
        for route in app.routes
    }
    assert ("/api/tools/video-subtitle-burn", ("POST",)) in routes
    assert ("/api/tools/video-subtitle-burn/files/{file_id}", ("GET",)) in routes


def test_video_subtitle_burn_rejects_unsupported_extension():
    response = client.post(
        "/api/tools/video-subtitle-burn",
        headers=AUTH_HEADERS,
        files={"file": ("note.txt", b"hello", "text/plain")},
        data={"language": "auto"},
    )
    assert response.status_code == 400
    assert "Unsupported video format" in response.text


def test_video_subtitle_burn_returns_download_metadata():
    sample = b"0" * 100

    def fake_generate(source_path: Path, file_id: str, language: str):
        output_path = source_path.parent.parent / "burned" / f"{file_id}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"video-with-subtitles")
        return output_path, 3

    with patch("app.routers.tools.generate_burned_subtitle_video", side_effect=fake_generate):
        response = client.post(
            "/api/tools/video-subtitle-burn",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", sample, "video/mp4")},
            data={"language": "auto"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["outputFormat"] == "mp4"
    assert payload["segmentCount"] == 3
    assert payload["downloadUrl"].startswith("/api/tools/video-subtitle-burn/files/")


def test_video_subtitle_burn_reports_missing_transcription_dependency():
    sample = b"0" * 100

    with patch("app.routers.tools.generate_burned_subtitle_video", side_effect=RuntimeError("TRANSCRIBER_NOT_AVAILABLE")):
        response = client.post(
            "/api/tools/video-subtitle-burn",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", sample, "video/mp4")},
            data={"language": "auto"},
        )

    assert response.status_code == 500
    assert "Subtitle generation dependency unavailable" in response.text


def test_video_subtitle_burn_creates_failed_tool_run_record(tmp_path: Path):
    _clear_tool_runs()
    _set_storage_paths(tmp_path)

    with patch("app.routers.tools.generate_burned_subtitle_video", side_effect=RuntimeError("TRANSCRIBER_NOT_AVAILABLE")):
        response = client.post(
            "/api/tools/video-subtitle-burn",
            headers=AUTH_HEADERS,
            files={"file": ("sample.mp4", b"video", "video/mp4")},
            data={"language": "auto"},
        )

    assert response.status_code == 500
    runs = client.get("/api/tools/runs", headers=AUTH_HEADERS, params={"toolType": "video-subtitle-burn"}).json()
    assert runs[0]["toolType"] == "video-subtitle-burn"
    assert runs[0]["status"] == "failed"
    assert runs[0]["inputFileName"] == "sample.mp4"
    assert runs[0]["errorMessage"]
    assert runs[0]["metadata"]["language"] == "auto"


def test_admin_storage_policy_get_returns_default_policy(tmp_path: Path):
    _, _, _, policy_file = _set_storage_paths(tmp_path)

    response = client.get("/api/admin/storage-policy", headers=AUTH_HEADERS)

    assert response.status_code == 200
    payload = response.json()
    assert payload["isAdmin"] is True
    assert payload["policy"]["autoCleanupEnabled"] is True
    assert payload["policy"]["deleteIntermediateAudio"] is True
    assert payload["policy"]["cleanupFailedTemporaryFiles"] is True
    assert Path(policy_file).exists()


def test_admin_storage_policy_rejects_non_admin(tmp_path: Path):
    _set_storage_paths(tmp_path)
    original_username = settings.auth_username
    try:
        settings.auth_username = "viewer"
        response = client.get("/api/admin/storage-policy", headers=AUTH_HEADERS)
    finally:
        settings.auth_username = original_username

    assert response.status_code == 403
    assert "Admin access required" in response.text


def test_admin_storage_policy_put_updates_policy(tmp_path: Path):
    _set_storage_paths(tmp_path)

    response = client.put(
        "/api/admin/storage-policy",
        headers=AUTH_HEADERS,
        json={
            "autoCleanupEnabled": False,
            "uploadRetentionHours": 12,
            "compressedRetentionHours": 24,
            "subtitleRetentionHours": 36,
            "deleteIntermediateAudio": False,
            "cleanupFailedTemporaryFiles": False,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["policy"]["autoCleanupEnabled"] is False
    assert payload["policy"]["uploadRetentionHours"] == 12
    assert payload["policy"]["deleteIntermediateAudio"] is False


def test_admin_storage_policy_run_cleanup_returns_stats(tmp_path: Path):
    upload_dir, compressed_dir, subtitle_dir, _ = _set_storage_paths(tmp_path)

    response = client.put(
        "/api/admin/storage-policy",
        headers=AUTH_HEADERS,
        json={
            "autoCleanupEnabled": True,
            "uploadRetentionHours": 1,
            "compressedRetentionHours": 1,
            "subtitleRetentionHours": 1,
            "deleteIntermediateAudio": True,
            "cleanupFailedTemporaryFiles": True,
        },
    )
    assert response.status_code == 200

    old_ts = 1_700_000_000
    fresh_ts = old_ts + 5_000
    for base_dir, old_name, fresh_name in [
        (upload_dir, "old.mp4", "fresh.mp4"),
        (compressed_dir, "old.mp4", "fresh.mp4"),
        (subtitle_dir, "old.vtt", "fresh.vtt"),
    ]:
        base_dir.mkdir(parents=True, exist_ok=True)
        old_file = base_dir / old_name
        fresh_file = base_dir / fresh_name
        old_file.write_bytes(b"12345")
        fresh_file.write_bytes(b"123456")
        os.utime(old_file, (old_ts, old_ts))
        os.utime(fresh_file, (fresh_ts, fresh_ts))

    with patch("app.storage_policy.time.time", return_value=old_ts + 7200):
        cleanup_response = client.post("/api/admin/storage-policy/run-cleanup", headers=AUTH_HEADERS)

    assert cleanup_response.status_code == 200
    payload = cleanup_response.json()
    assert payload["filesDeleted"] == 3
    assert payload["bytesFreed"] == 15
    assert upload_dir.joinpath("old.mp4").exists() is False
    assert compressed_dir.joinpath("old.mp4").exists() is False
    assert subtitle_dir.joinpath("old.vtt").exists() is False
    assert upload_dir.joinpath("fresh.mp4").exists() is True


def test_admin_storage_policy_run_cleanup_returns_tool_run_cleanup_stats(tmp_path: Path):
    _set_storage_paths(tmp_path)
    response = client.put(
        "/api/admin/storage-policy",
        headers=AUTH_HEADERS,
        json={
            "autoCleanupEnabled": True,
            "uploadRetentionHours": 72,
            "compressedRetentionHours": 72,
            "subtitleRetentionHours": 72,
            "toolRunRetentionHours": 1,
            "deleteIntermediateAudio": True,
            "cleanupFailedTemporaryFiles": True,
        },
    )
    assert response.status_code == 200

    with patch("app.services.storage_policy.cleanup_tool_runs", return_value=3):
        cleanup_response = client.post("/api/admin/storage-policy/run-cleanup", headers=AUTH_HEADERS)

    assert cleanup_response.status_code == 200
    payload = cleanup_response.json()
    assert payload["toolRunsDeleted"] == 3


def test_cleanup_tool_runs_deletes_only_expired_records():
    _clear_tool_runs()
    db = SessionLocal()
    try:
        old_run = ToolRun(
            tool_type="video-compress",
            username="hagsyn",
            status="success",
            input_file_name="old.mp4",
            input_file_size=10,
            started_at=datetime.utcfromtimestamp(1_700_000_000),
            completed_at=datetime.utcfromtimestamp(1_700_000_100),
            duration_ms=100,
            metadata_json="{}",
        )
        fresh_run = ToolRun(
            tool_type="vtt-subtitle",
            username="hagsyn",
            status="success",
            input_file_name="fresh.mp4",
            input_file_size=12,
            started_at=datetime.utcfromtimestamp(1_700_010_000),
            completed_at=datetime.utcfromtimestamp(1_700_010_100),
            duration_ms=100,
            metadata_json="{}",
        )
        db.add_all([old_run, fresh_run])
        db.commit()
    finally:
        db.close()

    deleted = cleanup_tool_runs(now_ts=1_700_000_000 + 7200, retention_hours=1)

    assert deleted == 1
    runs = client.get("/api/tools/runs", headers=AUTH_HEADERS).json()
    assert len(runs) == 1
    assert runs[0]["toolType"] == "vtt-subtitle"


def test_generate_vtt_subtitle_removes_intermediate_wav_after_success(tmp_path: Path):
    _, _, subtitle_dir, _ = _set_storage_paths(tmp_path)
    source_path = tmp_path / "source.mp4"
    source_path.write_bytes(b"video")

    class Segment:
        def __init__(self, start: float, end: float, text: str):
            self.start = start
            self.end = end
            self.text = text

    class FakeModel:
        def transcribe(self, _path: str, language=None):
            return [Segment(0.0, 1.2, "hello world")], {"language": language or "en"}

    def fake_run(command, capture_output=True, text=True):
        wav_path = Path(command[-1])
        wav_path.write_bytes(b"wav")

        class Result:
            returncode = 0

        return Result()

    with patch.dict("sys.modules", {"faster_whisper": type("Module", (), {"WhisperModel": lambda *args, **kwargs: FakeModel()})}):
        with patch("app.subtitle_tools.subprocess.run", side_effect=fake_run):
            output_path, segment_count = subtitle_tools_module.generate_vtt_subtitle(source_path, "demo", "auto")

    assert segment_count == 1
    assert output_path.exists() is True
    assert subtitle_dir.joinpath("demo.wav").exists() is False


def test_generate_vtt_subtitle_uses_configured_runtime_dependencies(tmp_path: Path):
    _, _, subtitle_dir, _ = _set_storage_paths(tmp_path)
    source_path = tmp_path / "source.mp4"
    source_path.write_bytes(b"video")
    original_ffmpeg_bin = settings.ffmpeg_bin
    original_whisper_model = settings.whisper_model
    original_whisper_device = settings.whisper_device
    created_models = []

    class Segment:
        start = 0.0
        end = 1.0
        text = "hello"

    class FakeModel:
        def __init__(self, model_name: str, device: str, compute_type: str):
            created_models.append((model_name, device, compute_type))

        def transcribe(self, _path: str, language=None):
            return [Segment()], {"language": language or "en"}

    def fake_run(command, capture_output=True, text=True):
        Path(command[-1]).write_bytes(b"wav")

        class Result:
            returncode = 0

        return Result()

    try:
        settings.ffmpeg_bin = "/custom/bin/ffmpeg"
        settings.whisper_model = "small"
        settings.whisper_device = "gpu"
        with patch.dict("sys.modules", {"faster_whisper": type("Module", (), {"WhisperModel": FakeModel})}):
            with patch("app.subtitle_tools.subprocess.run", side_effect=fake_run) as run_mock:
                output_path, segment_count = subtitle_tools_module.generate_vtt_subtitle(source_path, "configured", "auto")
    finally:
        settings.ffmpeg_bin = original_ffmpeg_bin
        settings.whisper_model = original_whisper_model
        settings.whisper_device = original_whisper_device

    assert output_path == subtitle_dir / "configured.vtt"
    assert segment_count == 1
    assert run_mock.call_args.args[0][0] == "/custom/bin/ffmpeg"
    assert created_models == [("small", "gpu", "int8")]
    assert subtitle_dir.joinpath("configured.wav").exists() is False


def test_generate_vtt_subtitle_cleans_intermediate_wav_when_transcribe_fails(tmp_path: Path):
    _, _, subtitle_dir, _ = _set_storage_paths(tmp_path)
    source_path = tmp_path / "source.mp4"
    source_path.write_bytes(b"video")

    class FakeModel:
        def transcribe(self, _path: str, language=None):
            raise RuntimeError("boom")

    def fake_run(command, capture_output=True, text=True):
        wav_path = Path(command[-1])
        wav_path.write_bytes(b"wav")

        class Result:
            returncode = 0

        return Result()

    with patch.dict("sys.modules", {"faster_whisper": type("Module", (), {"WhisperModel": lambda *args, **kwargs: FakeModel()})}):
        with patch("app.subtitle_tools.subprocess.run", side_effect=fake_run):
            try:
                subtitle_tools_module.generate_vtt_subtitle(source_path, "demo-fail", "auto")
            except RuntimeError as error:
                assert str(error) == "boom"
            else:  # pragma: no cover
                raise AssertionError("expected runtime error")

    assert subtitle_dir.joinpath("demo-fail.wav").exists() is False


def test_render_vtt_lines_outputs_valid_webvtt_blocks():
    segments = [
        {"start": 0.0, "end": 2.0, "text": "你好世界"},
        {"start": 2.0, "end": 4.5, "text": "这是第二句"},
    ]
    lines = render_vtt_lines(segments)
    assert lines[0] == "WEBVTT"
    assert "00:00:00.000 --> 00:00:02.000" in lines
    assert "00:00:02.000 --> 00:00:04.500" in lines


def test_render_vtt_lines_splits_long_text_for_readability():
    segments = [
        {
            "start": 0.0,
            "end": 6.0,
            "text": "这是一个很长的字幕句子，用来验证在文本过长时会被拆成更适合阅读的多行内容，而不是整段堆在同一条字幕里。",
        }
    ]
    lines = render_vtt_lines(segments, max_chars_per_line=18)
    text_lines = [line for line in lines if line and "-->" not in line and line != "WEBVTT"]
    assert len(text_lines) >= 2


def test_render_srt_lines_outputs_valid_srt_blocks():
    segments = [
        {"start": 0.0, "end": 2.0, "text": "你好世界"},
        {"start": 2.0, "end": 4.5, "text": "这是第二句"},
    ]
    lines = render_srt_lines(segments)
    assert lines[0] == "1"
    assert "00:00:00,000 --> 00:00:02,000" in lines
    assert "00:00:02,000 --> 00:00:04,500" in lines
