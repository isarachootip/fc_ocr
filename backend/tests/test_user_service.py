import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app.models.user import User  # noqa: F401  (register model)
from app.services import user_service as svc
from app.services.password_service import verify_password


@pytest.fixture()
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine, tables=[User.__table__])
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


def test_create_and_authenticate(db):
    svc.create_user(db, "alice", "password-123", "user")
    assert svc.authenticate(db, "alice", "password-123").username == "alice"
    assert svc.authenticate(db, "alice", "nope") is None
    assert svc.authenticate(db, "ghost", "password-123") is None


def test_username_normalised_and_unique(db):
    svc.create_user(db, "Alice", "password-123", "user")
    with pytest.raises(svc.UserError):
        svc.create_user(db, "alice", "password-123", "user")


def test_invalid_input_rejected(db):
    with pytest.raises(svc.UserError):
        svc.create_user(db, "bob", "short", "user")
    with pytest.raises(svc.UserError):
        svc.create_user(db, "bad name!", "password-123", "user")
    with pytest.raises(svc.UserError):
        svc.create_user(db, "bob", "password-123", "superuser")


def test_disabled_user_cannot_authenticate(db):
    u = svc.create_user(db, "carol", "password-123", "user")
    svc.update_user(db, u.id, is_active=False)
    assert svc.authenticate(db, "carol", "password-123") is None


def test_reset_password(db):
    u = svc.create_user(db, "dave", "password-123", "user")
    svc.update_user(db, u.id, password="new-password-9")
    assert svc.authenticate(db, "dave", "password-123") is None
    assert svc.authenticate(db, "dave", "new-password-9") is not None


def test_cannot_remove_last_admin(db):
    a = svc.create_user(db, "root", "password-123", "admin")
    with pytest.raises(svc.UserError):
        svc.update_user(db, a.id, is_active=False)
    with pytest.raises(svc.UserError):
        svc.update_user(db, a.id, role="user")
    b = svc.create_user(db, "root2", "password-123", "admin")
    svc.update_user(db, a.id, role="user")  # allowed: another admin remains
    with pytest.raises(svc.UserError):
        svc.update_user(db, b.id, is_active=False)


def test_change_own_password(db):
    u = svc.create_user(db, "erin", "password-123", "user")
    with pytest.raises(svc.UserError):
        svc.change_own_password(db, u, "wrong-current", "new-password-9")
    svc.change_own_password(db, u, "password-123", "new-password-9")
    assert verify_password("new-password-9", u.password_hash)


def test_seed_first_admin_only_when_empty(db):
    assert svc.seed_first_admin(db, "admin", "seed-password-1") is True
    assert svc.authenticate(db, "admin", "seed-password-1").role == "admin"
    assert svc.seed_first_admin(db, "other", "seed-password-2") is False
    assert svc.seed_first_admin(db, "x", "") is False  # no password configured


def test_seed_skipped_without_password(db):
    assert svc.seed_first_admin(db, "admin", "") is False
    assert svc.list_users(db) == []
