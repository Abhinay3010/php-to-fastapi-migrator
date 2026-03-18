import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from fastapi_app.generated import app   # ✅ important change

client = TestClient(app)

def test_get():
    res = client.get("/get_users")
    assert res.status_code == 200

def test_post():
    res = client.post("/create_user", params={
        "name": "abhi",
        "email": "test@test.com"
    })
    assert res.status_code == 200
