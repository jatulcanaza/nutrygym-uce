from app.routes.auth import (
    hash_password_safely,
    verify_password_safely,
    create_access_token,
    create_refresh_token,
)


def test_hash_password():
    password = "ja123456"

    hashed = hash_password_safely(password)

    assert hashed != password
    assert verify_password_safely(password, hashed)


def test_wrong_password():
    hashed = hash_password_safely("123456")

    assert verify_password_safely(
        "abcdef",
        hashed
    ) is False


def test_create_access_token():
    token = create_access_token(
        {
            "sub": "1",
            "email": "juan@uce.edu.ec"
        }
    )

    assert isinstance(token, str)
    assert len(token) > 50


def test_create_refresh_token():
    token = create_refresh_token(
        {
            "sub": "1",
            "email": "juan@uce.edu.ec"
        }
    )

    assert isinstance(token, str)
    assert len(token) > 50