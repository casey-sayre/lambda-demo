FROM python:3.13-slim-bullseye

# Install system dependencies (as root)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    unzip \
    git \
    less \
    sudo \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and AWS CLI (as root)
ENV POETRY_HOME=/etc/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_HOME python - \
    && chmod a+x ${POETRY_HOME}/bin/poetry \
    && ln -s ${POETRY_HOME}/bin/poetry /usr/local/bin/poetry \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip \
    && rm -rf ./aws

# Create the vscode user (as root)
RUN useradd -ms /bin/bash vscode \
    && usermod -aG sudo vscode \
    && echo "vscode ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER vscode

RUN mkdir -p /home/vscode/.local \
    && curl -fsSL https://nodejs.org/dist/v20.9.0/node-v20.9.0-linux-x64.tar.gz | tar xz --strip-components=1 -C /home/vscode/.local

# Set the PATH (now we know exactly where npm and node are)
ENV PATH="/home/vscode/.local/bin:$PATH"

RUN npm install -g aws-cdk