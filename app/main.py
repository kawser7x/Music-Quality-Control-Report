# app/main.py

from fastapi import FastAPI
from app.routes import upload
from app.routes import health  # নতুন যুক্ত করো

app = FastAPI()

# Include both upload and health routers
app.include_router(upload.router)
app.include_router(health.router)  # নতুন যুক্ত করো
