Load tests for the Api

Install artillery 

https://artillery.io/docs/guides/getting-started/installing-artillery.html#System-requirements

```
npm install -g artillery
```

Ensure that you know secret admin key (see .secret config). This you must
deploy and change value in test.yaml. This is to avoid captcha.

Create new account and configure for authentication in the test.yaml.

To run tests

```
artillery run test.yaml
```