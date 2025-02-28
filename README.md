# Demo Project: Python 3.13 CDK App with Poetry 2.1

## Deploys a little AWS ecosystem with Lambdas, a Cognito user pool, and an API Gateway.

See app.py

## Uses vscode devcontainers

From Windows WSL bash, from the toplevel project directory, run:
```
code .
``` 
Answer yes to "reopen in container?".  All
devtools will be installed in the resulting devcontainer.

Note that the devcontainer mounts the WSL ~/.ssh and ~/.aws readonly so AWS and ssh (think github) credentials are available in vscode.

When starting out it's probably advisable to run the following from the vscode devcontainer terminal (bash):

`python -m venv .venv`

`source .venv/bin/activate`

`poetry update`

`poetry install`

`sudo poetry self add poetry-plugin-export`

`./generate_lambda_runtime_deps.sh`

## Uses poetry-plugin-export to get requirements.txt for the various lambdas

A lambda function's runtime dependencies are be maintained in the corresponding group in `pyproject.toml`

That is, the dependencies for the customers lambda function handler are in the `pyproject.toml` group

```
[tool.poetry.group.customers_lambda_function.dependencies]
fastapi = ">=0.115.8,<0.116.0"
mangum = ">=0.19.0,<0.20.0"
```

### poetry-plugin-export Reference

