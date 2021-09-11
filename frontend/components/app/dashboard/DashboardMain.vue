<template>
  <div>
    <DashboardIcons :stats="dashboardStore.dashboard.stats"/>
    <LogList :logs="dashboardStore.dashboard.logs"/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import DashboardIcons from "~/components/app/dashboard/DashboardIcons.vue";
import LogList from "~/components/app/dashboard/LogList.vue";
import {proxy} from "~/store/store";
import {DashboardStore} from "~/store/modules/app/dashboard-store";

@Component({
  components: {
    DashboardIcons,
    LogList
  },
  head: {bodyAttrs: {class: "rounded"}}
})
export default class DashboardMain extends Vue {
  dashboardStore: DashboardStore = proxy.dashboardStore

  mounted() {
    this.dashboardStore.onMounted()
  }

}
</script>

