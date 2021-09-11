<template>
  <div>
    <div class="container-fluid">
      <div class="card rounded-top shadow-lg mb-4">
        <div class="card-body">
          <div class="jumbotron">
            <div class="row">
              <div class="col-12">
                <b-row>
                  <Colxx xxs="12">
                    <h1><a href="/">Slawomir Stec</a></h1>
                    <div class="top-right-button-container">
                      <b-dropdown id="ddown5" :text="$t('piaf.livePreview')" size="lg" variant="outline-primary"
                                  class="top-right-button top-right-button-single" no-fade="true">
                        <b-dropdown-item href="/signup">{{$t("piaf.signUp")}}</b-dropdown-item>
                        <b-dropdown-item href="/login">{{$t("piaf.login")}}</b-dropdown-item>
                      </b-dropdown>
                    </div>
                    <nuxt/>
                  </Colxx>
                </b-row>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="page-footer font-small">
      <div class="text-center py-1 text-small">© 2020 Copyright:
        <a href="https://slawomirstec.com" rel="noopener noreferrer" target="_blank">Slawomir Stec</a>
      </div>
      <div class="text-center py-1 text-small">
        <a href="https://piaf-vue.coloredstrategies.com/" rel="noopener noreferrer" target="_blank">UI template</a>
      </div>
      <div class="text-center py-1 text-small">
        <span>PyAws {{releaseInfo.version}}</span>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import releaseData from "~/data/release-version.json"
import Colxx from '~/components/common/Colxx.vue'

@Component({
  components: {
    Colxx
  }
})
export default class DefaultLayout extends Vue {
  releaseInfo: Object = releaseData
}

</script>

