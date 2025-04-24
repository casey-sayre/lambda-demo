#!/bin/bash

source .env

ID_TOKEN=$(./get-admin-id-token.sh)

curl -s -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $ID_TOKEN" $DEFAULT_ENDPOINT/customers

