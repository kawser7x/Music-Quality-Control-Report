from fastapi import FastAPI
from app.routes.upload_audio import router as upload_router
from app.routes.pdf_generator import router as pdf_router
from app.routes.copyright_checker import router as copyright_router

app = FastAPI()

# Include all routers
app.include_router(upload_router)
app.include_router(pdf_router)
app.include_router(copyright_router)

# Health check endpoint for Render deploy
@app.get("/healthz")
def health_check():
    return {"status": "ok"}
