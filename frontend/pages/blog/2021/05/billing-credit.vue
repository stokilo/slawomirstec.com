<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="AWS Billing credit">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/05/credit.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="Aws credit"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">AWS Billing credit</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">AWS Billing credit</h3>
                <p></p>
                <p>This is a very short post about a billing credit that I've got from AWS today.</p>
                <p>I've received an email from Amazon stating that I may be eligible for a 300 $ credit for AWS services.</p>
                <p>I was thinking that my personal website won't qualify. The AWS credit form took 1 minute to fill.
                Today I've checked my billing dashboard and amount was already credited.</p>
                <p>I hope someone find it useful. I didn't know about it before, if you receive an email from AWS about
                it, I think it is worth to spend few minutes and apply for it.</p>
                <p>This is great marketing move from AWS, this extra bonus allows me to check more services and save some money.</p>
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
    title: 'AWS Billing credit',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'AWS Billing credit'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'aws, billing, credit'
      }
    ]
  }
})
export default class AwsBillingCredit extends Vue {
}
</script>
