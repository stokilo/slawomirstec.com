<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Cloud9">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/06/cloud9.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="Cloud9"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Cloud9</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Cloud9</h3>
                <p>Cloud9 is an AWS IDE for a web browser. Last week I had a chance to play around with it few hours.
                  I checkout my template project for TypeScript and Vue:</p>
                <a href="https://github.com/stokilo/aws-sst-rest-vue" rel="noopener noreferrer" target="_blank">https://github.com/stokilo/aws-sst-rest-vue</a>
                <p></p>
                <p>under the Cloud9 project folder.</p>
                <p>I want to share only a few observations that I think may interest some of you</p>
              </div>
            </b-card-body>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">1. Typescript and autocomplete support</h3>
                <p>Typescript is supported. My sample project is based on the SST framework where the typescript compiler
                  Is embedded. No issue though with this combination. The IDE autocomplete types and class members
                  on the fly. There is a small and noticeable delay between pressing the keyboard key and getting the display refreshed. But it is much better than I thought.
                </p>
                <p>When you create a new project you must choose the underlying EC2 instance to host it. I think anything with
                  8GB of RAM is ok for javascript projects. I would keep away from lower EC2 configurations. It is easy to
                  Freeze a server while running yarn or doing some more CPU intensive tasks.</p>
              </div>
              <p>With this configuration project refresh times are acceptable. </p>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">2. VIM support</h3>
                <p>I was surprised that is built into the IDE. Very nice addition. I always use the default subset of VIM keybindings. This comes in handy when I do any editing work on remote machines.
                  Simply all defaults work for me.</p>
                <p>Typing on Chrome with small files is completely usable.</p>
                <ResizeImageTag resizeTo=1200 src="blog/2021/06/vim.png"
                                class-name="responsive border-0 card-img-top mb-3" alt="Cloud9 VIM"/>
              </div>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">3. IAM</h3>
                <p>No need to configure access keys and secrets on the EC2 machine that runs Cloud9.
                  I did a test with IAM Administrator so maybe that was the reason everything runs smoothly.
                  I was able to deploy the CDK project without any configuration changes. That is a big plus.</p>
                <ResizeImageTag resizeTo=1200 src="blog/2021/06/stack.png"
                                class-name="responsive border-0 card-img-top mb-3" alt="Cloud9 IAM CDK"/>
              </div>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">4. VS Code</h3>
                <p>It is possible to setup VS Code remote development plugin to work with the Cloud9 project.
                  In the case of the SST framework, it allows to perform lambda debugging. I could not make the SST debugger run on Cloud9.</p>
              </div>
            </b-card-body>


            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Summary</h3>
                <p>I can say I see Cloud9 working in some scenarios for me. I think this is a good backup plan for a laptop i.e. when you setup your workspace in the browser running inside iPad. Your battery life is not affected
                  and with current Apple M1 chips it makes a really quiet and fast setup.</p>
                <p>Give it a try!</p>
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
    title: 'Cloud9',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'A quick review of AWS Cloud9'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'cloud9, aws, typescript, IDE'
      }
    ]
  }
})
export default class Cloud9 extends Vue {

  snippet1: String = ``

}

</script>
