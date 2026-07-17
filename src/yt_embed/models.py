from datetime import datetime
from sqlalchemy import String, Boolean, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from yt_embed.db import Base

class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String(11), primary_key = True)
    title: Mapped[str | None] = mapped_column(String, nullable = True)

class Audio(Base):
    __tablename__ = "songs"

    id: Mapped[str] = mapped_column(String(11), primary_key = True)
