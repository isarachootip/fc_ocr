from app.services.secret_box import decrypt, encrypt

SECRET = "s" * 40


def test_round_trip():
    token = encrypt("AIzaSy-example-key-123", SECRET)
    assert token != "AIzaSy-example-key-123"
    assert decrypt(token, SECRET) == "AIzaSy-example-key-123"


def test_tokens_are_randomised():
    assert encrypt("same", SECRET) != encrypt("same", SECRET)


def test_wrong_secret_returns_none():
    token = encrypt("value", SECRET)
    assert decrypt(token, "t" * 40) is None


def test_garbage_token_returns_none():
    assert decrypt("not-a-fernet-token", SECRET) is None
