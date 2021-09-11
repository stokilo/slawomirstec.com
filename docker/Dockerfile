FROM python:3.8.7 as base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV AWS_PAGER ""

FROM base AS pyaws-general-libs
RUN apt-get update && apt-get upgrade -y && \
    apt-get install make unzip libglu1 libxi6 libgconf-2-4 jq curl git sudo nodejs libffi-dev -y && \
    curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash - && \
    apt-get -y install nodejs && \
    ln -s /usr/bin/nodejs /usr/local/bin/node && \
    curl -sL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.1.36.zip" -o "awscliv2.zip"  && \
    unzip awscliv2.zip &&\
    sudo ./aws/install

FROM pyaws-general-libs AS pyaws-python-npm-libs
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
RUN mkdir /home/appuser/.node_modules_global && \
    npm config set prefix=$HOME/.node_modules_global && \
    npm set HOME "/home/appuser/" -g && \
    chmod 777 /home/appuser/.node_modules_global && \
    export PATH="$HOME/.node_modules_global/bin:$PATH" && \
    npm config list && \
    npm i npm@latest -g && \
    mkdir -p "$HOME/.wrangler" && chmod -R 777 "$HOME/.wrangler" && \
    npm i @cloudflare/wrangler@1.15.0 -g && \
    npm i yarn@1.22.10 -g && \
    yarn global add aws-cdk@1.97.0 && \
    yarn global add nuxt@2.14.12 && \
    pip3 install --upgrade pip==21.0.1 && \
    pip3 install pipenv pipenv==2020.11.15

FROM pyaws-python-npm-libs AS pyaws-cli-app
USER appuser
COPY Pipfile .
COPY Pipfile.lock .
ENV PATH="/home/appuser/.venv/bin:/home/appuser/.local/bin:/home/appuser/.node_modules_global/bin:$PATH"
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev

EXPOSE 8000
EXPOSE 3000
EXPOSE 8090
