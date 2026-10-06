from app.services import password_service as pw


def test_hash_and_verify():
    h = pw.hash_password("correct horse")
    assert h != "correct horse"
    assert pw.verify_password("correct horse", h)
    assert not pw.verify_password("wrong", h)


def test_hashes_are_salted():
    assert pw.hash_password("same-password") != pw.hash_password("same-password")


def test_malformed_hash_never_verifies():
    for bad in ["", "plain", "scrypt$1$2", "scrypt$x$y$z$a$b"]:
        assert not pw.verify_password("anything", bad)


def test_policy():
    assert pw.password_problem("short") is not None
    assert pw.password_problem("a" * 201) is not None
    assert pw.password_problem("long-enough-pass") is None
