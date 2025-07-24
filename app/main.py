# FastAPI app entrypoint
from fastapi import FastAPI
from app.routes import upload

app = FastAPI()

# ✅ Add health check endpoint for Render
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

app.include_router(upload.router)
