# PyAws

This is a published source code of website/webapp 

[slawomirstec.com](https://slawomirstec.com)

Source code was stripped from CSS/Piaf UI components (commercial license is required).

It includes blog entries, AWS infrastructure provisioning scripts, webapp and Chalice backend source code, Cloudflare
worker scripts, and more.

Serverless application build with Python/NuxtJS+Vue/AWS Chalice.

#### Setting up 

Install a docker on your system and start the daemon.

Execute main application. It is an access point to the Chalice server, Nuxt client and pyaws-cli.

```bash
./run.sh
	-b: build docker image
	-i: start /bin/bash session
	-p: start pyaws-cli
	-n: run nuxt in dev mode (yarn dev) under 'frontend' folder
	-c: run chalice with auto-reload enabled
	-d: run chalice with auto-reload disabled, connect to debug session
```


#### Synthesize and deploy development stack

Copy .secret.config.yaml.template under new name .secret.config.yaml. Never add this file to git.
Any change in this file should be done using PyAWS CLI.
Execute the PyAWS CLI:

```bash
./run.sh -p
```

And execute commands to setup various accounts like AWS/Cloudflare/Google Captcha.

#### Undeploy stack

Run PyAWS and select undeploy action (only DEV system possible)

```bash
./run.sh -p
```

#### Run local dev server

```bash
./run.sh -c
```

#### Debug local dev server

Create Python Debug Server config in Intelijj Idea or PyCharm. Start if on localhost and port 8090.
Enable in the web-api/app.py following line:

```
#pydevd_pycharm.settrace('host.docker.internal', port=8090, stdoutToServer=True, stderrToServer=True)
```

run chalice in debug mode (with auto-reload disabled)
```bash
./run.sh -d
```

#### Testing the web API

Select pyaws-cli and command tests. 
Alternatively, create a new Intelijj Idea or PyCharm configuration with running tests under web-api/test folder.
Set the docker interpreter as python SDK for the project. Use pyaws-cli image for the interpeter target. Image 
is being build from command ./run.sh -b

```bash
./run.sh -p
```

#### Releasing

Release 1.0.0 

```bash
./release.sh perform 1.0.0 1.0.1
```

Command tags 1.0.0 , change next release version to 1.0.1 and commit this into the git repo.

#### Release installation

Installation of 1.0.0, execute command on VM for target installation system:

```bash
./release.sh checkout 1.0.0
```

The command checkout previously release tag 1.0.0 as branch. From this branch you can run:

```bash
# Build image from the tag
./run.sh -b
# Run pyaws-cli and deploy to production
./run.sh -p
```



