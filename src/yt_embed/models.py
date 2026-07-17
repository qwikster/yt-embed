from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from yt_embed.db import Base

def time() -> datetime:
    return datetime.now(timezone.utc)

class Item(Base):
    __tablename__ = "videos"

    id: Mapped[str]                     = mapped_column(String(11), primary_key = True)
    cached_at: Mapped[datetime]         = mapped_column(DateTime(timezone=True), default = time)
    title: Mapped[str | None]           = mapped_column(String,   nullable = True)
    duration: Mapped[int | None]        = mapped_column(Integer,  nullable = True)
    audio_path: Mapped[str | None]      = mapped_column(String,   nullable = True)
    video_path: Mapped[str | None]      = mapped_column(String,   nullable = True)
    dearrow_title: Mapped[str | None]   = mapped_column(String,   nullable = True)
    dearrow_thumb: Mapped[float | None] = mapped_column(Float,    nullable = True)
    filesize: Mapped[int | None]        = mapped_column(Integer,  nullable = True)
    resolution: Mapped[int | None]      = mapped_column(Integer,  nullable = True)
