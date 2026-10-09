from datetime import datetime
from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from app.api.deps import require_admin
from app.database import get_db
from app.models.user import User
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(require_admin)])

Role = Literal["admin", "user", "sysadmin"]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    role: str
    is_active: bool
    created_at: datetime


class UserCreate(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=200)
    role: Role = "user"


class UserPatch(BaseModel):
    role: Optional[Role] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, max_length=200)


def _http_error(e: user_service.UserError) -> HTTPException:
    if isinstance(e, user_service.UserPermissionError):
        return HTTPException(status_code=403, detail=str(e))
    status = 404 if str(e) == "User not found" else 400
    return HTTPException(status_code=status, detail=str(e))


@router.get("", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.post("", response_model=UserOut, status_code=201)
def create_user(body: UserCreate, actor: User = Depends(require_admin), db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, body.username, body.password, body.role, actor_role=actor.role)
    except user_service.UserError as e:
        raise _http_error(e)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int, body: UserPatch, actor: User = Depends(require_admin), db: Session = Depends(get_db)
):
    try:
        return user_service.update_user(
            db, user_id, role=body.role, is_active=body.is_active, password=body.password,
            actor_role=actor.role,
        )
    except user_service.UserError as e:
        raise _http_error(e)
