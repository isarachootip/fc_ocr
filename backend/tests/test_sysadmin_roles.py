"""Role hierarchy: sysadmin > admin > user. Admins must not be able to touch sysadmin accounts."""
from fastapi.testclient import TestClient
from app.database import SessionLocal
from app.main import app
from app.models.user import User
from app.services import user_service

ADMIN, SYSADMIN = ("t_admin", "s3cret-pass"), ("t_sysadmin", "sys-pass-1234")


def login_as(creds):
    client = TestClient(app)
    res = client.post("/api/auth/login", json={"username": creds[0], "password": creds[1]})
    assert res.status_code == 200, res.text
    return client


def user_id(client, name):
    return next(u["id"] for u in client.get("/api/users").json() if u["username"] == name)


def test_sysadmin_can_manage_users():
    client = login_as(SYSADMIN)
    assert client.get("/api/users").status_code == 200
    body = {"username": "t_by_sys", "password": "password-123", "role": "admin"}
    assert client.post("/api/users", json=body).status_code == 201


def test_admin_cannot_modify_sysadmin_account():
    admin = login_as(ADMIN)
    sid = user_id(admin, SYSADMIN[0])
    for patch in ({"is_active": False}, {"password": "hijacked-pass-1"}, {"role": "user"}):
        assert admin.patch(f"/api/users/{sid}", json=patch).status_code == 403
    login_as(SYSADMIN)  # still works with the original password


def test_admin_cannot_grant_sysadmin_role():
    admin = login_as(ADMIN)
    body = {"username": "t_escalate", "password": "password-123", "role": "sysadmin"}
    assert admin.post("/api/users", json=body).status_code == 403
    assert admin.patch(f"/api/users/{user_id(admin, 't_user')}", json={"role": "sysadmin"}).status_code == 403
    assert admin.patch(f"/api/users/{user_id(admin, ADMIN[0])}", json={"role": "sysadmin"}).status_code == 403


def test_sysadmin_can_grant_sysadmin_role():
    client = login_as(SYSADMIN)
    res = client.patch(f"/api/users/{user_id(client, 't_user')}", json={"role": "sysadmin"})
    assert res.status_code == 200
    assert res.json()["role"] == "sysadmin"


def test_seed_sysadmin_creates_once_without_overwriting():
    db = SessionLocal()
    try:
        assert user_service.seed_sysadmin(db, "t_seeded", "") is False
        assert user_service.seed_sysadmin(db, "t_seeded", "seed-pass-123") is True
        assert user_service.get_by_username(db, "t_seeded").role == "sysadmin"
        assert user_service.seed_sysadmin(db, "t_seeded", "other-pass-456") is False
        assert user_service.authenticate(db, "t_seeded", "seed-pass-123") is not None
    finally:
        db.query(User).filter_by(username="t_seeded").delete()
        db.commit()
        db.close()
