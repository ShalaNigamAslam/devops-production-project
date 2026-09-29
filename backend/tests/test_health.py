from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
def test_users():
    response = client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert isinstance(users, list)
    assert len(users) >= 1
    assert "id" in users[0]
    assert "name" in users[0]
