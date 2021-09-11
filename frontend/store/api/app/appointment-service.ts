import {SERVER_API_ROUTES} from "~/store/api/routes";
import AxiosService from "~/store/api/axios-service";
import {Status} from "~/store/model/shared";
import {Appointment, AppointmentForMonthResult, AppointmentSubmitResult} from "~/store/model/app/appointment";

export default class AppointmentService extends AxiosService {

  async getAppointments(year: number, month: number): Promise<AppointmentForMonthResult> {
    const url = `${SERVER_API_ROUTES.ROUTE_APPOINTMENT}/?year=${escape(year.toString())}&month=${escape(month.toString())}`
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
