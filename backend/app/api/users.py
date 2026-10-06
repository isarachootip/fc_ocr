from datetime import datetime
from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from app.api.deps import require_admin
from app.database import get_db
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(require_admin)])

Role = Literal["admin", "user"]


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


@router.get("", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.post("", response_model=UserOut, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, body.username, body.password, body.role)
    except user_service.UserError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, body: UserPatch, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(
            db, user_id, role=body.role, is_active=body.is_active, password=body.password
        )
    except user_service.UserError as e:
        status = 404 if str(e) == "User not found" else 400
        raise HTTPException(status_code=status, detail=str(e))
