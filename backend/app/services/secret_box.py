"""Symmetric encryption for secrets stored in the database, keyed from SESSION_SECRET."""
import base64
import hashlib
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken

_CONTEXT = b"fc_ocr/app-settings/v1:"


def _fernet(secret: str) -> Fernet:
    # Domain-separated so the derived key differs from the session-signing use of the secret.
    digest = hashlib.sha256(_CONTEXT + secret.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt(plain: str, secret: str) -> str:
    return _fernet(secret).encrypt(plain.encode()).decode()


def decrypt(token: str, secret: str) -> Optional[str]:
    """Return the plaintext, or None if the token is invalid or the secret has changed."""
    try:
        return _fernet(secret).decrypt(token.encode()).decode()
    except (InvalidToken, ValueError):
        return None
