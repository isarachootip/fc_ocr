"""Gemini API key storage and resolution: DB (encrypted) first, then .env, else none."""
import logging
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.config import settings
from app.models.app_setting import AppSetting
from app.schemas.settings import GeminiStatus, KeySource
from app.services.secret_box import decrypt, encrypt

GEMINI_KEY = "gemini_api_key"
logger = logging.getLogger(__name__)


def _mask(key: str) -> str:
    return "••••" + key[-4:]


def _db_key(db: Session) -> Tuple[Optional[str], Optional[AppSetting]]:
    row = db.get(AppSetting, GEMINI_KEY)
    if row is None:
        return None, None
    plain = decrypt(row.value, settings.SESSION_SECRET)
    if plain is None:
        logger.warning("Stored Gemini key cannot be decrypted (SESSION_SECRET changed?); ignoring it")
    return plain, row


def _resolve(db: Session) -> Tuple[str, KeySource, Optional[AppSetting]]:
    plain, row = _db_key(db)
    if plain:
        return plain, "database", row
    if settings.GEMINI_API_KEY:
        return settings.GEMINI_API_KEY, "env", None
    return "", "none", None


def get_gemini_key(db: Session) -> str:
    """The key OCR should use, or "" for Local OCR."""
    return _resolve(db)[0]


def gemini_status(db: Session) -> GeminiStatus:
    key, source, row = _resolve(db)
    return GeminiStatus(
        configured=bool(key),
        source=source,
        engine="AI_GEMINI" if key else "LOCAL_OCR",
        masked=_mask(key) if key else None,
        updated_by=row.updated_by if row else None,
        updated_at=row.updated_at if row else None,
    )


def set_gemini_key(db: Session, api_key: str, updated_by: str) -> None:
    token = encrypt(api_key.strip(), settings.SESSION_SECRET)
    row = db.get(AppSetting, GEMINI_KEY)
    if row is None:
        db.add(AppSetting(key=GEMINI_KEY, value=token, updated_by=updated_by))
    else:
        row.value, row.updated_by = token, updated_by
    db.commit()


def clear_gemini_key(db: Session) -> None:
    db.query(AppSetting).filter_by(key=GEMINI_KEY).delete()
    db.commit()
