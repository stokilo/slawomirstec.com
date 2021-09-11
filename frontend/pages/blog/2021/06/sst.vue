<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Serverless stack (SST) + Amplify auth">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/06/sst.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="SST"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Serverless stack (SST) + Amplify auth</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Serverless frameworks - starting with Chalice</h3>
                <p>My first serverless application was written in a Python language using the Chalice framework. This blog backend is based on this configuration. </p>
                <p>It was a pleasant development experience. Chalice supports live reload, debugging, and local testing. It calculates IAM permissions from the source code and provisions required resources. </p>
                <p>I combined a Cloudformation template that Chalice outputs with the CDK framework. On the front side, I’ve added a Nuxt framework and the blog was ready.</p>
                <p>I didn’t have a lot of Python experience when I started. My initial plan was to test Chalice first and then move to the Zappa framework. I never had a chance to do that. </p>
                <p>Sample applications on this blog and an authentication module took me around 100 hours of work.</p>
                <p>Then I’ve moved to other topics.</p>
              </div>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">AWS Serverless Application Model (SAM)</h3>
                <p>A few weeks ago I was playing around with AWS Toolkit for Intellij Idea </p>
                <a href="https://aws.amazon.com/intellij/" rel="noopener noreferrer" target="_blank">https://aws.amazon.com/intellij/</a>
                <p></p>
                <p>It offers nice integration with Serverless Application Model (SAM). I've implemented a test application using Typescript language. For tests, I added </p>
                <p><b>aws-sdk-mock</b></p>
                <p>Node library. It allows mocking AWS services in unit tests. With SAM I can run lambda locally and remotely. Debug is supported and works nicely with Intellij Idea debugger.</p>
                <p>Integrated AWS Toolkit for CloudWatch logs and lambda triggers works very well in the IDE. I like the way how the plugin groups the log streams and how the interface handle viewing them. I miss the tailing of the live log but in general, all features improve lambda development experience.</p>
                <p>What I don’t like is the delay between the code change and lambda reload. It takes too long to see your changes. And you have to ensure proper permissions are assigned to the lambda. Otherwise, you can have working lambda code locally and receiving access denied remotely. But the biggest issue is the code reload speed.</p>
                <p>I think this is quite ok as an additional module for i.e. Java Fargate application. In such setup, you may need some lambda code to react to AWS events. In this scenario, I would go with SAM. But for implementing API with API Gateway + Lambda + DynamoDB I think SST is better.</p>
              </div>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Serverless Stack (SST)</h3>
                <p>I found it while searching serverless frameworks on Github and sorting by popularity. This is a solid piece of code I have to say. I didn’t have time to do a bigger project with the SST framework yet. What I see as a beginner is mind-blowing.</p>
                <p>Documentation is short and filled with examples. The official website works fast and delivers a pleasant experience. A big plus is a tutorial for a severless framework that covers multiple interesting topics.</p>
                <p>SST internally wraps a CDK library. Additionally, it includes some higher-level CDK constructs that are part of the framework. This natural combination works fast and without errors so far for me. I can easily provision my infrastructure and lambda based API. All in the same codebase and programming language of choice.</p>
                <p>What is the most exciting is live code reload. And this is a live reload on the AWS side. We are not talking here about local development. This allows you to code lambda as you would edit code under AWS Console lambda editor. But without the need to press the ‘Deploy’ button. Additionally, this tool detects infrastructure changes and prompts you to accept them for deployment. Nice. SST is a framework of the year for me.</p>
                <p></p>
              </div>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Template project</h3>
                <p></p>
                <a href="https://github.com/stokilo/aws-sst-rest-vue" rel="noopener noreferrer" target="_blank">https://github.com/stokilo/aws-sst-rest-vue</a>
                <p></p>
                <p>Ok, so I’ve decided to create a sample template project. It is a typescript project that includes</p>
                <ul>
                  <li>Lambda function to react on S3 Event</li>
                  <li>Lambda function behind Api Gateway to output some JSON. The API endpoint is private. Authentication is required</li>
                  <li>Cognito user pool</li>
                  <li>Amplify authentication module integrated with a Vue frontend application</li>
                </ul>
                <p>This is a stack that I use for quick prototyping. API access requires authentication. UI components for sign up and signing are taken from th Amplify web component library.</p>
                <p>This is a very limited example but it presents a few ideas described before. You can deploy this with few commands to your AWS account and start coding directly on the AWS side with hot reload enabled.</p>
                <p>Please refer to the official SST framework website for more details.</p>
                <p></p>
                <p>Links:</p>
                <p></p>
                <a href="https://serverless-stack.com/" rel="noopener noreferrer" target="_blank">https://serverless-stack.com/</a>
                <p></p>
                <a href="https://aws.amazon.com/serverless/sam/" rel="noopener noreferrer" target="_blank">https://aws.amazon.com/serverless/sam/</a>
                <p></p>
                <a href="https://aws.amazon.com/intellij/" rel="noopener noreferrer" target="_blank">https://aws.amazon.com/intellij/</a>
                <p></p>
                <a href="https://github.com/aws/chalice" rel="noopener noreferrer" target="_blank">https://github.com/aws/chalice</a>
                <p></p>
                <a href="https://github.com/Miserlou/Zappa" rel="noopener noreferrer" target="_blank">https://github.com/Miserlou/Zappa</a>
                <p></p>
                <a href="https://github.com/dwyl/aws-sdk-mock" rel="noopener noreferrer" target="_blank">https://github.com/dwyl/aws-sdk-mock</a>
                <p></p>
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
//@ts-ignore


@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag,
    Colxx
  },
  head: {
    title: 'Serverless stack (SST) + amplify auth',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'Template project for SST + amplify auth stacks'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'aws, serverless, stack, sst, amplify, auth'
      }
    ]
  }
})
export default class SST extends Vue {

  snippet1: String = ``

}

</script>
