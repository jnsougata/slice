import random
import fastapi
from asyncdeta import Deta, Field
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response


app = fastapi.FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
deta = Deta("c0pid2se_XRCwFqcrCXTEXJZpoyt45yMHvhkDfVFQ")

pages = Jinja2Templates(directory="pages")


@app.get("/", response_class=HTMLResponse)
async def home(request: fastapi.Request):
    return pages.TemplateResponse("index.html", {"request": request})


@app.get("/shrink")
async def shrink(url: str = fastapi.Query(None)):
    await deta.connect()
    base = deta.base("DB")
    key = random.randbytes(4).hex()
    await base.put(key=key, field=Field(name="redirect", value=url))
    return fastapi.responses.PlainTextResponse(f'https://bite.deta.dev/{key}', status_code=200)


@app.get("/{redirect_id}")
async def redirect(redirect_id: str):
    await deta.connect()
    base = deta.base("DB")
    redirect_payload = await base.fetch(key=redirect_id)
    if redirect_payload:
        return fastapi.responses.RedirectResponse(redirect_payload["redirect"])
    else:
        return fastapi.responses.JSONResponse({"error": "url does not exist"}, status_code=404)
