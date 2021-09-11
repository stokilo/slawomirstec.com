<template>
  <b-card :title="$t('dashboard.audit-events')">
    <perfect-scrollbar
      class="dashboard-logs scroll"
      :settings="{ suppressScrollX: true, wheelPropagation: false }"
    >
      <table class="table table-sm table-borderless">
        <tbody>
        <tr v-for="(log, index) in this.logs" :log="log" :key="index">
          <td>
            <span :class="`log-indicator align-middle ${color(log)}`"/>
          </td>
          <td>
            <span class="font-weight-medium">{{label(log)}}</span>
          </td>
          <td class="text-right">
            <span class="text-muted">{{ log.time | formatPDate }}</span>
          </td>
        </tr>
        </tbody>
      </table>
    </perfect-scrollbar>
  </b-card>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import {DashboardLogItem, UILogItemType} from "~/store/model/app/dashboard";
import {$i18n} from "~/utils/api";

const DashboardLogListProps = Vue.extend({
  props: {
    logs: Array
  }
})

@Component
export default class DashboardLogList extends DashboardLogListProps {

  color(item: DashboardLogItem) {
    if (item.type == UILogItemType.CONTACT_CREATION) {
       return "border-theme-1"
    } else if(item.type == UILogItemType.TODO_CREATION) {
      return "border-theme-2"
    } else {
      return "border-danger"
    }
  }

  label(item: DashboardLogItem) {
    if (item.type == UILogItemType.CONTACT_CREATION) {
      return $i18n.t("dashboard.log-item-contact-created")
    } else if(item.type == UILogItemType.TODO_CREATION) {
      return $i18n.t("dashboard.log-item-todo-created")
    } else if(item.type == UILogItemType.USER_CREATION){
      return $i18n.t("dashboard.log-item-user-created")
    }
  }
}
</script>
