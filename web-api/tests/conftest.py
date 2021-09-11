import pytest
from app import app
from .lib.helpers import *
from chalicelib.routes.constants import *

@pytest.fixture
def gateway_factory():
    return gateway_factory_internal()


def gateway_factory_internal():
    from chalice.config import Config
    from chalice.local import LocalGateway

    def create_gateway(config=None):
        if config is None:
            config = Config()
        return LocalGateway(app, config)
    return create_gateway


@pytest.fixture(scope='class')
def class_client(request):

    payload_string = json.dumps({
        "email": generate_email(),
        "password": "test_password"
    })

    gateway = gateway_factory_internal()()
    response = post(gateway, ROUTE_PATH_AUTH_SIGNUP, payload_string)
    assert_200_return_body_as_json(response)
    response = post(gateway, ROUTE_PATH_AUTH_LOGIN, payload_string)
    json_data = assert_200_return_body_as_json(response)
    assert json_data["status"]["success"] == True

    request.cls.JWT = json_data["auth"]['jwt']
    yield
