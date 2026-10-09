from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import require_sysadmin
from app.database import get_db
from app.models.user import User
from app.schemas.settings import GeminiKeyUpdate, GeminiStatus
from app.services import settings_service

router = APIRouter(prefix="/settings", tags=["System Settings"], dependencies=[Depends(require_sysadmin)])


@router.get("/gemini", response_model=GeminiStatus)
def get_gemini(db: Session = Depends(get_db)):
    return settings_service.gemini_status(db)


@router.put("/gemini", response_model=GeminiStatus)
def put_gemini(body: GeminiKeyUpdate, actor: User = Depends(require_sysadmin), db: Session = Depends(get_db)):
    settings_service.set_gemini_key(db, body.api_key, actor.username)
    return settings_service.gemini_status(db)


@router.delete("/gemini", response_model=GeminiStatus)
def delete_gemini(db: Session = Depends(get_db)):
    settings_service.clear_gemini_key(db)
    return settings_service.gemini_status(db)
