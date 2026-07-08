from starlette.responses import HTMLResponse
import uvicorn

from fastapi import FastAPI, Request
from importlib.metadata import version
from fastapi.responses import FileResponse

def get_config():
    return ...

app = FastAPI(
    title = "yt-embed",
    description = "",
    version = version("yt_embed"),
)

@app.get("/")
async def root() -> FileResponse:
    return FileResponse("html/index.html", media_type="text/html")

@app.get("/v/{id}")
async def video(id: str, request: Request) -> FileResponse | HTMLResponse:
    agent = request.headers.get("user-agent", "").lower()

    if "discord" in agent:
        return FileResponse(..., media_type="video/mp4")
    elif "slack" in agent:
        return FileResponse(..., media_type="text/html")
    else:
        return HTMLResponse(...)

@app.get("/{id}")
async def audio(id: str, request: Request) -> FileResponse | HTMLResponse:
    agent = request.headers.get("user-agent", "").lower()

    if "discord" in agent:
        return FileResponse(..., media_type="audio/mpeg")
    elif "slack" in agent:
        return FileResponse(..., media_type="text/html")
    else:
        return HTMLResponse(...)

def entry():
    config = get_config()
    uvicorn.run(
        app,
        host = "0.0.0.0", # config.host,
        port = 12864, # config.port,
        log_level = "info"
    )

if __name__ == "__main__":
    entry()
