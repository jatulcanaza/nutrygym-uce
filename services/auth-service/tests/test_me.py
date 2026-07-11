def test_get_current_user(client):

    # Registrar usuario
    register = client.post(
        "/auth/register",
        json={
            "email": "me@uce.edu.ec",
            "password": "123456",
            "name": "Juan"
        }
    )

    assert register.status_code == 200


    # Login
    login = client.post(
        "/auth/login",
        data={
            "username": "me@uce.edu.ec",
            "password": "123456"
        }
    )

    assert login.status_code == 200


    access_token = login.json()["access_token"]


    # Consultar usuario actual
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )


    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "me@uce.edu.ec"
    assert data["name"] == "Juan"