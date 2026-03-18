import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add project root to path so imports work in CI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi_app.generated import app

client = TestClient(app)

PHP_DIR = "php_app"
endpoints = [f.replace(".php", "") for f in os.listdir(PHP_DIR)]


@pytest.fixture(scope="module", autouse=True)
def clear_db():
    """Clear users table before tests for repeatability."""
    import sqlite3
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    print("🧹 Database cleared before tests")
    yield
    # Optional: clear after tests
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    print("🧹 Database cleared after tests")


def test_post_endpoints():
    """
    Test all POST endpoints (INSERT) with dummy data.
    """
    for endpoint in endpoints:
        if "create" in endpoint.lower() or "insert" in endpoint.lower():
            print(f"📝 Testing POST /{endpoint} ...")
            res = client.post(f"/{endpoint}", params={"name": "Abhinay", "email": "abhi@example.com"})
            print(f"🔹 Status code: {res.status_code}")
            assert res.status_code == 200, f"POST /{endpoint} failed"
            json_res = res.json()
            print(f"🔹 Response: {json_res}")
            assert "message" in json_res and json_res["message"] == "created"
            print(f"✅ POST /{endpoint} passed\n")


def test_get_endpoints():
    """
    Test all GET endpoints (SELECT) and validate structure.
    """
    for endpoint in endpoints:
        if "get" in endpoint.lower() or "select" in endpoint.lower():
            print(f"📝 Testing GET /{endpoint} ...")
            res = client.get(f"/{endpoint}")
            print(f"🔹 Status code: {res.status_code}")
            assert res.status_code == 200, f"GET /{endpoint} failed"
            json_res = res.json()
            print(f"🔹 Response: {json_res}")
            assert isinstance(json_res, list), f"GET /{endpoint} did not return a list"
            if len(json_res) > 0:
                assert all(isinstance(row, list) for row in json_res), f"GET /{endpoint} returned wrong row structure"
            print(f"✅ GET /{endpoint} passed\n")


def test_post_get_integration():
    """
    Integration test: POST a user and verify it exists in GET endpoint.
    """
    post_endpoint = next((e for e in endpoints if "create" in e.lower()), None)
    get_endpoint = next((e for e in endpoints if "get" in e.lower()), None)

    if post_endpoint and get_endpoint:
        name = "IntegrationTest"
        email = "integration@example.com"
        print(f"📝 Integration test: POST /{post_endpoint} ...")
        res_post = client.post(f"/{post_endpoint}", params={"name": name, "email": email})
        print(f"🔹 Status code: {res_post.status_code}, Response: {res_post.json()}")
        assert res_post.status_code == 200

        print(f"📝 Integration test: GET /{get_endpoint} ...")
        res_get = client.get(f"/{get_endpoint}")
        print(f"🔹 Status code: {res_get.status_code}, Response: {res_get.json()}")
        users = res_get.json()
        assert any(u[1] == name and u[2] == email for u in users), "Integration user not found in GET response"
        print(f"✅ Integration test POST → GET passed\n")
