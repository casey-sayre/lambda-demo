# Demo Project: Python 3.13 CDK App with Poetry 2.1

## Deploys a little AWS ecosystem with Lambdas, a Cognito user pool, and an API Gateway.

See app.py

## Uses vscode devcontainers

From Windows WSL bash, from the toplevel project directory, run:
```
code .
``` 
Answer yes to "reopen in container?".  All
devtools will be installed in the resulting devcontainer.

Note that the devcontainer mounts the WSL ~/.ssh and ~/.aws readonly so AWS and ssh (think github) credentials are available in vscode.

When starting out it's probably advisable to run the following from the vscode devcontainer terminal (bash):

`python -m venv .venv`

`source .venv/bin/activate`

`poetry update`

`poetry install`

`sudo poetry self add poetry-plugin-export`

`./generate_lambda_runtime_deps.sh`

## Uses poetry-plugin-export to get requirements.txt for the various lambdas

A lambda function's runtime dependencies are be maintained in the corresponding group in `pyproject.toml`

That is, the dependencies for the customers lambda function handler are in the `pyproject.toml` group

```
[tool.poetry.group.customers_lambda_function.dependencies]
fastapi = ">=0.115.8,<0.116.0"
mangum = ">=0.19.0,<0.20.0"
```

### poetry-plugin-export Reference

[https://github.com/python-poetry/poetry-plugin-export]


### Install (after every devcontainer rebuild)

```
sudo poetry self add poetry-plugin-export
```


When it's time to deploy, if any lambda function handler dependencies have changed, from vscode devcontainer terminal (bash), run

`./generate_lambda_runtime_deps.sh`
