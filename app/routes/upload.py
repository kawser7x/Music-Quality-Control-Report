# app/routes/upload_audio.py

from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.qc_engine import analyze_audio
from app.core.copyright_checker import run_copyright_checks
import os
import shutil

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/upload-audio/", response_class=HTMLResponse)
async def upload_audio(request: Request, file: UploadFile = File(...)):
    temp_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run QC Analysis
    qc_report, waveform_plot_path = analyze_audio(temp_path)

    # Run Copyright Checks
    copyright_result = run_copyright_checks(temp_path)

    os.remove(temp_path)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "qc_report": qc_report,
        "waveform_plot_path": f"/{waveform_plot_path}",
        "copyright_data": copyright_result
    })