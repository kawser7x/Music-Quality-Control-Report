# app/routes/upload_audio.py

from fastapi import APIRouter, UploadFile, Request, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.qc_engine import analyze_audio_quality
from app.core.copyright_checker import check_copyright
from app.utils.waveform_plotter import generate_waveform_plot
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

    # QC analysis
    qc_result = analyze_audio_quality(temp_path)

    # Copyright check
    copyright_result = check_copyright(temp_path)

    # Waveform plot
    waveform_img_path = generate_waveform_plot(temp_path)

    # Final result merge
    final_result = qc_result + "\n\n" + copyright_result

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": final_result,
        "waveform_img": waveform_img_path
    })
