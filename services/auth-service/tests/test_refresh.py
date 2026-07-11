from tests.conftest import client



def test_refresh_token_success(client):

    # Registrar usuario
    register = client.post(
        "/auth/register",
        json={
            "email": "refresh@uce.edu.ec",
            "password": "123456",
            "name": "Juan"
        }
    )

    assert register.status_code == 200


    # Login
    login = client.post(
        "/auth/login",
        data={
            "username": "refresh@uce.edu.ec",
            "password": "123456"
        }
    )


    assert login.status_code == 200


    tokens = login.json()

    refresh_token = tokens["refresh_token"]


    # Solicitar nuevo token
    response = client.post(
        "/auth/refresh",
        params={
            "refresh_token": refresh_token
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"