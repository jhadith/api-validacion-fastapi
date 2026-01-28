from fastapi.testclient import TestClient
from app.main import app, db

client = TestClient(app)

def setup_function():
    # Reinicia DB antes de cada test para que sea repetible
    db.reset()

def test_create_product_then_get_product():
    r = client.post("/products", json={"name": "Coca Cola 1L", "price": 1.25, "stock": 10})
    assert r.status_code == 201
    created = r.json()
    assert created["id"] == 1

    g = client.get(f"/products/{created['id']}")
    assert g.status_code == 200
    got = g.json()
    assert got["name"] == "Coca Cola 1L"
    assert got["stock"] == 10

def test_sale_decreases_stock():
    r = client.post("/products", json={"name": "Coca Cola 1L", "price": 1.25, "stock": 10})
    pid = r.json()["id"]

    s = client.post("/sales", json={"product_id": pid, "quantity": 3})
    assert s.status_code == 201
    sale = s.json()
    assert sale["remaining_stock"] == 7

    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert g.json()["stock"] == 7

def test_sale_without_stock_returns_409():
    r = client.post("/products", json={"name": "Coca Cola 1L", "price": 1.25, "stock": 1})
    pid = r.json()["id"]

    s = client.post("/sales", json={"product_id": pid, "quantity": 3})
    assert s.status_code == 409
