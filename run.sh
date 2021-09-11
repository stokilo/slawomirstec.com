#!/bin/bash

helpFunction() {
  echo "Usage: $0 command"
  echo "All command attempt to rebuild the docker image."
  echo "All commands run the container."
  echo ""
  echo -e "\t-b: build docker image"
  echo -e "\t-i: start /bin/bash session"
  echo -e "\t-p: start pyaws-cli"
  echo -e "\t-n: run nuxt in dev mode (yarn dev) under 'frontend' folder"
  echo -e "\t-c: run chalice with auto-reload enabled"
  echo -e "\t-d: run chalice with auto-reload disabled, connect to debug session"
  exit 1
}

if [ -z "$1" ]; then
  helpFunction
fi


if [ "$1" == "-b" ]; then
  echo "Selected -b: build docker image"
  docker build -t pyaws-cli -f docker/Dockerfile .
  exit 0
fi

if [ "$1" == "-i" ]; then
  echo "Selected -i: run interactive mode"
  docker run -it \
    -v "$(pwd)"/web-api:/home/appuser/web-api \
    -v "$(pwd)"/worker:/home/appuser/worker \
    -v "$(pwd)"/infra:/home/appuser/infra \
    -v "$(pwd)"/frontend:/home/appuser/frontend \
    -v "$(pwd)"/Pipfile:/home/appuser/Pipfile \
    -v "$(pwd)"/Pipfile.lock:/home/appuser/Pipfile.lock \
    pyaws-cli:latest /bin/bash
  exit 0
fi

if [ "$1" == "-p" ]; then
  docker build -t pyaws-cli -f docker/Dockerfile .
  echo "Selected -p: run pyaws-cli"
  docker run -it \
    -v "$(pwd)"/web-api:/home/appuser/web-api \
    -v "$(pwd)"/worker:/home/appuser/worker \
    -v "$(pwd)"/infra:/home/appuser/infra \
    -v "$(pwd)"/frontend:/home/appuser/frontend \
    -v "$(pwd)"/.secret.config.yaml:/home/appuser/.secret.config.yaml \
    -v "$(pwd)"/pyaws-cli.py:/home/appuser/pyaws-cli.py \
    -v "$(pwd)"/pyaws-cli.sh:/home/appuser/pyaws-cli.sh \
    -v "$(pwd)"/release-version.json:/home/appuser/release-version.json \
    -v "$(pwd)"/Pipfile:/home/appuser/Pipfile \
    -v "$(pwd)"/Pipfile.lock:/home/appuser/Pipfile.lock \
    pyaws-cli:latest pipenv run python pyaws-cli.py
  exit 0
fi

if [ "$1" == "-n" ]; then
  echo "Selected -n: run nuxt dev mode"
  docker run -it \
    -v $HOME/.aws:/home/appuser/.aws \
    -v "$(pwd)"/frontend:/home/appuser/frontend \
    -w /home/appuser/frontend \
    -p 0.0.0.0:3000:3000/tcp \
    pyaws-cli:latest yarn dev --hostname 0.0.0.0 --port 3000
  exit 0
fi

if [ "$1" == "-c" ]; then
  echo "Selected -c: run chalice dev mode"
  docker run -it \
    -e DGB_CHALICE='false' \
    -v $HOME/.aws:/home/appuser/.aws \
    -v "$(pwd)"/web-api:/home/appuser/web-api \
    -w /home/appuser/web-api \
    -p 0.0.0.0:8000:8000/tcp \
    pyaws-cli:latest chalice local --port=8000 --host=0.0.0.0
  exit 0
fi

if [ "$1" == "-d" ]; then
  echo "Selected -d: run chalice debug mode"
  docker run -it \
    -e DGB_CHALICE='true' \
    -v $HOME/.aws:/home/appuser/.aws \
    -v "$(pwd)"/web-api:/home/appuser/web-api \
    -w /home/appuser/web-api \
    -p 0.0.0.0:8000:8000/tcp \
    pyaws-cli:latest chalice local --no-autoreload --port=8000 --host=0.0.0.0
  exit 0
fi
