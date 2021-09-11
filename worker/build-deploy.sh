#!/bin/bash

set -o xtrace

cd .. || exit
cd frontend || exit
rm -rf dist
rm -rf node_modules
yarn install
yarn generate
rm -rf ../worker/dist
cp -R dist ../worker/dist
cd ../worker || exit
CF_ACCOUNT_ID="$PYAWS_CLI_CF_ACCOUNT_ID" CF_API_TOKEN="$PYAWS_CLI_CF_API_TOKEN" wrangler publish
