from chalice import Blueprint, Response

from chalicelib.routes.constants import *
from chalicelib.routes.authorizer import lambda_authorizer
from chalicelib.services.dashboard import dashboardService
from chalicelib import logger

dashboard_routes = Blueprint(__name__)


@dashboard_routes.route(ROUTE_DASHBOARD, methods=['GET'], authorizer=lambda_authorizer)
def get_todos() -> Response:
    dashboard = dashboardService.get_dashboard()

    try:
        if dashboard.status.success:
            return Response(dashboard.to_json())
    except Exception as e:
        logger.exception(e)

    return Response(dashboard.to_json(), {}, 500)
