import json
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
async def get_orders():
    return {"message": "Hello from orders FastAPI (GET)"}


@app.post("/")
async def create_order():
    return {"message": "Hello from orders FastAPI (POST)"}


@app.get("/{order_id}")
async def get_order_by_id(order_id: int):
    return {"message": f"Hello from orders FastAPI (GET by ID: {order_id})"}


# ... other FastAPI routes as needed

handler = Mangum(app)  # Important: Create Mangum handler


# Important: This is the handler function that API Gateway will call
def lambda_handler(event, context):
    return handler(event, context)
