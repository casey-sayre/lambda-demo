import json
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
async def get_products():
    return {"message": "Hello from products FastAPI (GET)"}


@app.post("/")
async def create_product():
    return {"message": "Hello from products FastAPI (POST)"}


@app.get("/{product_id}")
async def get_product_by_id(product_id: int):
    return {"message": f"Hello from products FastAPI (GET by ID: {product_id})"}


# ... other FastAPI routes as needed

handler = Mangum(app)  # Important: Create Mangum handler


# Important: This is the handler function that API Gateway will call
def lambda_handler(event, context):
    return handler(event, context)
