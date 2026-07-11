from tests.conftest import client


def test_login_invalid_password(client):

    # Registrar usuario
    register_response = client.post(
        "/auth/register",
        json={
            "email": "invalid@uce.edu.ec",
            "password": "123456",
            "name": "Juan"
        }
    )

    assert register_response.status_code == 200


    # Intentar login con contraseña incorrecta
    response = client.post(
        "/auth/login",
        data={
            "username": "invalid@uce.edu.ec",
            "password": "wrongpassword"
        }
    )


    assert response.status_code == 401


    data = response.json()

    assert data["detail"] == "Credenciales incorrectas"