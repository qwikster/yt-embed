from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    base_url: str = "yt.qwik.top"
    db_url: str = "sqlite+aiosqlite:///yt-embed.db"
    cache_dir: str = "cache"
    ytdlp: str = "ytdlp"

    host: str = "0.0.0.0"
    port: int = 12864

    filesize: str = "0"
    resolution: str = "0"
    audio_format: str = "mp3"
    video_format: str = "mp4"
    download_timeout: int = 20 # seconds
    rate_limit: str = "100m"
    retries: int = 4
    cookies_path: str = ""

    file_expiry: bool = True
    expiry_time: int = 168 # hours

    dearrow_titles: bool = False
    dearrow_api: str = "https://sponsor.ajay.app"

    serve_thumbs: bool = True
    dearrow_thumbs: bool = False
    dearrow_thumb_api: str = "https://dearrow-thumb.ajay.app"

    model_config = SettingsConfigDict(env_file="yt-embed.config", env_file_encoding="utf-8")

@lru_cache
def get_config() -> Settings:
    return Settings()
