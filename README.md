# Python 3.13 CDK App with Poetry 2.1

## Uses vscode devcontainers

From Windows WSL bash, open the folder directory with 
```
code .
``` 
Answer yes to "reopen in container?".  All
devtools will be installed in the resulting devcontainer.

## Uses poetry-plugin-export to get requirements.txt for the various lambdas

[https://github.com/python-poetry/poetry-plugin-export]
```
sudo poetry self add poetry-plugin-export
```

When it's time to deploy, to prepare, from bash, run `./generate_lambda_runtime_deps.sh`

## Deploys a little AWS ecosystem with multiple Lambdas, a Cognito user pool, and an API Gateway.

See app.py
