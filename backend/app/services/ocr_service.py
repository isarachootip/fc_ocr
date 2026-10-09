import logging
from pathlib import Path
from app.schemas.ocr import IdCardOcrResult
from app.services.ocr_gemini import scan_id_card_gemini
from app.services.ocr_local import scan_id_card_local

logger = logging.getLogger(__name__)

def process_id_card(file_path: Path, gemini_api_key: str = "") -> IdCardOcrResult:
    """
    Process ID card with Gemini Vision AI, falling back to Local OCR if unavailable.
    """
    if gemini_api_key:
        try:
            logger.info("Attempting OCR with Gemini Vision API...")
            return scan_id_card_gemini(file_path, gemini_api_key)
        except Exception as e:
            logger.warning(f"Gemini OCR failed: {e}. Falling back to Local OCR.")

    logger.info("Running Local OCR parser...")
    return scan_id_card_local(file_path)
