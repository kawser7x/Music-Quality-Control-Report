# app/routes/pdf_generator.py

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from fpdf import FPDF
import io

router = APIRouter()

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "TrackVerify - Music QC Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "TrackVerify OFFSTEP v2.2", align="C")

@router.post("/generate-pdf/")
async def generate_pdf(request: Request):
    data = await request.json()
    report_text = data.get("report", "No report data found.")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in report_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=qc_report.pdf"
    })