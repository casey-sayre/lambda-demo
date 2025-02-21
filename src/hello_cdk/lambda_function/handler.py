import json


def main(event, context):
    print("Event:", json.dumps(event))
    return {"statusCode": 200, "body": json.dumps("Hello from AWS Lambda!")}
