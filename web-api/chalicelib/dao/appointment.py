from chalicelib.dao.strategies.strategy_base import BaseEntityForPyAwsV1, BaseDao
from chalicelib.model.appointment import AppointmentModel
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

