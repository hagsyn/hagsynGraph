from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Hagsyn Graph"
    app_runtime_mode: str = "local"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_origin: str = "http://127.0.0.1:5173"
    database_url: str = "sqlite:///./hagsyn_graph.db"
    auth_username: str = "hagsyn"
    auth_password: str = "hagsyn123"
    auth_token: str = "hagsyn-local-dev-token"
    auth_token_ttl_hours: int = 24 * 7
    video_upload_dir: str = "./storage/uploads"
    video_output_dir: str = "./storage/compressed"
    subtitle_output_dir: str = "./storage/subtitles"
    storage_policy_file: str = "./storage/storage_policy.json"
    ffmpeg_bin: str = "ffmpeg"
    ffprobe_bin: str = "ffprobe"
    transcribe_provider: str = "local"
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    admin_users: list[str] = ["hagsyn"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
