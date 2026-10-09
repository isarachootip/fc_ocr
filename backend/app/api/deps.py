from typing import Optional
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.services import user_service
from app.services.auth_service import verify_token

SESSION_COOKIE = "session"
MIN_SECRET_LENGTH = 32


def auth_configured() -> bool:
    return len(settings.SESSION_SECRET) >= MIN_SECRET_LENGTH


def current_user(request: Request, db: Session) -> Optional[User]:
    """Resolve the session cookie to an active user, checked against the DB on every request
    so that disabling a user or changing a role takes effect immediately."""
    token = request.cookies.get(SESSION_COOKIE)
    if not token or not auth_configured():
        return None
    username = verify_token(token, settings.SESSION_SECRET)
    if username is None:
        return None
    user = user_service.get_by_username(db, username)
    if user is None or not user.is_active:
        return None
    return user


def require_user(request: Request, db: Session = Depends(get_db)) -> User:
    """FastAPI dependency: 401 unless a valid session cookie of an active user is present."""
    user = current_user(request, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def require_admin(user: User = Depends(require_user)) -> User:
    if user.role not in user_service.ADMIN_ROLES:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def require_sysadmin(user: User = Depends(require_user)) -> User:
    if user.role != "sysadmin":
        raise HTTPException(status_code=403, detail="Sysadmin access required")
    return user
