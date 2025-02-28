from typing import List
from fastapi import FastAPI, Request, HTTPException
from mangum import Mangum
from src.lambda_demo.utils.logger import setup_json_logger

logger = setup_json_logger(__name__)

app = FastAPI()


def check_permission(request: Request, permitted_groups: List[str]) -> str:
    claims = request.scope.get("aws.authorizer.cognito.claims", {})
    username = claims.get("cognito:username", "Anonymous User")
    user_groups = claims.get("cognito:groups", [])

    if not any(g in permitted_groups for g in user_groups):
        logger.warning(f"User {username} is not authorized to POST /customers (missing ProductWriters group)")
        raise HTTPException(status_code=403, detail="Insufficient write permissions")

    return username


@app.get("/customers")
async def get_customers(request: Request):

    username = check_permission(
        request,
        ["customers_view", "customers_admin"],
        "not permitted to view customers"
    )

    return {"message": f"{username} permitted to GET /customers"}


@app.post("/customers")
async def create_customer(request: Request):

    username = check_permission(
        request,
        ["customers_admin"],
        "not permitted to create customers"
    )

    return {"message": f"{username} permitted to POST /customers"}


@app.get("/customers/{customer_id}")
async def get_customer_by_id(request: Request, customer_id: int):
    username = check_permission(
        request,
        ["customers_view", "customers_admin"],
        "not permitted to view customers"
    )
    return {"message": f"{username} permitted to GET /customers/{customer_id}"}


handler = Mangum(app)


def lambda_handler(event, context):  # pragma: no cover
    logger.info(f"{event=}; {context=}")
    return handler(event, context)
