import re
import subprocess

from sqlalchemy.ext.asyncio.session import AsyncSession

from yt_embed.db import is_expired
from yt_embed.models import Item
from yt_embed.config import get_config

config = get_config()

async def fetch(id: str, db: AsyncSession, get_video: bool = False) -> Item:
    item = await db.get(Item, id)
    if item and not await is_expired(item, db):
        video = get_video and item.video_path
        audio = not get_video and item.audio_path
        if video or audio:
            return item

    if get_video:
        return await dl_video(id, db)
    return await dl_audio(id, db)

async def id_safe(id: str) -> bool:
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', id):
        return False
    return True

async def dl_video(id: str, db: AsyncSession) -> Item:
    item = Item(

    )

    db.add(item)
    await db.commit(item)
    return item

async def dl_audio(id: str, db: AsyncSession) -> Item:
    item = Item(

    )

    db.add(item)
    await db.commit(item)
    return item
