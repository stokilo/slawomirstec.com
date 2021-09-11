<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Caching AWS API using Cloudflare KV storage">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/02/kv-cache.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="Appointment calendar"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Appointment calendar</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">AWS API caching using Cloudflare KV storage</h3>
                <p></p>
                <p>
                  This article is about an appointment calendar, the next application that I introduced into the sample application stack.
                  I will try to describe it briefly in this paragraph.
                </p>
                <p>
                  The client side consists of a calendar component that is supporting view and edit mode.
                  The edit mode is available for authenticated users. It allows to add and remove application global list of
                  events. Every user edits the same list to make things simpler for me. The view mode is accessible on this page.
                  Viewing is limited to fetching the calendar events for any month and view details of the event.
                </p>
                <p>
                  Separation of the edit mode (requires authentication) and the view mode (public access) is for a purpose,
                  namely to test API caching on Cloudflare KV storage. I wanted to test it a long time ago. Cloudflare
                  allows using Cache API or Worker source code + KV storage to do the caching. In such scenarios,
                  cache control remains on the Cloudflare side. I tested it in opposite direction, my AWS API decides when
                  to push to the KV storage and Cloudflare workers fetch data from it whenever cached resources are requested.
                </p>
                <p>
                  In the sample application, in order to edit an appointment, we have to execute code on the AWS side. The AWS lambda function is called
                  (chalice framework), and data is stored in the DynamoDb. The final step is a data push to the KV storage. This is done
                  by calling the Cloudflare API.
                  In order to see appointments, there are two options. On the edit screen we do standard, an authenticated data
                  fetch directly from the DynamoDB. This ensures consistency, we edit data directly in the primary data store.
                  On unauthenticated pages, where the appointment calendar in a view mode is running,
                  we call an endpoint that fetches data only from KV storage. This is executed by the Cloudflare worker instance.
                  Worker instance is not allowed to fetch data from an origin server in case of a cache miss. This would be an unsafe operation
                  because the Worker can't authenticate itself (this is public access request, there is not JWT token because the user is anonymous).
                </p>
                <p>
                  Ok, so the client side is a standard example of CRUD app supporting two modes. Edit mode allows adding an appointment,
                  update its start date, end date, and title.
                  It is possible to delete an event. Edited data is stored in the DynamoDb, each update is propagated to the KV
                  storage for caching. On the top of the page, there is a screenshot of the calendar with some sample
                  events. Under this paragraph, there is a real component in the view mode. You can press next and previous
                  month, the current date, and click on the appointments. The last action will open a view dialog.
                  If you want to add events, you can login with a dummy account and access it under 'Appointment' menu.
                </p>
                <p>
                  I will present here few code snippets with a short description.
                </p>

                <AppointmentCalendar :editable="false"/>

              </div>

              <div class="mb-5">
                <h3 class="card-title">The client side</h3>
                <p></p>
                <p></p>
                <p>
                 I'm using a Nuxt framework and Vue as a barebone for the client application. For the calendar, I selected vue-simple-calendar component,
                 I could not find Nuxt module for it, I wrapped this component with a Nuxt plugin.
                 For scripting typescript is used, it is combined with vue-class-component and Vuex store.
                 The template side is styled with bootstrap and custom styles from piaf admin template pack.
                </p>

                <client-only>
                  <highlightjs langugage="xml" :code="snippet1"/>
                  <highlightjs langugage="javascript" :code="snippet2"/>
                </client-only>
                <p></p>
                <p>
                  Calendar accepts a property 'editable' to support both modes, it is shared with an edit appointment dialog
                  to hide/show action buttons. The loading of appointments depends on this property as well. Component
                  vue-simply-calendar required to use //@ts-ignore for typescript imports, I could not find the way to fix this
                  error.
                  The main calendar component references the Vuex store like following:
                </p>
                <client-only>
                   <highlightjs langugage="javascript" :code="snippet3"/>
                </client-only>
                <p>
                  I integrated a vuex-class-component library that allows to use @mutations, @get, and @actions annotations.
                  I find it easy to read and maintain, all my stores make use of this library. I decided to use a combination
                  of Vue and vue-vuex class components instead of Angular. Some tinkering is required to put it together
                  but it works very well.
                  In the store, we have two functions for loading items, one that goes over authenticated API, second
                  access KV storage directly. Axios service to interact with the API is presented below.
                </p>
                <client-only>
                  <highlightjs langugage="javascript" :code="snippet4"/>
                </client-only>
                <p></p>
                <p>
                   Next is the KV store service responsible for accessing cached data from KV storage.
                   I pass a cache key in query params. Each key is in the format '__APPOINTMENT__YYYY-MM' .
                   I don't use the same cache key for API requests. I just pass year and month to 'getAppointments' function.
                </p>
                <p></p>
                <client-only>
                  <highlightjs langugage="javascript" :code="snippet5"/>
                </client-only>
                <p>
                </p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">The backend</h3>
                <p></p>
                <p></p>
                <p>
                  Below lambda code for DAO and service layer for appointment handling on the backend side.
                </p>

                <client-only>
                  <highlightjs langugage="python" :code="snippet6"/>
                  <highlightjs langugage="python" :code="snippet7"/>
                </client-only>
                <p>
                  Here we store items in the DynamoDb in so-called 'complex attribute' column.
                  Internally the complex attribute is a pynamodb map. I store there appointment data using the same structure
                  as JSON data exchanged with the client. There is a limit set for the number of items (100 items).
                  The title is limited to 100 characters. This is because of 400KB column size limit in the DynamoDb.
                </p>
                <p>
                  Class 'AppointmentItem' is our pynamodb map attribute. Each appointment has PK in the format 'APPOINTMENT#YYYY-MM'.
                  The row we store for the appointment is represented by 'AppointmentEntity' class, it is a list of appointments
                  plus mandatory keys. Each DAO action operates on this list. Actions are synchronized with the Cloudflare using a function
                  below:
                </p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet8"/>
                </client-only>
                <p>
                  I integrated the AWS secrets to store Cloudflare account id, KV storage namespace id, and a bearer token.
                  The edit action will not be used too often, thus accessing secrets won't be rate-limited.
                  Timeout is set to 4 seconds, a web service call is executed inside the lambda function, blocking time must be
                  kept to a minimum.
                  One note, I should probably extract secrets interaction outside kv_put function to cache them in the lambda.
                  Data is stored in the KV in the format as presented in the image below:
                </p>

                <ResizeImageTag resizeTo=1200 src="blog/2021/02/kv-cache-details.png"
                                class-name="responsive border-0 card-img-top mb-3" alt="Appointment details"/>

                <p></p>
                <p>
                  Each entry represents appointments for a given month. The content is an array of appointments.
                  Same that we store in the DynamoDb. This is in general serialized content of the data from a database.
                  This format is returned as JSON from KvService.kvAppointments function call.
                  The DynamoDb model data below:
                </p>
                <ResizeImageTag resizeTo=1200 src="blog/2021/02/dynamodb-model.png"
                                class-name="responsive border-0 card-img-top mb-3" alt="Appointment details"/>
                <p>
                  Please notice that map entries attribute names match data stored in the KV store.
                  I will look further into this strategy of storing the data where the DynamoDb complex attribute is
                  duplicated in the same format in the KV storage. I think it should be possible
                  to implement converter services that will automate such tasks. It should be beneficial for
                  small features that I plan to add to the sample application.
                </p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Summary</h3>
                <p></p>
                <p></p>
                <p>
                  I decided to add more code snippets to blog entries, these are experimental python/javascript
                  functions that I don't recommend copying. I hope they will be useful in some cases.
                </p>
                <p>
                  To summarize, the cache solution implemented here is good for storing data that can be edited by one entity and
                  a short delay is acceptable before the update is visible to the users. The appointment calendar I think is a good
                  example of such functionality. I would consider using it to edit blog entries, non-critical configuration
                  data, website updates, etc.
                </p>
                <p>
                  It is important to remember that cache entries must have TTL or expiration date defined. It must be aligned
                  with the application requirements or the cache update strategy must be implemented. I decided not to do it because
                  my app is a sample only, any real application should have it in place.
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
import ResizeImageTag from "~/components/common/ResizeImageTag.vue";
//@ts-ignore
import AppointmentCalendar from "@/components/app/appointment/AppointmentCalendar";


