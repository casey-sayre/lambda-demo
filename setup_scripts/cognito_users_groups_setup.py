import boto3
import os
import json
from dotenv import load_dotenv

# NB: make sure .env is up to date

load_dotenv()

region = os.getenv("REGION")
user_pool_id = os.getenv("USER_POOL_ID")

VIEWER_GROUP_NAMES = json.loads(os.getenv("VIEWER_GROUP_NAMES"))
ADMIN_GROUP_NAMES = json.loads(os.getenv("ADMIN_GROUP_NAMES"))

ADMIN_USER = {
    "PASSWORD": os.getenv("ADMIN_PASSWORD"),
    "EMAIL": os.getenv("ADMIN_EMAIL"),
    "USERNAME": os.getenv("ADMIN_USERNAME"),
    "GROUP_NAMES": ADMIN_GROUP_NAMES,
}
VIEWER_USER = {
    "PASSWORD": os.getenv("VIEWER_PASSWORD"),
    "EMAIL": os.getenv("VIEWER_EMAIL"),
    "USERNAME": os.getenv("VIEWER_USERNAME"),
    "GROUP_NAMES": VIEWER_GROUP_NAMES,
}

cognito_client = boto3.client("cognito-idp", region_name=region)

# Create Groups
for group_name in VIEWER_GROUP_NAMES + ADMIN_GROUP_NAMES:
    cognito_client.create_group(
        UserPoolId=user_pool_id,
        GroupName=group_name,
        Description=f"Group: {group_name}",
    )

for user_spec in [ADMIN_USER, VIEWER_USER]:
    # create user
    cognito_client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=user_spec["USERNAME"],
        TemporaryPassword=user_spec["PASSWORD"],
        UserAttributes=[{"Name": "email", "Value": user_spec["EMAIL"]}],
        MessageAction="SUPPRESS",
    )
    # Add user to groups
    for group_name in user_spec["GROUP_NAMES"]:
        cognito_client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=user_spec["USERNAME"],
            GroupName=group_name,
        )
