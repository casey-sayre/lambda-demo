from pathlib import Path
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    BundlingOptions,
)
from constructs import Construct
from src.lambda_demo.utils.logger import setup_json_logger

logger = setup_json_logger(__name__)
PROJECT_SRC = Path(__file__).parents[1].resolve()


class LambdaStack(Stack):

    def __init__(self, scope: Construct, *, lambda_key: str, **kwargs) -> None:
        super().__init__(scope, lambda_key.title() + "LambdaStack", **kwargs)

        lambda_id = f"{lambda_key.title()}LambdaFunction"

        # Define the Lambda function
        lambda_dir = f"src/lambda_demo/{lambda_key}_lambda_function"
        utils_dir = f"src/lambda_demo/utils"
        asset_output_path = "/asset-output"
        self.function = _lambda.Function(
            self,
            lambda_id,
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler=f"src.lambda_demo.{lambda_key}_lambda_function.handler.lambda_handler",
            code=_lambda.Code.from_asset(
                ".",
                bundling=BundlingOptions(
                    command=[
                        "bash",
                        "-c",
                        (
                            f"mkdir -p {asset_output_path}/{lambda_dir} && "
                            f"mkdir -p {asset_output_path}/{utils_dir} && "
                            f"pip install --no-cache -r {lambda_dir}/requirements.txt -t {asset_output_path} && "
                            f"cp -au {lambda_dir}/*.py {asset_output_path}/{lambda_dir}/ && "
                            f"cp -au {utils_dir}/*.py {asset_output_path}/{utils_dir}/"
                        ),
                    ],
                    image=_lambda.Runtime.PYTHON_3_13.bundling_image,
                ),
            ),
        )
