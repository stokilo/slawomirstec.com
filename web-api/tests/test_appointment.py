from chalicelib.routes.constants import *
from .lib.helpers import *
import pytest


@pytest.mark.usefixtures('class_client')
class TestAppointment(object):

    def test_appointment(self, gateway_factory):
        gateway = gateway_factory()

        payload_string = json.dumps({
             "id": uuid.uuid4().__str__(),
             "startDate": "2021-02-11T04:00:00.000Z",
             "endDate": "2021-02-11T04:00:00.000Z",
             "title": "test",
             "priority": "purple"
        })
        response = post(gateway, ROUTE_APPOINTMENT, payload_string,  self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True

        response = get(gateway, f"{ROUTE_APPOINTMENT}?month=2&year=2021", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True
        assert len(body_as_json['appointments']) > 0
