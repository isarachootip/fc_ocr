import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.schemas.ocr import IdCardOcrResult
from app.services import settings_service
from app.services.ocr_service import process_id_card

router = APIRouter(prefix="/ocr", tags=["OCR"])

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

@router.post("/scan-id-card", response_model=IdCardOcrResult)
async def scan_id_card(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type {ext}. Supported: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Save uploaded file
    file_id = f"{uuid.uuid4().hex[:10]}_{file.filename}"
    saved_path = settings.UPLOAD_DIR / file_id
    
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = process_id_card(saved_path, settings_service.get_gemini_key(db))
        result.file_path = f"/uploads/{file_id}"
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR error: {str(e)}")
