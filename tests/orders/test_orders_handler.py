from src.lambda_demo.orders_lambda_function.handler import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from GET orders/"}


def test_post_root():
    response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from POST orders/"}


def test_get_order_id():
    fake_order_id = "246"
    response = client.get(f"/{fake_order_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello from GET orders/{fake_order_id}"}
