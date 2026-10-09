import pytest
from sqlalchemy import delete
from app.config import settings
from app.database import SessionLocal
from app.models.app_setting import AppSetting
from app.models.user import User
from app.services import settings_service, user_service

TEST_PREFIX = "t_"
ADMIN = ("t_admin", "s3cret-pass")
USER = ("t_user", "user-pass-123")
SYSADMIN = ("t_sysadmin", "sys-pass-1234")


@pytest.fixture
def preserve_gemini_setting(monkeypatch):
    """Snapshot the real Gemini key row and restore it afterwards; blank the .env fallback."""
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    db = SessionLocal()
    try:
        row = db.get(AppSetting, settings_service.GEMINI_KEY)
        saved = (row.value, row.updated_by) if row else None
        db.query(AppSetting).filter_by(key=settings_service.GEMINI_KEY).delete()
        db.commit()
        yield
        db.query(AppSetting).filter_by(key=settings_service.GEMINI_KEY).delete()
        if saved:
            db.add(AppSetting(key=settings_service.GEMINI_KEY, value=saved[0], updated_by=saved[1]))
        db.commit()
    finally:
        db.close()


@pytest.fixture(autouse=True)
def auth_settings(monkeypatch):
    """Deterministic session configuration for every test."""
    monkeypatch.setattr(settings, "SESSION_SECRET", "x" * 40)
    monkeypatch.setattr(settings, "SESSION_HOURS", 8)
    monkeypatch.setattr(settings, "COOKIE_SECURE", False)


@pytest.fixture(autouse=True)
def test_users():
    """(Re)create t_admin / t_user / t_sysadmin. Only rows with the t_ prefix are ever deleted."""
    db = SessionLocal()
    try:
        db.execute(delete(User).where(User.username.like(f"{TEST_PREFIX}%")))
        db.commit()
        user_service.create_user(db, ADMIN[0], ADMIN[1], "admin")
        user_service.create_user(db, USER[0], USER[1], "user")
        user_service.create_user(db, SYSADMIN[0], SYSADMIN[1], "sysadmin")
        yield
        db.execute(delete(User).where(User.username.like(f"{TEST_PREFIX}%")))
        db.commit()
    finally:
        db.close()
