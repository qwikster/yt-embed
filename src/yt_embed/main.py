import uvicorn

from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager
from importlib.metadata import version
from fastapi.staticfiles import StaticFiles
from yt_embed.config import get_config
from yt_embed.routes import router
from yt_embed.db import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    lifespan = lifespan,
    title = "yt-embed",
    description = "",
    version = version("yt_embed"),
)

app.mount("/static", StaticFiles(directory=Path("static").resolve()), name="static")
app.include_router(router, prefix = "", tags = ["root", "yt_embed"])

def entry():
    uvicorn.run(
        app,
        host = get_config().host,
        port = get_config().port,
        log_level = "info"
    )

if __name__ == "__main__":
    entry()
