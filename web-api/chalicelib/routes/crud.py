from chalice import Blueprint, Response
from chalicelib.model.crud import Crud, CrudBook, CrudType, crud_model_by_type
from chalicelib.routes.authorizer import lambda_authorizer
from chalicelib.routes.constants import *
from chalicelib.services.crud import crudService

crud_routes = Blueprint(__name__)


@crud_routes.route(ROUTE_CRUD, methods=['POST'], authorizer=lambda_authorizer)
def create() -> Response:
    crud = Crud.from_json(crud_routes.current_request.raw_body)
    crud = crud_model_by_type(crud.crudType).from_json(crud_routes.current_request.raw_body)

    crud_save_result = crudService.create(crud)

    if crud_save_result.status.success:
        return Response(crud_save_result.to_json())

    return Response(crud_save_result.to_json(), {}, 500)


@crud_routes.route(ROUTE_CRUD, methods=['PUT'], authorizer=lambda_authorizer)
def update() -> Response:
    crud = Crud.from_json(crud_routes.current_request.raw_body)
    crud = crud_model_by_type(crud.crudType).from_json(crud_routes.current_request.raw_body)

    crid_save_result = crudService.update(crud)

    if crid_save_result.status.success:
        return Response(crid_save_result.to_json())

    return Response(crid_save_result.to_json(), {}, 500)

@crud_routes.route(ROUTE_CRUD, methods=['GET'], authorizer=lambda_authorizer)
def get() -> Response:
    params = crud_routes.current_request.query_params
    crud_get_result = crudService.get(params['id'], params['crudType'])

    if crud_get_result.status.success:
        return Response(crud_get_result.to_json())

    return Response(crud_get_result.to_json(), {}, 500)