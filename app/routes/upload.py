# app/routes/upload_audio.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.core import qc_engine
import shutil
import os
import uuid

router = APIRouter()


@router.post("/upload/audio/")
async def upload_audio(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/x-wav", "audio/flac"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a WAV or FLAC file.")

    # Generate unique filename and save
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    temp_path = os.path.join("app", "temp", filename)

    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Run QC Analysis
        qc_result = qc_engine.analyze_audio(temp_path)

        # Delete temp file after analysis
        os.remove(temp_path)

        return JSONResponse(content={"qc_report": qc_result})
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")