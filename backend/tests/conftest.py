import pytest
from app.config import settings


@pytest.fixture(autouse=True)
def auth_settings(monkeypatch):
    """Deterministic auth configuration for every test."""
    monkeypatch.setattr(settings, "ADMIN_USERNAME", "admin")
    monkeypatch.setattr(settings, "ADMIN_PASSWORD", "s3cret-pass")
    monkeypatch.setattr(settings, "SESSION_SECRET", "x" * 40)
    monkeypatch.setattr(settings, "SESSION_HOURS", 8)
    monkeypatch.setattr(settings, "COOKIE_SECURE", False)
