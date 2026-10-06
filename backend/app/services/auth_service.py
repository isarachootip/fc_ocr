"""Pure authentication logic: signed session tokens, credential check, login throttle."""
import hashlib
import hmac
import threading
import time
from typing import Dict, List, Optional


def _sign(payload: str, secret: str) -> str:
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def create_token(username: str, secret: str, ttl_seconds: float) -> str:
    expires = int(time.time() + ttl_seconds)
    payload = f"{username}.{expires}"
    return f"{payload}.{_sign(payload, secret)}"


def verify_token(token: str, secret: str) -> Optional[str]:
    """Return the username if the token is authentic and unexpired, else None."""
    try:
        username, expires, signature = token.rsplit(".", 2)
        expires_at = int(expires)
    except (ValueError, AttributeError):
        return None
    expected = _sign(f"{username}.{expires}", secret)
    if not hmac.compare_digest(signature, expected):
        return None
    if expires_at < time.time():
        return None
    return username


def check_credentials(username: str, password: str, expected_user: str, expected_pass: str) -> bool:
    """Constant-time comparison. An empty expected password never authenticates."""
    if not expected_pass:
        return False
    user_ok = hmac.compare_digest(username.encode(), expected_user.encode())
    pass_ok = hmac.compare_digest(password.encode(), expected_pass.encode())
    return user_ok and pass_ok


class LoginThrottle:
    """In-memory sliding window limiting failed logins per client key."""

    def __init__(self, max_failures: int = 5, window_seconds: float = 300):
        self.max_failures = max_failures
        self.window = window_seconds
        self._failures: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def _recent(self, key: str) -> List[float]:
        cutoff = time.monotonic() - self.window
        recent = [t for t in self._failures.get(key, []) if t > cutoff]
        self._failures[key] = recent
        return recent

    def is_blocked(self, key: str) -> bool:
        with self._lock:
            return len(self._recent(key)) >= self.max_failures

    def record_failure(self, key: str) -> None:
        with self._lock:
            self._recent(key).append(time.monotonic())

    def reset(self, key: str) -> None:
        with self._lock:
            self._failures.pop(key, None)
