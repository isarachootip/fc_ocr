from fastapi.testclient import TestClient
from app.main import app


def login_as(username, password):
    client = TestClient(app)
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200, res.text
    return client


def admin_client():
    return login_as("t_admin", "s3cret-pass")


def user_client():
    return login_as("t_user", "user-pass-123")


def test_users_endpoints_require_login():
    client = TestClient(app)
    assert client.get("/api/users").status_code == 401
    assert client.post("/api/users", json={}).status_code == 401


def test_regular_user_forbidden_from_user_management():
    client = user_client()
    assert client.get("/api/users").status_code == 403
    body = {"username": "t_x", "password": "password-123", "role": "user"}
    assert client.post("/api/users", json=body).status_code == 403
    assert client.patch("/api/users/1", json={"is_active": False}).status_code == 403


def test_me_includes_role():
    assert admin_client().get("/api/auth/me").json() == {"username": "t_admin", "role": "admin"}
    assert user_client().get("/api/auth/me").json()["role"] == "user"


def test_admin_lists_users_without_password_hashes():
    res = admin_client().get("/api/users")
    assert res.status_code == 200
    names = {u["username"] for u in res.json()}
    assert {"t_admin", "t_user"} <= names
    assert "password_hash" not in res.text


def test_admin_creates_user_who_can_log_in():
    admin = admin_client()
    res = admin.post("/api/users", json={"username": "T_New", "password": "password-123", "role": "user"})
    assert res.status_code == 201, res.text
    assert res.json()["username"] == "t_new"
    assert login_as("t_new", "password-123").get("/api/auth/me").json()["role"] == "user"


def test_create_user_validation_errors():
    admin = admin_client()
    dup = admin.post("/api/users", json={"username": "t_user", "password": "password-123", "role": "user"})
    assert dup.status_code == 400
    weak = admin.post("/api/users", json={"username": "t_weak", "password": "short", "role": "user"})
    assert weak.status_code == 400
    bad_role = admin.post("/api/users", json={"username": "t_r", "password": "password-123", "role": "root"})
    assert bad_role.status_code in (400, 422)


def test_disabling_user_kills_existing_session():
    victim = user_client()
    assert victim.get("/api/vendors").status_code == 200
    uid = next(u["id"] for u in admin_client().get("/api/users").json() if u["username"] == "t_user")
    assert admin_client().patch(f"/api/users/{uid}", json={"is_active": False}).status_code == 200
    assert victim.get("/api/vendors").status_code == 401
    res = TestClient(app).post("/api/auth/login", json={"username": "t_user", "password": "user-pass-123"})
    assert res.status_code == 401


def test_admin_resets_password():
    admin = admin_client()
    uid = next(u["id"] for u in admin.get("/api/users").json() if u["username"] == "t_user")
    assert admin.patch(f"/api/users/{uid}", json={"password": "brand-new-pass-1"}).status_code == 200
    assert TestClient(app).post(
        "/api/auth/login", json={"username": "t_user", "password": "user-pass-123"}
    ).status_code == 401
    login_as("t_user", "brand-new-pass-1")


def test_update_unknown_user_404():
    assert admin_client().patch("/api/users/999999", json={"is_active": False}).status_code == 404


def test_change_own_password():
    client = user_client()
    bad = client.post("/api/auth/change-password", json={"current_password": "wrong", "new_password": "another-pass-1"})
    assert bad.status_code == 400
    ok = client.post("/api/auth/change-password", json={"current_password": "user-pass-123", "new_password": "another-pass-1"})
    assert ok.status_code == 200
    login_as("t_user", "another-pass-1")


def test_vendor_records_creator():
    client = user_client()
    payload = {"vendor_name_th": "ร้านทดสอบ", "tax_id": "1234567890123"}
    res = client.post("/api/vendors", json=payload)
    assert res.status_code == 201, res.text
    assert res.json()["created_by"] == "t_user"
    vid = res.json()["id"]
    assert client.get(f"/api/vendors/{vid}").json()["created_by"] == "t_user"
    client.delete(f"/api/vendors/{vid}")
