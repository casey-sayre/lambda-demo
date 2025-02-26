from src.lambda_demo.customers_lambda_function.handler import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from GET customers/"}


def test_post_root():
    response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from POST customers/"}


def test_get_customer_id():
    fake_customer_id = "246"
    response = client.get(f"/{fake_customer_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello from GET customers/{fake_customer_id}"}
