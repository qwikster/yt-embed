from pathlib import Path
import re
import subprocess

from fastapi import HTTPException, status
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio.session import AsyncSession

from yt_embed.db import is_expired
from yt_embed.models import Item
from yt_embed.config import get_config

config = get_config()

async def fetch(id: str, db: AsyncSession, get_video: bool = False) -> Item:
    print("WANT FETCH")
    item = await db.get(Item, id)
    if item and not await is_expired(item, db):
        video = get_video and item.video_path
        audio = not get_video and item.audio_path
        if video or audio:
            return item

    print("FETCH READY")
    if get_video:
        return await dl_video(id, db)
    return await dl_audio(id, db)

async def id_safe(id: str) -> bool:
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', id):
        return False
    return True

async def dl_video(id: str, db: AsyncSession) -> Item:
    if not await id_safe(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid YouTube ID")

    command = [
        f"{config.ytdlp}",
        f"-t {config.video_format}",
        f"-- https://youtube.com/watch?v={id}"
    ]

    subprocess.run(command, capture_output = True, text = True)

    item = Item(

    )

    db.add(item)
    await db.commit()
    return item

async def dl_audio(id: str, db: AsyncSession) -> Item:
    print("DOWNLOAD TIME")

    if not await id_safe(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid YouTube ID")

    command = [
        config.ytdlp,
        "-x",
        "--audio-format", config.audio_format,
        "--audio-quality", "0",
        "--no-playlist",
        "--retries", str(config.retries),
        # "--print", "%(title)s",
        # "--print", "%(duration)s",
        "-o", f"{config.cache_dir}/{id}.{config.audio_format}",
    ]

    if config.filesize != "0":
        command += ["-S", f"filesize:{config.filesize}"]
    if config.rate_limit:
        command += ["--rate-limit", config.rate_limit]
    if config.cookies_path:
        command += ["--cookies", config.cookies_path]
    command += ["--", f"https://youtube.com/watch?v={id}"]

    print("GETTING AUDIO")
    with subprocess.Popen(
        command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, text = True, bufsize = 1
    ) as process:
        for line in process.stdout:
            print(line, end="", flush=True)

    item = Item(
        id = id,
        cached_at = datetime.now(timezone.utc),
        audio_path = f"{config.cache_dir}/{id}.{config.audio_format}"
    )

    db.add(item)
    await db.commit()
    return item
