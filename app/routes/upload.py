from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def homepage():
    return "<h1>Music QC System</h1>"

@router.post("/upload/audio/")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename}
