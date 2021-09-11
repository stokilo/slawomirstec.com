<template>
  <b-card :title="$t('appointment.calendar')">
    <client-only>
      <calendar-view
        style="min-height:500px"
        :items="appointmentStore.items"
        :show-date="appointmentStore.showDate"
        :time-format-options="{hour: 'numeric', minute:'2-digit'}"
        :enable-drag-drop="false"
        :show-event-times="true"
        display-period-uom="month"
        :starting-day-of-week="1"
        current-period-label="Today"
        @click-date="onClickDay"
        @click-item="onClickItem"
        itemTop="2.2em"
        class="theme-default"
      >
        <calendar-view-header
          slot="header"
          slot-scope="t"
          :header-props="t.headerProps"
          @input="onLoadAppointments"
        />
      </calendar-view>
    </client-only>

    <AppointmentEditItem
      :item="appointmentStore.selectedItem"
      ref="appointment-edit-item"
      @onSaveItem="onSaveItem"
      @onDeleteItem="onDeleteItem"
      :editable="editable"
    />

  </b-card>
</template>
<script lang="ts">
import Vue from 'vue'
import { v4 as uuidv4 } from 'uuid'
import Colxx from '~/components/common/Colxx.vue'
import Component from 'vue-class-component'
import {Appointment} from "@/store/model/app/appointment"
//@ts-ignore
import {CalendarView, CalendarViewHeader, CalendarMathMixin} from '~/node_modules/vue-simple-calendar/src/components/bundle'
import {proxy} from "~/store/store";
import {AppointmentStore, AppointmentStoreHelper} from "~/store/modules/app/appointment-store"
import AppointmentEditItem from "~/components/app/appointment/AppointmentEditItem.vue";

const AppointmentCalendarProps = Vue.extend({
  props: {
    editable: Boolean
  }
})

@Component({
  components: {
    Colxx,
    AppointmentEditItem,
    "calendar-view": CalendarView,
    "calendar-view-header": CalendarViewHeader
  },
  head: {bodyAttrs: {class: "rounded"}}
})
export default class AppointmentCalendar extends AppointmentCalendarProps {

  $refs!: {
    'appointment-edit-item': AppointmentEditItem
  }
  appointmentStore: AppointmentStore = proxy.appointmentStore
  appointmentStoreHelper: AppointmentStoreHelper = new AppointmentStoreHelper()

  mounted() {
    if(this.editable){
      this.appointmentStore.onMounted()
    } else {
      this.appointmentStore.onLoadAppointmentsFromKv(new Date())
    }
  }

  onLoadAppointments(selectedDate: Date) {
    if(this.editable){
      this.appointmentStore.onLoadAppointments(selectedDate)
    } else {
      this.appointmentStore.onLoadAppointmentsFromKv(selectedDate)
    }
  }

  onClickDay(selectedDate: Date) {
    if (!this.editable){
      return
    }
    let app = new Appointment(uuidv4(), "",
        this.appointmentStoreHelper.toUTC(selectedDate.toString()),
        this.appointmentStoreHelper.toUTC(selectedDate.toString()), "purple")

    this.appointmentStore.addAppointment(app)
    this.appointmentStore.selectAppointment(app)
    this.showEditDialog()
  }

  onClickItem(appointment: Appointment) {
    this.appointmentStore.selectAppointment(appointment)
    this.showEditDialog()
  }

  showEditDialog() {
    this.$refs['appointment-edit-item'].showItem()
  }

  onSaveItem(item: Appointment) {
    this.appointmentStore.onSaveAppointment(item)
  }

  onDeleteItem(appointment: Appointment) {
    this.appointmentStore.onDeleteAppointment(appointment)
  }
}
</script>
