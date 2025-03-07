from aws_cdk import (
    aws_cognito as cognito,
    Stack,
)
from constructs import Construct

USER_POOL_NAME = "LambdaDemoUserPool"
USER_POOL_CDK_ID = f"{USER_POOL_NAME}CdkId"
USER_POOL_CLIENT_NAME = "LambdaDemoServerSideUserPoolClient"
USER_POOL_CLIENT_CDK_ID = f"{USER_POOL_CLIENT_NAME}CdkId"
USER_POOL_DOMAIN_PREFIX = "lambda-demo"
CALLBACK_URLS = ["http://localhost:3000/api/auth/callback/cognito"]
LOGOUT_URLS = ["http://localhost:3000/api/auth/callback/cognito"]


class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Deploy User Pool
        self.user_pool = cognito.UserPool(
            self,
            USER_POOL_CDK_ID,
            user_pool_name=USER_POOL_NAME,
        )

        # Deploy User Pool Client
        self.user_pool_client = self.user_pool.add_client(
            USER_POOL_CLIENT_CDK_ID,
            user_pool_client_name=USER_POOL_CLIENT_NAME,
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL, cognito.OAuthScope.PROFILE],
                callback_urls=CALLBACK_URLS,
                logout_urls=LOGOUT_URLS,
            ),
            generate_secret=True,
            supported_identity_providers=[cognito.UserPoolClientIdentityProvider.COGNITO],
        )

        # add a domain to the User Pool
        cognito.UserPoolDomain(
            self,
            "LambdaDemoUserPoolDomain",
            user_pool=self.user_pool,
            cognito_domain=cognito.CognitoDomainOptions(domain_prefix=USER_POOL_DOMAIN_PREFIX),
        )
