from fastapi import FastAPI
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger

logger = setup_json_logger(__name__)


logger.info("begin")

app = FastAPI()


@app.get("/")
async def get_customers():
    return {"message": "Hello from Customers FastAPI (GET)"}


@app.post("/")
async def create_customer():
    return {"message": "Hello from Customers FastAPI (POST)"}


@app.get("/{customer_id}")
async def get_customer_by_id(customer_id: int):
    return {"message": f"Hello from Customers FastAPI (GET by ID: {customer_id})"}


# ... other FastAPI routes as needed

handler = Mangum(app)  # Important: Create Mangum handler


# Important: This is the handler function that API Gateway will call
def lambda_handler(event, context):
    logger.info(f"{event=}; {context=}")
    return "200"  # handler(event, context)


logger.info("end")
