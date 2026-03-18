from fastapi.testclient import TestClient
from fastapi_app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/get_users")
    assert response.status_code == 200

def test_create_user():
    response = client.post("/create_user", params={
        "name": "abhi",
        "email": "abhi@test.com"
    })
    assert response.status_code == 200
