from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import FileResponse, Response, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# == redirects ==

@router.get("/")
async def root(request: Request, v: str | None = None) -> Response:
    if v:
        return RedirectResponse(f"/{v}")
    return FileResponse("static/index.html", media_type="text/html")

@router.get("/watch")
async def watch_catch(request: Request, v: str) -> RedirectResponse:
    return RedirectResponse(f"/{v}")

@router.get("/watch/{id}")
async def watch_catch_byid(request: Request, id: str) -> RedirectResponse:
    return RedirectResponse(f"/{id}")

@router.get("/v/watch")
async def watch_catch_v_byid(request: Request, v: str) -> RedirectResponse:
    return RedirectResponse(f"/v/{v}")

@router.get("/v/watch/{id}")
async def watch_catch_v(request: Request, id: str) -> RedirectResponse:
    return RedirectResponse(f"/v/{id}")

# == content ==

@router.get("/v/{id}")
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

@router.get("/{id}")
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
              <meta property="og:image" content="https://img.youtube.com/vi/{id}/0.jpg">
            </head></html>
            """
        )
    else:
        return templates.TemplateResponse(request, "audio.html", {"id": id})

@router.get("/video/{id}")
async def get_video(id: str) -> FileResponse:
    ...
    return FileResponse(..., media_type="video/mp4")

@router.get("/audio/{id}")
async def get_audio(id: str) -> FileResponse:
    ...
    return FileResponse(..., media_type="audio/mpeg")
