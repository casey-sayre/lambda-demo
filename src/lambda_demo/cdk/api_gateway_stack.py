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

        self.lambda_rest_api = apigateway.RestApi(
            self,
            "DemoRestApi",
            rest_api_name="RedirectedLambdaAPI",
            description="API Gateway redirecting to Lambda functions in other stacks",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["*"],
                status_code=200,
            ),
        )

        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self,
            "CognitoAuthorizer",
            cognito_user_pools=[user_pool],
        )

        # integrate the lambdas
        for spec in lambda_specs:
            integration = apigateway.LambdaIntegration(spec.fn)

            resource = self.lambda_rest_api.root.add_resource(spec.key)
            resource.add_method(
                "GET",
                integration,
                authorization_type=apigateway.AuthorizationType.COGNITO,
                authorizer=authorizer
            )
            resource.add_method(
                "POST",
                integration,
                authorization_type=apigateway.AuthorizationType.COGNITO,
                authorizer=authorizer
            )
            resource_id = resource.add_resource("{id}")
            resource_id.add_method(
                "GET",
                integration,
                authorization_type=apigateway.AuthorizationType.COGNITO,
                authorizer=authorizer
            )
