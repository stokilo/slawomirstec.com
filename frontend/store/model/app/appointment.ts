import {Status, WithFromJson} from "~/store/model/shared";


export class Appointment extends WithFromJson {
  public id: string
  public title: string
  public startDate: string
  public endDate: string
  public priority: string

  constructor(id: string = "", title: string  = "", startDate: string = "", endDate: string = "", priority: string = "") {
    super();
    this.id = id;
    this.title = title;
    this.startDate = startDate;
    this.endDate = endDate;
    this.priority = priority
  }

}

export class AppointmentForMonthResult extends WithFromJson{
  public appointments: Array<Appointment>
  public status: Status

  constructor(appointmentsParam: Array<Appointment>, status: Status) {
    super();
    this.appointments = appointmentsParam
    this.status = status;
  }
}

export class AppointmentSubmitResult extends WithFromJson{
  public appointment: Appointment
  public status: Status

  constructor(appointment: Appointment, status: Status) {
    super();
    this.appointment = appointment;
    this.status = status;
  }
}

