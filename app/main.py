from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routes.upload_audio import router as upload_router
from app.routes.pdf_generator import router as pdf_router
from app.routes.copyright_checker import router as copyright_router

app = FastAPI()

# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include all API routers
app.include_router(upload_router)
app.include_router(pdf_router)
app.include_router(copyright_router)

# Serve the index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check for Render
@app.get("/healthz")
def health_check():
    return {"status": "ok"}
