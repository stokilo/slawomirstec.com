from http import HTTPStatus

import pytest

from chalicelib.dao.todo import TodoItemStatus, TodoItemCategory, TodoItemLabel
from chalicelib.routes.constants import *
from .lib.helpers import *

@pytest.mark.usefixtures('class_client')
class TestTodo(object):

    def test_create_todo(self, gateway_factory):
        gateway = gateway_factory()

        response = get(gateway, f"{ROUTE_DASHBOARD}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        contact_count_before = body_as_json["dashboard"]["stats"]['contactCount']
        todo_count_before = body_as_json["dashboard"]["stats"]['todoCount']
        user_count_before = body_as_json["dashboard"]["stats"]['userCount']

        #
        # Contact
        #
        email = generate_email()
        payload_string = json.dumps({"name": "John Doe", "email": email, "details": "Hello there"})
        post(gateway, ROUTE_CONTACT, payload_string)

        #
        # Todo
        #
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

        #
        # User
        #
        test_email = generate_email()
        payload_string = json.dumps({
            "email": test_email,
            "password": "test_password"
        })
        response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
        assert_200_return_body_as_json(response)

        response = get(gateway, f"{ROUTE_DASHBOARD}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        contact_count_after= body_as_json["dashboard"]["stats"]['contactCount']
        todo_count_after = body_as_json["dashboard"]["stats"]['todoCount']
        user_count_after = body_as_json["dashboard"]["stats"]['userCount']

        assert contact_count_before == contact_count_after - 1
        assert todo_count_before == todo_count_after - 1
        assert user_count_before == user_count_after - 1

        log_len = len(body_as_json["dashboard"]["logs"])
        assert log_len >= 3
