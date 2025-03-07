from fastapi import FastAPI, HTTPException, Request, status
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger
from src.lambda_demo.utils.path_operation_utils import check_permission
from typing import List
from pydantic import BaseModel

logger = setup_json_logger(__name__)

app = FastAPI()


class Customer(BaseModel):
    id: int
    name: str


READ_PERMISSION_GROUP_LIST = ["customers_viewers", "customers_admins"]
READ_WRITE_PERMISSION_GROUP_LIST = ["customers_admins"]


@app.get("/customers", response_model=List[Customer], status_code=status.HTTP_200_OK)
async def get_customers(request: Request):
    check_permission(request, READ_PERMISSION_GROUP_LIST, "not permitted to view customers")
    return [
        Customer(id=1000, name="John Doe"),
        Customer(id=1001, name="Jane Smith"),
    ]


@app.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: Customer, request: Request):
    check_permission(request, READ_WRITE_PERMISSION_GROUP_LIST, "not permitted to create customers")
    return customer


@app.get("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def get_customer_by_id(customer_id: int, request: Request):
    check_permission(request, READ_PERMISSION_GROUP_LIST, "not permitted to view customers")
    match customer_id:
        case 1000:
            return Customer(id=1000, name="John Doe")
        case 1001:
            return Customer(id=1001, name="Jane Smith")
        case _:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover
    logger.info(f"{event=}; {context=}")
    return handler(event, context)
