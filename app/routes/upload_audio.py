from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
import os
from uuid import uuid4
from app.core.qc_engine import analyze_audio_quality

router = APIRouter()


@router.post("/upload/audio/", response_class=HTMLResponse)
async def upload_audio(request: Request, audio: UploadFile = File(...)):
    # Generate secure filename
    file_ext = os.path.splitext(audio.filename)[-1].lower()
    filename = f"{uuid4().hex}{file_ext}"
    file_path = os.path.join("uploads", filename)

    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await audio.read())

    # Run QC Analysis
    qc_result = analyze_audio_quality(file_path)

    # Pass result to UI template
    return request.app.state.templates.TemplateResponse("result.html", {
        "request": request,
        "qc_result": qc_result
    })
