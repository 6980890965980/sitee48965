from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import asyncio 

SERVICE_URL = "https://n3xus.onrender.com/"

app = FastAPI()

# mount the static folder at /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2Templates will look in ./templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Renders landing.html (the N3XUS hero page).
    """
    return templates.TemplateResponse("landing.html", {"request": request})


@app.get("/commands", response_class=HTMLResponse)
async def commands(request: Request):
    """
    Renders commands.html (the Commands grid page).
    """
    return templates.TemplateResponse("commands.html", {"request": request})


@app.get("/ping")
async def ping():
    return {"status": "alive"}


@app.on_event("startup")
async def schedule_ping_task():
    async def ping_loop():
        async with httpx.AsyncClient(timeout=5.0) as client:
            while True:
                try:
                    r = await client.get(f"{SERVICE_URL}/ping")
                    if r.status_code != 200:
                        print(f"[Ping] returned {r.status_code}")
                except Exception as e:
                    print(f"[PingError] {e!r}")
                await asyncio.sleep(10)
    asyncio.create_task(ping_loop())
