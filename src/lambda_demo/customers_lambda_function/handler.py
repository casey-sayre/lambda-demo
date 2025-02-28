from fastapi import FastAPI
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger
import logging

logger = setup_json_logger(__name__)

app = FastAPI()


@app.get("/customers")
async def get_customers():
    return {"message": "Hello from GET customers/"}


@app.post("/customers")
async def create_customer():
    return {"message": "Hello from POST customers/"}


@app.get("/customers/{customer_id}")
async def get_customer_by_id(customer_id: int):
    return {"message": f"Hello from GET customers/{customer_id}"}


handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover
    logger.info(f"{event=}; {context=}")
    return handler(event, context)