[https://github.com/python-poetry/poetry-plugin-export]


### Install (after every devcontainer rebuild)

```
sudo poetry self add poetry-plugin-export
```


When it's time to deploy, if any lambda function handler dependencies have changed, from vscode devcontainer terminal (bash), run

`./generate_lambda_runtime_deps.sh`

## AWS CLI scripts

for your reference

```
REGION=us-east-1
USER_POOL_ID=us-east-1_xxxxKbuUd
USER_POOL_CLIENT_ID=xxxxxxxxdad52436pajoehkbqm


# set up auth flows
aws cognito-idp update-user-pool-client \
    --user-pool-id "$USER_POOL_ID" \
    --client-id "$USER_POOL_CLIENT_ID" \
    --explicit-auth-flows "ALLOW_USER_SRP_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" "ALLOW_USER_PASSWORD_AUTH"

# create cognito user management groups
VIEWER_GROUP_NAMES=(
    "customers_viewers"
    "orders_viewers"
    "products_viewers"
)
ADMIN_GROUP_NAMES=(
    "customers_admins"
    "orders_admins"
    "products_admins"
)
GROUP_NAMES=("${VIEWER_GROUP_NAMES[@]}" "${ADMIN_GROUP_NAMES[@]}")

for GROUP_NAME in "${GROUP_NAMES[@]}"; do
    aws cognito-idp create-group \
        --user-pool-id "$USER_POOL_ID" \
        --group-name "$GROUP_NAME" \
        --description "Group: $group_name"
done

# create admin user and add admin groups
PASSWORD=xxxxxxxx

USERNAME=admin
EMAIL=foo+admin@gmail.com

aws cognito-idp admin-create-user \
    --user-pool-id "$USER_POOL_ID" \
    --username "$USERNAME" \
    --temporary-password "$PASSWORD" \
    --user-attributes Name="email",Value="$EMAIL" \
    --message-action "SUPPRESS"

for GROUP_NAME in "${ADMIN_GROUP_NAMES[@]}"; do
    aws cognito-idp admin-add-user-to-group \
        --user-pool-id "$USER_POOL_ID" \
        --username "$USERNAME" \
        --group-name "$GROUP_NAME"
done

# create viewer user and add viewer groups
USERNAME=viewer
EMAIL=foo+viewer@gmail.com

aws cognito-idp admin-create-user \
    --user-pool-id "$USER_POOL_ID" \
    --username "$USERNAME" \
    --temporary-password "$PASSWORD" \
    --user-attributes Name="email",Value="$EMAIL" \
    --message-action "SUPPRESS"

for GROUP_NAME in "${VIEWER_GROUP_NAMES[@]}"; do
    aws cognito-idp admin-add-user-to-group \
        --user-pool-id "$USER_POOL_ID" \
        --username "$USERNAME" \
        --group-name "$GROUP_NAME"
done

# authenticate and satisfy the new user's change password challenge if necessary
aws cognito-idp initiate-auth \
    --region us-east-1 \
    --client-id $USER_POOL_CLIENT_ID \
    --auth-flow USER_PASSWORD_AUTH \
    --auth-parameters "USERNAME=$USERNAME,PASSWORD=$PASSWORD"

SESSION_ID=xxxxxxxxxxxxMkNG2h7X-Laj8nwAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMTo3NDU2MjM0Njc1NTU6a2V5L2IxNTVhZmNhLWJmMjktNGVlZC1hZmQ4LWE5ZTA5MzY1M2RiZQC4AQIBAHjHL4WD3WpekpFe85nxP9Nwg99u3bPN6BTSaB-uHZcTLAFd8pxebXhx1zl2KFl7H4PCAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMODXsseWl3YZkTybsAgEQgDutIGKAjqyxJrOZJIO1n2Y_zxsG0qSMoOlOK13VLqEOfnutVGdeKLjdnn2PeZHSX6S8wc3V6haLqnb6GAIAAAAADAAAEAAAAAAAAAAAAAAAAACkJYxDrvxzuMKetRKr-K_______wAAAAEAAAAAAAAAAAAAAAEAAADSEn_1OhP5VJAZnkxp6ln-NikYEk6fJD9OQFCDOn3P-8ZHbwBBtU-JziHyBFuREFVMwXNS9tE8NhF8uXA24frTdl20fxWpuUJc4HhYDVO0RbfdAo6ISbGhL9y4IEJ0PXzDR9AD8QDoR9v7n_1yl38M7qh9BDG9SYpseALzZZOp7usoHKm_VKT9VKC-WUe_JL2WrtPU_EEltmxKeab-ooZ6LcyXT3fQHqv1-0kMrjRrcIp4JU1pV_fh8bdWwYuvt5qoun0VapJmKp0CsgrH0pxJbvnFBqQ5a2tA8Qf3A9wyo5OFoA

aws cognito-idp respond-to-auth-challenge \
    --region $REGION \
    --client-id $USER_POOL_CLIENT_ID \
    --challenge-name NEW_PASSWORD_REQUIRED \
    --session "$SESSION_ID" \
    --challenge-responses "USERNAME=$USERNAME,NEW_PASSWORD=$PASSWORD"

# Access Token
AUTH_TOKEN=XXXXXXXiOiJ2MFlTMWhUVTJlYzlVK3ptTThDZXNDajJYejViblFjTGZUb3pGcEc3RFBRPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJkNDU4YjQzOC1mMGIxLTcwNDUtZDZiZi1kYTE2OThiZTQyNjYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9TTGtjS2J1VWQiLCJjbGllbnRfaWQiOiIxMWhvN29jNmRhZDUyNDM2cGFqb2Voa2JxbSIsIm9yaWdpbl9qdGkiOiIzMmQ0YTQyMy02N2ZlLTRlZTctYmNhNi1iNGEyY2I4NGJkNjIiLCJldmVudF9pZCI6IjZlMTFhYTA1LWYzMmItNDUzYy1hMDFmLWRhYTI3YzQwYjA0MiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NDA3NjY5MDUsImV4cCI6MTc0MDc3MDUwNSwiaWF0IjoxNzQwNzY2OTA1LCJqdGkiOiJlYzRiNDVmMi05MTcwLTQ0MzUtYWNmZC1iMjlhMzFjMmI4ZjAiLCJ1c2VybmFtZSI6ImFkbWluIn0.Iu0jjPYStUcY1hFo7ssnJ17O0qIej-sbXLG295I5DD7Ly0PkEc32TcasgVnwQ421Ljii1F6hZBvX4u9g78arcv_Z9kMqvHPThVbgBzexISU4ft3Z5ODqcak13MYyjDW0UadnIS8cTRpSXuF3w2FTPYpMrdoFNihkkUBj4RjwgKPoHP7IZ542ypLx7YQc4xaWLoF92NmwsCdu3SbnQkNm1EdWywvGXSz2OM8aySPWYel4W3tSWVZ5_GL2ZsK8jewTxUiadNgvByC041PrP9YzOB3dXk3NmOoz0ZlF9TGqP47vlTC3zJeBOGeCsQ0cFIcHpM19DPTjaZNvtGsIrbAttQ

curl -X GET -i -H "Authorization: Bearer=$AUTH_TOKEN" https://xxxxxxrskc.execute-api.us-east-1.amazonaws.com/prod/customers
```