from tests.conftest import client


def test_register_success(client):

    response = client.post(
        "/auth/register",
        json={
            "email": "prueba1@uce.edu.ec",
            "password": "123456",
            "name": "Juan"
        }
    )


    assert response.status_code == 200, response.json()


    data = response.json()


    assert data["email"] == "prueba1@uce.edu.ec"

    assert data["name"] == "Juan"