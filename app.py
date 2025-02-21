from aws_cdk import App

from src.hello_cdk.cdk.lambda_stack import LambdaStack

app = App()
LambdaStack(app, "LambdaStack")
app.synth()
