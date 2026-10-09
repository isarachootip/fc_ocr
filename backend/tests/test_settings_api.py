import pytest
from fastapi.testclient import TestClient
from app.main import app

ADMIN, USER, SYSADMIN = ("t_admin", "s3cret-pass"), ("t_user", "user-pass-123"), ("t_sysadmin", "sys-pass-1234")

URL = "/api/settings/gemini"
KEY = "AIzaSyTEST-key-0000000000wxyz"
pytestmark = pytest.mark.usefixtures("preserve_gemini_setting")


def login_as(creds):
    client = TestClient(app)
    res = client.post("/api/auth/login", json={"username": creds[0], "password": creds[1]})
    assert res.status_code == 200, res.text
    return client


def test_requires_login():
    client = TestClient(app)
    assert client.get(URL).status_code == 401
    assert client.put(URL, json={"api_key": KEY}).status_code == 401


@pytest.mark.parametrize("creds", [ADMIN, USER])
def test_non_sysadmin_forbidden(creds):
    client = login_as(creds)
    assert client.get(URL).status_code == 403
    assert client.put(URL, json={"api_key": KEY}).status_code == 403
    assert client.delete(URL).status_code == 403


def test_sysadmin_full_cycle_never_returns_full_key():
    client = login_as(SYSADMIN)
    assert client.get(URL).json()["engine"] == "LOCAL_OCR"

    res = client.put(URL, json={"api_key": KEY})
    assert res.status_code == 200, res.text
    body = res.json()
    assert (body["engine"], body["source"], body["masked"]) == ("AI_GEMINI", "database", "••••wxyz")
    assert KEY not in res.text
    assert KEY not in client.get(URL).text

    assert client.delete(URL).json()["engine"] == "LOCAL_OCR"


@pytest.mark.parametrize("bad", ["short", "has space in-the-middle-of-key", "x" * 201, ""])
def test_put_validates_key(bad):
    assert login_as(SYSADMIN).put(URL, json={"api_key": bad}).status_code == 422


def test_me_reports_sysadmin_role():
    assert login_as(SYSADMIN).get("/api/auth/me").json()["role"] == "sysadmin"
