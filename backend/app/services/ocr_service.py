import logging
from pathlib import Path
from app.config import settings
from app.schemas.ocr import IdCardOcrResult
from app.services.ocr_gemini import scan_id_card_gemini
from app.services.ocr_local import scan_id_card_local

logger = logging.getLogger(__name__)

def process_id_card(file_path: Path) -> IdCardOcrResult:
    """
    Process ID card with Gemini Vision AI, falling back to Local OCR if unavailable.
    """
    if settings.GEMINI_API_KEY:
        try:
            logger.info("Attempting OCR with Gemini Vision API...")
            return scan_id_card_gemini(file_path)
        except Exception as e:
            logger.warning(f"Gemini OCR failed: {e}. Falling back to Local OCR.")

    logger.info("Running Local OCR parser...")
    return scan_id_card_local(file_path)
