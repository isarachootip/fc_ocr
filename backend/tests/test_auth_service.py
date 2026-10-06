import time
from app.services import auth_service as auth


SECRET = "k" * 40


def test_token_roundtrip():
    token = auth.create_token("admin", SECRET, ttl_seconds=60)
    assert auth.verify_token(token, SECRET) == "admin"


def test_token_tampered_rejected():
    token = auth.create_token("admin", SECRET, ttl_seconds=60)
    assert auth.verify_token(token + "x", SECRET) is None
    assert auth.verify_token("garbage", SECRET) is None
    assert auth.verify_token("", SECRET) is None


def test_token_wrong_secret_rejected():
    token = auth.create_token("admin", SECRET, ttl_seconds=60)
    assert auth.verify_token(token, "z" * 40) is None


def test_token_expired_rejected():
    token = auth.create_token("admin", SECRET, ttl_seconds=-1)
    assert auth.verify_token(token, SECRET) is None


def test_throttle_blocks_after_limit():
    t = auth.LoginThrottle(max_failures=3, window_seconds=60)
    for _ in range(3):
        assert not t.is_blocked("1.2.3.4")
        t.record_failure("1.2.3.4")
    assert t.is_blocked("1.2.3.4")
    assert not t.is_blocked("5.6.7.8")
    t.reset("1.2.3.4")
    assert not t.is_blocked("1.2.3.4")


def test_throttle_window_expires():
    t = auth.LoginThrottle(max_failures=1, window_seconds=0.05)
    t.record_failure("ip")
    assert t.is_blocked("ip")
    time.sleep(0.1)
    assert not t.is_blocked("ip")
