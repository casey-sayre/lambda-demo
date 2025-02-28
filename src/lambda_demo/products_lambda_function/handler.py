from fastapi import FastAPI
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger

logger = setup_json_logger(__name__)

app = FastAPI()


@app.get("/products")
async def get_products():
    return {"message": "Hello from GET products/"}


@app.post("/products")
async def create_product():
    return {"message": "Hello from POST products/"}


@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    return {"message": f"Hello from GET products/{product_id}"}


handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover
    logger.info(f"{event=}; {context=}")
    return handler(event, context)


logger.info("end")
