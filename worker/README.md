## Cloudflare workers setup

Application deploy target is Cloudflare workers, it requires wrangler CLI to be installed

Install wrangler 

$cd worker
$npm install -g @cloudflare/wrangler

This is required to save account id that is associated with paid subscription to Cloudflare workers.
You need account id and secret token that is saved in dot file under your home dir.

$wrangler configure

In order to preview website

$wranger preview --watch

In order to deploy to live system

$wrangler publish

To build production version of the client, copy to worker dist and publish

#./build-deploy.sh

## What is purpose of wrangler_bak.toml

This is backup of the original file that was deployed during installation.
In includes secretes and allows to run

```
wrangler publish && wrangler tail
```

after you copy content of this file to wrangler.toml 
Without original values it is not possible to debug the system

















