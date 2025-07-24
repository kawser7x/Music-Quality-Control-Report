# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import upload_audio, pdf_generator, copyright_checker

app = FastAPI()

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(upload_audio.router)
app.include_router(pdf_generator.router)
app.include_router(copyright_checker.router)

# Health check endpoint for Render deployment
@app.get("/healthz")
def health_check():
    return {"status": "ok"}