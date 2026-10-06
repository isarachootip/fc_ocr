from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

PROTECTED = [
    ("GET", "/api/vendors"),
    ("GET", "/api/vendors/1"),
    ("GET", "/api/vendors/1/export-excel"),
    ("GET", "/api/vendors/1/export-pdf"),
    ("POST", "/api/ocr/scan-id-card"),
    ("GET", "/uploads/anything.jpg"),
]


def login(client, password="s3cret-pass", username="t_admin"):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def test_health_is_public():
    assert TestClient(app).get("/health").status_code == 200


def test_protected_routes_require_login():
    client = TestClient(app)
    for method, path in PROTECTED:
        res = client.request(method, path)
        assert res.status_code == 401, f"{method} {path} -> {res.status_code}"


def test_login_success_sets_httponly_cookie_and_grants_access():
    client = TestClient(app)
    res = login(client)
    assert res.status_code == 200
    assert res.json()["username"] == "t_admin"
    assert "httponly" in res.headers["set-cookie"].lower()
    assert client.get("/api/auth/me").json()["username"] == "t_admin"
    assert client.get("/api/vendors").status_code == 200


def test_login_wrong_password_rejected():
    client = TestClient(app)
    assert login(client, password="nope").status_code == 401
    assert client.get("/api/auth/me").status_code == 401


def test_logout_clears_session():
    client = TestClient(app)
    login(client)
    assert client.post("/api/auth/logout").status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_forged_cookie_rejected():
    client = TestClient(app)
    client.cookies.set("session", "t_admin.9999999999.deadbeef")
    assert client.get("/api/vendors").status_code == 401


def test_short_session_secret_fails_closed(monkeypatch):
    monkeypatch.setattr(settings, "SESSION_SECRET", "short")
    assert login(TestClient(app)).status_code == 503


def test_login_throttled_after_repeated_failures():
    from app.api.auth import throttle
    throttle.reset("testclient")
    client = TestClient(app)
    for _ in range(5):
        assert login(client, password="bad").status_code == 401
    assert login(client, password="bad").status_code == 429
    assert login(client).status_code == 429  # even the right password is blocked
    throttle.reset("testclient")


def test_uploads_path_traversal_blocked():
    client = TestClient(app)
    login(client)
    assert client.get("/uploads/..%2F.env").status_code in (400, 404)
    assert client.get("/uploads/%2e%2e/.env").status_code in (400, 404)