@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag,
    Colxx,
    AppointmentCalendar
  },
  head: {
    title: 'Caching AWS API using Cloudflare KV storage',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'Caching AWS API using Cloudflare KV storage'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'cloudflare, kv, cache, aws, appointment, calendar, store, database'
      }
    ]
  }
})
export default class CloudflareKvCache extends Vue {

  snippet1: String = `
----- AppointmentCalendar.vue

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

----- AppointmentEditItem.vue
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
  `

    snippet2: String = `
----- AppointmentCalendar.vue
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


----- AppointmentEditItem.vue
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
`

  snippet3: String = `
import {action, createModule, mutation} from "vuex-class-component";
import {Appointment, AppointmentForMonthResult, AppointmentSubmitResult} from "~/store/model/app/appointment";
import AppointmentService from "~/store/api/app/appointment-service";
import {$i18n, $loader, $notify} from "~/utils/api";
import KvService from "~/store/api/app/kv-service";


export class AppointmentStoreHelper {
  getMonthLike(day: number): string {
    const now = new Date();
    const newDate = new Date(now.getFullYear(), now.getMonth(), day, 0, 0)
    // return date in UTC (TZ shifted)
    return new Date(newDate.getTime() - (newDate.getTimezoneOffset() * 60000 )).toISOString()
  }

  toUTC(targetDateString: string): string {
    const targetDate = new Date(targetDateString)
    return new Date(targetDate.getTime() - (targetDate.getTimezoneOffset() * 60000 )).toISOString()
  }
}

export const VuexModule = createModule({
  namespaced: "appointment-store",
  strict: false,
  target: "nuxt"
});

export class AppointmentStore extends VuexModule {

  appointmentService: AppointmentService = new AppointmentService()
  kvService: KvService = new KvService()
  appointmentStoreHelper: AppointmentStoreHelper = new AppointmentStoreHelper()

  items: Array<Appointment> = []
  showDate: Date = new Date()
  selectedItem: Appointment = new Appointment()

  isEditable: boolean = false

  @mutation
  setShowDate(selectedDate: Date) {
    this.showDate = selectedDate
  }

  @mutation
  selectAppointment(appointment: Appointment) {
    this.selectedItem = appointment
  }

  @mutation
  addAppointment(appointment: Appointment) {
    this.items.push(appointment)
  }

  @mutation
  updateAppointment(appointment: Appointment) {
    this.items.filter(item => item.id === appointment.id).map(
      (item) => {
        item.endDate = appointment.startDate < appointment.endDate ? appointment.endDate : appointment.startDate
        item.startDate = appointment.startDate >= appointment.endDate ? appointment.endDate : appointment.startDate
        item.title = appointment.title
        item.priority = appointment.priority
        item.id = appointment.id
      }
    )
  }

  @mutation
  deleteAppointment(appointment: Appointment) {
    this.items = this.items.filter(app => app.id != appointment.id)
  }

  @mutation
  deleteAllAppointments() {
    this.items = []
  }

  @action
  async onMounted() {
    await this.onLoadAppointments(new Date())
  }

  @action
  async onLoadAppointments(selectedDate: Date) {
    let loader = $loader.show()
    try {

      this.setShowDate(selectedDate)
      this.deleteAllAppointments()

      const year = selectedDate.getFullYear()
      const month = selectedDate.getMonth() + 1
      let result: AppointmentForMonthResult = await this.appointmentService.getAppointments(year, month)

      if (result.status.success) {
        for (const app of result.appointments) {
          this.addAppointment(app)
        }
      }
    } catch (error) {
      console.dir(error)
      $notify("error", $i18n.t("appointment.action-load-msg-title"), $i18n.t("appointment.action-load-msg-error"));
    }
    setTimeout(() => {
      loader.hide()
    }, 300)
  }

  @action
  async onLoadAppointmentsFromKv(selectedDate: Date) {
    try {

      this.setShowDate(selectedDate)
      this.deleteAllAppointments()

      const year = selectedDate.getFullYear()
      const month = selectedDate.getMonth() + 1
      let result: AppointmentForMonthResult = await this.kvService.kvAppointments(year, month)

      //@ts-ignore
      for (const app of result.data) {
          this.addAppointment(app)
      }
    } catch (error) {
      console.info(error)
    }
  }

  @action
  async onSaveAppointment(appointment: Appointment) {
    let loader = $loader.show()
    try {
      let result: AppointmentSubmitResult = await this.appointmentService.saveAppointment(appointment)

      if (!result.status.success) {
        $notify("error", $i18n.t("appointment.action-load-msg-title"), $i18n.t("appointment.action-load-msg-error"));
      } else {
        this.updateAppointment(appointment)
      }
    } catch (error) {
      $notify("error", $i18n.t("appointment.action-load-msg-title"), $i18n.t("appointment.action-load-msg-error"));
    }
    setTimeout(() => {
      loader.hide()
    }, 300)
  }

  @action
  async onDeleteAppointment(appointment: Appointment) {
    try {
      let result: AppointmentSubmitResult = await this.appointmentService.deleteAppointment(appointment)
      if (result.status.success) {
        this.deleteAppointment(appointment)
      }
    } catch (error) {
      $notify("error", $i18n.t("appointment.action-load-msg-title"), $i18n.t("appointment.action-load-msg-error"));
    }
  }

  get count() {
    return this.items.length
  }
}
  `

