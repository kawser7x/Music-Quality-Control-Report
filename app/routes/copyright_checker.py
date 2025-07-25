from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.core.copyright_checker import run_copyright_checks

router = APIRouter()

@router.post("/check/copyright/")
async def check_copyright(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run copyright checks
    result = run_copyright_checks(file_path)

    # Remove temp file
    os.remove(file_path)

    return result
