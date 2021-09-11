<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="AWS CDK - Cloudflare Worker deployment">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2020/12/deploy.jpg" class-name="responsive border-0 card-img-top mb-3" alt="Deployment"/>
            <span class="badge badge-pill badge-theme-2 position-absolute badge-top-left">PyAWS CLI</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Application deployment</h3>
                <p>Hello</p>
                <p>
                  In this article, I will describe what the backend and frontend deployment process looks like.
                  The screenshot on the top is from a command-line application written in Python (PyAWS CLI).
                  This application was implemented to handle AWS and Cloudflare clouds deployments. Init screen lists
                  all possible commands and supported target systems. Here only DEV and PROD are listed. Not all
                  commands are available on the production system because destructive actions aren't allowed here,
                  such as deleting infrastructure or running tests.
                </p>
                <p>
                  There are various frameworks available, free and paid that can help you do what I have done with
                  PyAWS CLI. I've decided to implement my own for a few reasons. Firstly, I wanted something simple.
                  Secondly, I wanted to be as productive as possible. To achieve this, I decided to avoid fighting
                  with framework bugs or limitations. I have an AWS backend, and the frontend is deployed on Cloudflare.
                  These are two different providers with different APIs. As an example of limitations, the Chalice
                  framework does not offer all configurations for provisioned lambda functions. I wanted to set a
                  retention policy for Cloud Watch logs for the lambda, but it wasn't possible at the time of writing
                  this article.
                </p>
                <p>
                  Additionally, I wanted to unify secret management for both deployments. I didn't want to store
                  passwords for AWS in one place, Cloudflare Worker secrets in another. I found it hard to
                  maintain this even for a single deployment. I can't imagine doing it for three and more.
                </p>
                <p>
                  Another reason was that I wanted to have one machine for development and my other machine for
                  deployment only. AWS CLI/Wrangler CLI store their credentials in user settings that are
                  available for their applications. As a result, I can, for example, run the AWS CLI
                  command from my machine without authentication, which is handy but dangerous at the same time.
                  I'm the paranoid type! If I feel there is a chance I could run a command against the wrong system,
                  I always check the credentials, which is not productive. PyAWS protects me from doing that because
                  it forces me to set up deployment on a different machine (i.e., VM). It will not allow
                  me to set up DEV/PROD in a single config.
                </p>
                <p>
                  My last requirement was to have atomic deployment executed with a single command; this was quite
                  important for me. My target was to have reproducible deployments and also downgrades of environments.
                  My current development setup is not allowing any AWS service mocks.
                  By that, I mean I didn't want to run a 99.99% compatible docker based service during development and
                  fix bugs after deployment on real infrastructure. With AWS and Chalice, this is simple to set up,
                  for example, DynamoDB that I access locally from hot reloaded lambda functions. I can monitor logs,
                  service metrics, set correct rate-limiting, and test them as development progress. That is why
                  the docker approach was a no go for me! I did a similar setup with Quarkus and Java, and I got
                  errors on the lambda environments that were perfectly fine on my machine.
                </p>
                <p></p>
                <p></p>
              </div>
              <hr/>
              <div class="mb-5">
                <h3 class="card-title">Secret and config management </h3>
                <p>Let's start from the template source to describe how it is used.</p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet1"/>
                </client-only>
                <p></p>
                <p>
                  This is a template of the config file that is stored in a source repository. We store in the
                  repository an empty file. A new machine setup requires copying this file with a new name.
                  The file is not included in the source repository, in my case Git. Accidental removal
                  of this file will mean rerunning the setup. The user gets assigned new AWS/Cloudflare accounts,
                  both of them come with access tokens.
                </p>
                <p>
                  Config file should not be directly modified. Configuration must be done by running PyAWS CLI, and executing specialized commands.
                  The command can be executed only for a specific environment.
                  The tool will produce an error when attempting to configure multiple systems on a single machine.
                  Every command that sets a value in the config requires a secret key. The tool uses this key to encrypt
                  the setting. It is not possible to save secrets in clear text. Of course, the user can edit a file
                  manually; however running the commands requires a non-empty secret key. Such a mistake will result
                  in an error during the execution of action that requires the secret. Additionally, running the
                  command on the production system requires typing 'production_deployment_confirm_sentence'
                  every time a change is deployed. This sentence is configurable.
                </p>
              </div>
              <hr/>
              <div class="mb-5">
                <h3 class="card-title">AWS CDK - backend provisioning</h3>
                <p>
                  AWS CDK is an open-source framework to provision infrastructure. It supports multiple languages; Python is one of them.
                </p>
                <p>
                  I'm using this framework to deploy and un-deploy the backend stack. The stack definition is written
                  in Python language. Python API defines models for each service in the AWS Cloud with their parameters
                  and many defaults to save development time. The developer's task is to select the desired services,
                  configure them, and assign them to the stack. Below is an example of how to create the DynamoDb
                  table in the WebApi stack.
                </p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet2"/>
                </client-only>
                <p></p>
                <p>
                  We will need a DynamoDb table with PK/SK and GSI index. The table should have enabled streams and
                  be deleted when the stack is destroyed.
                </p>
                <p>
                  This code is not very impressive. We create CDK model instances for the desired service with
                  mandatory parameters. You could do that from AWS Console, AWS CLI, or other frameworks, there are many ways
                  of doing this. The benefit of AWS CDK is that deployment is very easy, CLI is well-written, and
                  stack rollback is possible. Most important for me is an option to do the diff between my backend stack in the
                  code and running infrastructure.
                <p>
                  Additionally, updates are easy and apply only changes to the stack calculated from the diff, so there is no need to do it yourself.
                </p>
                <p>
                  Okay, so every service I need on the AWS backend side is described similarly in the stack code. This includes all IAM roles and policies.
                </p>
                <p>
                  Whenever I need to make a change, I can do it in the code, deploy it, and test it on the development
                  machine. That is why I don't want to use docker to mock AWS services; my environment is sufficient
                  for development and testing and, as a bonus, the same as the target production system deployed
                  from the same stack file.
                </p>
              </div>
              <hr/>
              <div class="mb-5">
                <h3 class="card-title">Cloudflare Worker - frontend provisioning</h3>
                <p>
                  The Frontend application is built with Nuxt framework in so-called 'static' mode. All pages
                  are pre-rendered, assets optimized, SPA js files split by webpack.
                  The build's result is a directory with all files that can be deployed on the webserver.
                  I've decided to deploy these files with Wrangler CLI directly to worker instances on Cloudflare.
                  Files built by Nuxt are copied by Wrangler to Cloudflare key-value storage (KV) and served
                  directly by worker instances. The worker is associated with the target domain under which I
                  deploy the client. Sample Wrangler config in toml format looks like that:
                </p>

                <client-only>
                   <highlightjs langugage="python" :code="snippet3"/>
                </client-only>
                <p></p>
                <p>
                  All uppercase config strings are replaced with PyAWS CLI with values configured or created during
                  backend deployment. Environment variables are later exposed to the Worker instances and used to
                  execute pre-processing logic. For example, google captcha limit access to the API that
                  goes through AWS, ApiGateway, and more.
                </p>
                <p>
                  What is important to note is that only workers are exposed to the world. AWS API Gateway is
                  configured to allow connections from a limited set of IPs that belongs to Cloudflare. This is
                  because we use rate-limiting offerings from Cloudflare, and we additionally rely on their
                  DDOS protection. As a result, workers execute a proxy request to the AWS API Gateway. It was
                  set up this way because Cloudflare is cheaper than AWS, and we wanted to limit the resources
                  (basically, we don't even trust authorized access even though this is a sample
                  application, yes, I'm a bit paranoid).
                </p>
              </div>


            </b-card-body>
          </b-card>
        </b-row>
      </div>
    </b-tab>
  </b-tabs>
</template>

<script lang="ts">
import Component from "vue-class-component";
import Vue from "vue";
import Colxx from '~/components/common/Colxx.vue'
import ResponsiveImageTag from '~/components/common/ResponsiveImageTag.vue'
import ResizeImageTag from "~/components/common/ResizeImageTag.vue";

@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag,
    Colxx
  },
  head: {
    title: 'AWS CDK - Wrangler CLI deployment',
    meta: [
      {hid: 'description', name: 'description', content: 'Description of sample application deployment using AWS CDK and Wrangler CLI'},
      {hid: 'keywords', name: 'keywords', content: 'AWS, Cloudflare, CDK, Wrangler, CLI, command, Python, backend, frontend, provisioning, PyAWS' }
    ]
  }
})
export default class PiafDesign extends Vue {
  snippet1: String  = `
File: .secret.config.yaml.template

production_deployment_confirm_sentence:I confirm that I deploy new release on the PROD system !!!
environments:
  dev:
    domain: dev.slawomirstec.com
    cf-zone-id: ''
    region: me-south-1
    sns-email-region: us-east-2
    encrypted_aws_access_key_id: ''
    encrypted_aws_secret_access_key: ''
    recaptcha: ''
    admin-secret-key: ''
    admin-ip: ''
  prod:
    domain: slawomirstec.com
    cf-zone-id: ''
    region: me-south-1
    sns-email-region: us-east-2
    encrypted_aws_access_key_id: ''
    encrypted_aws_secret_access_key: ''
    recaptcha: ''
    admin-secret-key: ''
    admin-ip: ''
  `