  snippet4: String = `
import {SERVER_API_ROUTES} from "~/store/api/routes";
import AxiosService from "~/store/api/axios-service";
import {Status} from "~/store/model/shared";
import {Appointment, AppointmentForMonthResult, AppointmentSubmitResult} from "~/store/model/app/appointment";

export default class AppointmentService extends AxiosService {

  async getAppointments(year: number, month: number): Promise<AppointmentForMonthResult> {
    const url = \`\${SERVER_API_ROUTES.ROUTE_APPOINTMENT}/?year=\${escape(year.toString())}&month=\${escape(month.toString())}\`
    return await super.genericFetch(url, new AppointmentForMonthResult([], new Status()))
  }

  async saveAppointment(appointment: Appointment): Promise<AppointmentSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_APPOINTMENT, appointment, new AppointmentSubmitResult(
      new Appointment(), new Status())
    )
  }

  async deleteAppointment(appointment: Appointment): Promise<AppointmentSubmitResult> {
    // appointments without end date are deleted from the db
    appointment.endDate = ""
    return this.saveAppointment(appointment)
  }
}

  `

  snippet5: String = `
import AxiosService from "~/store/api/axios-service";
import {$axios} from "~/utils/api";
import {AppointmentForMonthResult} from "~/store/model/app/appointment";
import {SERVER_API_ROUTES} from "~/store/api/routes";

export default class KvService extends AxiosService {

  /**
   * Query KV cache namespace for appointments data
   * @param year
   * @param month
   */
  async kvAppointments(year: number, month: number): Promise<AppointmentForMonthResult> {
    const kv_key = \`__APPOINTMENT__\${year}-\${month}\`
    const url = \`\${this.resolveHost()}/api/\${SERVER_API_ROUTES.ROUTE_APPOINTMENT_CACHED}?q=\${escape(kv_key)}\`
    return $axios.get(url, this.getRequestConfig())
  }

  ...
}
  `

