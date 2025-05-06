from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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


# To run, use:
#    uvicorn main:app --reload
