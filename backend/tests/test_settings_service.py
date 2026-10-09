import pytest
from app.config import settings
from app.database import SessionLocal
from app.models.app_setting import AppSetting
from app.services import settings_service

KEY = "AIzaSyTEST-key-0000000000wxyz"
pytestmark = pytest.mark.usefixtures("preserve_gemini_setting")


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_no_key_means_local_ocr(db):
    status = settings_service.gemini_status(db)
    assert settings_service.get_gemini_key(db) == ""
    assert (status.configured, status.source, status.engine, status.masked) == (False, "none", "LOCAL_OCR", None)


def test_env_key_is_fallback(db, monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "env-key-abcd")
    status = settings_service.gemini_status(db)
    assert settings_service.get_gemini_key(db) == "env-key-abcd"
    assert (status.source, status.engine, status.masked) == ("env", "AI_GEMINI", "••••abcd")


def test_db_key_overrides_env_and_is_encrypted(db, monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "env-key-abcd")
    settings_service.set_gemini_key(db, KEY, "t_sysadmin")
    assert settings_service.get_gemini_key(db) == KEY
    row = db.get(AppSetting, settings_service.GEMINI_KEY)
    assert KEY not in row.value
    status = settings_service.gemini_status(db)
    assert (status.source, status.masked, status.updated_by) == ("database", "••••wxyz", "t_sysadmin")


def test_set_strips_whitespace(db):
    settings_service.set_gemini_key(db, f"  {KEY}\n", "t_sysadmin")
    assert settings_service.get_gemini_key(db) == KEY


def test_clear_falls_back(db):
    settings_service.set_gemini_key(db, KEY, "t_sysadmin")
    settings_service.clear_gemini_key(db)
    assert settings_service.gemini_status(db).source == "none"


def test_changed_session_secret_treated_as_missing(db, monkeypatch):
    settings_service.set_gemini_key(db, KEY, "t_sysadmin")
    monkeypatch.setattr(settings, "SESSION_SECRET", "y" * 40)
    assert settings_service.get_gemini_key(db) == ""
    assert settings_service.gemini_status(db).engine == "LOCAL_OCR"
