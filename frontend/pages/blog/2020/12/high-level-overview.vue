<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="High level overview">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2020/12/high-level.jpg" class-name="responsive border-0 card-img-top mb-3" alt="High level overview"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Diagram 1</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Introduction</h3>
                <p>
                  This website is a programming sandbox and blog at the same time.
                  I have documented all frameworks/libraries/patterns that I have tested and implemented.
                  My goal is to list all of my findings and techniques and to write tutorials.
                </p>
                <p>
                  The website consists of:
                </p>
                <ol class="list-group">
                  <li>A landing page with information about the author, contact page, and blog entries</li>
                  <li>Single page application, detailing my live system with samples.</li>
                </ol>
                <p></p>
                <p>
                  The application is fully <strong>serverless</strong> and deployed from the command line to stage and prod instances.
                  I've chosen AWS as a provider, and backend infrastructure is provisioned with AWS CDK.
                  The frontend is hosted on the Cloudflare Workers environment.
                </p>
              </div>
              <hr/>
              <div class="mb-5">
                <h4 class="card-title">Backend</h4>
                <p>
                  Let's start with the backend description. As mentioned before, AWS is the environment used.
                  <strong>Diagram 1</strong> shows the AWS CloudFormation stack structure, with the Roles and Policies removed for clarity.
                </p>
                <p>
                  We can see here that we have the Rest API and some Lambda functions that talk with the DynamoDB table.
                  As you can imagine, the SPA client talks with the Rest API and the logic of the endpoint is executed by Lambda.
                </p>
                <p>
                  You will also notice that there are two specialized lambda functions, one for DynamoDb stream,
                  second for the periodic execution logic.
                </p>
                <h6>Framework / Language</h6>
                <p>
                  I build this using the Python framework <strong>Chalice</strong>. Here is the official website where
                  you can find more details
                </p>
                <p>
                  <a href="https://aws.github.io/chalice/" rel="noopener noreferrer" target="_blank">https://aws.github.io/chalice/</a>
                </p>
                <p>
                  In short, Chalice is very convenient to work with. You can develop your lambda functions locally with the hot reload option.
                  This framework provision for you necessary AWS resources, and is a huge time saver.
                  Here is a quick look at how the sample code will look:
                </p>


                <client-only>
                   <highlightjs language='python' :code="snippet1"/>
                </client-only>

                <p>
                In this example, you can see how to handle <strong>POST</strong> request to the route /contact (ROUTE_CONTACT).
                </p>
                <p>
                Chalice uses the concept of <strong>blueprints</strong> for code organization. For example, all contact entity resources can
                be included in a single blueprint, with the name <strong>contact_routes</strong>
                and imported into the main application.
                </p>
                <p>
                For functional testing, I use  <strong>Pytest</strong>:
                </p>
                <a href="https://docs.pytest.org/en/stable/" rel="noopener noreferrer" target="_blank">https://docs.pytest.org/en/stable/</a>
                <p></p>
                <p>
                  It is possible to mock the Chalice gateway and perform functional tests of the API.
                </p>

                <hr/>
                <h4 class="card-title">Frontend</h4>
                <p>
                  The frontend is a static SPA implemented with Vue and Nuxt framework:
                </p>
                <a href="https://nuxtjs.org/" rel="noopener noreferrer" target="_blank">https://nuxtjs.org/</a>
                <p></p>
                <a href="https://vuejs.org/" rel="noopener noreferrer" target="_blank">https://vuejs.org/</a>
                <p></p>
                <p>
                  The client is built with Nuxt in the so-called static mode where pages are pre-generated for better SEO.
                  Client files are installed on Cloudflare Worker instances, for that I use Wrangler CLI
                </p>
                <a href="https://developers.cloudflare.com/workers/cli-wrangler" rel="noopener noreferrer" target="_blank">https://developers.cloudflare.com/workers/cli-wrangler</a>
                <p></p>

                <hr/>
                <h4 class="card-title">Infrastructure</h4>
                <p>
                  For the backend infrastructure provisioning, I'm using AWS CDK (Python version).
                </p>
                <a href="https://github.com/aws/aws-cdk" rel="noopener noreferrer" target="_blank">https://github.com/aws/aws-cdk</a>
                <p>
                  The deployment process is controlled from a custom-built CLI that applies CDK synth/deploy commands.
                  This handles the backend side. The frontend is deployed at the same time with Cloudflare instances using Wrangler.
                </p>
                <p> Infrastructure provisioning sample:</p>

                <client-only>
                   <highlightjs language='python' :code="snippet2"/>
                </client-only>
                <p></p>
                <p>
                  I will publish a more detailed description in the following blog posts.
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
  title: 'High level overview of the sample application',
    meta: [
    {hid: 'description', name: 'description', content: 'General description of the sample application'},
    {hid: 'keywords', name: 'keywords', content: 'AWS, DynamoDB, PynamoDb, Boto3, CDK, Python, backend, frontend, Chalice, Blueprint, Rest, API' }
  ]
}
})
export default class PiafDesign extends Vue {
   snippet1: String  = `
from chalice import Blueprint, Response
from chalicelib.routes.constants import *
from chalicelib.model.contact import ContactModel
from chalicelib.services.contact import contactService

contact_routes = Blueprint(__name__)


@contact_routes.route(ROUTE_CONTACT, methods=['POST'], )
def save_contact() -> Response:
    contact_model = ContactModel.from_json(contact_routes.current_request.raw_body)
    contact_save_result = contactService.save_contact(contact_model)

    if contact_save_result.status.success:
        return Response(contact_save_result.to_json())

    return Response(contact_save_result.to_json(), {}, 500)

   `

  snippet2: String = `
import os

from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    core as cdk
)
from aws_cdk.aws_dynamodb import StreamViewType
from aws_cdk.aws_iam import PolicyStatement
from cdk_chalice import Chalice


class WebApi(cdk.Stack):

    _API_HANDLER_LAMBDA_MEMORY_SIZE_1024 = 1024
    _API_HANDLER_LAMBDA_MEMORY_SIZE_128 = 128
    _API_HANDLER_LAMBDA_MEMORY_SIZE_256 = 256
    _API_HANDLER_LAMBDA_MEMORY_SIZE_512 = 512

    _API_HANDLER_LAMBDA_TIMEOUT_SHORT_SECONDS = 5
    _API_HANDLER_LAMBDA_TIMEOUT_SECONDS = 10

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #
        # DynamoDb
        #
        partition_key = dynamodb.Attribute(name='pk', type=dynamodb.AttributeType.STRING)
        sort_key = dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING)
        gsi1pk = dynamodb.Attribute(name="gsi1pk", type=dynamodb.AttributeType.STRING)
        gsi1sk = dynamodb.Attribute(name="gsi1sk", type=dynamodb.AttributeType.STRING)

        .... removed for brevity
  `
}
</script>

