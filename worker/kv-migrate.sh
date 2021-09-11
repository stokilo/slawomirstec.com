#!/bin/bash

export CF_ACCOUNT_ID=$PYAWS_CLI_CF_ACCOUNT_ID
export CF_API_TOKEN=$PYAWS_CLI_CF_API_TOKEN
export CF_AUTOCOMPLETE_NID=$PYAWS_CLI_KV_AUTOCOMPLETE_NAMESPACE_ID
export CF_CACHE_NID=$PYAWS_CLI_KV_CACHE_NAMESPACE_ID

m013="$(wrangler kv:key get --namespace-id="$CF_AUTOCOMPLETE_NID" __0.1.3__)"
m014="$(wrangler kv:key get --namespace-id="$CF_CACHE_NID" __0.1.4__)"

if [[ $m013 = "migration:true" ]]
then
  echo "Migration [0.1.3] already done, skipping."
else
  echo "Start migration to KV [0.1.3]"
  unzip -d /tmp/0.1.3 migration/0.1.3.zip
  wrangler kv:bulk put \
   --namespace-id="$CF_AUTOCOMPLETE_NID" /tmp/0.1.3/kv-data.json

   wrangler kv:key put \
   --namespace-id="$CF_AUTOCOMPLETE_NID" "__0.1.3__" "migration:true"
fi

if [[ $m014 = "migration:true" ]]
then
  echo "Migration [0.1.4] already done, skipping."
else
  echo "Start migration to KV [0.1.4]"
  wrangler kv:bulk put \
   --namespace-id="$CF_CACHE_NID" migration/kv-cache.json

   wrangler kv:key put \
   --namespace-id="$CF_CACHE_NID" "__0.1.4__" "migration:true"
fi