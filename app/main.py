# app/main.py

from fastapi import FastAPI
from app.routes import upload

app = FastAPI()

# Health check endpoint for Render.com
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# Include the upload route (for showing the homepage)
app.include_router(upload.router)