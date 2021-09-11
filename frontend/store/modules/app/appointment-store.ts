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

