from typing import List
from fastapi import Request, HTTPException
from src.lambda_demo.utils.logger import setup_json_logger


logger = setup_json_logger(__name__)


def get_cognito_username(request: Request) -> str:
    event = request.scope["aws.event"]
    authorizer_claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    return authorizer_claims.get("cognito:username", "UNKNOWN")


def check_permission(request: Request, permitted_groups: List[str], err_msg) -> None:
    event = request.scope["aws.event"]
    path = event.get("path")
    http_method = event.get("httpMethod")
    logger.debug(f"checking authorization of {http_method} {path}")
    authorizer_claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    cognito_groups = authorizer_claims.get("cognito:groups", '').split(',')
    cognito_username = authorizer_claims.get("cognito:username", "UNKNOWN")
    logger.debug(f"from token user {cognito_username} is member of {cognito_groups}")

    if not any(g in permitted_groups for g in cognito_groups):
        logger.warning(f"User {cognito_username} is not authorized to {http_method} {path}")
        raise HTTPException(status_code=403, detail=err_msg)
