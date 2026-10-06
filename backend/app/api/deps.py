from typing import Optional
from fastapi import HTTPException, Request
from app.config import settings
from app.services.auth_service import verify_token

SESSION_COOKIE = "session"
MIN_SECRET_LENGTH = 32


def auth_configured() -> bool:
    return bool(settings.ADMIN_PASSWORD) and len(settings.SESSION_SECRET) >= MIN_SECRET_LENGTH


def current_user(request: Request) -> Optional[str]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token or not auth_configured():
        return None
    username = verify_token(token, settings.SESSION_SECRET)
    if username is None or username != settings.ADMIN_USERNAME:
        return None
    return username


def require_user(request: Request) -> str:
    """FastAPI dependency: 401 unless a valid session cookie is present."""
    username = current_user(request)
    if username is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username
