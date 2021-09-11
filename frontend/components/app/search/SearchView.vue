<template>
  <div class="disable-text-selection">
    <form id="rulesForm" class="tooltip-label-right" novalidate>

      <label class="form-group has-float-label mb-4">
        <span>{{ $t('search.howto') }}</span>

      <v-select
        class="form-control"
        label="name"
        :filterable="false"
        :options="autoCompleteOptions"
        @search="fetchOptions"
      >
        <template slot="no-options">{{ $t('search.placeholder') }}</template>
        <template slot="option" slot-scope="option">
          <div class="d-center">
            {{ option.value }}
          </div>
        </template>
        <template slot="selected-option" slot-scope="option">
          <div class="selected d-center">
            {{ option.value }}
          </div>
        </template>
        <template slot="spinner" slot-scope="spinner">
          <div class="spinner-border text-primary" v-show="spinner"></div>
        </template>
      </v-select>
      </label>
      <br/>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import KvService from "~/store/api/app/kv-service";

@Component({
  head: {bodyAttrs: {class: "rounded"}}
})
export default class SearchViewComponent extends Vue {

  kvService: KvService = new KvService()

  autoCompleteOptions: Array<Object> = []

  async fetchOptions(search: string, loading: any) {

    this.autoCompleteOptions = []
    if (search.length < 3) {
      return
    }

    try{
      loading(true);
      let response = await this.kvService.kvStreetsSearch(search)
      this.autoCompleteOptions = response.data
    } catch (e) {
      console.info(e)
    } finally {
       loading(false)
    }

  }
}
</script>

