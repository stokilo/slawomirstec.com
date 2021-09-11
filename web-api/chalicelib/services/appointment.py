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
