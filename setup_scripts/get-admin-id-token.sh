#!/bin/bash

source .env

# to use curl to get an id token for testing, add ALLOW_USER_PASSWORD_AUTH flow to the cognito app client

USERNAME=$ADMIN_USERNAME
PASSWORD=$ADMIN_PASSWORD
SECRET_HASH=$(echo -n "$USERNAME$CLIENT_ID" | openssl dgst -sha256 -hmac "$CLIENT_SECRET" -binary | base64)

AWS_OUTPUT=$(aws cognito-idp initiate-auth \
    --client-id $CLIENT_ID \
    --auth-flow USER_PASSWORD_AUTH \
    --auth-parameters USERNAME=$USERNAME,PASSWORD=$PASSWORD,SECRET_HASH=$SECRET_HASH)

ID_TOKEN=$(echo "$AWS_OUTPUT" | jq -r '.AuthenticationResult.IdToken')

echo $ID_TOKEN
