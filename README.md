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

## Uses poetry-plugin-export to get requirements.txt for the various lambdas

[https://github.com/python-poetry/poetry-plugin-export]
```
sudo poetry self add poetry-plugin-export
```

When it's time to deploy, to prepare, from bash, run `./generate_lambda_runtime_deps.sh`
