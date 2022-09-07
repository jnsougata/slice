"""
ABC
"""

import os
import secrets
import string
from pydantic import BaseModel
from micro import Micro
from micro.responses import *
from micro.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


pages = Jinja2Templates(directory="pages")


class ShrinkRequest(BaseModel):
    target: str


micro = Micro()
micro.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
micro.mount('/static', StaticFiles(directory='static'), name='static')


@micro.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return pages.TemplateResponse("index.html", {"request": request})


@micro.get("/ping", response_class=JSONResponse)
async def ping(request: Request):
    return JSONResponse({"message": "pong"})


@micro.post("/shrink")
async def shrink(shrink_request: ShrinkRequest, request: Request):
    target = shrink_request.target
    if not target:
        return RedirectResponse("/")
    if not micro.deta:
        return PlainTextResponse("/")
    key = secrets.token_urlsafe(5)
    micro.deta.Base("SHRINK").put(data={"url": target}, key=key)
    return {"url": f"{request.url.scheme}://{request.url.hostname}/{key}"}


@micro.get("/{redirect_id}")
async def redirect(redirect_id: str):
    resp = micro.deta.Base(name="SHRINK").get(str(redirect_id))
    if resp:
        return RedirectResponse(resp.get("url") or "/")
    return RedirectResponse("/")

app = micro.export
