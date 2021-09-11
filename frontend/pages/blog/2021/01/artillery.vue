<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Load tests with artillery tool">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/01/artillery.jpg"
                            class-name="responsive border-0 card-img-top mb-3" alt="Artillery load tests"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Profile</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Load testing with artillery tool</h3>
                <p>
                  It may look a little strange that I incorporated load tests into the application with so few functions.
                  I had few reasons for doing that. Here is my explanation.
                </p>
                <p>
                  Firstly, I wanted to test out the artillery tool/load test framework:
                </p>
                <a href="https://artillery.io/" rel="noopener noreferrer" target="_blank">https://artillery.io/</a>
                <p></p>
                <p>
                  Secondly, this is a serverless application. I focused from the beginning on services that I add to the
                  stack,
                  their initial limits and the total number of users I thought I need to handle. I wanted to know how far I
                  can push the stack I created. For this, I needed load testing tool to fire a specified number of requests
                  against the app.
                </p>
                <p>
                  One more reason for adding load tests. It is useful in finding issues with the provisioned stack.
                  For instance, I found that the parameter store was limited when I fired too many lambda functions in a short amount of time.
                  So I've decided to replace it with environment variables. There is a lot of AWS blogs and books that
                  give answer for most of the question you can think of. Sometimes it is easier to
                  test it yourself instead of investing your time into long google sessions. And very often
                  you don't know what you don't know, load tests can give you some data to think about.
                </p>
                <p>
                  Below a sample artillery configuration that I created for the application load tests.
                  I configured one flow that match more and less what you can click through the UI.
                  You can login, receive JWT, fetch todo items and dashboard. This was quite easy to configure.
                </p>

                <client-only>
                  <highlightjs langugage="javascript" :code="snippet1"/>
                </client-only>
                <p></p>
                <p>
                  One problem I faced was google captcha that is integrated for all unauthenticated routes.
                  I decided to keep it enabled and implement logic to skip captcha inside the Cloudflare Worker.
                  For that I defined secret key 'PyAws-Admin-Access-Secret' and flag with capability name to enable
                  'PyAws-Admin-Access-SkipCaptcha'. I pass this data via HTTP headers.
                  The worker instance checks a condition and skip captcha validation if secret match
                  the one provided in the artillery config. The secret is provided to the Worker via PyAWS CLI on deploy time.
                </p>
                <p>
                  This is straightforward setup and I didn't have to add special conditions to disable the captcha for some
                  hosts. I don't like to add such conditions because it is easy to forget to remove them or accidentally
                  disable captcha check completely for prod. As this is serverless application, it must be protected against
                  scripted attacks.
                </p>
                <p>
                  To test it out you need to install it with npm: <strong>npm install -g artillery</strong>
                </p>
                <p>
                  To execute testcase from test.yaml scenario: <strong>artillery run test.yaml</strong>
                </p>
                <p>
                  Output of the command is presented on the top picture. The artillery CLI will refresh status of all running scenarios, with
                  response times and success/failure rates. Works really nice.
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
    title: 'Load tests with artillery tool',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'Load testing for serverless applications with artillery tool'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'artillery, load, testing, aws, cloudflare'
      }
    ]
  }
})
export default class ArtilleryLoadTesting extends Vue {
  snippet1: String = `
config:
  target: "https://slawomirstec.com/api/"
  phases:
    - duration: 5
      arrivalRate: 1
scenarios:
  - name: "Login, dashboard and todo"
    flow:
      - post:
          url: "/auth/login"
          json:
            email: "test@test.com"
            password: "--password--here--"
          headers:
            PyAws-Admin-Access-Secret: "--secret--here--"
            PyAws-Admin-Access-SkipCaptcha: "true"
          capture:
            json: "$.auth.jwt"
            as: "jwt-token"
      - get:
          url: "/todo?status="
          headers:
            authorization: "{{jwt-token}}"
      - get:
          url: "/todo?status=PENDING"
          headers:
            authorization: "{{jwt-token}}"
      - get:
          url: "/todo?status=COMPLETED"
          headers:
            authorization: "{{jwt-token}}"
      - get:
          url: "/dashboard?status="
          headers:
            authorization: "{{jwt-token}}"
`


}
</script>

