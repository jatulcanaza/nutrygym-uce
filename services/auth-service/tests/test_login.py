from tests.conftest import client


def test_login_success(client):

    register_response = client.post(
        "/auth/register",
        json={
            "email": "login@uce.edu.ec",
            "password": "123456",
            "name": "Juan"
        }
    )

    assert register_response.status_code == 200


    response = client.post(
        "/auth/login",
        data={
            "username": "login@uce.edu.ec",
            "password": "123456"
        }
    )


    assert response.status_code == 200, response.json()


    data = response.json()


    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"