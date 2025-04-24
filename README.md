# Demo Project: Python 3.13 CDK App with Poetry 2.1

## Overview

Deploys a little AWS ecosystem with Lambdas, a Cognito user pool, and an API Gateway.
This makes a very simple microservices architecture on AWS.

### Implementation Overview

* app.py is the cognito app that ties the CDK stacks together

* In cognito_stack.py, notice the `Cognito Userpool name` and 
`App Client name` are specified in code.

### Dev Setup Overview

Uses vscode devcontainers

From Windows WSL bash, from the toplevel project directory, run:
```
code .
``` 
Answer yes to "reopen in container?".  All
devtools will be installed in the resulting devcontainer.

Note that the devcontainer mounts the host WSL ~/.ssh and ~/.aws.
These are mounted readonly. This makes AWS and ssh (think github) credentials available in vscode.

#### Getting Started overview

Open a vscode devcontainer terminal (bash):

##### Create the python virtual env

`python -m venv .venv`

`source .venv/bin/activate`

##### Get the CDK deploy-time dependencies for the CDK Python app via Poetry

`poetry update`

`poetry install`

##### Set up Poetry Export and get the the runtime dependencies to bundle for the Lambdas

[poetry export plugin reference](https://github.com/python-poetry/poetry-plugin-export)

`sudo poetry self add poetry-plugin-export`

`./setup_scripts/generate_lambda_runtime_deps.sh`

A lambda function's runtime dependencies are maintained in the corresponding group in `pyproject.toml`

That is, the dependencies for the customers lambda function handler are in the `pyproject.toml` group.
For example, here is the section of poetry.toml that defines the dependencies for hte customers_lambda_function:

```
[tool.poetry.group.customers_lambda_function.dependencies]
fastapi = ">=0.115.8,<0.116.0"
mangum = ">=0.19.0,<0.20.0"
```

### "One Time" Intialization of Devcontainer

(after every devcontainer rebuild)

```
sudo poetry self add poetry-plugin-export
```

### Deployment time overview

if any lambda function handler dependencies have changed, from vscode devcontainer terminal (bash),
from directory /setup_scripts/, run

`/generate_lambda_runtime_deps.sh`

### "One Time" Creation of Users and Groups in the Userpool

CDK deploy does not reinitialize Cognito user pool users and groups.

CDK destroy does not destroy Cognito user pool users and groups.

There is a script `setup_scripts/cognito_users_groups_setup.py` that

* creates user named `admin` and a user named `viewer`.
* creates user groups:

    `customers_viewers`, `products_viewers`, `orders_viewers`,

    `customers_admins`, `products_admins`, `orders_admins`
* adds users to the groups appropriately.

The required inputs are pulled from .env in the setup_scripts directory.

```bash .env
# admin, viewer user setup
ADMIN_USERNAME=admin
ADMIN_PASSWORD='FIXTHIS'
ADMIN_EMAIL=me+admin1@example.com
VIEWER_USERNAME=viewer
VIEWER_PASSWORD='FIXTHIS'
VIEWER_EMAIL=me+viewerl@example.com
VIEWER_GROUP_NAMES='["customers_viewers","orders_viewers","products_viewers"]'
ADMIN_GROUP_NAMES='["customers_admins","orders_admins","products_admins"]'

REGION=us-east-1

# cognito user pool values
USER_POOL_ID=us-east-1_FIXTHIS
CLIENT_ID=FIXTHIS
CLIENT_SECRET=FIXTHIS

# api gateway values
DEFAULT_ENDPOINT=https://FIXTHIS.execute-api.us-east-1.amazonaws.com/prod

```

### Plant UML in /docs

There is a very preliminary .puml diagram of the AWS architecture in /docs.

To run a local rendering server at port 8080, from a vscode Terminal, run:

`docker run -d -p 8080:8080 plantuml/plantuml-server:jetty`