import pytest

from chalicelib.routes.constants import *
from .lib.helpers import *

class TestAuthorizer(object):

    @staticmethod
    def test_authorizer(gateway_factory):
        """Go over list of routes that requires authentication, call each without and expect auth error

        This is very important test, we don't want to expose these resources to unauthenticated users.
        List of routes must be maintained with special care!
        """
        gateway = gateway_factory()
        for route in ROUTES_WITH_REQUIRED_AUTH_GET:
            AssertBase.assert_get_only_for_authenticated_users(gateway, route)

        for route in ROUTES_WITH_REQUIRED_AUTH_POST:
            AssertBase.assert_post_only_for_authenticated_users(gateway, route)