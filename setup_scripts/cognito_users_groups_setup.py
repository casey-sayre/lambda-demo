import boto3
import os
from dotenv import load_dotenv

# edit .env and fill in the values
load_dotenv()
admin_password = os.getenv("ADMIN_PASSWORD")
admin_email = os.getenv("ADMIN_EMAIL")
viewer_password = os.getenv("VIEWER_PASSWORD")
viewer_email = os.getenv("VIEWER_EMAIL")
region = os.getenv("REGION")
user_pool_id = os.getenv("USER_POOL_ID")

VIEWER_GROUP_NAMES = [
    "customers_viewers",
    "orders_viewers",
    "products_viewers",
]
ADMIN_GROUP_NAMES = [
    "customers_admins",
    "orders_admins",
    "products_admins",
]

# input required BEGIN

ADMIN_USER = {
    "PASSWORD": admin_password,
    "EMAIL": admin_email,
    "USERNAME": "admin",
    "GROUP_NAMES": ADMIN_GROUP_NAMES,
}
VIEWER_USER = {
    "PASSWORD": viewer_password,
    "EMAIL": viewer_email,
    "USERNAME": "viewer",
    "GROUP_NAMES": VIEWER_GROUP_NAMES,
}
# input required END

cognito_client = boto3.client("cognito-idp", region_name=region)

GROUP_NAMES = VIEWER_GROUP_NAMES + ADMIN_GROUP_NAMES

# Create Groups
for group_name in GROUP_NAMES:
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
