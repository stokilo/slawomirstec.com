<template>
  <b-row>
    <Colxx xxs="12">
      <h2 class="mb-4 card-title">{{ $t('dashboard.dashboard') }}</h2>
      <b-row class="icon-cards-row mb-3">
        <Colxx xxs="6" sm="4" md="3" lg="2">
          <icon-card
            :title="$t('dashboard.contacts')"
            icon="mailbox"
            :value="stats.contactCount"
          />
        </Colxx>
        <Colxx xxs="6" sm="4" md="3" lg="2">
          <icon-card
            :title="$t('dashboard.users')"
            icon="person"
            :value="stats.userCount"
          />
        </Colxx>
        <Colxx xxs="6" sm="4" md="3" lg="2">
          <icon-card
            :title="$t('dashboard.todos')"
            icon="calendar"
            :value="stats.todoCount"
          />
        </Colxx>
      </b-row>
    </Colxx>
  </b-row>
</template>


<script lang="ts">
import Vue from 'vue';
import IconCard from "~/components/common/IconCard.vue";
import Component from 'vue-class-component';
import Colxx from "~/components/common/Colxx.vue";
import {DashboardStats} from "~/store/model/app/dashboard";

const DashboardIconsProps = Vue.extend({
  props: {
    stats: DashboardStats
  }
})

@Component({
  components: {
    Colxx,
    IconCard
  }
})
export default class DashboardIcons extends DashboardIconsProps {
}
</script>
