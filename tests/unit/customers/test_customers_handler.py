import json
from src.lambda_demo.customers_lambda_function.handler import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import status

client = TestClient(app)


@patch('src.lambda_demo.customers_lambda_function.handler.check_permission')
def test_get_customers(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None

    # Act
    response = client.get("/customers")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == json.loads('[{"id": 1000, "name": "John Doe"},{"id": 1001, "name": "Jane Smith"}]')


@patch('src.lambda_demo.customers_lambda_function.handler.check_permission')
def test_post_customers(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None
    new_customer_data = {"id": 1002, "name": "Peter Jones"}

    # Act
    response = client.post("/customers", json=new_customer_data)

    # Assert
    assert response.status_code == 201
    assert response.json() == new_customer_data


@patch('src.lambda_demo.customers_lambda_function.handler.check_permission')
def test_get_customer_existing_id(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None
    customer_id = "1000"

    # Act
    response = client.get(f"/customers/{customer_id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == json.loads('{"id": 1000, "name": "John Doe"}')


@patch('src.lambda_demo.customers_lambda_function.handler.check_permission')
def test_get_customer_nonexisting_id(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None
    customer_id = "9900"

    # Act
    response = client.get(f"/customers/{customer_id}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == json.loads('{"detail": "Item not found"}')
