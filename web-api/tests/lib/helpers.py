import uuid
import json
import time
from datetime import datetime
from chalice.local import ForbiddenError


class AssertBase(object):

    @staticmethod
    def assert_get_only_for_authenticated_users(gateway, route: str):
        try:
            get(gateway, route, jwt=uuid.uuid4().__str__())
            assert 1 != 1
        except ForbiddenError:
            assert 1 == 1

    @staticmethod
    def assert_post_only_for_authenticated_users(gateway, route: str):
        try:
            post(gateway, route, {}, uuid.uuid4().__str__())
            assert 1 != 1
        except ForbiddenError:
            assert 1 == 1


def generate_username():
    return "test-username-" + uuid.uuid4().__str__() + "-" + datetime.now().__str__()


def generate_email():
    return "test-email-" + uuid.uuid4().__str__() + (int)(time.time()).__str__() + '@test.com'


def post(gateway, path, payload, jwt="", lang="en"):
    """Issue POST request with given payload and path"""

    headers = {"Content-Type": "application/json", "X-Language": lang}
    if jwt:
        headers["Authorization"] = jwt
    return gateway.handle_request(method='POST',
                                  path=path,
                                  headers=headers,
                                  body=payload)


def put(gateway, path, payload, jwt="", lang="en"):
    """Issue PUT request with given payload and path"""

    headers = {"Content-Type": "application/json", "X-Language": lang}
    if jwt:
        headers["Authorization"] = jwt
    return gateway.handle_request(method='PUT',
                                  path=path,
                                  headers=headers,
                                  body=payload)


def get(gateway, path, jwt, lang = "en"):
    """Issue GET request with given payload and path"""

    headers = {"Content-Type": "application/json", "X-Language": lang}
    if jwt:
        headers["Authorization"] = jwt
    return gateway.handle_request(method='GET', path=path, headers=headers, body='')


def assert_500_return_body_as_json(response):
    """Ensures that response status code is 500 and returns its parsed json body"""

    assert response["statusCode"] == 500
    return json.loads(response["body"])


def assert_200_return_body_as_json(response):
    """Ensures that response status code is 200 and returns its parsed json body"""

    assert response["statusCode"] == 200
    return json.loads(response["body"])