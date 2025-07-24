# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import upload_audio

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Health check route
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# Upload and UI route
app.include_router(upload_audio.router)