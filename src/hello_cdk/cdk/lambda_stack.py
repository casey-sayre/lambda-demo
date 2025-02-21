from pathlib import Path
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct

PROJECT_SRC = Path(__file__).parents[1].resolve()


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the Lambda function
        _ = _lambda.Function(
            self,
            "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="handler.main",
            code=_lambda.Code.from_asset(str(PROJECT_SRC / "lambda_function")),
        )
