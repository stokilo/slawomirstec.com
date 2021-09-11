from chalice import Blueprint, Response
from chalicelib.model.appointment import AppointmentModel
from chalicelib.routes.authorizer import lambda_authorizer
from chalicelib.routes.constants import *
from chalicelib.services.appointment import appointmentService

appointment_routes = Blueprint(__name__)


@appointment_routes.route(ROUTE_APPOINTMENT, methods=['POST'], authorizer=lambda_authorizer)
def save_appointment() -> Response:
    appointment_model = AppointmentModel.from_json(appointment_routes.current_request.raw_body)
    appointment_save_result = appointmentService.save_appointment(appointment_model)

    if appointment_save_result.status.success:
        return Response(appointment_save_result.to_json())

    return Response(appointment_save_result.to_json(), {}, 500)

@appointment_routes.route(ROUTE_APPOINTMENT, methods=['GET'], authorizer=lambda_authorizer)
def get_appointment() -> Response:
    qparams = appointment_routes.current_request.query_params
    appointment_get_result = appointmentService.get_appointment(qparams['year'], qparams['month'])

    if appointment_get_result.status.success:
        return Response(appointment_get_result.to_json())

    return Response(appointment_get_result.to_json(), {}, 500)