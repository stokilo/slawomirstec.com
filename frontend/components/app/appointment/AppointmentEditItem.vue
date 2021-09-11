<template>
  <b-modal id="edit-item" ref="edit-item" :title="$t('appointment.edit-item')">
    <b-form>
      <div role="alert" class="alert alert-danger" :hidden="errorMessage.length <= 0">
        {{ errorMessage }}
      </div>
      <b-form-group :label="$t('todo.title')">
        <b-form-input v-model="item.title" maxlength="100"/>
      </b-form-group>

      <b-form-group :label="$t('appointment.range')">
        <client-only>
          <date-picker
            :minimumView="'day'"
            :maximumView="'month'"
            :bootstrap-styling="true"
            v-model="item.startDate"
          ></date-picker>

          <date-picker
            :minimumView="'day'"
            :maximumView="'month'"
            :bootstrap-styling="true"
            v-model="item.endDate"
          ></date-picker>
        </client-only>
      </b-form-group>

    </b-form>
    <template slot="modal-footer">
      <b-button v-if="editable" variant="primary" @click="saveItem()" class="mr-1">{{ $t('appointment.save-item') }}</b-button>
      <b-button v-if="editable" variant="primary" @click="deleteItem()" class="mr-1">{{ $t('appointment.delete-item') }}</b-button>
      <b-button variant="secondary" @click="cancelItem()">{{ $t('appointment.cancel-item') }}</b-button>
    </template>
  </b-modal>
</template>

<script lang="ts">
import Vue from 'vue'
//@ts-ignore
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import Colxx from '~/components/common/Colxx.vue'
import {Appointment} from "@/store/model/app/appointment";
import Component from 'vue-class-component'
import {BModal} from "bootstrap-vue";
import {AppointmentStoreHelper} from "~/store/modules/app/appointment-store";

const AppointmentEditItemProps = Vue.extend({
  props: {
    item: {
      type: Object as () => Appointment,
    },
    editable: Boolean
  }
})

@Component({
  components: {
    Colxx,
    "v-select": vSelect
  }
})
export default class AppointmentEditItem extends AppointmentEditItemProps {

  $refs!: {
    'edit-item': BModal
  }
  errorMessage: string = ""
  appointmentStoreHelper: AppointmentStoreHelper = new AppointmentStoreHelper()

  priorities: Array<object> = [{"label": "purple", "value": "purple"}]

  saveItem() {
     if (new Date(this.item.endDate) < new Date(this.item.startDate)) {
       let swap = this.item.endDate
       this.item.endDate = this.item.startDate
       this.item.startDate = swap
     }

     this.item.startDate = this.appointmentStoreHelper.toUTC(this.item.startDate)
     this.item.endDate = this.appointmentStoreHelper.toUTC(this.item.endDate)


     this.$emit("onSaveItem", this.item)
     this.cancelItem()
  }

  deleteItem() {
    this.$emit("onDeleteItem", this.item)
    this.cancelItem()
  }

  cancelItem() {
    this.$refs['edit-item'].hide()
  }

  showItem() {
    this.$refs['edit-item'].show()
  }
}
</script>
