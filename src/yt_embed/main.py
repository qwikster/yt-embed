from starlette.responses import HTMLResponse, RedirectResponse
import uvicorn

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
from importlib.metadata import version
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

def get_config():
    return ...

app = FastAPI(
    title = "yt-embed",
    description = "",
    version = version("yt_embed"),
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=Path("static").resolve()), name="static")

# == redirects ==

@app.get("/")
async def root(request: Request, v: str | None = None) -> Response:
    if v:
        return RedirectResponse(f"/{v}")
    return FileResponse("static/index.html", media_type="text/html")

@app.get("/watch")
async def watch_catch(request: Request, v: str) -> RedirectResponse:
    return RedirectResponse(f"/{v}")

@app.get("/watch/{id}")
async def watch_catch_byid(request: Request, id: str) -> RedirectResponse:
    return RedirectResponse(f"/{id}")

@app.get("/v/watch")
async def watch_catch_v_byid(request: Request, v: str) -> RedirectResponse:
    return RedirectResponse(f"/v/{v}")

@app.get("/v/watch/{id}")
async def watch_catch_v(request: Request, id: str) -> RedirectResponse:
    return RedirectResponse(f"/v/{id}")

# == content ==

@app.get("/v/{id}")
async def video(id: str, request: Request) -> Response:
    agent = request.headers.get("user-agent", "").lower()

    if "discord" in agent:
        return RedirectResponse(f"/video/{id}")
    elif "slack" in agent:
        return HTMLResponse(
            f"""
            <html><head>
              <meta property="og:title" content="...">
              <meta property="og:type" content="video.other">
              <meta property="og:video" content="https://yt.qwik.top/video/{id}">
              <meta property="og:video:type" content="video/mp4">
              <meta property="og:image" content="https://img.youtube.com/vi/{id}/0.jpg">
            </head></html>
            """
        )
    else:
        return templates.TemplateResponse(request, "video.html", {"id": id})

@app.get("/{id}")
async def audio(id: str, request: Request) -> Response:
    agent = request.headers.get("user-agent", "").lower()

    if "discord" in agent:
        return RedirectResponse(f"/audio/{id}")
    elif "slack" in agent:
        return HTMLResponse(
            f"""
            <html><head>
              <meta property="og:title" content="...">
              <meta property="og:type" content="music.song">
              <meta property="og:audio" content="https://yt.qwik.top/audio/{id}">
              <meta property="og:audio:type" content="audio/mpeg">
              <!-- <meta property="og:image" content="https://img.youtube.com/vi/{id}/0.jpg"> -->
            </head></html>
            """
        )
    else:
        return templates.TemplateResponse(request, "audio.html", {"id": id})

@app.get("/video/{id}")
async def get_video(id: str) -> FileResponse:
    ...
    return FileResponse(..., media_type="video/mp4")

@app.get("/audio/{id}")
async def get_audio(id: str) -> FileResponse:
    ...
    return FileResponse(..., media_type="audio/mpeg")

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
