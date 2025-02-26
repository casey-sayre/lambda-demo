from src.lambda_demo.products_lambda_function.handler import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from GET products/"}


def test_post_root():
    response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from POST products/"}


def test_get_product_id():
    fake_product_id = "246"
    response = client.get(f"/{fake_product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello from GET products/{fake_product_id}"}