  snippet6: String = `
from chalicelib.model.appointment import AppointmentModel
from chalicelib.dao.shared import BaseDao
from chalicelib.dao.shared import BaseEntityForPyAwsV1
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute

from chalicelib.ws.cloudflare import kv_put
import dateutil.parser as dt


class AppointmentItem(MapAttribute):
    id = UnicodeAttribute()
    startDate = UnicodeAttribute()
    endDate = UnicodeAttribute()
    title = UnicodeAttribute()
    priority = UnicodeAttribute()


class AppointmentEntity(BaseEntityForPyAwsV1):
    """Entity for Appointment
    """

    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, unique_id: str = "", **kwarg):
        super().__init__(unique_id, **kwarg)

    appointments = ListAttribute(of=AppointmentItem)

    def prefix(self) -> str:
        return "APPOINTMENT#"

    def generate_unique_id(start_date_str: str):
        date_time_obj = dt.parse(start_date_str)
        return f"{date_time_obj.year}-{date_time_obj.month}"


def from_entity(appointment_entity: AppointmentEntity) -> [AppointmentModel]:
    result: [AppointmentModel] = []

    if appointment_entity.appointments is not None:
        for app in appointment_entity.appointments:
            model = AppointmentModel(
                startDate=app.startDate,
                endDate=app.endDate,
                id=app.id,
                title=app.title,
                priority=app.priority
            )
            result.append(model)

    return result


class AppointmentDao(BaseDao[AppointmentItem]):

    def create_appointment(self, appointment: AppointmentModel) -> AppointmentModel:
        appointment_unique_id = AppointmentEntity.generate_unique_id(appointment.startDate)

        appointment_item = AppointmentItem()
        appointment_item.startDate = appointment.startDate
        appointment_item.endDate = appointment.endDate
        appointment_item.id = appointment.id
        appointment_item.title = appointment.title[0:100]
        appointment_item.priority = appointment.priority

        appointment_entity = AppointmentDao.get_appointment(appointment.startDate)
        if appointment_entity.appointments is None:
            appointment_entity = AppointmentEntity(appointment_unique_id)
            appointment_entity.appointments = [appointment_item]
        else:
            # simplest solution, max 100 elements
            if appointment_entity.appointments.__len__() > 100:
                appointment_entity.appointments.pop(0)

            app_iter = filter(lambda app: app.id != appointment.id, appointment_entity.appointments)
            appointment_entity.appointments = list(app_iter)
            # this effectively deletes an item if end date is not defined
            if len(appointment.endDate):
               appointment_entity.appointments.append(appointment_item)

        success_cache = kv_put(appointment_unique_id, from_entity(appointment_entity))
        if success_cache:
           appointment_entity.save()
        else:
            # note: I don't care here about removing data from cache, this is for testing only
            raise Exception("Unable to save data into the cache, aborting.")

        return appointment

    @staticmethod
    def get_appointment(start_date: str) -> AppointmentEntity:
        appointment: AppointmentEntity = AppointmentEntity()
        appointment_unique_id = AppointmentEntity.generate_unique_id(start_date)
        return BaseDao.get(appointment, appointment.get_pk(appointment_unique_id),
                           appointment.get_sk(appointment_unique_id))

    @staticmethod
    def get_appointments_for(year: str, month: str):
        appointment: AppointmentEntity = AppointmentEntity()
        appointment_unique_id = f"{year}-{month}"
        return BaseDao.get(appointment, appointment.get_pk(appointment_unique_id),
                           appointment.get_sk(appointment_unique_id))


  `

