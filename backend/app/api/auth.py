from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from app.api.deps import SESSION_COOKIE, auth_configured, require_user
from app.config import settings
from app.services.auth_service import LoginThrottle, check_credentials, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])
throttle = LoginThrottle(max_failures=5, window_seconds=300)


class LoginRequest(BaseModel):
    username: str = Field(max_length=100)
    password: str = Field(max_length=200)


class UserResponse(BaseModel):
    username: str


def _client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@router.post("/login", response_model=UserResponse)
def login(body: LoginRequest, request: Request, response: Response):
    if not auth_configured():
        raise HTTPException(status_code=503, detail="Authentication is not configured on the server")
    key = _client_key(request)
    if throttle.is_blocked(key):
        raise HTTPException(status_code=429, detail="Too many failed attempts. Try again later.")
    if not check_credentials(body.username, body.password, settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD):
        throttle.record_failure(key)
        raise HTTPException(status_code=401, detail="Invalid username or password")

    throttle.reset(key)
    ttl = settings.SESSION_HOURS * 3600
    response.set_cookie(
        SESSION_COOKIE,
        create_token(body.username, settings.SESSION_SECRET, ttl),
        max_age=int(ttl),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return UserResponse(username=body.username)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE, path="/")
    return {"ok": True}


@router.get("/me", response_model=UserResponse)
def me(username: str = Depends(require_user)):
    return UserResponse(username=username)
