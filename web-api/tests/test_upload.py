import pytest

from chalicelib.model.constants import AWSConstants
from chalicelib.routes.constants import *
from .lib.helpers import *
import datetime

@pytest.mark.usefixtures('class_client')
class TestUpload(object):

    def test_upload(self, gateway_factory):
        gateway = gateway_factory()

        response = get(gateway, f"{ROUTE_UPLOAD}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json["status"]["success"] == True
        now = datetime.datetime.now()
        object_name = f"{now.year}/{now.month}/{now.day}/{now.hour}/profile_image_"
        assert body_as_json["upload"]["fields"]["key"].startswith(object_name)
        assert AWSConstants.PYAWS_CLI_IMAGE_SUBDOMAIN.value in body_as_json["upload"]["url"]

