from chalicelib.model.crud import CrudType
from chalicelib.routes.constants import *
from .lib.helpers import *
import pytest


@pytest.mark.usefixtures('class_client')
class TestCrud(object):

    def test_crud(self, gateway_factory):
        gateway = gateway_factory()

        crudType = CrudType.BOOK.value
        payload = {
            "crudType": crudType,
            "id": uuid.uuid4().__str__(),
            "title": "",
            "isbn": "99921-58-10-7",
            "arr": ["1", "2"]
        }

        payload_string = json.dumps(payload)
        response = post(gateway, ROUTE_CRUD, payload_string,  self.JWT)
        body_as_json = assert_500_return_body_as_json(response)
        assert body_as_json['status']['success'] == False
        assert body_as_json['errors']['title'][0] == 'Field is required'

        payload['title'] = 'test_title'
        payload_string = json.dumps(payload)
        response = post(gateway, ROUTE_CRUD, payload_string,  self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True

        payload['id'] = body_as_json['crud']['id']
        payload['title'] = "test_title_updated"
        payload_string = json.dumps(payload)
        response = put(gateway, ROUTE_CRUD, payload_string,  self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True
        assert body_as_json['crud']['title'] == "test_title_updated"

        id = body_as_json['crud']['id']
        response = get(gateway, f"{ROUTE_CRUD}?id={id}&crudType={crudType}", self.JWT)
        body_as_json = assert_200_return_body_as_json(response)
        assert body_as_json['status']['success'] == True
        assert body_as_json['crud']['title'] == "test_title_updated"
        assert body_as_json['crud']['isbn'] == "99921-58-10-7"

