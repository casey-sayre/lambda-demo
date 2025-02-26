from fastapi import FastAPI
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger

logger = setup_json_logger(__name__)


logger.info(f"begin {__name__}")

app = FastAPI()


@app.get("/")
async def get_orders():
    return {"message": "Hello from GET orders/"}


@app.post("/")
async def create_order():
    return {"message": "Hello from POST orders/"}


@app.get("/{order_id}")
async def get_order_by_id(order_id: int):
    return {"message": f"Hello from GET orders/{order_id}"}


handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover
    logger.info(f"{event=}; {context=}")
    return handler(event, context)


logger.info("end")
