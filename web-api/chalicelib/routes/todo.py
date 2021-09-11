from chalice import Blueprint, Response

from chalicelib.model.todo import TodoModel, TodosArray
from chalicelib.routes.constants import *
from chalicelib.services.todo import todoService
from chalicelib.routes.authorizer import lambda_authorizer
todo_routes = Blueprint(__name__)


@todo_routes.route(ROUTE_TODO, methods=['POST'], authorizer=lambda_authorizer)
def save_todo() -> Response:
    todo_model = TodoModel.from_json(todo_routes.current_request.raw_body)
    todo_save_result = todoService.save_todo(todo_model)

    if todo_save_result.status.success:
        return Response(todo_save_result.to_json())

    return Response(todo_save_result.to_json(), {}, 500)


@todo_routes.route(ROUTE_TODO_BATCH, methods=['POST'], authorizer=lambda_authorizer)
def update_batch() -> Response:
    todo_model = TodosArray.from_json(todo_routes.current_request.raw_body)
    todo_save_result = todoService.batch_update(todo_model)

    if todo_save_result.status.success:
        return Response(todo_save_result.to_json())

    return Response(todo_save_result.to_json(), {}, 500)


@todo_routes.route(ROUTE_TODO, methods=['GET'], authorizer=lambda_authorizer)
def get_todos() -> Response:
    status = todo_routes.current_request.query_params['status']
    todo_get_result = todoService.get_todos(status)

    if todo_get_result.status.success:
        return Response(todo_get_result.to_json())

    return Response(todo_get_result.to_json(), {}, 500)
