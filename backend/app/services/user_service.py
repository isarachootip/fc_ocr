import re
from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.password_service import hash_password, password_problem, verify_password

ROLES = ("admin", "user")
_USERNAME_RE = re.compile(r"^[a-z0-9._-]{3,50}$")
# Used to keep login timing similar whether or not the username exists.
_DUMMY_HASH = hash_password("dummy-password-for-timing")


class UserError(ValueError):
    """Raised for invalid user operations; message is safe to show to the admin."""


def normalise_username(username: str) -> str:
    return username.strip().lower()


def get_by_username(db: Session, username: str) -> Optional[User]:
    return db.scalar(select(User).where(User.username == normalise_username(username)))


def list_users(db: Session) -> List[User]:
    return list(db.scalars(select(User).order_by(User.id)))


def _active_admin_count(db: Session) -> int:
    return db.scalar(
        select(func.count(User.id)).where(User.role == "admin", User.is_active.is_(True))
    ) or 0


def create_user(db: Session, username: str, password: str, role: str) -> User:
    name = normalise_username(username)
    if not _USERNAME_RE.match(name):
        raise UserError("Username must be 3-50 characters: letters, digits, '.', '_' or '-'")
    if role not in ROLES:
        raise UserError("Invalid role")
    problem = password_problem(password)
    if problem:
        raise UserError(problem)
    if get_by_username(db, name):
        raise UserError("Username already exists")
    user = User(username=name, password_hash=hash_password(password), role=role, is_active=True)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise UserError("Username already exists")
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> Optional[User]:
    user = get_by_username(db, username)
    if user is None:
        verify_password(password, _DUMMY_HASH)
        return None
    if not verify_password(password, user.password_hash) or not user.is_active:
        return None
    return user


def update_user(
    db: Session,
    user_id: int,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    password: Optional[str] = None,
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise UserError("User not found")
    if role is not None and role not in ROLES:
        raise UserError("Invalid role")

    new_role = user.role if role is None else role
    new_active = user.is_active if is_active is None else is_active
    loses_admin = user.role == "admin" and user.is_active and not (new_role == "admin" and new_active)
    if loses_admin and _active_admin_count(db) <= 1:
        raise UserError("Cannot remove or disable the last active admin")

    if password is not None:
        problem = password_problem(password)
        if problem:
            raise UserError(problem)
        user.password_hash = hash_password(password)
    user.role, user.is_active = new_role, new_active
    db.commit()
    db.refresh(user)
    return user


def change_own_password(db: Session, user: User, current: str, new: str) -> None:
    if not verify_password(current, user.password_hash):
        raise UserError("Current password is incorrect")
    problem = password_problem(new)
    if problem:
        raise UserError(problem)
    user.password_hash = hash_password(new)
    db.commit()


def seed_first_admin(db: Session, username: str, password: str) -> bool:
    """Create the first admin from configuration, only when no users exist yet."""
    if not password or db.scalar(select(func.count(User.id))):
        return False
    create_user(db, username, password, "admin")
    return True
