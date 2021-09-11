from chalice import Blueprint, Response
from chalicelib.routes.constants import *
from chalicelib.model.contact import ContactModel
from chalicelib.services.contact import contactService

contact_routes = Blueprint(__name__)


@contact_routes.route(ROUTE_CONTACT, methods=['POST'], )
def save_contact() -> Response:
    contact_model = ContactModel.from_json(contact_routes.current_request.raw_body)
    contact_save_result = contactService.save_contact(contact_model)

    if contact_save_result.status.success:
        return Response(contact_save_result.to_json())

    return Response(contact_save_result.to_json(), {}, 500)
