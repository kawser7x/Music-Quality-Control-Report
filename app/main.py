# app/main.py

from fastapi import FastAPI
from app.routes import upload
from app.routes import health  # health route আলাদা রাখা ভালো

app = FastAPI()

# Health check route (for Render)
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(upload.router)
app.include_router(health.router)
