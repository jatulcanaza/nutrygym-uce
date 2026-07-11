def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert "status" in body
    assert "service" in body
    assert "database" in body
    assert "timestamp" in body

    assert body["service"] == "auth-service"