  snippet7: String = `
from chalicelib.dao.appointment import AppointmentDao, from_entity
from chalicelib.model.appointment import AppointmentSubmitResult, AppointmentModel, AppointmentForMonthResult
from chalicelib import logger
from chalicelib.model.shared import Status


class AppointmentService:

    def __init__(self) -> None:
        self.appointment_dao = AppointmentDao()

    def save_appointment(self, appointment: AppointmentModel) -> AppointmentSubmitResult:
        result = AppointmentSubmitResult(appointment, Status())
        try:
            self.appointment_dao.create_appointment(appointment)
            result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result

    def get_appointment(self, year: str, month: str) -> AppointmentForMonthResult:
        result = AppointmentForMonthResult([], Status())
        try:
            appointment_entity = self.appointment_dao.get_appointments_for(year, month)
            result.appointments = from_entity(appointment_entity)
            result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result



appointmentService = AppointmentService()

  `

  snippet8: String = `
from typing import List

import boto3
import requests

from botocore.session import Session

from chalicelib.model.appointment import AppointmentModel

session = boto3.session.Session()

def kv_put(appointment_id: str, appointments: List[AppointmentModel]) -> bool:
    region_name = Session().get_config_variable('region')
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )
    account_id = client.get_secret_value(
        SecretId='PYAWS_CLI_CF_ACCOUNT_ID'
    )["SecretString"]

    namespace_id = client.get_secret_value(
        SecretId='PYAWS_CLI_KV_CACHE_NAMESPACE_ID'
    )["SecretString"]

    api_token = client.get_secret_value(
        SecretId='PYAWS_CLI_CF_API_TOKEN'
    )["SecretString"]

    kv_key = f"__APPOINTMENT__{appointment_id}"
    print(f"kv_key {kv_key}")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{kv_key}?expiration_ttl=99999999"

    headers = {
        'Content-Type' : 'text/plain',
        'Authorization' : f"Bearer {api_token}"
    }

    cache_data = AppointmentModel.schema().dumps(appointments, many=True)
    r = requests.put(url, data = f"{cache_data}", headers=headers, timeout=4)
    return r.status_code == 200
  `

}
</script>

