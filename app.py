from aws_cdk import App

from lambda_demo.cdk.lambda_stack import LambdaStack
from src.lambda_demo.cdk.cognito_stack import CognitoStack
from src.lambda_demo.cdk.api_gateway_stack import ApiGatewayStack, LambdaSpec
from src.lambda_demo.utils.logger import setup_json_logger


logger = setup_json_logger(__name__)

logger.info("begin cdk app")
app = App()

callback_url = "http://localhost:3000/api/auth/callback/cognito"
logout_callback_url = "http://localhost:3000/api/auth/callback/cognito"
cognito_stack = CognitoStack(app, "CognitoStack")

customers_lambda_key = "customers"
customers_lambda_stack = LambdaStack(app, lambda_key=customers_lambda_key)
customers_lambda_spec = LambdaSpec(customers_lambda_key, customers_lambda_stack.function)

orders_lambda_key = "orders"
orders_lambda_stack = LambdaStack(app, lambda_key=orders_lambda_key)
orders_lambda_spec = LambdaSpec(orders_lambda_key, orders_lambda_stack.function)

products_lambda_key = "products"
products_lambda_stack = LambdaStack(app, lambda_key=products_lambda_key)
products_lambda_spec = LambdaSpec(products_lambda_key, products_lambda_stack.function)

api_gateway_stack = ApiGatewayStack(
    app,
    "ApiGatewayStack",
    lambda_specs=[
      customers_lambda_spec,
      orders_lambda_spec,
      products_lambda_spec
    ],
    stage_name="dev",
    user_pool=cognito_stack.user_pool,
)

app.synth()
logger.info("end cdk app")
