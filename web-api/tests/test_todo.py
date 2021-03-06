from http import HTTPStatus

import pytest

from chalicelib.dao.todo import TodoItemStatus, TodoItemCategory, TodoItemLabel
from chalicelib.routes.constants import *
from .lib.helpers import *

@pytest.mark.usefixtures('class_client')
class TestTodo(object):

    def test_create_todo(self, gateway_factory):
        gateway = gateway_factory()

        payload_data = {
            "subject": "test_subject",
            "details": "test_details",
            "status": TodoItemStatus.PENDING.value,
            "category": TodoItemCategory.JAVA.value,
            "label": TodoItemLabel.EDUCATION.value
        }
        payload = json.dumps(payload_data)
        response = post(gateway, ROUTE_TODO, payload, self.JWT)
        assert response["statusCode"] == HTTPStatus.OK
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        # update model autogenerated id for next updates
        payload_data["id"] = body_as_json["todoModel"]["id"]

        response = get(gateway, f"{ROUTE_TODO}?status=", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        assert body_as_json["items"][0]["subject"] == "test_subject"
        assert body_as_json["items"][0]["status"] == TodoItemStatus.PENDING.value

        response = get(gateway, f"{ROUTE_TODO}?status={TodoItemStatus.PENDING.value}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        assert body_as_json["items"][0]["subject"] == "test_subject"
        assert body_as_json["items"][0]["status"] == TodoItemStatus.PENDING.value

        response = get(gateway, f"{ROUTE_TODO}?status={TodoItemStatus.COMPLETED.value}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        assert len(body_as_json["items"]) == 0

        payload_data["status"] = TodoItemStatus.COMPLETED.value
        payload_data_arr = {"todos": [payload_data]}
        payload = json.dumps(payload_data_arr)
        response = post(gateway, ROUTE_TODO_BATCH, payload, self.JWT)
        assert response["statusCode"] == HTTPStatus.OK

        response = get(gateway, f"{ROUTE_TODO}?status={TodoItemStatus.COMPLETED.value}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        assert body_as_json["items"][0]["subject"] == "test_subject"
        assert body_as_json["items"][0]["status"] == TodoItemStatus.COMPLETED.value