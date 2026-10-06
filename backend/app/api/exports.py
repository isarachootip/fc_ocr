import urllib.parse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import vendor_service
from app.services.excel_export import export_vendor_to_excel
from app.services.pdf_export import generate_vendor_pdf

router = APIRouter(prefix="/vendors", tags=["Exports"])

@router.get("/{vendor_id}/export-excel")
def export_excel(vendor_id: int, db: Session = Depends(get_db)):
    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    excel_buffer = export_vendor_to_excel(vendor)
    filename = f"Vendor_{vendor.vendor_code}.xlsx"
    quoted_filename = urllib.parse.quote(filename)

    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=utf-8''{quoted_filename}"}
    )

@router.get("/{vendor_id}/export-pdf")
def export_pdf(vendor_id: int, db: Session = Depends(get_db)):
    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    pdf_buffer = generate_vendor_pdf(vendor)
    filename = f"Vendor_{vendor.vendor_code}.pdf"
    quoted_filename = urllib.parse.quote(filename)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename*=utf-8''{quoted_filename}"}
    )
