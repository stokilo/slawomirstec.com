from chalice import Blueprint, Response

from chalicelib.routes.constants import *
from chalicelib.routes.authorizer import lambda_authorizer
from chalicelib.services.upload import uploadService

upload_route = Blueprint(__name__)


@upload_route.route(ROUTE_UPLOAD, methods=['GET'], authorizer=lambda_authorizer)
def get_todos() -> Response:
    signed_upload_url_response = uploadService.created_signed_url_profile_update()

    if signed_upload_url_response.status.success:
        return Response(signed_upload_url_response.to_json())

    return Response(signed_upload_url_response.to_json(), {}, 500)
