from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.api.deps import SESSION_COOKIE, auth_configured, require_user
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.services import user_service
from app.services.auth_service import LoginThrottle, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])
throttle = LoginThrottle(max_failures=5, window_seconds=300)


class LoginRequest(BaseModel):
    username: str = Field(max_length=100)
    password: str = Field(max_length=200)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(max_length=200)
    new_password: str = Field(max_length=200)


class SessionUser(BaseModel):
    username: str
    role: str


def _client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@router.post("/login", response_model=SessionUser)
def login(body: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    if not auth_configured():
        raise HTTPException(status_code=503, detail="Authentication is not configured on the server")
    key = _client_key(request)
    if throttle.is_blocked(key):
        raise HTTPException(status_code=429, detail="Too many failed attempts. Try again later.")
    user = user_service.authenticate(db, body.username, body.password)
    if user is None:
        throttle.record_failure(key)
        raise HTTPException(status_code=401, detail="Invalid username or password")

    throttle.reset(key)
    ttl = settings.SESSION_HOURS * 3600
    response.set_cookie(
        SESSION_COOKIE,
        create_token(user.username, settings.SESSION_SECRET, ttl),
        max_age=int(ttl),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return SessionUser(username=user.username, role=user.role)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE, path="/")
    return {"ok": True}


@router.get("/me", response_model=SessionUser)
def me(user: User = Depends(require_user)):
    return SessionUser(username=user.username, role=user.role)


@router.post("/change-password")
def change_password(
    body: ChangePasswordRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    try:
        user_service.change_own_password(db, user, body.current_password, body.new_password)
    except user_service.UserError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}
