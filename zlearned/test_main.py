from fastapi.testclient import TestClient
import pytest
from main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"hello world"}

def test_read_item(client):
    response = client.get("/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "name": "item 5"}