import json
from src.lambda_demo.orders_lambda_function.handler import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import status

client = TestClient(app)

order_1000_string_value = '{"id": 1000, "product_id": 1, "quantity": 1}'
order_1001_string_value = '{"id": 1001, "product_id": 2, "quantity": 2}'
new_order_string_value = '{"id": 1002, "product_id": 2, "quantity": 3}'


@patch('src.lambda_demo.orders_lambda_function.handler.check_permission')
def test_get_orders(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None

    # Act
    response = client.get("/orders")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == json.loads(f'[{order_1000_string_value},{order_1001_string_value}]')


@patch('src.lambda_demo.orders_lambda_function.handler.check_permission')
def test_post_orders(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None
    new_order = json.loads(new_order_string_value)

    # Act
    response = client.post("/orders", json=new_order)

    # Assert
    assert response.status_code == 201
    assert response.json() == new_order


@patch('src.lambda_demo.orders_lambda_function.handler.check_permission')
def test_get_order_existing_id(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None
    order_id = 1000

    # Act
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == json.loads(order_1000_string_value)

@patch('src.lambda_demo.orders_lambda_function.handler.check_permission')
def test_get_order_nonexisting_id(mock_check_permission):
    # Arrange:
    mock_check_permission.return_value = None
    order_id = 8800

    # Act
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == json.loads('{"detail": "Item not found"}')
