from chalicelib.model.constants import ErrorCode
from chalicelib.routes.constants import *
from .lib.helpers import *
import pytest

@pytest.mark.usefixtures('class_client')
class TestAuthRoute(object):

    @staticmethod
    def test_signup_invalid_signup(gateway_factory):
        gateway = gateway_factory()
        payload_string = json.dumps({})
        response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
        body_as_json = assert_500_return_body_as_json(response)
        assert body_as_json["formValidation"]["passed"] == False
        assert len(body_as_json["formValidation"]["errors"]) == 2
        assert body_as_json["formValidation"]["passed"] == False
        assert body_as_json["formValidation"]["errors"]["email"][0] == "Field is required"
        assert body_as_json["formValidation"]["errors"]["password"][0] == "Field is required"

        payload_string = json.dumps({"email": "1", "password": "1"})
        response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
        body_as_json = assert_500_return_body_as_json(response)
        assert body_as_json["formValidation"]["passed"] == False
        assert body_as_json["formValidation"]["errors"]["email"][0] == "Min length is 3, max 250, provided 1"
        assert body_as_json["formValidation"]["errors"]["password"][0] == "Min length is 7, max 250, provided 1"

    @staticmethod
    def test_signup_success(gateway_factory):
        gateway = gateway_factory()
        test_email = generate_email()

        payload_string = json.dumps({
            "email": test_email,
            "password": "test_password"
        })

        response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
        json_data = assert_200_return_body_as_json(response)
        assert json_data["status"]["success"] == True

        response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
        body_as_json = assert_500_return_body_as_json(response)
        assert body_as_json["status"]["success"] == False
        assert body_as_json["status"]["error_message"] == "User already exists"

    @staticmethod
    def test_login(gateway_factory):
        gateway = gateway_factory()
        test_email = generate_email()

        payload_string = json.dumps({
            "email": test_email,
            "password": "test_password"
        })

        response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
        json_data = assert_200_return_body_as_json(response)
        assert json_data["status"]["success"] == True

        payload_string = json.dumps({})
        response = post(gateway, ROUTE_PATH_AUTH_LOGIN, payload_string)
        json_data = assert_500_return_body_as_json(response)
        assert json_data["formValidation"]["passed"] == False
        assert json_data["formValidation"]["errors"]["email"][0] == "Field is required"
        assert json_data["formValidation"]["errors"]["email"][1] == "Email is not valid"
        assert len(json_data["auth"]["jwt"]) == 0
        assert len(json_data["auth"]["refresh_token"]) == 0
        assert json_data["formValidation"]["errors"]["password"][0] == "Field is required"

        payload_string = json.dumps({
            "email": "dummy_not_existent_user@dot.com",
            "password": "password"
        })
        response = post(gateway, ROUTE_PATH_AUTH_LOGIN, payload_string)
        json_data = assert_500_return_body_as_json(response)
        assert json_data["status"]["success"] == False
        assert json_data["status"]["error_code"] == ErrorCode.FORM_PROCESSING_ERROR.value
        assert len(json_data["auth"]["jwt"]) == 0
        assert len(json_data["auth"]["refresh_token"]) == 0
        assert json_data["status"]["error_message"] == "Could not find the user"

        payload_string = json.dumps({
            "email": test_email,
            "password": "invalid_password"
        })
        response = post(gateway, ROUTE_PATH_AUTH_LOGIN, payload_string)
        json_data = assert_500_return_body_as_json(response)
        assert json_data["status"]["success"] == False
        assert json_data["status"]["error_code"] == ErrorCode.FORM_PROCESSING_ERROR.value
        assert json_data["status"]["error_message"] == "Invalid password"
        assert len(json_data["auth"]["jwt"]) == 0
        assert len(json_data["auth"]["refresh_token"]) == 0

        payload_string = json.dumps({
            "email": test_email,
            "password": "test_password"
        })
        response = post(gateway, ROUTE_PATH_AUTH_LOGIN, payload_string)
        json_data = assert_200_return_body_as_json(response)
        assert json_data["status"]["success"] == True
        assert len(json_data["auth"]["jwt"]) > 0
        assert len(json_data["auth"]["refresh_token"]) > 0


    @staticmethod
    def test_refresh_token(gateway_factory):
        gateway = gateway_factory()
        payload_string = json.dumps({
            "email": generate_email(),
            "password": "test_password"
        })

        response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
        json_data = assert_200_return_body_as_json(response)
        assert json_data["status"]["success"] == True

        response = post(gateway, ROUTE_PATH_AUTH_LOGIN, payload_string)
        json_data = assert_200_return_body_as_json(response)
        assert json_data["status"]["success"] == True

        payload_string = json.dumps({
            "refreshToken": json_data["auth"]["refresh_token"]
        })
        response = post(gateway, ROUTE_PATH_REFRESH_TOKEN, payload_string)
        json_data = assert_200_return_body_as_json(response)
        assert json_data["status"]["success"] == True
        assert (len(json_data["auth"]["jwt"]) > 0) == True
        assert (len(json_data["auth"]["refresh_token"]) > 0) == True

    def test_profile_update(self, gateway_factory):
        gateway = gateway_factory()
        payload_string = json.dumps({
            "firstName": "firstName",
            "lastName": "lastName"
        })
        response = post(gateway, f"{ROUTE_PROFILE}", payload_string, self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True

