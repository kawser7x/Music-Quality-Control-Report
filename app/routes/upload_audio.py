# app/routes/upload_audio.py

from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.core.qc_engine import analyze_audio
from app.core.copyright_checker import check_copyright
import os
import shutil

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/upload-audio/", response_class=JSONResponse)
async def upload_audio(request: Request, file: UploadFile):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, file.filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    qc_result, plot_path = analyze_audio(temp_path)
    copyright_result = check_copyright(temp_path)

    result_combined = qc_result + "\n\n" + copyright_result

    # Optional: remove temp file after processing
    os.remove(temp_path)

    return {
        "result": result_combined,
        "plot_image": f"/static/plots/{os.path.basename(plot_path)}" if plot_path else None
    }

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
