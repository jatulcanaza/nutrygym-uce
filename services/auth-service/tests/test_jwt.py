from datetime import timedelta

from jose import jwt

from app.routes.auth import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)


def test_access_token_payload():

    token = create_access_token(
        data={
            "sub": "123",
            "email": "test@uce.edu.ec"
        }
    )


    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )


    assert payload["sub"] == "123"
    assert payload["email"] == "test@uce.edu.ec"
    assert "exp" in payload



def test_refresh_token_payload():

    token = create_refresh_token(
        data={
            "sub": "123",
            "email": "test@uce.edu.ec"
        }
    )


    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )


    assert payload["sub"] == "123"
    assert payload["email"] == "test@uce.edu.ec"
    assert payload["type"] == "refresh"