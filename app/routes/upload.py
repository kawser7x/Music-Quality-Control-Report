# app/routes/upload_audio.py

from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core import qc_engine  # QC logic
import os
import shutil

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_audio(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run QC check using qc_engine.py
    qc_result, waveform_image = qc_engine.run_qc(file_path)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": qc_result,
        "waveform_plot": waveform_image,
        "show_result": True
    })