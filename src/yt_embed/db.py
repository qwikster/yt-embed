from typing import Annotated
from fastapi import Depends
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from yt_embed.config import get_config

config = get_config()
engine = create_async_engine(config.db_url, echo=True) # DEBUG: turn this off !!
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def init_engine(db_url: str):
    return create_async_engine(db_url, echo=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def is_expired(item, db) -> bool:
    diff = datetime.now(timezone.utc) - item.cached_at.replace(tzinfo=timezone.utc)
    if diff.total_seconds() / 3600 >= config.expiry_time:
        db.delete(item)
        await db.commit()
        return True
    return False

DBDep = Annotated[AsyncSession, Depends(get_db)]
