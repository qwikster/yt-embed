from starlette.responses import HTMLResponse, RedirectResponse
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
async def root(request: Request, v: str | None = None) -> FileResponse | RedirectResponse:
    if v:
        return RedirectResponse(f"/{v}")
    return FileResponse("html/index.html", media_type="text/html")

@app.get("/v/{id}")
async def video(id: str, request: Request) -> FileResponse | HTMLResponse | RedirectResponse:
    agent = request.headers.get("user-agent", "").lower()

    if "discord" in agent:
        return RedirectResponse(f"/video/{id}")
    elif "slack" in agent:
        return HTMLResponse(
            """
            <html><head>
              <meta property="og:title" content="...">
              <meta property="og:type" content="music.song">
              <meta property="og:video" content="https://yt.qwik.top/video/{id}">
              <meta property="og:video:type" content="video/mp4">
            </head></html>
            """
        )
    else:
        return FileResponse(..., media_type="text/html")

@app.get("/{id}")
async def audio(id: str, request: Request) -> FileResponse | HTMLResponse | RedirectResponse:
    agent = request.headers.get("user-agent", "").lower()

    if "discord" in agent:
        return RedirectResponse(f"/audio/{id}")
    elif "slack" in agent:
        return HTMLResponse(
            """
            <html><head>
              <meta property="og:title" content="...">
              <meta property="og:type" content="music.song">
              <meta property="og:audio" content="https://yt.qwik.top/audio/{id}">
              <meta property="og:audio:type" content="audio/mpeg">
            </head></html>
            """
        )
    else:
        # generic? how to do templates
        return FileResponse(..., media_type="text/html")

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
