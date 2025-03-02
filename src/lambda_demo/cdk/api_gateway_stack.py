from aws_cdk import (
    aws_apigateway as apigateway,
    Stack,
)
from constructs import Construct
from aws_cdk.aws_lambda import IFunction
from aws_cdk.aws_cognito import UserPool


class LambdaSpec:
    def __init__(self, key: str, fn: IFunction):
        self.key = key
        self.fn = fn


class ApiGatewayStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        lambda_specs: list[LambdaSpec],
        stage_name: str,
        user_pool: UserPool,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the API Gateway resource
        self.lambda_rest_api = apigateway.RestApi(
            self,
            "DemoRestApi",
            rest_api_name="RedirectedLambdaAPI",
            description="API Gateway redirecting to Lambda functions in other stacks",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["*"],
            ),
        )

        # Output API endpoint
        deployment_id = "LambdaDemoDeployment"
        deployment = apigateway.CfnDeployment(self, deployment_id, rest_api_id=self.lambda_rest_api.rest_api_id)
        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self,
            "CognitoAuthorizer",
            cognito_user_pools=[user_pool],
            identity_source=apigateway.IdentitySource.header("Authorization"),
        )

        # integrate the lambdas
        for spec in lambda_specs:
            integration = apigateway.LambdaIntegration(spec.fn, proxy=True)

            resource = self.lambda_rest_api.root.add_resource(spec.key)  # /widgets
            resource_id = resource.add_resource("{id}")  # /widgets/{id}

            resource.add_method("GET", integration, authorizer=authorizer)
            deployment.add_dependency(resource.node.default_child)

            resource.add_method("POST", integration, authorizer=authorizer)
            deployment.add_dependency(resource.node.default_child)

            resource_id.add_method("GET", integration, authorizer=authorizer)
            deployment.add_dependency(resource_id.node.default_child)

        apigateway.CfnStage(
            self,
            "LambdaDemoStage",
            rest_api_id=self.lambda_rest_api.rest_api_id,
            deployment_id=deployment.ref,
            stage_name=stage_name,
        )

        self.api_endpoint = (
            f"https://{self.lambda_rest_api.rest_api_id}"
            f".execute-self.lambda_rest_api.{self.region}.amazonaws.com/{stage_name}/"
        )
