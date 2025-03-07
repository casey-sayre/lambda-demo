from pathlib import Path
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as _iam,
    BundlingOptions,
)
from constructs import Construct
from src.lambda_demo.utils.logger import setup_json_logger

logger = setup_json_logger(__name__)
PROJECT_SRC = Path(__file__).parents[1].resolve()


class LambdaStack(Stack):

    def __init__(self, scope: Construct, *, lambda_key: str, **kwargs) -> None:
        super().__init__(scope, lambda_key.title() + "LambdaStack", **kwargs)

        logger.info(f"module name {type(self).__name__}; {PROJECT_SRC=}")

        lambda_id = f"{lambda_key.title()}LambdaFunction1"

        # Define the Lambda function
        lambda_dir = f"src/lambda_demo/{lambda_key}_lambda_function"
        utils_dir = "src/lambda_demo/utils"
        asset_output_path = "/asset-output"
        bundle_cmd = (
            f"mkdir -p {asset_output_path}/{lambda_dir} && "
            f"mkdir -p {asset_output_path}/{utils_dir} && "
            f"pip install --no-cache -r {lambda_dir}/requirements.txt -t {asset_output_path} && "
            f"cp -au {lambda_dir}/*.py {asset_output_path}/{lambda_dir}/ && "
            f"cp -au {utils_dir}/*.py {asset_output_path}/{utils_dir}/"
        )
        logger.info(f"{lambda_id=}; {bundle_cmd=}")
        self.function = _lambda.Function(
            self,
            lambda_id,
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler=f"src.lambda_demo.{lambda_key}_lambda_function.handler.lambda_handler",
            code=_lambda.Code.from_asset(
                ".",
                bundling=BundlingOptions(
                    command=["bash", "-c", bundle_cmd],
                    image=_lambda.Runtime.PYTHON_3_13.bundling_image,
                ),
            ),
        )

        # allow api gateway to invoke
        self.function.grant_invoke(_iam.ServicePrincipal("apigateway.amazonaws.com"))