  snippet2: String =`
class WebApi(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #
        # DynamoDb
        #
        partition_key = dynamodb.Attribute(name='pk', type=dynamodb.AttributeType.STRING)
        sort_key = dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING)
        gsi1pk = dynamodb.Attribute(name="gsi1pk", type=dynamodb.AttributeType.STRING)
        gsi1sk = dynamodb.Attribute(name="gsi1sk", type=dynamodb.AttributeType.STRING)

        self.dynamodb_table = dynamodb.Table(
            self, 'WebApiTable',
            partition_key=partition_key,
            sort_key=sort_key,
            table_name="PyAwsV1",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            stream=StreamViewType.NEW_AND_OLD_IMAGES)
        cdk.CfnOutput(self, 'DynamoDbTableName', value=self.dynamodb_table.table_name)
        self.dynamodb_table.add_global_secondary_index(index_name="gsi1", partition_key=gsi1pk, sort_key=gsi1sk)
  `
  snippet3: String = `
name = "STAGE"
type = "webpack"
account_id = ""
workers_dev = false
route = "ROUTE_DOMAIN/*"
zone_id = "CF_ZONE_ID"
vars = { REST_API_ID = "REST_API_ID_TOKEN", DOMAIN="ROUTE_DOMAIN", REGION="REST_API_REGION", RECAPTCHA="RECAPTCHA_KEY", ADMIN_SECRET_KEY="PYAWS_ADMIN_SECRET_KEY", ADMIN_IP="PYAWS_ADMIN_IP"}

[site]
bucket = "./dist"
entry-point = "./workers-site"
  `
}
</script>

