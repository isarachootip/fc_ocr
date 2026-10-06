import pytest
from sqlalchemy import delete
from app.config import settings
from app.database import SessionLocal
from app.models.user import User
from app.services import user_service

TEST_PREFIX = "t_"
ADMIN = ("t_admin", "s3cret-pass")
USER = ("t_user", "user-pass-123")


@pytest.fixture(autouse=True)
def auth_settings(monkeypatch):
    """Deterministic session configuration for every test."""
    monkeypatch.setattr(settings, "SESSION_SECRET", "x" * 40)
    monkeypatch.setattr(settings, "SESSION_HOURS", 8)
    monkeypatch.setattr(settings, "COOKIE_SECURE", False)


@pytest.fixture(autouse=True)
def test_users():
    """(Re)create t_admin / t_user. Only rows with the t_ prefix are ever deleted."""
    db = SessionLocal()
    try:
        db.execute(delete(User).where(User.username.like(f"{TEST_PREFIX}%")))
        db.commit()
        user_service.create_user(db, ADMIN[0], ADMIN[1], "admin")
        user_service.create_user(db, USER[0], USER[1], "user")
        yield
        db.execute(delete(User).where(User.username.like(f"{TEST_PREFIX}%")))
        db.commit()
    finally:
        db.close()
