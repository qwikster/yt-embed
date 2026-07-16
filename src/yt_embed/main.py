from fastapi import FastAPI
import uvicorn

from pathlib import Path
from importlib.metadata import version
from fastapi.staticfiles import StaticFiles
from yt_embed.config import get_config
from yt_embed.routes import router

app = FastAPI(
    title = "yt-embed",
    description = "",
    version = version("yt_embed"),
)

app.mount("/static", StaticFiles(directory=Path("static").resolve()), name="static")
app.include_router(router, prefix = "", tags = ["root", "yt_embed"])

def entry():
    config = get_config()
    uvicorn.run(
        app,
        host = config.host,
        port = config.port,
        log_level = "info"
    )

if __name__ == "__main__":
    entry()
