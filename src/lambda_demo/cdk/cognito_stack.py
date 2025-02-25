from aws_cdk import (
    aws_cognito as cognito,
    Stack,
)
from constructs import Construct


class CognitoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the User Pool
        self.user_pool = cognito.UserPool(
            self,
            "MyUserPool",
            user_pool_name="MyFastAPIUserPool",
            # ... other User Pool configurations
        )

        # Create a User Pool Client
        self.user_pool_client = self.user_pool.add_client("MyUserPoolClient")
