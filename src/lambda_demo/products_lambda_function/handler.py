from fastapi import FastAPI
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger

logger = setup_json_logger(__name__)


logger.info(f"begin {__name__}")

app = FastAPI()


@app.get("/")
async def get_products():
    return {"message": "Hello from GET products/"}


@app.post("/")
async def create_product():
    return {"message": "Hello from POST products/"}


@app.get("/{product_id}")
async def get_product_by_id(product_id: int):
    return {"message": f"Hello from GET products/{product_id}"}


handler = Mangum(app)  # Important: Create Mangum handler


# Important: This is the handler function that API Gateway will call
def lambda_handler(event, context):  # pragma: no cover
    logger.info(f"{event=}; {context=}")
    return handler(event, context)


logger.info("end")
