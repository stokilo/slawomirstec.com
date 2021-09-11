<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Piaf design">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResponsiveImageTag src="blog/2020/12/piaf.jpg" class-name="responsive border-0 card-img-top mb-3"/>
            <b-card-body>
              <div class="mb-5">
                <h2 class="card-title">Website template</h2>
                <p>
                  All sample applications, components and landing page are based on designs from ColoredStrategies.
                  The name of the package is piaf-vue, UI demo page, more details can be found here:
                </p>
                <p>
                  <a href="https://piaf-vue.coloredstrategies.com/" rel="noopener noreferrer" target="_blank">https://piaf-vue.coloredstrategies.com/</a>
                </p>
              </div>
              <div class="mb-5">
                <h2 class="card-title">License</h2>
                <p>
                  Regular license cost <strong>24$</strong>
                </p>
                <q>
                  The majority of our items (themes, code, graphics, 3D and flash) are covered by our Standard Licenses. If your end product including the item is going to be free to the end user then a Regular License is what you need. An Extended License is required if the end user must pay to use the end product.
                </q>
                <p>
                  What to consider before buying is:
                </p>
                <ul class="list-unstyled">
                  <li>Number of end products: 1</li>
                  <li>Use in a single end product: Yes</li>
                  <li>Use in a free end product: Yes</li>
                  <li>Use in an end product that's sold: No</li>
                  <li>Use in stock items/templates: No</li>
                </ul>
                <p>Please follow the link and check more details.</p>
              </div>
              <div>
                <h2 class="card-title">What is included?</h2>
                <p>
                  Please check the latest documentation on their website, In my case, I've received a package that includes:
                </p>
                <ul class="list-unstyled">
                  <li>HTML templates plus documentation.</li>
                  <li>Vue version, plus documentation, which consists of two parts:
                    <ul>
                      <li>Vue starter to quickly start coding</li>
                      <li>Full version with all components and pages as described on the website</li>
                    </ul>
                  </li>

                </ul>
                <p>
                  I highly recommend this design, especially if you start with Vue.
                  I found the code easy to understand and amend to suit my own needs.
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

@Component({
  components: {
    ResponsiveImageTag,
    Colxx
  },
  head: {
    title: 'Piaf design template',
    meta: [
      {hid: 'description', name: 'description', content: 'UI template description'},
      {hid: 'keywords', name: 'keywords', content: 'Piaf, UI, template, design, ColoredStrategies'}
    ]
  }
})
export default class PiafDesign extends Vue {
}
</script>

