from fastapi import FastAPI, HTTPException, Request, status
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger
from src.lambda_demo.utils.path_operation_utils import check_permission
from typing import List
from pydantic import BaseModel

logger = setup_json_logger(__name__)

app = FastAPI()


class Order(BaseModel):
    id: int
    product_id: int
    quantity: int


READ_PERMISSION_GROUP_LIST = ["orders_viewers", "orders_admins"]
READ_WRITE_PERMISSION_GROUP_LIST = ["orders_admins"]


@app.get("/orders", response_model=List[Order], status_code=status.HTTP_200_OK)
async def get_orders(request: Request):
    check_permission(request, READ_PERMISSION_GROUP_LIST, "not permitted to view orders")
    return [
        Order(id=1000, product_id=1, quantity=1),
        Order(id=1001, product_id=2, quantity=2),
    ]


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_customer(order: Order, request: Request):
    check_permission(request, READ_WRITE_PERMISSION_GROUP_LIST, "not permitted to create orders")
    return order


@app.get("/orders/{order_id}", response_model=Order, status_code=status.HTTP_200_OK)
async def get_customer_by_id(order_id: int, request: Request):
    check_permission(request, READ_PERMISSION_GROUP_LIST, "not permitted to view orders")
    match order_id:
        case 1000:
            return Order(id=1000, product_id=1, quantity=1)
        case 1001:
            return Order(id=1001, product_id=2, quantity=2)
        case _:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover
    logger.info(f"{event=}; {context=}")
    return handler(event, context)
